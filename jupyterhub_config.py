import os
import binascii
from jupyterhub.spawner import SimpleLocalProcessSpawner

if os.getenv('HEROKU_OAUTH_ID'):
    print("Using OAuth for login")
    c.JupyterHub.authenticator_class = "generic-oauth"

    c.GenericOAuthenticator.client_id = os.getenv('HEROKU_OAUTH_ID') 
    c.GenericOAuthenticator.client_secret = os.getenv('HEROKU_OAUTH_SECRET') 
    c.GenericOAuthenticator.oauth_callback_url = 'https://' + os.getenv('HEROKU_APP_DEFAULT_DOMAIN_NAME') + '/hub/oauth_callback'

    c.GenericOAuthenticator.scope = ["identity"]

    c.GenericOAuthenticator.authorize_url = "https://id.heroku.com/oauth/authorize"
    c.GenericOAuthenticator.token_url = "https://id.heroku.com/oauth/token"
#    c.GenericOAuthenticator.userdata_url = 'https://api.heroku.com/account'

    c.Authenticator.allow_all = True

    c.HerokuOAuthenticator.userdata_from_id_token = True
    c.GenericOAuthenticator.username_key = 'email'
    c.GenericOAuthenticator.userdata_params = {'session': 'user'}

else:
    # setting a dummy user admin for now
    c.JupyterHub.authenticator_class = "dummy"
    c.DummyAuthenticator.password = "admin"

# using simplelocalspawner for now
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner
c.Spawner.cmd = ['jupyter-labhub']

# for creating new users
c.LocalAuthenticator.add_user_cmd = ['python3','/app/analysis/create-user.py','USERNAME']
c.LocalAuthenticator.create_system_users = True

# c.Spawner.pre_spawn_hook = lambda spawner: spawner.pip_install(['./grax_athena'])

c.Spawner.environment = {
    'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
    'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
    'AWS_REGION': os.environ.get('AWS_REGION'),
    'ATHENA_DATABASE': os.environ.get('ATHENA_DATABASE'),
    'S3_STAGING_DIR': os.environ.get('S3_STAGING_DIR')
}

c.JupyterHub.cookie_secret = os.urandom(32)

"""
# for xsrf
# Trust Heroku's proxy headers
c.JupyterHub.trusted_downstream_ips = ['*']
c.JupyterHub.proxy_headers = {
    'X-Scheme': 'https',
    'X-Forwarded-For': 'X-Forwarded-For',
    'X-Forwarded-Proto': 'X-Forwarded-Proto'
}

# Use secure cookies
c.ConfigurableHTTPProxy.auth_token = binascii.hexlify(os.urandom(32)).decode('ascii')

# Specify the proxy class
c.JupyterHub.proxy_class = 'jupyterhub.proxy.ConfigurableHTTPProxy'
"""
