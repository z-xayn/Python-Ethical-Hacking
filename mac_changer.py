#!/usr/bin/env python
import optparse
import re
import subprocess


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[+] Please specify an new_mac, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for ", interface, "to", new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(br"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_result:
        return mac_result.group(0)
    else:
        print("[-} Could not read MAC Address")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

