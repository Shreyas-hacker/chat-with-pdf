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
mamba activate haidonggpt

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


curl -X POST \
  https://api.together.xyz/inference \
  -H 'Authorization: Bearer 0fa26b7b2dcb2c0dfb5c5e81087c7e26eaf30b602f767898b04183f8de16d36a' \
  -H 'Content-Type: application/json' \
  -d '{"model": "togethercomputer/CodeLlama-13b-Instruct",  "prompt": "<s> [INST] <<SYS>> You are an e-commerce seller who is listing a product on an e-commerce platform and required to give me the result aboutproduct in json format based on product information inputed{”title”:””,”description":"","brand":"","category":"","variant":{"key":["value"]},"specifications":{"key":["value"]}} The title should not exceed 20 words and contain the main features and uses. descriptions can be based on input text and your own knowledge base, with a length between 200 and 250 words. variant should be physical \attributes of product and the value of each variant can be multiple.specifications can not be empty. the product inputed delimited by backticks listed<</SYS>> This is a Xiaomi 13 Ultra smartphone with 5.7 inches display of \FHD resolution. It is available in space grey and black with storage from 256GB to 1TB.[/INST]",  "max_tokens": 128,  "stop": ".",  "temperature": 0.7,  "top_p": 0.7,  "top_k": 50,  "repetition_penalty": 1}'

