class command_parse_manager():

    def __init__(self):
        pass

    def build_command_detail_info_dictionary(self,command_string):
        command_list = self.parse_command_string(command_string)
        command_info_dictionary = {}

        for the_command in command_list:
            tmp_cmd_item = self.get_command_detail_info(the_command)
            if tmp_cmd_item != "n/a":
                command_info_dictionary[tmp_cmd_item] = tmp_cmd_item
        
        
        return command_info_dictionary
    

    
    def get_command_detail_info(self,command_name):
        
        run_command = "whatis " + command_name    
        command_detail_info = "n/a"
        err = ""
        try:
            p = subprocess.Popen(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
            out, err = p.communicate()
            command_detail_info=out
        except:
            logging.error(str(err)+traceback.format_exc())

       
        logging.debug("command: "+command_detail_info+erar)
        
        if err is not None and err !="":
            command_detail_info = "n/a"
        else:
            command_detail_info = command_detail_info.strip()
            #format the string?
            pass

        return command_detail_info

    def parse_command_string(self,command_string):
        #TODO make this more advanced
        command_tokens = list(command_string.split(" "))

        logging.debug("command tokens: " + str(command_tokens[1:]))
        return command_tokens[1:]
