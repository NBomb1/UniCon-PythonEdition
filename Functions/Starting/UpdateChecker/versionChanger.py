import os
import shutil
import sys

copyFrom = sys.argv[1]
copyTo = sys.argv[2]
print(sys.argv)


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

    # Опционально: удалить исходную директорию, если она пустая
    if not os.listdir(src_dir):
        os.rmdir(src_dir)


move_all_contents(copyFrom, copyTo)
os.execl(sys.executable, sys.executable, copyTo + '\\main.py', '--updated')

input()
