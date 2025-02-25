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

    if not env.get('CM_TORRENT_DOWNLOADED_FILE_NAME'):
        return {'return': 1, 'error': 'CM_TORRENT_DOWNLOADED_FILE_NAME is not set'}

    return {'return': 0}


def postprocess(i):

    env = i['env']
    torrent_downloaded_path = os.path.join(
        env['CM_TORRENT_DOWNLOADED_DIR'],
        env['CM_TORRENT_DOWNLOADED_NAME'])
    env['CM_TORRENT_DOWNLOADED_PATH'] = torrent_downloaded_path

    if 'CM_TORRENT_DOWNLOADED_PATH_ENV_KEY' in env:
        key = env['CM_TORRENT_DOWNLOADED_PATH_ENV_KEY']
        env[key] = torrent_downloaded_path

    env['CM_GET_DEPENDENT_CACHED_PATH'] = torrent_downloaded_path

    return {'return': 0}
