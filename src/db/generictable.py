#!/usr/bin/python
# -*- coding: utf-8 -*-

class GenericTable(object):
    """ A very generic database table class."""
    __tableVersion = 1
    __key = ""
    __name = ""
    __createSQL = ""
    __fields = []
    def __init__(self):

        pass

    # Version
    def __get_version (self): return self.__tableVersion
    def __set_version (self,value): self.__tableVersion  = value
    Version = property(fget=__get_version, fset=__set_version, doc='Get/Set the table version number.')

    # Key
    def __get_key (self): return self.__key
    def __set_key (self,value): self.__key  = value
    Key = property(fget=__get_key, fset=__set_key, doc='Get/Set the table key.')

    # Name
    def __get_name (self): return self.__name
    def __set_name (self,value): self.__name  = value
    Name = property(fget=__get_name, fset=__set_name, doc='Get/Set the table name.')

    # CreateSQL
    def __get_createSQL (self): return self.__createSQL
    def __set_createSQL (self,value): self.__createSQL  = value
    CreateSQL = property(fget=__get_createSQL, fset=__set_createSQL, doc='Get/Set the SQL statement for the table creation.')

    # Fields
    def __get_fields (self): return self.__fields
    def __set_fields (self,value): self.__fields  = value
    Fields = property(fget=__get_fields, fset=__set_fields, doc='Get/Set the fields of the table.')
