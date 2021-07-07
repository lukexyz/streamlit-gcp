# streamlit-gcp

#### Deploy in Google App Engine

1. In GCP cloud shell
```sh
git clone https://github.com/lukexyz/streamlit-gcp.git
cd streamlit-gcp
```

2. Deploy into app engine
```sh
gcloud app deploy app.yaml
# choose location
```

# Contents

### Dockerfile
```sh
#Base Image to use
FROM python:3.7.9-slim

#Expose port 8080
EXPOSE 8080

#Copy Requirements.txt file into app directory
COPY requirements.txt app/requirements.txt

#install all requirements in requirements.txt
RUN pip3 install -r app/requirements.txt

#Copy all files in current directory into app directory
COPY . /app

#Change Working Directory to app directory
WORKDIR /app

#Run the application on port 8080
CMD streamlit run --server.port 8080 --server.enableCORS false app.py
```

___

### app.yaml
```sh
runtime: custom
env: flex
manual_scaling: 
  instances: 1
resources:
  cpu: 1
  memory_gb: 0.5
  disk_size_gb: 10
```

### Streamlit app.py
```py
import streamlit as st
st.title('Counter Example')
...
```
