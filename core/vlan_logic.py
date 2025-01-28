from netmiko import ConnectHandler
from time import sleep


class HuaweiSwitch:
    def __init__(self, device):
        self.device = device
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

    def disconnect(self):
        if self.connection:
            self.connection.disconnect()

    def configure_vlans(self, vlans):
        try:
            commands = [f"vlan batch {' '.join(map(str, vlans))}"]
            self.connection.send_command_timing(commands[0])  
            sleep(1)  
            for vlan in vlans:
                self.connection.send_command_timing(f"vlan {vlan}")  
                sleep(1)
                self.connection.send_command_timing(f"name VLAN_{vlan}") 
                sleep(1)

            
            self.connection.send_command_timing("commit")
            sleep(1)
            print(f"VLAN {vlans} настроены и зафиксированы на {self.device['host']}")
        except Exception as e:
            print(f"Ошибка настройки VLAN-ов на {self.device['host']}: {e}")

    def configure_interfaces(self, interfaces):
        """Настройка интерфейсов."""
        try:
            for interface in interfaces:
                commands = [f"interface {interface['name']}", f"port link-type {interface['mode']}"]
                if interface["mode"] == "trunk":
                    commands.append(f"port trunk allow-pass vlan {interface['vlans']}")
                elif interface["mode"] == "access":
                    commands.append(f"port default vlan {interface['vlans']}")
                
                
                for command in commands:
                    self.connection.send_command_timing(command)
                    sleep(1)  
            
            
            self.connection.send_command_timing("commit")
            sleep(1)
            print(f"Интерфейсы настроены на {self.device['host']}")
        except Exception as e:
            print(f"Ошибка настройки интерфейсов на {self.device['host']}: {e}")

