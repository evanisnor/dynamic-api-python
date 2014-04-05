import os, importlib

ENVIRONMENT_VARIABLE = 'DYNAPIENV'

env = os.environ.get(ENVIRONMENT_VARIABLE)
if env:
    try:
        settings_module = importlib.import_module('settings.' + env)
        for n in dir(settings_module):
            globals()[n] = getattr(settings_module, n)
        print('Using settings.{} for settings'.format(env))
    except ImportError as e:
        print('Unable to import settings.{}\r\n{}'.format(env, e))
        quit()
else:
    from settings.base import *
    print('Envonment Variable "{}" is not set. Using settings.base for settings.'.format(ENVIRONMENT_VARIABLE))