import json;
import os
import math;
import ast;
import yaml;
import ipaddress;

#_______________________________________________________________

RED = '\033[31m'  #Red text
GREEN = '\033[32m'  # Green text
YELLOW = '\033[33m'  # Yellow text
RESET = '\033[0m'  # Reset to default color

#_______________________________________________________________

def validate_ip_address(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def validate_network(address, netmask):
    try:
        ipaddress.ip_network(f"{address}/{netmask}", strict=False)
        return True
    except ValueError:
        return False

def choose_datacenter():
        with open("../output/datacentername.txt") as datacenter_names:
                data=ast.literal_eval(datacenter_names.readline());
                print(data[0])


def choose_datastore():
        with open("../output/datastore_details.json") as datastore_details:
                 data=json.load(datastore_details)
        i=0
        print("_______________________________________________________________");
        for key in data:
                i=i+1
                size=int(math.trunc(data[key]/1073741824))
                if(size>10000):
                        data[key]=str(GREEN+str(size))
                elif (size>5000):
                        data[key]=str(YELLOW+str(size))
                else:
                        data[key]=str(RED+str(size))
                print("         DataStore"+str(i)+": "+key+ " Free space: "+ data[key]+"GB"+RESET)
                print("_______________________________________________________________");
        chosen_datastore=-1;
        while(chosen_datastore not in range(1,i+1)):
                chosen_datastore=int(input("Donner le numéro du Datastore sur lequels vous voulez deployer les VMs:"));

        return list(data.keys())[chosen_datastore-1]


def main():
    templates_list=["TEMPLATE_RHEL-8.8_STG","TemplateCentos8_1"]
    vm_numbers=-1
    while(vm_numbers<1):
       vm_numbers=int(input("Donner le nombre de VMs à déployer:"))
    #os.system("ansible-playbook ../playbooks/gather_vcenter_infos.yml")
    datacenter=choose_datacenter()
    datastore=choose_datastore();
    vms=[]
    for x in range(vm_numbers):
        dict={}
        hostname=input("Donner le Hostname de la VM"+str(x)+" :")
        dict["hostname"]=hostname
        ram=-1;
        while(int(ram)<1 or int(ram)%2!=0):
            ram=input("Donner le nombre de Ram de la VM"+str(x)+" :")
        dict["memory_mb"]=int(ram)*1024
        cpu=0;
        while(int(cpu)<1):
            cpu=input("Donner le nombre de vCPUs de la VM"+str(x)+" :")
        dict["cpu"]=cpu
        ipaddress='';
        while(not validate_ip_address(ipaddress)):
            ipaddress=input("Donner l'adresse IP de la  VM"+str(x)+" :")
        dict["ipaddress"]=ipaddress
        netmask='';
        while(not validate_network(ipaddress,netmask)):
            netmask=input("Donner le netmask de la  VM"+str(x)+" :")
        dict["netmask"]=netmask
        gateway='';
        while(gateway==''):
            gateway=input("Donner le gateway de la  VM"+str(x)+" :")
        dict["gateway"]=gateway
        dns='';
        while(dns==''):
            dns=input("Donner le DNS de la  VM"+str(x)+" :")
        dict["dns"]=dns
        dict["template"]=templates_list[0]
        dict["datastore"]=datastore
        vms.append(dict);

    with open("../output/vm_configs.yml","w") as vm_configs:
        yaml.dump({"vms":vms},vm_configs,default_flow_style=False)

main()
