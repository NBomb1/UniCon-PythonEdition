import os
import msvcrt
from typing import IO


class MultipleStartRestriction:
    def __init__(self):
        self.lock_file_path = "program.lock"
        self.file: IO

    def checkIsLocked(self) -> bool:
        try:
            # Попытка открыть файл для блокировки
            with open(self.lock_file_path, 'w') as lock_file:
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                return True
        except IOError:
            # Если файл уже заблокирован другим процессом
            return False

    def lock_file(self):
        try:
            # Создание файла для блокировки
            self.file = open(self.lock_file_path, 'w')
            msvcrt.locking(self.file.fileno(), msvcrt.LK_LOCK, 1)
        except IOError as e:
            raise IOError(f"Ошибка при блокировке файла: {e}")

    def unlock_file(self):
        try:
            # Разблокировка файла
            msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, 1)
            self.file.close()
            # Удаление файла
            os.remove(self.lock_file_path)
        except IOError as e:
            raise IOError(f"Ошибка при разблокировке файла: {e}")
