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


# Google OAuth
Go to the Google API Console OAuth consent screen page.
Choose Internal so only users within your organization can access the app.
Fill in the necessary information.
Click Add Scopes and add any necessary scopes you require. For this example, we don’t need any.



#### Acknowledgements
* Duc Anh Bui, Implementing Google OAuth in Streamlit
  - https://towardsdatascience.com/implementing-google-oauth-in-streamlit-bb7c3be0082c
