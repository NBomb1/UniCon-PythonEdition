import os
import shutil
import sys
from time import sleep

copyFrom = sys.argv[1]
copyTo = sys.argv[2]
print(sys.argv)
DeleteExtensions = ('py', 'gif')


def move_all_contents(src_dir, dest_dir):
    # Проверяем, существует ли директория назначения, если нет, создаём её
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Проходим по всем элементам в исходной директории
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        # Если элемент - директория, используем shutil.move для перемещения
        if os.path.isdir(s):
            shutil.move(s, d)
        else:
            # Если элемент - файл, используем shutil.move для перемещения
            shutil.move(s, d)
        print('\nmoving:', s, 'to:', d)

    # Опционально: удалить исходную директорию, если она пустая
    if not os.listdir(src_dir):
        os.rmdir(src_dir)
        print(f'Directory {src_dir} has been deleted.')


def deleteOldFiles(directory):
    print(__file__.split('\\')[-1])
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            # if os.path.isfile(file_path):
            print(file_path, copyFrom)
            if os.path.isfile(file_path) and file_path.endswith(DeleteExtensions):
                if __file__.split('\\')[-1] == file:
                    return
                os.remove(file_path)
                print(f'FILE {file_path} has been deleted.')
            elif file != copyFrom.split('\\')[-1] and os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f'PATH {file_path} has been deleted.')
        except Exception as e:
            print(f'Error occurred while deleting {file_path}: {e}')


print(copyFrom, copyTo)
sleep(2)
deleteOldFiles(copyTo)
print('Old files have been deleted.')
print('Moving all files...')
# move_all_contents(copyFrom, copyTo)
print(sys.executable, copyFrom, copyTo, copyTo + '\\main.py', '--updated')
print('not Starting...')
# os.execl(sys.executable, sys.executable, copyTo + '\\main.py', '--updated')

input()
