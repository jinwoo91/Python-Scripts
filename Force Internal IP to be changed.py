import os

def change_ip(new_ip):
    os.system(f'sudo ifconfig eth0 {new_ip}')

change_ip('192.168.1.138')