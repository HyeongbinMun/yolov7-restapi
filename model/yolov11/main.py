import torch
import cv2
import numpy as np
import os
from pathlib import Path
from models.yolo.model import YOLO as InternalYOLO  # 기존 model.py 내부 YOLO 클래스
from models.yolo.detect.predict import DetectionPredictor


class YOLOv11:

    def __init__(self, model_path="/workspace/model/weights/best.pt", image_size=1280, conf_thresh=0.25, iou_thresh=0.45):
        self.model = InternalYOLO(model_path)
        self.image_size = image_size
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh

        self.class_names = self.model.model.names
        self.predictor = DetectionPredictor(overrides={
            "model": model_path,
            "conf": self.conf_thresh,
            "iou": self.iou_thresh,
            "imgsz": self.image_size
        })

    def draw_bounding_boxes(self, image, results):
        color_map = {
            'text': (255, 0, 0),
            'image': (0, 255, 0),
            'button': (0, 0, 255),
            'heading': (255, 255, 0),
            'link': (255, 0, 255),
            'input': (0, 255, 255)
        }

        for result in results:
            label = result['label'][0]['description']
            score = result['label'][0]['score']
            x = int(result['position']['x'])
            y = int(result['position']['y'])
            w = int(result['position']['w'])
            h = int(result['position']['h'])

            color = color_map.get(label, (255, 255, 255))
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, f"{label}: {score:.2f}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return image

    def _convert_results(self, result_obj, score_max=1):
        detections = []
        for box in result_obj.boxes.data.cpu().numpy():
            x1, y1, x2, y2, score, cls = box
            label = self.class_names[int(cls)]
            score_val = float(score * score_max) if score_max == 100 else float(score)
            detections.append({
                "label": [{
                    "description": label,
                    "score": score_val,
                    "class_idx": int(cls)
                }],
                "position": {
                    "x": float(x1),
                    "y": float(y1),
                    "w": float(x2 - x1),
                    "h": float(y2 - y1)
                }
            })
        return detections

    def inference_image(self, image, score_max=1, conf_thresh=None):
        results = self.model.predict(image, conf=conf_thresh or self.conf_thresh)
        parsed = self._convert_results(results[0], score_max=score_max)
        image_with_boxes = self.draw_bounding_boxes(image.copy(), parsed)
        return parsed, image_with_boxes

    def inference_image_batch(self, images, conf_thresh=None, score_max=1):
        all_results = []
        all_out_images = []

        for image in images:
            parsed, image_with_boxes = self.inference_image(image, score_max=score_max, conf_thresh=conf_thresh)
            all_results.append(parsed)
            all_out_images.append(image_with_boxes)

        # 클래스별 이미지 시각화
        for image, result in zip(images, all_results):
            for class_idx in range(len(self.class_names)):
                label_specific_results = [res for res in result if res['label'][0]['class_idx'] == class_idx]
                if label_specific_results:
                    image_copy = image.copy()
                    image_labeled = self.draw_bounding_boxes(image_copy, label_specific_results)
                    all_out_images.append(image_labeled)

        return all_results, all_out_images

    def inference(self, image, conf_thresh=None, is_batch=True):
        if is_batch:
            return self.inference_image_batch(image, conf_thresh)
        else:
            return self.inference_image(image, conf_thresh)


# if __name__ == "__main__":
#     import cv2
#     import numpy as np

#     image_path = "C:/Users/Moon/Desktop/코딩/연구실과제/package/yolov11/test1.jpg"
#     image = cv2.imread(image_path)

#     model = YOLOv11()
#     results, image_with_boxes = model.inference(image, is_batch=False)

#     print("결과:", results)

#     if image_with_boxes is not None:
#         if image_with_boxes.dtype != np.uint8:
#             image_with_boxes = (image_with_boxes * 255).astype(np.uint8)
#         saved = cv2.imwrite("C:/Users/Moon/Desktop/코딩/연구실과제/package/yolov11/result.jpg", image_with_boxes)
#         print("저장 성공 여부:", saved)
#     else:
#         print("image_with_boxes가 None입니다.")