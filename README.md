# GRAX Notebook 

Data analytics with Jupyter for GRAX Data Lakehouse on Heroku.

This repo provides an installation of JupyterHub to allow multi-user access
to a set of notebooks. It includes a small client that provides SQL access to the
Lakehouse and has the ability to customize user login (via OAuth) and file storage
on S3. 

## Installation

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.png)](https://www.heroku.com/deploy/?template=https://github.com/graxlabs/grax-jupyter/tree/main)

### Required Config

#### Data Lake Credentials

Eventually:
Run `heroku addons:add grax:datalake`
or
Run `heroku addons:attach grax:datalake`

Until then, these credentials will be provided by a GRAX admin:
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_STAGING_DIR=
AWS_WORKGROUP=
ATHENA_DATABASE=
```

#### For S3 persistence

Run `heroku addons:add bucketeer`

#### For Heroku OAuth:

Heroku makes it simple to create a new OAuth client.

Run `heroku labs:enable runtime-dyno-metadata`

To enable in the Environment: 
```
HEROKU_APP_DEFAULT_DOMAIN_NAME=
```

Run 
```bash
heroku clients:create "GRAX Jupyter for <INSTALLATION>" https://<HEROKU_APP_DEFAULT_DOMAIN_NAME>/hub/oauth_callback
```

To set:
```
HEROKU_OAUTH_SECRET=
HEROKU_OAUTH_ID=
```