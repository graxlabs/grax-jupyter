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

Run `heroku addons:attach grax` 

To set 

```
GRAX_DATALAKE_URL=
```

#### For S3 persistence

Run `heroku addons:add bucketeer --as S3`

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