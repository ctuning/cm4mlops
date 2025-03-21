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
import shutil


def preprocess(i):

    os_info = i['os_info']

#    if os_info['platform'] == 'windows':
# return {'return':1, 'error': 'Windows is not supported in this script
# yet'}

    env = i['env']
    meta = i['meta']

    script_path = i['run_script_input']['path']

    if env.get('CM_GIT_CHECKOUT', '') == '' and env.get(
            'CM_GIT_URL', '') == '' and env.get('CM_VERSION', '') == '':
        # if custom checkout and url parameters are not set and CM_VERSION is
        # not specified
        env['CM_VERSION'] = "master"
        env["CM_GIT_CHECKOUT"] = "master"
        env["CM_GIT_URL"] = "https://github.com/mlcommons/inference"
    elif env.get('CM_GIT_CHECKOUT', '') != '' and env.get('CM_TMP_GIT_CHECKOUT', '') != '' and env.get('CM_GIT_CHECKOUT', '') != env.get('CM_TMP_GIT_CHECKOUT', ''):
        # if checkout branch is assigned inside version and custom branch is
        # also specified
        return {
            "return": 1, "error": "Conflicting branches between version assigned and user specified."}
    elif env.get('CM_GIT_URL', '') != '' and env.get('CM_TMP_GIT_URL', '') != '' and env.get('CM_GIT_URL', '') != env.get('CM_TMP_GIT_URL', ''):
        # if GIT URL is assigned inside version and custom branch is also
        # specified
        return {
            "return": 1, "error": "Conflicting URL's between version assigned and user specified."}

    if env.get('CM_VERSION', '') == '':
        env['CM_VERSION'] = "custom"

    # check whether branch and url is specified,
    # if not try to assign the values specified in version parameters,
    # if version parameters does not have the value to a parameter, set the
    # default one
    if env.get('CM_GIT_CHECKOUT', '') == '':
        if env.get('CM_TMP_GIT_CHECKOUT', '') != '':
            env["CM_GIT_CHECKOUT"] = env["CM_TMP_GIT_CHECKOUT"]
        else:
            env["CM_GIT_CHECKOUT"] = "master"

    if env.get('CM_GIT_URL', '') == '':
        if env.get('CM_TMP_GIT_URL', '') != '':
            env["CM_GIT_URL"] = env["CM_TMP_GIT_URL"]
        else:
            env["CM_GIT_URL"] = "https://github.com/mlcommons/inference"

    if env.get("CM_MLPERF_LAST_RELEASE", '') == '':
        env["CM_MLPERF_LAST_RELEASE"] = "v4.1"

    if 'CM_GIT_DEPTH' not in env:
        env['CM_GIT_DEPTH'] = ''

    if 'CM_GIT_RECURSE_SUBMODULES' not in env:
        env['CM_GIT_RECURSE_SUBMODULES'] = ''
    submodules = []
    possible_submodules = {
        "gn": "third_party/gn",
        "pybind": "third_party/pybind",
        "deeplearningexamples": "language/bert/DeepLearningExamples",
        "3d-unet": "vision/medical_imaging/3d-unet-brats19/nnUnet"
    }
    for submodule in possible_submodules:
        env_name = submodule.upper().replace("-", "_")
        if env.get("CM_SUBMODULE_" + env_name) == "yes":
            submodules.append(possible_submodules[submodule])

    env['CM_GIT_SUBMODULES'] = ",".join(submodules)

    if env.get('CM_GIT_PATCH_FILENAME', '') != '':
        patch_file_name = env['CM_GIT_PATCH_FILENAME']
        env['CM_GIT_PATCH_FILEPATHS'] = os.path.join(
            script_path, 'patch', patch_file_name)

    need_version = env.get('CM_VERSION', '')
    versions = meta['versions']

    if need_version != '' and not need_version in versions:
        env['CM_GIT_CHECKOUT'] = need_version

    return {'return': 0}


def postprocess(i):

    env = i['env']
    state = i['state']

    inference_root = env['CM_MLPERF_INFERENCE_SOURCE']
    env['CM_MLPERF_INFERENCE_VISION_PATH'] = os.path.join(
        inference_root, 'vision')
    env['CM_MLPERF_INFERENCE_CLASSIFICATION_AND_DETECTION_PATH'] = os.path.join(
        inference_root, 'vision', 'classification_and_detection')
    env['CM_MLPERF_INFERENCE_BERT_PATH'] = os.path.join(
        inference_root, 'language', 'bert')
    env['CM_MLPERF_INFERENCE_GPTJ_PATH'] = os.path.join(
        inference_root, 'language', 'gpt-j')
    env['CM_MLPERF_INFERENCE_RNNT_PATH'] = os.path.join(
        inference_root, 'speech_recognition', 'rnnt')
    env['CM_MLPERF_INFERENCE_DLRM_PATH'] = os.path.join(
        inference_root, 'recommendation', 'dlrm')
    env['CM_MLPERF_INFERENCE_DLRM_V2_PATH'] = os.path.join(
        inference_root, 'recommendation', 'dlrm_v2')
    env['CM_MLPERF_INFERENCE_3DUNET_PATH'] = os.path.join(
        inference_root, 'vision', 'medical_imaging', '3d-unet-kits19')

    env['CM_GET_DEPENDENT_CACHED_PATH'] = inference_root

#        20221024: we save and restore env in the main script and can clean env here for determinism
#    if '+PYTHONPATH' not in env: env['+PYTHONPATH'] = []
    env['+PYTHONPATH'] = []
    env['+PYTHONPATH'].append(
        os.path.join(
            env['CM_MLPERF_INFERENCE_CLASSIFICATION_AND_DETECTION_PATH'],
            'python'))

    if os.path.exists(os.path.join(inference_root, "loadgen", "VERSION.txt")):
        with open(os.path.join(inference_root, "loadgen", "VERSION.txt")) as f:
            version_info = f.read().strip()
        env['CM_MLPERF_INFERENCE_SOURCE_VERSION'] = version_info

    if env.get('CM_GET_MLPERF_IMPLEMENTATION_ONLY', '') == "yes":
        return {'return': 0}

    env['CM_MLPERF_INFERENCE_CONF_PATH'] = os.path.join(
        inference_root, 'mlperf.conf')
    env['+PYTHONPATH'].append(
        os.path.join(
            env['CM_MLPERF_INFERENCE_SOURCE'],
            'tools',
            'submission'))

    valid_models = get_valid_models(
        env['CM_MLPERF_LAST_RELEASE'],
        env['CM_MLPERF_INFERENCE_SOURCE'])

    state['CM_MLPERF_INFERENCE_MODELS'] = valid_models

    if env.get('CM_GIT_REPO_CURRENT_HASH', '') != '':
        env['CM_VERSION'] += "-git-" + env['CM_GIT_REPO_CURRENT_HASH']

    return {'return': 0, 'version': env['CM_VERSION']}


def get_valid_models(mlperf_version, mlperf_path):

    import sys

    submission_checker_dir = os.path.join(mlperf_path, "tools", "submission")

    sys.path.append(submission_checker_dir)

    if not os.path.exists(os.path.join(
            submission_checker_dir, "submission_checker.py")):
        shutil.copy(os.path.join(submission_checker_dir, "submission-checker.py"), os.path.join(submission_checker_dir,
                                                                                                "submission_checker.py"))

    import submission_checker as checker

    config = checker.MODEL_CONFIG

    valid_models = config[mlperf_version]["models"]

    return valid_models
