#!/usr/bin/python
import urwid
import json
import sys
import logging
import os
import subprocess
import traceback
from list_button import list_button

# Program settings UI
class terminal_overflow_settings_popup(urwid.WidgetWrap):
    signals = ['close']
    
    checkbox_category_group = []
    text_checkbox_list = [u"history", u"social", u"saved"]
    checkboxes = []
    selected_category = None


    #category selected
    def checkbox_item_chosen(self, button, newstate, selected_category):
        if newstate is True or newstate is "firstTrue":
            self.selected_category=selected_category

    def generate_checkbox_menu(self, choices):
        self.checkboxes = []
        for checkbox_category in choices:
            checkbox_item = urwid.CheckBox(checkbox_category,state=self.settings_manager.get_category_enabled(checkbox_category))
            urwid.connect_signal(checkbox_item, 'change', self.checkbox_item_chosen, checkbox_category)
            checkbox_item=urwid.AttrWrap(checkbox_item, 'radregular','radfocus')           
            self.checkboxes.append(checkbox_item)
            columns_checkboxes = urwid.Columns(self.checkboxes,dividechars=1, focus_column=0)
        return columns_checkboxes
    
    def save_settings_click(self):

        settings_urls = {"history":self.history_file_widget.get_edit_text(),
                         "social":self.social_url_widget.get_edit_text(),
                         "saved":self.saved_url_widget.get_edit_text()}

        categories_enabled = {}

        for current_checkbox in self.checkboxes:
            categories_enabled[current_checkbox.get_label()] = current_checkbox.get_state()

        settings_text={"settings_urls":settings_urls,"categories_enabled":categories_enabled}
        self.settings_manager.write_user_settings(settings_text)
        self.settings_manager.load_user_settings()
        self._emit("close")
        

    def __init__(self,palette,settings_manager):

        # Get current instance of settings manager
        self.settings_manager = settings_manager

        # Settings headers
        self.settings_category_header = urwid.Text(u'Enabled Categories')
        self.settings_social_header = urwid.Text(u'Social URL')
        self.settings_saved_header = urwid.Text(u'Saved URL')
        self.settings_history_header = urwid.Text(u'History File')

        # Save and Close Buttons
        self.save_button_widget = list_button("[ Update ]")
        self.close_button_widget = list_button("[ Cancel ]")
        self.save_button = urwid.AttrWrap((self.save_button_widget),'settings_edit_button_save','settings_edit_button_focus')
        self.close_button = urwid.AttrWrap((self.close_button_widget),'settings_edit_button_close','settings_edit_button_focus')

        urwid.connect_signal(self.save_button_widget, 'click',lambda button:self.save_settings_click())
        urwid.connect_signal(self.close_button_widget, 'click',lambda button:self._emit("close"))
        
        # Edit Saved URL
        self.saved_url_widget = urwid.Edit(u"",self.settings_manager.get_user_settings("saved"))
        self.saved_url_widget.set_caption(('editbx','Search: '))
        self.saved_url = urwid.AttrWrap((self.saved_url_widget),'settings_edit_text','settings_edit_text_focus')  
        # Edit History File
        self.history_file_widget = urwid.Edit(u"",self.settings_manager.get_user_settings("history"))
        self.history_file_widget.set_caption(('editbx','File: '))
        self.history_file = urwid.AttrWrap((self.history_file_widget),'settings_edit_text','settings_edit_text_focus') 
        # Edit Social URL
        self.social_url_widget = urwid.Edit(u"",self.settings_manager.get_user_settings("social"))
        self.social_url_widget.set_caption(('editbx','File: '))
        self.social_url = urwid.AttrWrap((self.social_url_widget),'settings_edit_text','settings_edit_text_focus')

        # Generate checkbox button categories
        self.checkbox_category_menu = self.generate_checkbox_menu(self.text_checkbox_list)


        self.button_cols = urwid.GridFlow([self.save_button,self.close_button],10,5,0,align="center")

        self.pile_settings = urwid.Pile([
                                    self.settings_category_header,
                                    self.checkbox_category_menu,
                                    self.settings_social_header,
                                    self.social_url,
                                    self.settings_saved_header,
                                    self.saved_url,
                                    self.settings_history_header,
                                    self.history_file,
                                    self.button_cols
                                    ])

                                    
        settings_filler = urwid.Filler(self.pile_settings, valign='top', top=0, bottom=1)
        settings_box_details = urwid.LineBox(settings_filler)
        
        super(terminal_overflow_settings_popup, self).__init__(urwid.AttrWrap(settings_box_details, ''))


# Settings popup widget
class terminal_overflow_settings_module(urwid.PopUpLauncher):
    import list_button

    isOpen = False
    palette = []

    def __init__(self,title,palette,settings_manager):
        
        self.palette = palette
        self.settings_manager = settings_manager

        the_popup_button = list_button(title)
        super(terminal_overflow_settings_module, self).__init__(the_popup_button)
        urwid.connect_signal(self.original_widget, 'click',lambda button: self.toggle_open_close())
        
    def create_pop_up(self):
        pop_up = terminal_overflow_settings_popup(self.palette,self.settings_manager)
        urwid.connect_signal(pop_up, 'close',lambda button: self.toggle_open_close())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left':0, 'top':1, 'overlay_width':75, 'overlay_height':14}                

    def toggle_open_close(self):
        if self.isOpen:
            self.isOpen = False
            self.close_pop_up()
            
        else:
            self.isOpen = True
            self.open_pop_up()
