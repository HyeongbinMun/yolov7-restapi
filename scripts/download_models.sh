DIR="/workspace/model/weights"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
  # If the directory does not exist, create it
  mkdir -p "$DIR"
  echo "Directory $DIR created."
else
  echo "Directory $DIR already exists."
fi

echo "======================================="
echo "Download start(yolov7-w6 webui 24)"
wget -q ftp://mldisk.sogang.ac.kr/etri/webui/models/yolov7e6e_webui_240812.pt -O /workspace/model/weights/yolov7e6e_webui_240812.pt \
&& echo "Download successful(yolov7-w6 webui 24)" \
|| echo "\e[31mDownload failed(yolov7-w6 webui 24)\e[0m"
echo "======================================="

echo "======================================="
echo "Download start(yolov7-w6 webui 25)"
wget -q ftp://mldisk.sogang.ac.kr/etri/webui/models/yolov7e6e_webui_250401.pt -O /workspace/model/weights/yolov7e6e_webui_250401.pt \
&& echo "Download successful(yolov7-w6 webui 25)" \
|| echo "\e[31mDownload failed(yolov7-w6 webui 25)\e[0m"
echo "======================================="
