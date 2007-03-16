#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['Config']

from model.dal import DAL

class Config:
    
    __default = {
        'Notification.Days': '7', #days
        'Notification.Interval': '43200', #seconds
        'Notification.Alarm': '16:00' # hh:mm
        }
    __dic = {}

    def __init__(self):
        self.__dal = DAL()
        self.load()
        
    def load(self):
        """ Load configuration from database. """
    	entries = self.__dal.get('tblconfig', {'key': '*'})
    	print entries
    	if not entries: 
    	    return
    	for entry in entries:
    	    self.__dic[entry['key']] = entry['value']
    
    def save(self):
        pass
    
    def get(self, key):
        return self.__dic.get(key, self.__default.get(key, ''))
    
    def set(self, key, value):
        self.__dic[key] = value
