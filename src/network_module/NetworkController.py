import nmcli

def network_get_ssid_list():
    try:
        nmcli.disable_use_sudo()
        ssid_list_pry=set()
        connections_list = nmcli.device.wifi()
        count = 0
        while(len(ssid_list_pry) <= 5 or len(connections_list) < count):
            if not(connections_list[count].ssid in ssid_list_pry) and connections_list[count].ssid != '':
                ssid_list_pry.add(connections_list[count].ssid)
            count+=1
    except IndexError:
        print("IndexError")

    return ssid_list_pry


def network_connect(ssid_input,pwd_input):
    nmcli.device.wifi_connect(ssid_input, pwd_input)
    #print(nmcli.device.status())
