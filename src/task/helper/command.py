import logging
import shlex

from subprocess import Popen, PIPE
from luigi.contrib.ssh import RemoteContext, RemoteCalledProcessError


logger = logging.getLogger('luigi-interface')


def local_command(command: str):
    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    ret = proc.wait()

    if out and ret == 0:
        return out.decode('utf8').split('\n')
    if err and ret != 0:
        raise Exception(f'Command failed: {err}')


def lc(command):
    logger.info(f"[!] Running the local command: {command}")
    return local_command(command)


def get_context(host: str, username: str, key_file: str):
    try:
        return RemoteContext(host=host, username=username, key_file=key_file, no_host_key_check=True)
    except RemoteCalledProcessError as e:
        pass
        # raise Exception(f'Command failed: {e.__str__()}')


def remote_command(context: RemoteContext, command: str):
    try:
        return context.check_output(shlex.split(command))
    except RemoteCalledProcessError as e:
        pass
        # raise Exception(f'Command failed: {e.__str__()}')


def rc(context: RemoteContext, command: str):
    logger.info(f"[!] Running the remote command: {command}")
    return remote_command(context, command)
