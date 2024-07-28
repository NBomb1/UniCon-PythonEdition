import os
import subprocess
from sys import executable


def run_independent_process(script_path, *args):
    list_ = [executable, script_path]
    list_.extend(args)
    # print(f'Command to run: {list_}')

    if os.name == 'nt':  # Windows
        DETACHED_PROCESS = 0x00000008
        process = subprocess.Popen(
            list_,
            creationflags=DETACHED_PROCESS,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True
        )
    else:  # Unix-системы
        process = subprocess.Popen(
            list_,
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True
        )