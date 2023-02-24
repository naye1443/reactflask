# Important Info
[Here](https://blog.ldtalentwork.com/2019/11/29/how-to-serve-a-reactapp-with-a-flask-server/) is how to Build react files into a flask appliaction.
## Steps of creating a container registery image
---
[here](https://cloud.google.com/run/docs/deploying) is the syntax for creating a container registry image
### Building docker image
---
```sh
docker build -t python_server:1.0 .
```
### running docker image to test image
---
```sh
docker run -d -p 80:80 python_server:1.0
```
### Create Tag for docker image
---
```sh
docker tag python_server:1.0 gcr.io/[Project-Id]/webapp:v1
```
### Push tag to container Registry
---
```sh
docker push gcr.io/[Project-Id]/webapp:v1
```