#!/usr/bin/python
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class social_search_manager():

    def __init__(self):
        pass

    def run_search(self,url):
        try:
            import ssl
        except ImportError:
            print("error: no ssl support")
        
        http = urllib3.PoolManager()

        try:
            response = http.request('GET', url)
        except ImportError:
            return ["connection failure"]
        
        parsed_json = json.loads(str(response.data))
        data_list = list(parsed_json["data"]["children"])
        return_list =[]

        for post in data_list:
            return_list.append(post["data"]["title"])
            
        return return_list

   
