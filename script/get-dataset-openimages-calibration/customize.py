#
# Copyright: https://github.com/mlcommons/ck/blob/master/cm-mlops/COPYRIGHT.md
# License: https://github.com/mlcommons/ck/blob/master/cm-mlops/LICENSE.md
#
# White paper: https://arxiv.org/abs/2406.16791
# History: https://github.com/mlcommons/ck/blob/master/HISTORY.CM.md
# Original repository: https://github.com/mlcommons/ck/tree/master/cm-mlops
#
# CK and CM project contributors: https://github.com/mlcommons/ck/blob/master/CONTRIBUTING.md
#

from cmind import utils
import os


def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    meta = i['meta']

    automation = i['automation']

    quiet = (env.get('CM_QUIET', False) == 'yes')

    if env.get("CM_CALIBRATE_FILTER", "") == "yes":
        i['run_script_input']['script_name'] = "run-filter"
        env['CM_MLPERF_OPENIMAGES_CALIBRATION_FILTERED_LIST'] = os.path.join(
            os.getcwd(), "filtered.txt")
        env['CM_MLPERF_OPENIMAGES_CALIBRATION_LIST_FILE_WITH_PATH'] = env['CM_MLPERF_OPENIMAGES_CALIBRATION_FILTERED_LIST']

    return {'return': 0}


def postprocess(i):

    env = i['env']

    return {'return': 0}
