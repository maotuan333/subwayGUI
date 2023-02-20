import pathlib

PROJECT_PATH = pathlib.Path('C:/Users/damao/PycharmProjects/subway')
CONFIG_FOLDER = PROJECT_PATH / 'config'
PROGRAM_FILES_FOLDER = PROJECT_PATH / 'data'
ASSETS_FOLDER = PROJECT_PATH / 'static'
CUR_WORK_FOLDER = pathlib.Path('//umms-crburge.turbo.storage.umich.edu/umms-crburge')
# CUR_WORK_FOLDER = pathlib.Path('C:/Users/damao/PycharmProjects/subway') #TODO will be read from config.
RUN_HISTORY = PROGRAM_FILES_FOLDER / 'tmp_last_run.json'

debug = True

if not debug:
    import matlab.engine

    MATLAB_ENGINE = matlab.engine.start_matlab()
    # TODO more specific start, maybe in pre-parsing of schema

# 2. try read in json
# 3. try a subway run on t07 using Lex's flowchart
# 4. the goal is to call a function with parameters: haven't decided exactly how yet
