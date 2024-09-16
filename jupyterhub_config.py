import os
import sys
import binascii
import subprocess
from jupyterhub.spawner import SimpleLocalProcessSpawner
from oauthenticator.generic import GenericOAuthenticator
from s3contents import S3ContentsManager
import logging

#c.JupyterHub.log_level = logging.DEBUG

class HerokuOAuthenticator(GenericOAuthenticator):
    login_service = "Heroku"

    # used for userdata_url flows
    def build_userdata_request_headers(self, access_token, token_type):
        headers = super().build_userdata_request_headers(access_token, token_type)
        headers["Accept"] = "application/vnd.heroku+json; version=3"
        return headers

    # used for userdata_from_id_token flows
    async def token_to_user(self, token_info):
        print("TOKEN INFO:")
        print(token_info)
        # Heroku includes user info in the token response, so we don't need to make an additional request
        return {
            "name": token_info["user_id"],
            "auth_state": {
                "access_token": token_info["access_token"],
                "refresh_token": token_info.get("refresh_token"),
                "token_type": token_info["token_type"],
                "expires_in": token_info["expires_in"],
                "scope": token_info.get("scope", "").split(),
            }
        }

    def user_info_to_username(self, user_info):
        print("USER INFO:")
        print(user_info)
        # The username is the user_id in this case
        return user_info["name"]

if os.getenv('HEROKU_OAUTH_ID'):
    print("Using OAuth for login")

    c.JupyterHub.authenticator_class = HerokuOAuthenticator 
    #c.JupyterHub.authenticator_class = "oauthenticator.generic.GenericOAuthenticator"

    #c.HerokuOAuthenticator.login_service = 'Heroku'

    c.HerokuOAuthenticator.client_id = os.getenv('HEROKU_OAUTH_ID') 
    c.HerokuOAuthenticator.client_secret = os.getenv('HEROKU_OAUTH_SECRET') 
    c.HerokuOAuthenticator.oauth_callback_url = 'https://' + os.getenv('HEROKU_APP_DEFAULT_DOMAIN_NAME') + '/hub/oauth_callback'

    c.HerokuOAuthenticator.scope = ["identity"]

    c.HerokuOAuthenticator.authorize_url = "https://id.heroku.com/oauth/authorize"
    c.HerokuOAuthenticator.token_url = "https://id.heroku.com/oauth/token"

    c.GenericOAuthenticator.userdata_url = 'https://api.heroku.com/account'
    c.HerokuOAuthenticator.userdata_from_id_token = False

    c.HerokuOAuthenticator.username_claim = 'email'

    c.Authenticator.allow_all = True
else:
    # setting a dummy user admin for now
    c.JupyterHub.authenticator_class = "dummy"
    c.DummyAuthenticator.password = "admin"

# using simplelocalspawner for now
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.cookie_secret = os.urandom(32)

spawner_env = dict(os.environ)
spawner_env['LD_LIBRARY_PATH'] = '/app/.heroku/vendor/lib:/app/.heroku/python/lib:' + spawner_env.get('LD_LIBRARY_PATH', '')
c.Spawner.environment = spawner_env

c.Spawner.cmd = ['jupyter-labhub']
c.Spawner.args = [
    f'--ServerApp.contents_manager_class=s3contents.S3ContentsManager',
    f'--S3ContentsManager.bucket={os.environ.get("BUCKETEER_BUCKET_NAME")}',
    f'--S3ContentsManager.access_key_id={os.environ.get("BUCKETEER_AWS_ACCESS_KEY_ID")}',
    f'--S3ContentsManager.secret_access_key={os.environ.get("BUCKETEER_AWS_SECRET_ACCESS_KEY")}',
    f'--S3ContentsManager.region_name={os.environ.get("BUCKETEER_AWS_REGION")}',
]

NOTEBOOK_DIR = os.environ.get('NOTEBOOK_DIR', 'notebooks')
def pre_spawn_hook(spawner):
    spawner.args.append(f"--S3ContentsManager.prefix={NOTEBOOK_DIR}/{spawner.user.name}/")

c.Spawner.pre_spawn_hook = pre_spawn_hook

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
