from guizero import App,Text
import subprocess,re
import wifi
import time
from colorama import init, Fore
app = App(title="GUI")
#app.set_full_screen()



# scan for available WiFi networks
wifi_scanner = wifi.Cell.all('wlp3s0')
available_networks = [cell.ssid for cell in wifi_scanner]

# print available networks
print(f"Available Networks: {available_networks}")

# connect to a WiFi network
network_ssid = input("Enter network SSID: ")
network_pass = input("Enter network password: ")

for cell in wifi_scanner:
    if cell.ssid == network_ssid:
        scheme = wifi.Scheme.for_cell('wlp3s0', cell.ssid, cell, network_pass)
        scheme.save()
        scheme.activate()
        print(f"Connected to network: {network_ssid}")
        break
    else:
	    print(f"Unable to find network: {network_ssid}")

app.display()

