







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