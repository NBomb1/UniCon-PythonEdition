import os
import shutil
import sys
from time import sleep

logs = ''


def log_message(*args):
    global logs
    message = ' '.join(map(str, args))
    logs += message + '\n'
    print(message)


try:
    copyFrom = sys.argv[1]
    copyTo = sys.argv[2]
    os.chdir(copyTo)
    pid = int(sys.argv[3])

    log_message('Attempting to terminate parent process with PID:', pid)
    try:
        os.kill(pid, 0)
        sleep(1)  # Даем время процессу завершиться
        os.kill(pid, 9)  # Принудительное завершение
        log_message(f'Parent process {pid} terminated successfully.')
    except Exception as e:
        log_message(f'Error terminating parent process: {e}')

    log_message('Received arguments:', sys.argv)
    DeleteExtensions = ('.py', '.gif')


    def move_all_contents(src_dir, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dest_dir, item)
            if os.path.isdir(s):
                shutil.move(s, copyTo)
            else:
                shutil.move(s, copyTo)
            log_message('Moving:', s, 'to:', copyTo)

        if not os.listdir(src_dir):
            os.rmdir(src_dir)
            log_message(f'Directory {src_dir} has been deleted.')


    def delete_old_files(directory):
        log_message('Checking for files to delete in:', directory)
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path) and file_path.endswith(DeleteExtensions):
                    # if __file__.split('\\')[-1] == file:
                    #     continue
                    os.remove(file_path)
                    log_message(f'FILE {file_path} has been deleted.')
                elif os.path.isdir(file_path) and file != copyFrom.split('\\')[-1]:
                    shutil.rmtree(file_path)
                    log_message(f'PATH {file_path} has been deleted.')
            except Exception as e:
                log_message(f'Error occurred while deleting {file_path}: {e}')


    log_message('Waiting 8 seconds...')
    sleep(3)
    log_message('Deleting old files...')
    delete_old_files(copyTo)
    sleep(3)
    log_message('Old files have been deleted.')
    log_message('Moving all files...')
    move_all_contents(copyFrom, copyTo)
    log_message('Files moved successfully.')
    log_message('Restarting application...')
    os.execl(sys.executable, sys.executable, '"' + os.path.join(copyTo, 'main.py') + '"', '--updated')

finally:
    import tkinter as tk
    import traceback

    log_message('Error occurred while moving files.')
    error_message = traceback.format_exc()
    log_message('Traceback:', error_message)

    root = tk.Tk()
    text = tk.Text(root)
    text.insert(tk.END, f'Error occurred while moving files.\n\n{error_message}\n\nLOGS:\n{logs}')
    text.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
