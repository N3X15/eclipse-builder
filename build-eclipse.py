'''
The point of this is just to cobble together all the properties we need from multiple sources,
including stuff like passwords.
'''

import os,sys, tempfile

script_dir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(script_dir,'buildtools'))

from buildtools import log, Config, Properties, replace_vars
from buildtools.wrapper import Ant

DefaultConfig={
    'ant': {
        'properties':{
            'files':['build.properties'],
            'keys': {},
            'secret-keys':[],
            'outfile': '/tmp/jenkins-%%JOB_NAME%%.properties'
        }
    }
}

config=Config('build-eclipse.yml',DefaultConfig)

outfile=config.get('outfile','/tmp/jenkins-%%JOB_NAME%%.properties')
with log.info('Building %s...',outfile):
    properties=Properties()
    properties.properties=config.get('ant.properties.keys',{})
    env = os.environ.copy()
    for filename in config.get('ant.properties.files',[]):
        properties.Load(filename,expand_vars=env)
    properties.Save(outfile)