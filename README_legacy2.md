# preview demo video

![img.png](docs/img.png)
![img_1.png](docs/img_1.png)
# Step 1 Cloud resources
## 1.1 create ecs with security group 8501 open


# Step 2 env init
![img_22.png](docs/img_22.png)

```apt update && apt install git -y && apt install unzip -y && apt install docker-compose -y && apt install postgresql -y```
![img_23.png](docs/img_23.png)

# Step 3 install packages
```git clone https://github.com/daviddhc20120601/chat-with-pdf.git && cd chat-with-pdf/```
![img_24.png](docs/img_24.png)

# Step 4 run the docker
```cp .devops/Dockerfile . && docker build . -t haidonggpt/front:1.0   && docker run -d -p 8501:8501 haidonggpt/front:1.0```
![img_25.png](docs/img_25.png)

# Step 5 insert you token and start using
![img_26.png](docs/img_26.png)
## 5.1 chatgpt token:
[steps](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)
