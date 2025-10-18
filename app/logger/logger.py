from config.config import LOGS_PATH

class Logger:
    #TODO Стоит реализовать некоторое уникальное имя лога, чтобы его отличать
    def __init__(self, filename: str = 'log.txt'):
        self.log_file = LOGS_PATH / filename
        LOGS_PATH.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.touch()

    #TODO добавить необязательный параметр для логгера (для определения потока вывода сообщений)
    def write(self, data: str):
        with self.log_file.open('a', encoding='utf-8') as f:
            f.write(data + '\n')