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
echo "Download start(yolov7-w6 webui)"
wget -q ftp://mldisk.sogang.ac.kr/etri/webui/models/yolov7e6e_webui.pt -O /workspace/model/weights/yolov7e6e_webui.pt \
&& echo "Download successful(yolov7-w6 webui)" \
|| echo "\e[31mDownload failed(yolov7-w6 webui)\e[0m"
echo "======================================="

echo "======================================="
echo "Download start(yolov11-w6 webui)"
wget -q ftp://mldisk.sogang.ac.kr/etri/webui/models/yolov11e6e_webui.pt -O /workspace/model/weights/yolov11e6e_webui.pt \
&& echo "Download successful(yolov11-w6 webui)" \
|| echo "\e[31mDownload failed(yolov11-w6 webui)\e[0m"
echo "======================================="
