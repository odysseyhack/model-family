import os
import sys

import git
from importlib import import_module
from fabric.api import env, run

env.forward_agent = True
env.always_use_pty = False
env.linewise = True
env.shell = '/bin/dash -e -c'
env.use_ssh_config = True


def setup(server, branch):
    env.server = server
    sys.path.append(os.getcwd())
    deployment_module = 'deployment.{0}'.format(env.server)
    deployment_config = import_module(deployment_module)
    env.branch = branch or deployment_config.branch
    env.host_string = deployment_config.deployhost
    env.sitename = deployment_config.sitename
    env.projectdir = deployment_config.projectdir
    env.source = git.Repo().remote().url
    env.virtualenv = deployment_config.virtualenv
    env.requirements = deployment_config.requirements


def deploy(server='pi1', branch=None):
    setup(server, branch)
    print('deploying %(branch)s to %(sitename)s' % env)

    # git
    run("""
        if [ -d %(projectdir)s ]
        then
            cd %(projectdir)s
            git fetch
            git checkout %(branch)s
            git pull
        else
            git clone --branch=%(branch)s \
                    %(source)s %(projectdir)s
            cd %(projectdir)s
        fi
        """ % env)

    # virtualenv and requirements
    run("""
        if [ ! -d %(virtualenv)s ]
        then
            virtualenv --python=/usr/bin/python3 %(virtualenv)s
        fi
        cd %(projectdir)s
        . %(virtualenv)s/bin/activate
        pip install -r %(requirements)s
        """ % env)


    # log dir
    run("""
        cd %(projectdir)s
        if [ ! -d logs ]
        then
            mkdir logs
            chmod 0777 logs
        fi
        """ % env)

    # django setup
    run("""
        cd %(projectdir)s
        . %(virtualenv)s/bin/activate
        python manage.py collectstatic --noinput
        python manage.py migrate
        """ % env)

    # django restart
    run("""
        touch %(projectdir)s/generic/wsgi.py
        """ % env)
