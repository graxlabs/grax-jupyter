import os
import binascii
import subprocess
from jupyterhub.spawner import SimpleLocalProcessSpawner
from oauthenticator.generic import GenericOAuthenticator

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
c.Spawner.cmd = ['jupyter-labhub']

c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.debug = True

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

def pre_spawn_hook(spawner):
    spawner.log.info(f"Python executable: {sys.executable}")
    spawner.log.info(f"Current working directory: {os.getcwd()}")
    spawner.log.info(f"Environment PATH: {os.environ.get('PATH', '')}")
    
    try:
        output = subprocess.check_output(['/app/.heroku/python/bin/jupyter-labhub', '--version'], stderr=subprocess.STDOUT)
        spawner.log.info(f"jupyter-labhub version: {output.decode('utf-8').strip()}")
    except subprocess.CalledProcessError as e:
        spawner.log.error(f"Error checking jupyter-labhub version: {e.output.decode('utf-8')}")
    
    try:
        output = subprocess.check_output(['/app/.heroku/python/bin/jupyter-labhub', '--paths'], stderr=subprocess.STDOUT)
        spawner.log.info(f"jupyter-labhub paths:\n{output.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        spawner.log.error(f"Error checking jupyter-labhub paths: {e.output.decode('utf-8')}")

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
