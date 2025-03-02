from data.devices import HUAWEI_SWITCHES
from data.stp_data import STP_CONFIGS
from core.mstp_logic import STPConfigurator

INTERFACE_TO_DISABLE = "GE 1/0/2"  

for device in HUAWEI_SWITCHES:
    host = device["host"]
    stp_commands = STP_CONFIGS.get(host)

    if not stp_commands:
        print(f"Команды для {host} не заданы. Пропуск.")
        continue

    configurator = STPConfigurator(device, stp_commands)
    try:
        configurator.connect()
        configurator.configure_stp()  
        configurator.disable_interface(INTERFACE_TO_DISABLE)  
        configurator.commit_changes()  
    except Exception as e:
        print(f"Ошибка на устройстве {host}: {e}")
    finally:
        configurator.disconnect()
