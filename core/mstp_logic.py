from netmiko import ConnectHandler
from time import sleep


class STPConfigurator:
    def __init__(self, device, commands):
        self.device = device
        self.commands = commands
        self.connection = None

    def connect(self):
        """Подключение к устройству."""
        try:
            self.connection = ConnectHandler(**self.device)
            self.connection.timeout = 60  
            self.connection.read_timeout = 60
            self.connection.send_command_timing("system-view")
            sleep(1)  
            print(f"Перешли в режим system-view на {self.device['host']}")
        except Exception as e:
            print(f"Ошибка подключения к {self.device['host']}: {e}")
            self.connection = None

    def configure_stp(self):
        """Выполняем команды конфигурации STP."""
        if not self.connection:
            print(f"Соединение с {self.device['host']} не установлено. Пропуск.")
            return

        try:
            for command in self.commands:
                print(f"Отправка команды: {command}")
                if "stp enable" in command:  
                    output = self.connection.send_command_timing(command)
                    if "Y/N" in output:
                        output += self.connection.send_command_timing("Y")
                        print(f"STP enable подтверждено на {self.device['host']}")
                    sleep(10)  
                else:
                    output = self.connection.send_command_timing(command)
                    print(f"Команда выполнена: {command}")
        except Exception as e:
            print(f"Ошибка выполнения команды на {self.device['host']}: {e}")

    def disable_interface(self, interface):
        """Отключение указанного интерфейса."""
        if not self.connection:
            print(f"Соединение с {self.device['host']} не установлено. Пропуск.")
            return

        try:
            print(f"Включаем интерфейс {interface} на {self.device['host']}")
            self.connection.send_command_timing(f"interface {interface}")
            self.connection.send_command_timing("undo shutdown")
            print(f"Интерфейс {interface} включен на {self.device['host']}")
        except Exception as e:
            print(f"Ошибка при отключении интерфейса {interface} на {self.device['host']}: {e}")

    def commit_changes(self):
        """Применяем изменения."""
        if not self.connection:
            print(f"Соединение с {self.device['host']} не установлено. Пропуск.")
            return

        try:
            self.connection.send_command_timing("commit")
            print(f"Изменения применены на {self.device['host']}")
        except Exception as e:
            print(f"Ошибка при применении изменений на {self.device['host']}: {e}")

    def disconnect(self):
        """Закрываем соединение."""
        if self.connection:
            self.connection.disconnect()
            print(f"Соединение с {self.device['host']} закрыто.")


