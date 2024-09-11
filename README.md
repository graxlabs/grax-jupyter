# GRAX Notebook 

Data analytics with Jupyter for GRAX Data Lakehouse on Heroku.

## Installation

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.png)](https://www.heroku.com/deploy/?template=https://github.com/graxlabs/grax-jupyter/tree/main)

### Required Config

#### Data Lake Credentials

Run `heroku addons:add grax:datalake`

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_STAGING_DIR=
ATHENA_DATABASE=
```

#### For Heroku OAuth:

Run `heroku labs:enable runtime-dyno-metadata`

```
HEROKU_APP_DEFAULT_DOMAIN_NAME=
```

Run `heroku clients:create "GRAX Jupyter" https://<APP DOMAIN>/hub/oauth_callback`

```
HEROKU_OAUTH_SECRET=
HEROKU_OAUTH_ID=
```
