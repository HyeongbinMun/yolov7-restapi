import torch
import os
from torchvision import transforms
from PIL import Image
import argparse
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
def infer(image_path):
    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        logit = output.item()
        prob = torch.sigmoid(output).item()
        pred_class = 1 if prob > 0.5 else 0
        confidence = prob if pred_class == 1 else 1 - prob

    print(f"[{os.path.basename(image_path)}] → Predicted: {pred_class} (Confidence: {confidence*100:.2f}%) | Logit: {logit:.2f}")

    # 🔽 여기만 추가하면 됩니다
    if pred_class == 0:
        os.makedirs("class_0", exist_ok=True)
        image.save(os.path.join("class_0", os.path.basename(image_path)))

if args.image:
    infer(args.image)
else:
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_paths = [os.path.join(args.input_dir, fname)
                   for fname in os.listdir(args.input_dir)
                   if fname.lower().endswith(image_extensions)]
    image_paths.sort()
    for image_path in image_paths:
        infer(image_path)