import os
from contextlib import suppress
from dotenv import load_dotenv
from dotenv import dotenv_values
load_dotenv()
config = dotenv_values()
start_type = config['START_TYPE']
if start_type == 'DEBUG':
    for var in config.keys():
        if config.get(var + '_DEBUG',None) is not None:
            with suppress(TypeError):
                os.environ[var] = config.get(var + '_DEBUG')
        else:
            os.environ[var] = config.get(var)