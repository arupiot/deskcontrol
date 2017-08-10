from crypt import crypt
from fabric.api import local, settings, abort, run, env, sudo, put, get, prefix, cd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from config_local_pi import PI_PASSWORD

env.hosts = ["%s:%s" % ("raspberrypi.local", 22)]
# env.hosts = ["%s:%s" % ("169.254.162.179", 22)]
env.user = "pi"
env.password = PI_PASSWORD


############################################################################
##              Push code to card for dev                       ##
############################################################################
"""
On the pi stop the default containers from running:

cd /etc/opt/augment00
docker-compose stop

Then push the code with the command update below and run using the dev compose script:

cd /opt/augment00/dev
docker-compose up/start/stop etc as normal

"""

def update():
    sudo("mkdir -p /opt/augment00/dev")
    put("../deskcontrol", "/opt/augment00/dev", use_sudo=True)
    put("docker-compose-dev.yml", "/opt/augment00/dev/docker-compose.yml", use_sudo=True)
    put(".env", "/opt/augment00/dev/.env", use_sudo=True)
    put("config_local.py", "/opt/augment00/dev/deskcontrol/config_local.py", use_sudo=True)

