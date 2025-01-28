from netmiko import ConnectHandler
from time import sleep

class VlanIfConfigurator:
    def __init__(self, device, vlan_config, vrrp_config=None):
        self.device = device
        self.vlan_config = vlan_config
        self.vrrp_config = vrrp_config if vrrp_config else {}
        self.connection = None

    def connect(self):
        try:
            print(f"Подключаемся к {self.device['host']}...")
            self.connection = ConnectHandler(**self.device)
            self.connection.timeout = 90  
            self.connection.read_timeout = 300
            self.connection.send_command_timing("system-view")
            sleep(2)  
            print(f"Перешли в режим system-view на {self.device['host']}.")
        except Exception as e:
            print(f"Ошибка подключения к {self.device['host']}: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection:
            self.connection.disconnect()
            print(f"Отключено от {self.device['host']}.")

    def configure_vlanif(self):
        if not self.connection:
            print(f"Нет соединения с {self.device['host']}.")
            return

        try:
            for vlan_id, ip_mask in self.vlan_config.items():
                ip, mask = ip_mask.split()  # Разделяем IP и маску
                self.connection.send_command_timing(f"interface Vlanif{vlan_id}")
                sleep(1)
                self.connection.send_command_timing(f"ip address {ip} {mask}")
                print(f"[{self.device['host']}] Присвоен IP {ip} с маской {mask} на Vlanif{vlan_id}.")
                self.connection.send_command_timing("commit")
                self.connection.send_command_timing("quit")

            # Настройка VRRP
            self.configure_vrrp()

            self.connection.send_command_timing("commit")
            self.connection.send_command_timing("save")
            self.connection.send_command_timing("y")
            print(f"Конфигурация завершена на {self.device['host']}.")
        except Exception as e:
            print(f"Ошибка при настройке {self.device['host']}: {e}")

    def configure_vrrp(self):
        """Настроить VRRP на интерфейсах."""
        if not self.vrrp_config:
            print(f"Нет конфигурации VRRP для {self.device['host']}.")
            return

        for vlan_id, vrrp_settings in self.vrrp_config.items():
            for vrrp in vrrp_settings:
                self.connection.send_command_timing(f"interface Vlanif{vlan_id}")
                self.connection.send_command_timing(f"vrrp vrid {vrrp['vrid']} virtual-ip {vrrp['virtual_ip']}")
                if 'priority' in vrrp:
                    self.connection.send_command_timing(f"vrrp vrid {vrrp['vrid']} priority {vrrp['priority']}")
                print(f"[{self.device['host']}] Настроен VRRP для Vlanif{vlan_id}: vrid {vrrp['vrid']}, "
                      f"virtual-ip {vrrp['virtual_ip']}, priority {vrrp.get('priority', 'не указан')}.")
                self.connection.send_command_timing("commit")
                self.connection.send_command_timing("quit")


