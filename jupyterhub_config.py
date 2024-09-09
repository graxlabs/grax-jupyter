import os
import binascii
from jupyterhub.spawner import SimpleLocalProcessSpawner

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
c.JupyterHub.cookie_secret = os.urandom(32)
c.ConfigurableHTTPProxy.auth_token = binascii.hexlify(os.urandom(32)).decode('ascii')

# Specify the proxy class
c.JupyterHub.proxy_class = 'jupyterhub.proxy.ConfigurableHTTPProxy'
"""
