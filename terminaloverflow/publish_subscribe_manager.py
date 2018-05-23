#!/usr/bin/python

class publish_subscribe_manager():

    listeners={}

    def __init__(self):
        pass

    #Double check later if reference here causes memory leak issues
    def register_listener(self,event_name,listener_object):

        if event_name in self.listeners:
            self.listeners[event_name].append(listener_object)
        else:
            self.listeners[event_name] = [listener_object]

    def unregister_listener(self,event_name,listener_object):
        #del self.listeners[event_name][listener_object]
        pass  

    def publish_event(self,event_name,event_data):
        if self.listeners[event_name] is not None:
            for listener in self.listeners[event_name]:
                getattr(listener, "event_subscribe")(event_name,event_data)
