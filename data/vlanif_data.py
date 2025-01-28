VLAN_CONFIG = {
    "192.168.0.120": {
        10: "10.10.1.4 24",
        20: "10.20.1.4 24",
        30: "10.30.1.4 24",
    },
    "192.168.0.123": {
        10: "10.10.1.5 24",
        20: "10.20.1.5 24",
        30: "10.30.1.5 24",
    },
}

VRRP_CONFIG = {
    "192.168.0.120": {
        10: [{'vrid': 31, 'virtual_ip': '10.10.1.1', 'priority': 120}],
        20: [{'vrid': 32, 'virtual_ip': '10.20.1.1', 'priority': 120}],
        30: [{'vrid': 33, 'virtual_ip': '10.30.1.1', 'priority': 120}],
    },
    "192.168.0.123": {
        10: [{'vrid': 31, 'virtual_ip': '10.10.1.1'}],
        20: [{'vrid': 32, 'virtual_ip': '10.20.1.1'}],
        30: [{'vrid': 33, 'virtual_ip': '10.30.1.1'}],
    }
}
