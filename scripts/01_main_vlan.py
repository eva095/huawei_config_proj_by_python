from data.devices import HUAWEI_SWITCHES
from data.vlan_data import VLAN_DATA
from data.interface_tasks import INTERFACE_DATA
from core.vlan_logic import HuaweiSwitch



def main():
    for device in HUAWEI_SWITCHES:
        ip = device["host"]

        # Проверяем, есть ли задачи для устройства
        vlans = VLAN_DATA.get(ip, [])
        interfaces = INTERFACE_DATA.get(ip, [])

        if not vlans and not interfaces:
            print(f"Нет задач для устройства {ip}, пропускаем.")
            continue

        # Работаем с устройством
        switch = HuaweiSwitch(device)
        switch.connect()
        if switch.connection:
            if vlans:
                switch.configure_vlans(vlans)
            if interfaces:
                switch.configure_interfaces(interfaces)
            switch.disconnect()


if __name__ == "__main__":
    main()

