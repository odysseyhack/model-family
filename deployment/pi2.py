import os

import git

branch = git.Repo().head.ref.name
deployhost = 'pi2'
homedir = '/home/pi'
sitename = 'model-family'
virtualenv = os.path.join(homedir, 'virtualenvs', 'hackathon')
projectdir = os.path.join(homedir, sitename)
requirements = os.path.join('requirements.txt')
