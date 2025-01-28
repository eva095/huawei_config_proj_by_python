from netmiko import ConnectHandler
from time import sleep

class OSPFConfigurator:
    def __init__(self, device, commands, static_routes=None):
        self.device = device  # Переименовали host в device
        self.commands = commands
        self.static_routes = static_routes if static_routes else []
        self.connection = None

    def connect(self):
        """Подключение к устройству."""
        try:
            # Подключение через netmiko с использованием self.device
            self.connection = ConnectHandler(**self.device)
            self.connection.timeout = 60  # Увеличенный тайм-аут
            self.connection.read_timeout = 60
            self.connection.send_command_timing("system-view")
            sleep(1)
            print(f"Перешли в режим system-view на {self.device['host']}")
        except Exception as e:
            print(f"Ошибка подключения к {self.device['host']}: {e}")
            self.connection = None

    def send_commands(self):
        """Отправка команд OSPF на устройство."""
        if self.connection:
            for command in self.commands:
                print(f"Отправляем команду: {command}")
                self.connection.send_command_timing(command)
                sleep(1)  # Ожидание между командами

            # Добавим команду commit
            print(f"Подтверждаем изменения на устройстве {self.device['host']}")
            self.connection.send_command_timing("commit")
            sleep(1)  # Ожидание завершения команды commit
            print(f"Изменения подтверждены на {self.device['host']}")

    def delete_static_routes(self):
        """Применение статических маршрутов, если они есть."""
        if self.static_routes:
            for route in self.static_routes:
                print(f"Отправляем статический маршрут: {route}")
                self.connection.send_command_timing(route)
                sleep(1)  # Ожидание между командами
            print(f"Статические маршруты применены на {self.device['host']}")

    def disconnect(self):
        """Отключение от устройства."""
        if self.connection:
            self.connection.disconnect()
            print(f"Отключились от устройства {self.device['host']}")


    