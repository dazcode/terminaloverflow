import urwid.wimp
import urwid

from urwid.wimp import *

class CustomButton(WidgetWrap):
    def sizing(self):
        return frozenset([FLOW])
    button_left = Text("<")
    button_right = Text(">")
    signals = ["click"]

    def __init__(self, label, on_press=None, user_data=None):       
        self._label = self._label = ButtonLabel("")
        cols = Columns([self._label],dividechars=0)
        super(CustomButton, self).__init__(cols)
        if on_press:
            connect_signal(self, 'click', on_press, user_data)

        self.set_label(label)

    def _repr_words(self):
        return super(CustomButton, self)._repr_words() + [
            python3_repr(self.label)]
    def set_label(self, label):
        
        self._label.set_text(label)

    def get_label(self):
        
        return self._label.text
    label = property(get_label)

    def keypress(self, size, key):
        
        if self._command_map[key] != ACTIVATE:
            return key

        self._emit('click')

    def mouse_event(self, size, event, button, x, y, focus):
        
        if button != 1 or not is_mouse_press(event):
            return False

        self._emit('click')
        return True        
          
class ButtonLabel(urwid.SelectableIcon):
    def set_text(self, label):
        super(ButtonLabel, self).set_text(label)
        self._cursor_position = len(label) + 1

class list_button(CustomButton):
    pass
