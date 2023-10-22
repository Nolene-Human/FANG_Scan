
import nmap

def onclick():
    button=document.getElementById("button")


nm = nmap.PortScanner()
nm.scan(hosts='192.168.1.0/24', arguments='-sn')
                    
for host in nm.all_hosts():
    if 'mac' in nm[host]['addresses']:
        mac_address = nm[host]["addresses"]["mac"]
        manufacturer = nm[host]["vendor"].get(mac_address, "Unknown")
        print("IP Address: {}, MAC Address: {}, Manufacturer: {}".format(host, mac_address, manufacturer))