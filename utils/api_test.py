import requests
import time

# api url
url = 'http://mlgrape.sogang.ac.kr:28777/image/'

# test image
image_path = '1.png'

with open(image_path, 'rb') as image_file:
    response = requests.post(url, files={'image': image_file})

if response.status_code == 201:
    data = response.json()
    image_token = data['image_token']
    print(f"처리 시작. 5초 대기 후 결과를 확인합니다. (image_token={image_token})")
    time.sleep(5)

    result_url = f"{url}{image_token}/"
    result_response = requests.get(result_url)

    if result_response.status_code == 200:
        result_data = result_response.json()
        print("=== 전체 결과 ===")
        print(result_data)
        print("\n--- 디텍션 결과 ---")
        print(result_data.get('result'))
        print("\n--- 결과 이미지들 ---")
        print(result_data.get('result_images'))
        print("\n--- 기타 정보 ---")
        print(f"conf_threshold: {result_data.get('conf_threshold')}")
        print(f"uploaded_date: {result_data.get('uploaded_date')}")
        print(f"updated_date: {result_data.get('updated_date')}")
    else:
        print(f"결과를 아직 받을 수 없습니다. status: {result_response.status_code}, message: {result_response.text}")

else:
    print("에러 발생:", response.status_code, response.text)
