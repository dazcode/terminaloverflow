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

class terminal_overflow_search_module():

################### SETTINGS ################### 

    initial_search_results = ["none"]
    current_screen = urwid.raw_display.Screen()
    screen_cols,screen_rows = current_screen.get_cols_rows()
    current_list_height = screen_rows - 6
    current_list_width = (screen_cols/2) -10
    current_command_token_list_width = (screen_cols/2) -5
    radio_category_group = []
    text_radio_list = [u"history", u"social", u"saved"]
    radios = []
    selected_category="history"
 
    initial_search_result_details = {"none":["none"]}
    palette = [ ]
    
    
    def generate_radio_menu(self, choices):
        for rad_choice in choices:
            radio_button = urwid.RadioButton(self.radio_category_group, rad_choice)
            urwid.connect_signal(radio_button, 'change', self.radio_item_chosen, rad_choice)
            radio_button=urwid.AttrWrap(radio_button, 'radregular','radfocus')           
            self.radios.append(radio_button)
            columns_radios = urwid.Columns(self.radios,dividechars=1, focus_column=0)
        return columns_radios

    def update_radio_category_count(self,category_name,category_count):     
        for current_radio in self.radios:
            if category_name in current_radio.get_label():
                current_radio.set_label(category_name + "["+ str(category_count) + "]")

    # switch to and display results in selected category
    def load_search_category(self,pressed_enter=False,search_box_text=None):
            if search_box_text is not None:
                search_text = search_box_text
            else:
                search_text = self.ask.get_edit_text()
            search_results = []

            if "social" in self.selected_category:
                if pressed_enter:
                    tmp_reddit_data = self.social_search_manager.run_search(self.settings_manager.get_user_settings('social'))
                    search_results = list(filter(lambda x: search_text in x, tmp_reddit_data))
                    search_results = [self.format_search_result(x,self.selected_category) for x in search_results]
                    self.main_results.original_widget = self.generate_menu(u'', search_results)
                    self.update_radio_category_count(self.selected_category,len(search_results))
                else:
                    pass
                    #on social search dont update for every key press
                    #wait till user presses enter, todo: put timer here?
            elif "history" in self.selected_category:
                tmp_history_data = self.history_command_manager.get_history_list(self.settings_manager.get_user_settings("history"))
                search_results = list(filter(lambda x: search_text in x, tmp_history_data))
                search_results = [self.format_search_result(x,self.selected_category) for x in search_results]
                self.main_results.original_widget = self.generate_menu(u'', search_results)
                self.update_radio_category_count(self.selected_category,len(search_results))     
            elif "saved" in self.selected_category:
                pass
            else:
                pass

    
################### FORMAT ###################   

    #Search Results
    def format_search_result(self,unformatted_result,search_results_type):
        max_line_width = self.current_list_width    
        formatted_result = ""
        if "social" in search_results_type:
            formatted_result = " social " + unformatted_result[:max_line_width]
        elif "history" in search_results_type:
            tmp_string_list = unformatted_result.split(" ")
            tmp_string = "[#"+tmp_string_list[1]+"] " + " ".join(tmp_string_list[4:])
            formatted_result = tmp_string[:max_line_width]
        elif "saved" in search_results_type:
            formatted_result = " saved " + unformatted_result[:max_line_width]
        else:
            formatted_result = " bad search result type"
        return formatted_result

################### GENERATE ###################

    #Search Categories
    def generate_menu(self, title, choices):
        body = []
        for c in choices:
            button = list_button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            #button = urwid.Padding(button,align='left',width='clip')
            body.append(urwid.AttrMap(button,None, focus_map='reversed'))       
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))


################### CLICK EVENTS ###################
    
    #Category
    def radio_item_chosen(self, button, newstate, selected_category):
        if newstate is True or newstate is "firstTrue":
            self.selected_category = selected_category
            self.load_search_category(True)

    #Search
    def item_chosen(self,button, choice):
        self.publish_subscribe_manager.publish_event('search_input',choice)
        pass
        

################### KEY EVENTS ###################

    def on_search_input_change(self,edit, new_edit_text):
        self.load_search_category(False,new_edit_text)
        pass

    # Handles Unhandled MainLoop keyboard input
    def handle_input(self,key):

        # Module specific key
        if key == 'ctrl x':
            raise urwid.ExitMainLoop()
        

    def __init__(self):


################### CREATE MANAGERS ###################
        #Settings Manager
        self.settings_manager = settings_manager()
        self.history_command_manager = history_command_manager()
        self.social_search_manager = social_search_manager()

################### CREATE UI ###################

       
    def build_initial_layout(self):

         # Text input section
        self.ask_widget = urwid.Edit(u"")
        self.ask_widget.set_caption(('editbx','Search: '))
        self.ask = urwid.AttrWrap((self.ask_widget),'editbx','editfc')  
        urwid.connect_signal(self.ask.original_widget, 'change', self.on_search_input_change)

        # Generate radio button categories
        self.radio_category_menu = self.generate_radio_menu(self.text_radio_list)

        # Generate initial search result list area
        self.main_results = urwid.BoxAdapter(self.generate_menu(u'', self.initial_search_results),self.current_list_height)
        self.pile = urwid.Pile([self.ask,self.radio_category_menu,  self.main_results])
        self.quote_filler = urwid.Filler(self.pile, valign='top', top=0, bottom=1)
        self.quote_box = urwid.LineBox(self.quote_filler)

        # Assemble the widgets into the widget layout
        self.layout = urwid.Frame(header=None, body=self.quote_box, footer=None)

        
    def get_base_layout_widget(self):
        return self.layout  

    def begin(self,publish_subscribe_manager):
        self.publish_subscribe_manager = publish_subscribe_manager
        
        #load initial search results "everything"
        self.load_search_category()


logging.debug('Loading Search Module')

