# Windows 10 WSL2 & Docker Installation Guide

## 1\. Install WSL2

### Windows Terminal에서 커맨드 실행

*   설치
    
    ```
    wsl --install
    ```
    
*   설치 완료 후 컴퓨터 재부팅
    
    ```
    wsl --status
    ```    

      ![](https://github.com/JinhaSong/yolov7-restapi/blob/main/docs/Installation/1.png)


## 2\. start WSL2

### 검색 창에서 ubuntu 검색 후 해당 아이콘 실행

![image-20231014-130615](https://github.com/JinhaSong/yolov7-restapi/blob/main/docs/Installation/2.png)


## 3\. Install CUDA for WSL2

### 우분투 패키지 업데이트

*   설치
    
    ```
    sudo apt update && sudo apt install -y gcc vim wget zip
    ```
    
*   해당 링크에서 Get CUDA Driver 버튼을 통해 드라이버 다운로드
    
*   CUDA for WSL-ubuntu download : [download link](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=runfile_local)
    
    *   경로 : Linux → x86\_64-WSL → Ubuntu-2.0 → runfile(local)
        
    *   Base Installer 커맨드에 따라서 설치
    
*   ```sudo sh cuda_12.2.2_535.104.05_linux.run``` 커맨드 입력 시 아래와 같이 진행
    

      ![image-20231014-132501](https://github.com/JinhaSong/yolov7-restapi/blob/main/docs/Installation/3.png)
*   accept 입력 후 enter

![image-20231014-132541](https://github.com/JinhaSong/yolov7-restapi/blob/main/docs/Installation/4.png)

*   CUDA Toolkit 12.2 만 체크 후 Install에서 Enter
*   체크는 spacebar로 해제 가능


## 4\. Install Docker

### 가상환경 Docker를 쓰기 위한 패키지 설치

*   apt key 추가
    
    ```
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```
    
*   apt key 추가 확인
    
    ```
    sudo apt-key fingerprint 0EBFCD88
    ```
    
    *   다음 출력을 확인
        
        ```
        pub   4096R/0EBFCD88 2017-02-22
              Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
        uid                  Docker Release (CE deb) <docker@docker.com>
        sub   4096R/F273FCD8 2017-02-22
        ```
        
*   apt repository 추가
    
    ```
    sudo add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"
    sudo apt-get update
    ```
    
*   Docker 설치
    
    ```
    sudo apt-get install -y docker-ce
    ```
    
*   Docker test
    
    ```
    sudo docker run hello-world
    ```
    
    *   다음 출력을 확인
        
        ```
        Hello from Docker!
        This message shows that your installation appears to be working correctly.
         
        To generate this message, Docker took the following steps:
         1. The Docker client contacted the Docker daemon.
         2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
            (amd64)
         3. The Docker daemon created a new container from that image which runs the
            executable that produces the output you are currently reading.
         4. The Docker daemon streamed that output to the Docker client, which sent it
            to your terminal.
         
        To try something more ambitious, you can run an Ubuntu container with:
         $ docker run -it ubuntu bash
         
        Share images, automate workflows, and more with a free Docker ID:
         https://cloud.docker.com/
         
        For more examples and ideas, visit:
         https://docs.docker.com/engine/userguide/
        ```
        
*   특정 user에 Docker 실행권한 부여
    
    *   ex) user id가 test인 경우
        
        ```
        sudo usermod -aG docker $USER    # $USER 부분에 test 입력
        sudo reboot
        ```
        

## 5\. Install Docker-compose

### 가상환경 Docker를 쓰기 위한 패키지 설치

*   설치 및 실행권한 부여
    
    ```
    sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) \
    -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```
    
*   설치 확인
    
    ```
    docker-compose --version
    ```
    
    *   다음 출력을 확인
        
        ```
        docker-compose version 1.21.2, build 1719ceb
        ```
        

## 6\. Install Nvidia-docker2

### 가상환경 Docker를 쓰기 위한 패키지 설치

*   apt key 및 repository 추가
    
    ```
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
      sudo apt-key add -
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
      sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    sudo apt-get update
    ```
    
*   nvidia-docker2 설치
    
    ```
    sudo apt-get install -y nvidia-docker2
    ```
    
*   Window PC 재부팅
  
