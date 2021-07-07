# streamlit-gcp

#### Deploy in Google App Engine

1. Clone repo into GCP cloud shell
```sh
$ git clone https://github.com/lukexyz/streamlit-gcp.git
$ cd streamlit-gcp
```  


2. Deploy into app engine
```sh
$ gcloud app deploy app.yaml
# choose location and proceed
```  


3. To view your application url
 ```sh
 $ gcloud app browse
 ```
* Or look for the url at the top-right of the `app engine` dashboard
  * (Something like https://streamlit-gcp-319114.uc.r.appspot.com/)


# Contents


### Dockerfile


### app.yaml


### app.py
