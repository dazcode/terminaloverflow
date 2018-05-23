#!/usr/bin/python


import urwid
from urllib2 import urlopen
from HTMLParser import HTMLParser
from simplejson import loads

from history_command_manager import history_command_manager
from settings_manager import settings_manager
from social_search_manager import social_search_manager
from list_button import list_button
from command_parse_manager import command_parse_manager

import json
import sys
import logging
import os
import subprocess
import traceback



class terminal_overflow_command_info_module():

################### SETTINGS ################### 

    #define initial settings
    initial_search_results = ["none"]
    current_screen = urwid.raw_display.Screen()
    screen_cols,screen_rows = current_screen.get_cols_rows()
    current_list_height = screen_rows - 6
    current_list_width = (screen_cols/2) -10
    current_command_token_list_width = (screen_cols/2) -5


    initial_search_result_details = {"none":"none"}

    palette = []


################### KEY EVENTS ###################

        # Handles Unhandled MainLoop keyboard input
    def handle_input(self,key):
        pass


################### CLICK EVENTS ###################
 
    #Command
    def command_token_chosen(self,button, choice):

        command_token_list = choice.split(" ")
        command_token = str(command_token_list[0])

        details_text = self.command_parse_manager.get_command_extended_info(command_token)
        details_text = unicode(details_text, 'utf-8')
        self.command_token_details_text.set_edit_text(details_text)

    #Search
    def item_chosen(self,button, choice):
        self.result_details.set_edit_text(choice)      
        search_result_command_details = self.command_parse_manager.build_command_detail_info_dictionary(choice)
        #Refresh command info details
        self.main_result_details_list.original_widget = self.generate_result_details(u'', search_result_command_details)  
        
        #Fill command details
        command_token_default = ""
        for command in search_result_command_details:
            command_token_default = command
        
        self.command_token_chosen(None,command_token_default)

   

################### FORMAT ###################
    #Command Info
    def format_command_info_result(self,unformatted_result):
        max_line_width = self.current_command_token_list_width    
        formatted_result = ""
        formatted_result = unformatted_result[:max_line_width]  
        return formatted_result


################### GENERATE ###################

    def generate_result_details(self, title, command_selected_dict):

        body = []
        for c in command_selected_dict:
            detail_display_text = self.format_command_info_result(command_selected_dict[c])
            button = list_button(detail_display_text)
            urwid.connect_signal(button, 'click', self.command_token_chosen, detail_display_text)
            #button = urwid.Padding(button,align='left',width='clip')
            body.append(urwid.AttrMap(button,None, focus_map='reversed'))    

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))





    def __init__(self):
 

################### CREATE MANAGERS ###################
        self.settings_manager = settings_manager()
        self.command_parse_manager = command_parse_manager()



################### GET BASE LAYOUT ###################
    def get_base_layout_widget(self):
        return self.layout


################### BEGIN ###################
    def begin(self,publish_subscribe_manager):

        self.publish_subscribe_manager = publish_subscribe_manager
        self.publish_subscribe_manager.register_listener('search_input',self)

################### SUBSCRIBE EVENT ###################
    def event_subscribe(self,event_name,event_data):

        if event_name == 'search_input':
            self.item_chosen(None,event_data)


################### CREATE UI ###################
    def build_initial_layout(self):
        

        # Application Box
        self.result_details_header = urwid.AttrWrap(urwid.Text(u'Command:'),'result_details_header','result_details_focus')
        self.result_details = urwid.Edit(u'')

        # Info
        self.result_details_list_header = urwid.AttrWrap(urwid.Text(u'Info:'),'result_details_header','result_details_focus')
        self.main_result_details_list = urwid.BoxAdapter(self.generate_result_details(u'', self.initial_search_result_details),self.current_list_height/3)

        # Details pile
        self.command_token_details_header = urwid.AttrWrap(urwid.Text(u'Details:'),'result_details_header','result_details_focus')
        self.command_token_details_text = urwid.Edit(u'')
        self.pile_results = urwid.Pile([self.result_details_header, 
                                        self.result_details,
                                        self.result_details_list_header, 
                                        self.main_result_details_list,
                                        self.command_token_details_header,
                                        self.command_token_details_text
                                        ])

        self.details_filler = urwid.AttrMap(urwid.Filler(self.pile_results, valign='top', top=0, bottom=1),'result_details_body','result_details_body_focus')
        self.result_box_details = urwid.LineBox(self.details_filler)
        self.w = urwid.Columns([('weight',1,self.result_box_details)],dividechars=1, focus_column=0)
        self.layout = urwid.Frame(header=None, body=self.w, footer=None)


logging.debug('Loading Command Info Module')


