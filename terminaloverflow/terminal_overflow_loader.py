#!/usr/bin/python
import urwid
from urllib2 import urlopen
from HTMLParser import HTMLParser
from simplejson import loads

from list_button import list_button

from history_command_manager import history_command_manager
from settings_manager import settings_manager
from social_search_manager import social_search_manager
from command_parse_manager import command_parse_manager
from publish_subscribe_manager import publish_subscribe_manager

from terminal_overflow_search_module import terminal_overflow_search_module
from terminal_overflow_settings_module import terminal_overflow_settings_module
from terminal_overflow_command_info_module import terminal_overflow_command_info_module



import json
import sys
import logging
import os
import subprocess
import traceback

            

class terminal_overflow_layout():

################### SETTINGS ################### 

    #define initial settings
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
    text_title_header = '--TERMINAL-OVERFLOW'
    text_footer_text =[
        'Press ctl+(', ('help button', 'R'), ') for settings. ',
        'Press ctl+(', ('quit button', 'X'), ') to quit.']

    initial_search_result_details = {"none":["none"]}

    #Color Scheme
    palette = [    
        ('settings_box', 'dark blue','', 'bold'),
        ('settings_text', 'dark cyan', ''),
        ('settings_edit_text','light gray', 'dark blue'),
        ('settings_edit_text_focus','yellow', 'dark blue', 'bold'),
        ('settings_edit_button_save','light blue', ''),
        ('settings_edit_button_close','light blue', '', 'bold'),
        ('settings_edit_button_focus','standout', ''),
        ('result_details_header','light blue,bold', '',),
        ('result_details_focus','standout', ''),
        ('result_details_body','', '','bold'),
        ('result_details_body_focus','', '','bold'),
        ('reversed', 'standout', ''),
        ('titlebar', 'dark cyan', ''),
        ('help button', 'dark green,bold', ''),
        ('quit button', 'dark red,bold', ''),
        ('editbx','light gray', 'dark blue'),
        ('editfc','yellow', 'dark blue', 'bold'),
        ('bright','','', 'bold'),
        ('radregular','light blue', ''),
        ('radfocus','light blue','', 'bold')]
    

################### KEY EVENTS ###################

    # Handles Unhandled MainLoop keyboard input
    def handle_input(self,key):

        #Global key combos
        if key == 'ctrl x':
            raise urwid.ExitMainLoop()
        elif key == 'ctrl r':
            self.settings_popup.toggle_open_close()
            pass
 
        #Settings popup is open
        if self.settings_popup.isOpen:
            if key == 'esc':
                self.settings_popup.toggle_open_close()
        else:
            if key == 'enter':
                pass
                #self.load_search_category(True)






    def __init__(self):


################### CREATE MANAGERS ###################

        self.settings_manager = settings_manager()
        self.history_command_manager = history_command_manager()
        self.social_search_manager = social_search_manager()
        self.command_parse_manager = command_parse_manager()

        self.publish_subscribe_manager = publish_subscribe_manager()

################### CREATE MODULES ###################

        self.terminal_modules = {}
        self.terminal_modules['search'] = terminal_overflow_search_module()
        self.terminal_modules['search'].build_initial_layout()
        self.terminal_modules['search'].begin(self.publish_subscribe_manager)

        self.terminal_modules['command_info'] = terminal_overflow_command_info_module()
        self.terminal_modules['command_info'].build_initial_layout()
        self.terminal_modules['command_info'].begin(self.publish_subscribe_manager)


################### PUBLISH/SUBSCRIBE ###################

        


################### CREATE UI ###################

        # Place Holder
        #self.main_spot_1 = urwid.WidgetPlaceholder(self.menu_original)

        # Create Header
        self.settings_popup = terminal_overflow_settings_module(self.text_title_header,self.palette,self.settings_manager)
        self.header = urwid.AttrMap(self.settings_popup, 'titlebar')


        self.w = urwid.Columns(
            [
                ('weight',1,self.terminal_modules['search'].get_base_layout_widget()),
                ('weight',1,self.terminal_modules['command_info'].get_base_layout_widget())
            ]
             ,dividechars=1, focus_column=0)

        # Assemble the widgets into the widget layout
        self.layout = urwid.Frame(header=self.header, body=self.w, footer=None)


        # Create the event loop
        self.main_loop = urwid.MainLoop(self.layout, self.palette, unhandled_input=self.handle_input,pop_ups=True)
        self.main_loop.run()


log_dir = os.path.expanduser("terminal_overflow.log")
logging.basicConfig(filename=log_dir,level=logging.DEBUG)
logging.debug('Application startup')

main_terminal = terminal_overflow_layout()





