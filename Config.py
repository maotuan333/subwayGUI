PROGRAM_FILES_FOLDER = 'C:/Users/damao/PycharmProjects/subway/subway config files'
ASSETS_FOLDER = 'C:/Users/damao/PycharmProjects/subway'
cur_work_folder = 'C:/Users/damao/PycharmProjects/subway' #TODO will be read from config.

debug=True
POS_INPUT = POS_TYPE = 0
POS_FUNC = POS_SUFFIX = 1
POS_OUTPUT = 2
POS_QC = 3
POS_README = 4
POS_SCRIPT = 5
POS_IS_MANUAL = 6

DEFAULT_NO_QC = 'NOQC'
DEFAULT_NO_README = 'NOREADME'
DEFAULT_NO_SCRIPT = 'NOSCRIPT'

if not debug:
    import matlab.engine
    MATLAB_ENGINE = matlab.engine.start_matlab()
