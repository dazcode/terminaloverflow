import json
import sys
import logging
import os
import string
import traceback


class settings_manager():

    default_settings_urls = {"history":"~/.bash_history",
                            "social":"https://www.reddit.com/r/frontpage/.json",
                            "saved":"https://www.github.com"}

    default_categories_enabled = {"history":True,
                                  "social":False,
                                  "saved":True}

    config_file_default_location="~/terminal_overflow.config"

    current_settings_urls = {}
    current_settings_categories_enabled = {}
    

    def __init__(self):
        self.load_user_settings()
        pass

    # Gets the settings url for a category    
    def get_user_settings(self,category):
        return self.current_settings_urls[category]
    # Gets category enabled setting
    def get_category_enabled(self,category):
        return self.current_settings_categories_enabled[category]
    # Gets the application config file location
    def get_config_location(self):
        return self.config_file_default_location

    def has_printable_chars(self,test_string):
        printable_set = set(string.printable)
        tmpset = set(json.dumps(test_string))
        tmpset.difference_update(printable_set)
       
        if len(tmpset) is not 0:
            #writing the invalid chars can mess up logfile
            #logging.error("ERROR: Invalid characters in settings file:"+str(tmpset))
            return False
        else:
            return True
        
    
    def parse_user_settings(self,settings_data):

        if not self.has_printable_chars(settings_data):
            logging.error("Invalid characters in settings file")
            return False

        try:
            #TODO: check if settings urls are properly formatted
            parsed_settings_urls = settings_data["settings_urls"]
            parsed_categories_enabled = settings_data["categories_enabled"]

            for tmp_category in parsed_categories_enabled:
                tmp_str = str(parsed_categories_enabled[tmp_category])
                if tmp_str.upper() == "TRUE":
                    parsed_categories_enabled[tmp_category]=True
                else:
                    parsed_categories_enabled[tmp_category]=False
            
        except:
            logging.error("Invalid settings detected")
            return False
        

        self.current_settings_urls = parsed_settings_urls
        self.current_settings_categories_enabled = parsed_categories_enabled

        return True


    # Write the settings to the config file
    def write_user_settings(self,settings_text):
        
        write_success = True
        try:
            settings_location = os.path.expanduser(self.config_file_default_location)
            with open(settings_location, 'w') as f:
                json.dump(settings_text, f)
        except:
            write_success = False
            logging.error(traceback.format_exc())


        if write_success:
            logging.debug("Wrote settings file: " +settings_location)         
        else:
            logging.debug("Failed writing settings files: "+settings_location)

        #logging.debug("SETTINGS:"+str(settings_text))

    # Read the settings to the config file
    def load_user_settings(self):

        settings_location = os.path.expanduser(self.config_file_default_location)

        logging.debug("Loading settings: "+ settings_location)
        use_default_settings = False
        try:
            with open(settings_location, 'r') as f:
                file_content = json.load(f)

            if not file_content:
                use_default_settings = True
                logging.debug("Settings file is empty")
            else:
                if not self.parse_user_settings(file_content):
                    use_default_settings = True
                    logging.error("failed settings check")
        except:
            logging.error(traceback.format_exc())
            use_default_settings = True


        if use_default_settings:
            self.current_settings_urls = dict(self.default_settings_urls)
            self.current_settings_categories_enabled = dict(self.default_categories_enabled)
            logging.debug("Using default settings")
        
        logging.debug("Loaded settings"+str(self.current_settings_urls))
        logging.debug("Loaded settings:"+str(self.current_settings_categories_enabled))

        return   
