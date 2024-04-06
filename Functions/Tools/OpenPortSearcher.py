import socket
import threading


def findOpenPort(ip: str, from_: int, to_: int, inThreadCheck: int = 3) -> int | None:
    result = []
    currentPort = from_

    def _checkPort(checkPort):
        try:
            print(f"{checkPort},", end='')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((ip, checkPort))
            s.close()
            result.append(checkPort)
        except OSError:
            print('not right', checkPort)
            pass

    while not result and currentPort < to_:
        threads = []
        for currentPort in range(currentPort, currentPort + inThreadCheck + 1):
            if currentPort > to_:
                break

            threads.append(threading.Thread(target=_checkPort, args=(currentPort,)))
        for i in threads:
            i.start()
        for i in threads:
            i.join(0.2)

    return min(result) if result else None
