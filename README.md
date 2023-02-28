# ReactFlask
## Reason for application
---
The motive behind the creation of this application was to create a serverless application that utilizes both Blob storage with and non-Relational persistance to store images. The application interfaces with both systems to simulate a production-ready application.
# Important Info
[Here](https://blog.ldtalentwork.com/2019/11/29/how-to-serve-a-reactapp-with-a-flask-server/) is how to Build react files into a flask appliaction.
## Steps of creating a container registery image
---
[here](https://cloud.google.com/run/docs/deploying) is the syntax for creating a container registry image
### Building docker image
---
> Note, These commands must be run in gcp cloud console or with gcloud cli installed
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
## Used technologies
---
Technologies include:

|depenency | use|
|:---------|:---|
|react     | Used for frontend|
|python/flask| Used to handle http request|
|google-cloud-storage| Used to store images buckets|
|google-cloud-datastore| Used to store metadata|

## Future improvements
---
In the future, we would like to automate the deployment for this application. We would also like traffic to be split evenly between users and have multiple instance running in parallel.