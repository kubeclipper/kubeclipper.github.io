import os
import subprocess


def run_process(cmd, env=None):
    cmd_str = cmd
    if isinstance(cmd_str, list):
        cmd_str = ' '.join(cmd_str)
        env_str = ''
        if env is not None: 
            for k in env:
                env_str = '%s %s=%s' % (env_str, k, env[k])
        cmd_str = env_str + ' ' + cmd_str
    print("Execute cmd: %s" % (cmd_str, ))
    if isinstance(cmd, str):
        cmd = cmd.split()
    cur_env = os.environ
    if env:
        for k in env:
            cur_env[k] = env[k]
    return bytes.decode(subprocess.check_output(cmd, env=cur_env))
