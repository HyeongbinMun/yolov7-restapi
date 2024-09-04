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
echo "Download start(yolov7-w6 display fault)"
wget -q ftp://mldisk.sogang.ac.kr/etri/webui/models/yolov7e6e_webui.pt -O /workspace/model/weights/yolov7e6e_webui.pt \
&& echo "Download successful(yolov7-w6 display fault)" \
|| echo "\e[31mDownload failed(yolov7-w6 display fault)\e[0m"
echo "======================================="
