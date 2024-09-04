import os
import sys
import cv2
import numpy
import torch

# sys.path.insert(0, '/workspace/model/yolov7/')
from model.yolov7.models.experimental import attempt_load
from model.yolov7.utils.general import non_max_suppression, scale_coords
from model.yolov7.utils.torch_utils import select_device
from model.yolov7.utils.datasets import letterbox
from model.yolov7.utils.dataset_classes import get_class

class YOLOv7:
    model = None
    result = None
    conf_thresh = 0.0
    nms_thresh = 0.0
    path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        self.model_name  = "yolov7e6e_webui"
        self.dataset     = "webui"
        self.conf_thresh = 0.1
        self.nms_thresh  = 0.5
        self.is_batch    = True
        self.weight_path = os.path.join(f"/workspace/model/weights/{self.model_name}.pt")
        self.image_size = 1280
        if self.is_batch:
            self.batch_size = 32
        else:
            self.batch_size = 1
        __, self.class_names = get_class(self.dataset)

        self.device = select_device("0", batch_size=self.batch_size)
        self.model = attempt_load(self.weight_path, map_location=self.device)  # load FP32 model
        self.model.eval()
        self.model(torch.zeros(1, 3, self.image_size, self.image_size).to(self.device).type_as(next(self.model.parameters())))  # run once

    def draw_bounding_boxes(self, image, results):
        """
        Draw bounding boxes on the image.

        :param image: Input image (numpy array).
        :param results: Detection results from the inference method.
        :return: Image with drawn bounding boxes.
        """
        for result in results:
            label = result['label'][0]['description']
            score = result['label'][0]['score']
            x = int(result['position']['x'])
            y = int(result['position']['y'])
            w = int(result['position']['w'])
            h = int(result['position']['h'])

            # Draw rectangle
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Optionally, add label and score
            cv2.putText(image, f"{label}: {score:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return image

    def inference_image(self, image, score_max=1):
        """
        :param image: input image(np array)
        :return: dict format bounding box(x1, y1, x2, y2), scor, class, class index
            - format:
                [{"label": [{"description": cls, "score": score, "class_idx": cls_idx}],
                 "position": {"x": x, "y": y, "w": w, "h": h}}, ...]
        """
        origin_image = image.copy()
        origin_image_shape = image.copy().shape
        augment = False
        stride = int(self.model.stride.max())
        image = letterbox(image, self.image_size, stride=stride)[0]
        image = image[:, :, ::-1].transpose(2, 0, 1)
        image = numpy.ascontiguousarray(image)

        image = torch.from_numpy(image).to(self.device)
        image = image.float()  # uint8 to fp16/32
        image /= 255.0  # 0 - 255 to 0.0 - 1.0
        if image.ndimension() == 3:
            image = image.unsqueeze(0)
        pred = self.model(image, augment=augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres=self.conf_thresh, iou_thres=self.nms_thresh, labels=None,
                                   multi_label=True)
        results = []
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(image.shape[2:], det[:, :4], origin_image_shape).round()
                for *xyxy, conf, cls in reversed(det):
                    if conf > self.conf_thresh:
                        if score_max == 100:
                            score = float(conf) * score_max
                        else:
                            score = float(conf)
                        x = float(xyxy[0])
                        y = float(xyxy[1])
                        w = float(xyxy[2]) - x
                        h = float(xyxy[3]) - y
                        str_class = self.class_names[int(cls)]
                        results.append({
                            'label': [{
                                'description': str_class,
                                'score': score,
                                'class_idx': self.class_names.index(str_class)
                            }],
                            'position': {
                                'x': x,
                                'y': y,
                                'w': w,
                                'h': h
                            }
                        })
        self.results = results
        image_with_boxes = self.draw_bounding_boxes(origin_image, results)

        return results, image_with_boxes


    def inference_image_batch(self, images, score_max=1):
        """
        :param image: input images(list in dict: [np array])
        :return: detection results(bounding box(x1, y1, x2, y2), score, class, class index) of each images
            - format:
                [[{"label": [{"description": cls, "score": score, "class_idx": cls_idx}],
                 "position": {"x": x, "y": y, "w": w, "h": h}}, ...], ...]
        """
        results = []
        tensor_images = []
        shapes = []
        stride = int(self.model.stride.max())
        for image in images:
            shapes.append([[image.shape[0], image.shape[1]], [[0.3333333333333333, 0.3333333333333333], [16.0, 12.0]]])
            image = letterbox(image, self.image_size, stride=stride)[0]
            image = image[:, :, ::-1].transpose(2, 0, 1)
            image = numpy.ascontiguousarray(image)
            tensor_images.append(torch.from_numpy(image))

        targets =  torch.zeros((0, 6))
        try:
            image = torch.stack(tensor_images, 0)
        except:
            pass
        image = image.to(self.device, non_blocking=True)
        image = image.float()  # uint8 to fp16/32
        image /= 255.0  # 0 - 255 to 0.0 - 1.0
        targets = targets.to(self.device)
        nb, _, height, width = image.shape  # batch size, channels, height, width

        with torch.no_grad():
            out, __ = self.model(image, augment=False)
            targets[:, 2:] *= torch.Tensor([width, height, width, height]).to(self.device)  # to pixels
            labels = [targets[targets[:, 0] == i, 1:] for i in range(nb)]
            out = non_max_suppression(out, conf_thres=self.conf_thresh, iou_thres=self.nms_thresh, labels=labels, multi_label=True)

        for si, det in enumerate(out):
            result = []
            if len(det):
                detn = det.clone()
                detn[:, :4] = scale_coords(image[si].shape[1:], detn[:, :4], tuple(shapes[si][0])).round()
                for *xyxy, conf, cls in reversed(detn.tolist()):
                    if conf > self.conf_thresh:
                        if score_max == 100:
                            score = float(conf) * score_max
                        else:
                            score = float(conf)
                        x = float(xyxy[0])
                        y = float(xyxy[1])
                        w = float(xyxy[2]) - x
                        h = float(xyxy[3]) - y
                        str_class = self.class_names[int(cls)]
                        if w > 10 and h > 10:
                            result.append({
                                'label': [{
                                    'description': str_class,
                                    'score': score,
                                    'class_idx': self.class_names.index(str_class)
                                }],
                                'position': {
                                    'x': x,
                                    'y': y,
                                    'w': w,
                                    'h': h
                                }
                            })
            results.append(result)
        self.results = results
        out_images = []
        for image, result in zip(images, results):
            image_with_boxes = self.draw_bounding_boxes(image, result)
            out_images.append(image_with_boxes)

        return results, out_images

    def inference(self, image, is_batch=True):
        if is_batch :
            return self.inference_image_batch(image)
        else:
            return self.inference_image(image)
