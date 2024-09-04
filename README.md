# yolov7-restapi

- [Introduce](#introduce)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [API 결과](#api-결과)
    
## Introduce

본 프로젝트는 Neural Network의 결과를 REST API로 서비스 하기 위한 웹 서버를 제공합니다.

Python 코드로 구성되어 있으며, Django 및 Django REST framework를 사용하여 개발하였습니다.

Linux 사용을 가정하여 코드를 작성하였으며, 만약 다른 환경에서의 설치를 진행하려면 문의하시기 바랍니다.

프로젝트의 개발은 docker container에서 진행하시기를 권장합니다.

## Prerequisites

- Linux Based OS or WSL Ubuntu
  - [Install WSL Ubuntu and blow reqirements](docs/Installation/Windows.md)
- Python 3
- nvidia-driver >= 515 & CUDA >= 11.7
- docker.ce
- docker-compose==1.21.2
- nvidia-docker2


## Installation
- 이후, 디렉토리 내에서 다음과 같은 부분을 수정합니다.

1. docker-compose.yml
    * Module의 외부 통신을 위한 Port 수정이 필요하다면 다음을 수정합니다.
    ```docker
   service:
     ...
     main:
       container_name: yolov7-restapi_django
       ...
       ports:
       - "8777:8000" # -> 변경
    ```

2. docker/main.env
    * 특정 GPU만 사용하는 환경을 구성하고 싶다면 다음을 수정합니다.
    * 만약 GPU 번호를 바꾸고 싶으면 0을 1로 변경합니다.
    * torch 모델은 기본적으로 GPU를 하나만 쓰도록 설정되어 있습니다.
    ```text
    NVIDIA_VISIBLE_DEVICES=0 # -> 1
    ```    
    * all을 사용 시, 전체 GPU를 사용한다. 만약 0번 GPU만을 사용하고 싶다면 NVIDIA_VISIBLE_DEVICES=0으로 수정합니다.

- 모든 설정이 끝났다면 docker 디렉토리 내에서 ```docker-compose up -d```으로 실행하면 웹 서버가 시작됩니다.
- ```http://${SERVER_IP}:8777/```로 접근하여 접속이 되는지 확인합니다.
- 웹 서버가 실행된 것을 확인하였으면 Module 추가를 위해 main container에 docker attach로 접근하여 일단 웹 서버를 종료합니다.
    
    ```bash
    docker attach yolov7-restapi_django
    Ctrl + C
    sh server_shutdown.sh
    ```

- Docker container에 ssh 로 접속하고 싶은 경우, 아래와 같이 계정의 password를 설정하고 ssh service를 시작한다.
  ```bash
  passwd
  service ssh start
  ```
 

## API 결과

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "token": 1,
            "image": "http://163.239.25.46:8777/media/20230906/test_LQS2TQ3.jpg",
            "uploaded_date": "2023-09-06T22:04:27.198410+09:00",
            "updated_date": "2023-09-06T22:04:34.488734+09:00",
            "result_image": "http://163.239.25.46:8777/media/20230906/test_LQS2TQ3_result.png",
            "result": [
                {
                    "age": 24.27,
                    "face": {
                        "h": 53,
                        "w": 49,
                        "x": 925,
                        "y": 287
                    },
                    "gender": {
                        "class": "male",
                        "score": 0.9970703125
                    },
                    "person": {
                        "h": 543,
                        "w": 177,
                        "x": 864,
                        "y": 262
                    }
                },
                {
                    "age": 23.08,
                    "face": {
                        "h": 52,
                        "w": 48,
                        "x": 1037,
                        "y": 272
                    },
                    "gender": {
                        "class": "male",
                        "score": 0.9970703125
                    },
                    "person": {
                        "h": 561,
                        "w": 160,
                        "x": 998,
                        "y": 243
                    }
                }
            ]
        }
    ]
}
```
- 나이 추론 모델은 이미지를 입력으로 받아 결과 이미지와 분석 결과를 출력한다.
- 원본 이미지의 주소는 ```image```, 결과 이미지의 주소는 ```result_image```로 표시되며 결과 이미지에는 사람 객체 bounding box, 얼굴 객체 bounding box, 성별, 나이, 나이 추론 점수가 표시된다.
