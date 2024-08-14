logs = ''
from threading import Thread
import tkinter as tk

root = tk.Tk()
text = tk.Text(wrap=tk.WORD)


def log_message(*args):
    global logs
    message = ' '.join(map(str, args))
    text.insert(tk.END, message + '\n')
    logs += message + '\n'
    text.update()
    print(message)


def process(root: tk.Tk):
    try:
        import os
        import shutil
        import subprocess
        import sys

        copyFrom = sys.argv[1]
        copyTo = sys.argv[2]
        os.chdir(copyTo)

        log_message('Received arguments:', sys.argv)
        DeleteExtensions = ('.py', '.gif')

        def move_all_contents(src_dir, dest_dir):
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            for item in os.listdir(src_dir):
                s = os.path.join(src_dir, item)
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
                        os.remove(file_path)
                        log_message(f'FILE {file_path} has been deleted.')
                    elif os.path.isdir(file_path) and file != copyFrom.split('\\')[-1]:
                        shutil.rmtree(file_path)
                        log_message(f'PATH {file_path} has been deleted.')
                except Exception as e:
                    log_message(f'Error occurred while deleting {file_path}: {e}')

        log_message('Deleting old files...')
        delete_old_files(copyTo)
        log_message('Old files have been deleted.')
        log_message('Moving all files...')
        move_all_contents(copyFrom, copyTo)
        log_message('Files moved successfully.')
        log_message('Restarting application...')
        a = (sys.executable, os.path.join(copyTo, 'main.py'), '--updated', '--startAsAdmin')
        log_message(f"{a}")
        subprocess.Popen(
            a,
            creationflags=0x00000008,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            close_fds=True,
            cwd=copyTo
        )
        root.destroy()
        # root.after(5000, root.destroy)

    except:
        import traceback

        log_message('Error occurred while moving files.')
        error_message = traceback.format_exc()
        log_message('Traceback:', error_message)

        root = tk.Tk()
        text = tk.Text(root)
        text.insert(tk.END, f'Error occurred while moving files.\n\n{error_message}\n\nLOGS:\n{logs}')
        text.pack(fill=tk.BOTH, expand=True)
        root.mainloop()


Thread(target=process, args=(root,)).start()

text.pack(fill=tk.BOTH, expand=True)
root.mainloop()
