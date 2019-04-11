import os

import git

branch = git.Repo().head.ref.name
deployhost = 'pi@192.168.1.68'
homedir = '/home/pi'
sitename = 'model-family'
virtualenv = os.path.join(homedir, 'virtualenvs', 'hackathon')
projectdir = os.path.join(homedir, sitename)
requirements = os.path.join('requirements.txt')
