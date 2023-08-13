#!/bin/bash\n
# oss and model file
#sudo -v ; curl https://gosspublic.alicdn.com/ossutil/install.sh | sudo bash
#ossutil cp -r oss://aigcsg/models--TheBloke--Llama-2-13B-chat-GGML /root/.cache/huggingface/hub/

# upgrade python to 3.11

apt remove python3.8 -y &&
apt update &&
apt install software-properties-common -y &&
apt-get install software-properties-common -y &&
add-apt-repository ppa:deadsnakes/ppa && apt update &&
apt install python3.11 -y &&
apt install python3.11-dev -y &&
apt install python3-pip -y &&
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 &&
apt install python3-pip -y &&
apt install python3.11-distutils -y

# install mamba
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh" &&
bash Mambaforge-$(uname)-$(uname -m).sh

# restart shell
mamba create --name "haidonggpt" python=3.11 &&
mamba install -y --name "teshaidonggptter" -c conda-forge numpy pandas ipykernel jupyter pip-tools fastapi

# gcc

# apt install gcc-11 g++-11

# pg install

apt-get update && apt-get install apt-utils && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
 #
 ## install pg_config
#apt-get update && apt-get install wget ca-certificates -y && apt-get install -y gnupg2
#wget --quiet -O - https://www.postgresql.org/sudo apt install postgresql postgresql-contribmedia/keys/ACCC4CF8.asc | apt-key add - && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list'&&
#apt-get update && apt-get install postgresql postgresql-contrib -y

apt install libpq-dev -y # for pgconfig

apt update && apt install git -y && apt install unzip -y && apt install docker-compose -y && apt install postgresql -y

git clone https://github.com/daviddhc20120601/chat-with-pdf.git && cd chat-with-pdf/

git checkout llama2

cp .devops/Dockerfile . && docker build . -t haidonggpt/front:1.0

#docker run -d -e /etc/environmentadb -p 8501:8501 haidonggpt/front:1.0  -v /root/.cache/huggingface/hub:models

docker run -p 8501:8501 haidonggpt/front:1.0  -v /root/.cache/huggingface/hub:models



