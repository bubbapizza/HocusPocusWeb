from __future__ import print_function
import sys
import os
import ConfigParser
from functools import wraps
from fabric.api import env
from fabric.utils import _AttributeDict
from fabric.operations import local, put, sudo, run
from fabric.context_managers import lcd, cd
from fabric.contrib.files import exists


####################################################
# Danger Zone!
#
# Fabric currently doesn't support python 3,
# therefore, make sure the code you write in this
# file can be ran in python 2.7+
####################################################


def _package():
    with lcd('./'):
        local(('{python_path} '
              'setup.py sdist').format(
                  python_path=env.config.local_python_path))

        dist_file_name = 'HocusPocusWeb-{version}.tar.gz'.format(
            version=env.config.project_version)

        dist_path = 'dist/{file_name}'.format(file_name=dist_file_name)
        put(dist_path, '/tmp/{file_name}'.format(file_name=dist_file_name))


def update_supervisor_config():
    with lcd('./'):
        config_file = 'hocuspocusweb-supervisor.conf'

        put(config_file, '/tmp/{file_name}'.format(file_name=config_file))
        command = ('mv '
                   '/tmp/{config_file} '
                   '/etc/supervisor/conf.d/{config_file}')
        sudo(command.format(config_file=config_file))


def _parse_config_file(config_path):
    config = None
    env.update({'config': _AttributeDict()})

    if os.path.exists(config_path):
        with open(config_path) as f:
            config = ConfigParser.ConfigParser()
            config.readfp(f)
    else:
        print('ERROR: {} doesn\'t exist on the file system!')
        sys.exit(1)

    return config


def _merge_config_with_env(config):
    section = 'fabric'

    env.config.local_python_path = config.get(section, 'local_python_path')
    env.config.project_version = config.get(section, 'project_version')
    env.config.host_env_path = config.get(section, 'host_env_path')


def with_config(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config_path = args[0]
        config = _parse_config_file(config_path)
        _merge_config_with_env(config)
        return f(*args[1:], **kwargs)

    return wrapper


@with_config
def deploy():
    _package()

    if not exists('HocusPocus/'):
        run('mkdir HocusPocus')

    with cd('HocusPocus'):
        run('tar -zxvpf /tmp/HocusPocusWeb-{version}.tar.gz'.format(
            version=env.config.project_version))

        with cd('HocusPocusWeb-{version}'.format(
                version=env.config.project_version)):

            python_path = os.path.join(env.config.host_env_path,
                                       'bin/python')
            run('{python_path} setup.py install'.format(
                python_path=python_path))

            db_script_path = os.path.join(env.config.host_env_path,
                                          'bin/initialize_HocusPocusweb_db')
            run('{db_script_path} production.ini'.format(
                db_script_path=db_script_path))

    update_supervisor_config()
