import os

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Network.FileTransfer.Files.Receiving import ReceivingFileInfo


class ReceivingContainer(list[ReceivingFileInfo]):
    def __init__(self, files: dict[str, int], selfAccount: SelfAccount, sender: Account):
        """
        Класс для управления информацией о принимаемых файлах.
        """
        super().__init__()
        self.files = files
        self.receiver = selfAccount
        self.sender = sender
        self.resolved_paths = set()  # Для отслеживания уникальных путей

        received_dir = os.path.join(os.getcwd(), "Received files")

        # Создаем папку для хранения файлов, если её нет
        os.makedirs(received_dir, exist_ok=True)

        # Поиск конфликтных файлов и их обработка
        for path, size in files.items():
            resolved_path = self.resolve_conflict(received_dir, path)
            self.append(
                ReceivingFileInfo.ReceiveFileInfo(
                    resolved_path,
                    open(resolved_path, 'wb'),
                    size
                )
            )

    def resolve_conflict(self, base_dir: str, file_name: str) -> str:
        """
        Разрешает конфликты имен файлов, добавляя номер к имени файла.
        """
        # Создаем полный путь к файлу
        file_path = os.path.join(base_dir, file_name)
        name, ext = os.path.splitext(file_name)
        counter = 1

        # Проверяем наличие конфликтов
        while file_path in self.resolved_paths or os.path.exists(file_path):
            # Если конфликт найден, добавляем счетчик к имени файла
            file_path = os.path.join(base_dir, f"{name.rstrip(' ')} ({counter}){ext}")
            counter += 1

        # Добавляем путь в список уже обработанных
        self.resolved_paths.add(file_path)
        return file_path

    def closeAll(self):
        """
        Закрывает все открытые файлы.
        """
        for i in self:
            i.file.close()

    def sending_information_format(self) -> dict:
        text = {}
        for i in self:
            text[i.fullPath.split('\\')[-1]] = i.fullSize
        return text

    def calculate_bytes_sent(self) -> int:
        return sum(tuple(map(lambda x: x.receivedSize, self)))

    def calculate_bytes(self) -> int:
        return sum(self.files.values())
