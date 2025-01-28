from data.devices import HUAWEI_SWITCHES, ROUTERS  
from data.ospf_data import OSPF_CONFIG  
from core.ospf_config import OSPFConfigurator  


def main():
    ordered_devices = [
        ROUTERS[0],          # 10.60.7.2
        HUAWEI_SWITCHES[2],  # 192.168.0.123
        HUAWEI_SWITCHES[0],  # 192.168.0.120          
    ]

    for device in ordered_devices:  
        ospf_commands = OSPF_CONFIG.get(device["host"], [])
        if ospf_commands:
            ospf_configurator = OSPFConfigurator(device, ospf_commands)
            ospf_configurator.connect()   
            ospf_configurator.send_commands()  
            ospf_configurator.delete_static_routes()  
            ospf_configurator.disconnect()  
        else:
            print(f"Нет конфигурации OSPF для {device['host']}.")

if __name__ == "__main__":
    main()

