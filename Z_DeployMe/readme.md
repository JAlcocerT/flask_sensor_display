## Deploying

1. Make sure to get docker/container installed

2. Pull the container image:

```sh
docker pull ghcr.io/jalcocert/flask_sensor_display:latest
```

3. Use the docker-compose

```sh
wget https://github.com/JAlcocerT/flask_sensor_display/blob/main/Z_DeployMe/docker-compose.yml
sudo docker-compose up -d
```

Or, a quick CLI:

```sh
docker run --name flask_sensor_webapp \
-v flask_webapp:/app \
-w /app \
-p 9999:9999 \
--restart always \
ghcr.io/jalcocert/flask_sensor_display \
/bin/sh -c "python3 app.py"
```


> [!IMPORTANT]
> See the related [**Data-Chat Container** of this repo](https://github.com/users/JAlcocerT/packages/container/package/flask_sensor_display)



---

```sh
docker build -t flask_sensor .
#podman build -t flask_sensor .
```

```sh
docker run -d \
  --name flask_sensor_webapp \
  -v flaskwebapp:/app \
  -w /app \
  -p 9999:9999 \
  flask_sensor \
  /bin/sh -c "python3 app.py"
```