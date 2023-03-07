import pathlib
import sys
from os.path import abspath,dirname
import logging

PROJECT_PATH = pathlib.Path(dirname(abspath(sys.argv[0])))
PROGRAM_FILES_FOLDER = PROJECT_PATH / 'data'
ASSETS_FOLDER = PROJECT_PATH / 'static'
CUR_WORK_FOLDER = pathlib.Path('//umms-crburge.turbo.storage.umich.edu/umms-crburge')
RUN_HISTORY = PROGRAM_FILES_FOLDER / 'tmp_last_run.json'

debug = True

logging.basicConfig(filename='subwaygui.log', level=logging.NOTSET)
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger("app")
logger.info("subway gui started...")

if not debug:
    import matlab.engine

    MATLAB_ENGINE = matlab.engine.start_matlab()
    # TODO more specific start, maybe in pre-parsing of schema

# 4. the goal is to call a function with parameters:
#   1. for .m, try read the first non-empty line as function definition
#   2. display to user, let them confirm
#   3. if this is entirely not what they want (the main function is further back, etc.)
#       show the entire script and let them select
#   4. if it's
