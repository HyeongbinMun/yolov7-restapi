import os
import cv2
import torch
import numpy as np
from math import ceil
from PIL import Image
from torchvision import transforms
from model.efficientnet.efficientnet_pytorch import EfficientNet


class EfficientNetInference:
    def __init__(self):
        self.arch='efficientnet-b0'
        self.batch_size = 32
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model_path = '/workspace/model/weights/efficientnet_b0_250805.pth'
        self.image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

        # 모델 로드
        self.model = EfficientNet.from_name(self.arch, num_classes=1)
        checkpoint = torch.load(self.model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['state_dict'])
        self.model.to(self.device)
        self.model.eval()

        # 전처리 정의
        image_size = EfficientNet.get_image_size(self.arch)
        self.transform = transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    def infer_batch(self, images):
        """
        images: list of OpenCV images (numpy.ndarray, BGR format)
        returns: list of dicts with keys: index, pred, prob
        """
        results = []
        num_images = len(images)

        for i in range(0, num_images, self.batch_size):
            batch_images = images[i:i + self.batch_size]
            pil_images = [Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) for img in batch_images]
            input_tensors = torch.stack([self.transform(img) for img in pil_images]).to(self.device)

            with torch.no_grad():
                outputs = self.model(input_tensors)
                probs = torch.sigmoid(outputs).squeeze(1)
                pred_classes = (probs > 0.5).long()

            for idx, (pred, prob) in enumerate(zip(pred_classes, probs)):
                results.append({
                    'index': i + idx,
                    'pred': pred.item(),
                    'prob': round(prob.item(), 4)
                })

        return results

    def infer_batch_dict(self, images, results):
        """
        images: list of OpenCV images (numpy.ndarray, BGR format)
        results: list of detection results for each image
        """
        crop_images = []
        crop_index = []

        for idx, (img, result) in enumerate(zip(images, results)):
            for obj in result:
                label = obj.get('label', [{}])[0]
                if label.get('class_idx') == 2:  # class_idx == 2 인 경우만 처리
                    pos = obj.get('position', {})
                    x, y, w, h = int(pos['x']), int(pos['y']), int(pos['w']), int(pos['h'])

                    # 유효한 크기일 때만 crop
                    if w > 0 and h > 0:
                        crop = img[y:y + h, x:x + w]
                        if crop.size > 0:
                            crop_images.append(crop)
                            crop_index.append((idx, obj))  # 이미지 인덱스와 해당 객체 참조 저장

        # 크롭된 이미지가 없으면 바로 리턴
        if not crop_images:
            return results

        # 추론할 크롭 이미지 전처리
        pil_images = [Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)) for crop in crop_images]
        input_tensors = torch.stack([self.transform(img) for img in pil_images]).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_tensors)
            probs = torch.sigmoid(outputs).squeeze(1)
            pred_classes = (probs > 0.5).long()

        # 결과에 따라 description 업데이트
        for pred, (img_idx, obj) in zip(pred_classes, crop_index):
            label = obj.get('label', [{}])[0]
            if label.get('description') == 'button':
                label['description'] = 'play_button' if pred.item() == 0 else 'normal_button'

        return results

# main 함수 예시
if __name__ == '__main__':
    pass
    # classifier = EfficientNetInference()
    # img1 = cv2.imread("/workspace/images/1.jpg")
    # img2 = cv2.imread("/workspace/images/2.jpg")
    # img3 = cv2.imread("/workspace/images/3.jpg")
    # img4 = cv2.imread("/workspace/images/4.jpg")
    # img_list = [img1, img2, img3, img4]
    # results = classifier.infer_batch(img_list)
    # print('results : ', results)

