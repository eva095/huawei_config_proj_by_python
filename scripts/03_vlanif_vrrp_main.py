from data.devices import HUAWEI_SWITCHES
from data.vlanif_data import VLAN_CONFIG, VRRP_CONFIG  # добавляем VRRP_CONFIG
from core.vlanif_and_vrrp_logic import VlanIfConfigurator


def main():
    for device in HUAWEI_SWITCHES:
        vlan_config = VLAN_CONFIG.get(device["host"], {})
        vrrp_config = VRRP_CONFIG.get(device["host"], {})  # извлекаем настройки VRRP для устройства
        if vlan_config:
            configurator = VlanIfConfigurator(device, vlan_config, vrrp_config)
            configurator.connect()
            configurator.configure_vlanif()
            configurator.disconnect()
        else:
            print(f"Нет конфигурации VLAN для {device['host']}.")


if __name__ == "__main__":
    main()

