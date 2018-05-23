#!/usr/bin/python
import os
import subprocess
import logging
import traceback

class history_command_manager():

        def __init__(self):
                pass

        def get_history_list(self,history_file):

                #run_command = ['bash', '-i', '-c', 'history -r; history']
                run_command = ['bash', '-i', '-c', 'history -r; history']
                command_output = "n/a"
                err = ""
                command_detail_info = ""
                out = ""
                try:
                        p = subprocess.Popen(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        command_detail_info=out
                except:
                        logging.error(str(err)+traceback.format_exc())

        
                #logging.debug("load history command: "+command_detail_info+out+err)
                
                if err is not None and err !="":
                        command_detail_info = "n/a"

                #list_of_lines = [line.strip() for line in command_detail_info]
                list_of_lines = [line.strip() for line in command_detail_info.splitlines()]
                return list_of_lines

        """
        def get_history_list(self,history_file):

                #print(os.system('help'))
                # doesnt include current session yet
                user_history = os.path.expanduser(history_file)
                lines = open(user_history).readlines()
                list_of_lines = [line.strip() for line in lines]
                return list_of_lines

        """
