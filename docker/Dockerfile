FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu22.04

ENV TZ Asia/Seoul
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y install python3 python3-pip python3-dev \
    mysql-client libmysqlclient-dev python3-mysqldb \
    git wget ssh vim \
    apt-utils libgl1 ffmpeg tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN echo "root:password" | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes #prohibit-password/' /etc/ssh/sshd_config

WORKDIR /workspace
ADD . .
RUN while IFS= read -r line; do echo "export $line" >> /root/.bashrc; done < /workspace/docker/main.env
RUN while IFS= read -r line; do echo "export $line" >> /root/.bashrc; done < /workspace/docker/database.env

RUN pip3 install --upgrade pip
RUN pip3 install setuptools
RUN pip3 install torch==2.7.1+cu128 torchvision==0.22.1+cu128 --extra-index-url https://download.pytorch.org/whl/cu128
RUN pip3 install -r requirements.txt

RUN chmod +x scripts/download_models.sh
RUN sh scripts/download_models.sh

COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

RUN chmod -R a+w /workspace

EXPOSE 8000
