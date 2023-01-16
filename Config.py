
import pathlib

PROGRAM_FILES_FOLDER = pathlib.Path('C:/Users/damao/PycharmProjects/subway/subway config files')
ASSETS_FOLDER = pathlib.Path('C:/Users/damao/PycharmProjects/subway/static_assets')
CUR_WORK_FOLDER = pathlib.Path('//umms-crburge.turbo.storage.umich.edu/umms-crburge')
#CUR_WORK_FOLDER = pathlib.Path('C:/Users/damao/PycharmProjects/subway') #TODO will be read from config.
RUN_HISTORY=PROGRAM_FILES_FOLDER/'tmp_last_run.json'

debug=True

if not debug:
    import matlab.engine
    MATLAB_ENGINE = matlab.engine.start_matlab()
    #TODO more specific start, maybe in pre-parsing of schema

GLOBAL_QC_HANDLE=None

POS_INPUT=0
POS_FUNC=1
POS_OUTPUT=2
POS_QC=3
POS_README=4