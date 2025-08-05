import torch
import os
from torchvision import transforms
from PIL import Image
import argparse
from math import ceil
from efficientnet_pytorch import EfficientNet

# argparse
parser = argparse.ArgumentParser()

# 서로 배타적인 입력 그룹 설정
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--image', type=str, help='Path to a single image')
group.add_argument('--input-dir', type=str, help='Path to a directory of images')

# 기타 설정
parser.add_argument('--model', type=str, required=True, help='Path to model checkpoint')
parser.add_argument('--arch', type=str, default='efficientnet-b0')
parser.add_argument('--gpu', type=int, default=None)
parser.add_argument('--batch-size', type=int, default=32, help='Batch size for inference')
args = parser.parse_args()

# 이미지 확장자 필터
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

# Set device
device = torch.device(f'cuda:{args.gpu}' if args.gpu is not None and torch.cuda.is_available() else 'cpu')

# Load model
model = EfficientNet.from_name(args.arch, num_classes=1)
checkpoint = torch.load(args.model, map_location=device)
model.load_state_dict(checkpoint['state_dict'])
model.to(device)
model.eval()

image_size = EfficientNet.get_image_size(args.arch)
transform = transforms.Compose([
    transforms.Resize(image_size),
    transforms.CenterCrop(image_size),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# Inference
def infer_batch(image_paths):
    batch_size = args.batch_size
    num_images = len(image_paths)
    for i in range(0, num_images, batch_size):
        batch_paths = image_paths[i:i + batch_size]
        images = [Image.open(p).convert('RGB') for p in batch_paths]
        input_tensors = torch.stack([transform(img) for img in images]).to(device)

        with torch.no_grad():
            outputs = model(input_tensors)
            probs = torch.sigmoid(outputs).squeeze(1)  # (N,)
            pred_classes = (probs > 0.5).long()
            confidences = torch.where(pred_classes == 1, probs, 1 - probs)

        for path, pred, conf, logit in zip(batch_paths, pred_classes, confidences, outputs.squeeze(1)):
            print(f"[{os.path.basename(path)}] → Predicted: {pred.item()} (Confidence: {conf.item()*100:.2f}%) | Logit: {logit.item():.2f}")
        
if args.image:
    infer_batch([args.image])  # 하나만 있어도 리스트로 감싸야 함
else:
    image_paths = [os.path.join(args.input_dir, fname)
                   for fname in os.listdir(args.input_dir)
                   if fname.lower().endswith(image_extensions)]
    image_paths.sort()
    infer_batch(image_paths)