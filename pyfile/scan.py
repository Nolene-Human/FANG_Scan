import nmap   

def scan_network_devices():
    scan='no'
    scan=input("Enter yes")

    nm = nmap.PortScanner()
    if scan=='yes':
            print("List of Devices on your network")
            nm.scan(hosts='192.168.1.0/24', arguments='-sn')
                    
            for host in nm.all_hosts():
                if 'mac' in nm[host]['addresses']:
                    mac_address = nm[host]["addresses"]["mac"]
                    manufacturer = nm[host]["vendor"].get(mac_address, "Unknown")
                    device=print("IP Address: {}, MAC Address: {}, Manufacturer: {}".format(host, mac_address, manufacturer))
    return device

def scapy_scan():
    import scapy.all as s 
    Scapy_scan=lit.checkbox('Scapy Scan')
    save_devices=lit.checkbox("save to database")

    list_devices=[]

    if Scapy_scan:
        answered_list=s.arping("192.168.1.0/24")
                         
        # iterate through the result and add each host to the dictionary
        for sent, received in answered_list[0].res:
            ip=received.psrc
            mac=received.hwsrc
            device_name="New"
            devices={"ip":ip,"mac":mac,"name":device_name}
            list_devices.append(devices)
            if save_devices:
                database.child(user['localId']).child('Devices').push(devices)
                              
                with ip_col:
                    lit.write(ip)
                with mac_col:
                    lit.write(mac)
                with name_col:
                    lit.write(device_name)
                         
    #lit.json(list_devices)


    print("hi")
    scan_network_devices()