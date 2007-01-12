#!/usr/bin/python
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in the 
# Software without restriction, including without limitation the rights to use, copy, 
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the 
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# BillReminder - Copyright (c) 2006, 2007 Og Maciel
#
# -*- coding: utf-8 -*-

from datetime import datetime
import time

class Bill(object):
    def __init__(self, payee, dueDate, amountDue, notes=None, paid=0, id=-1):
        self.__set_id(id)
        self.__set_payee(payee)
        if not dueDate:
            self.__set_dueDate(time.time())
        else:
            self.__set_dueDate(dueDate)
        self.__set_amountDue(amountDue)
        self.__set_notes(notes)
        self.__set_paid(paid)

    # Id
    def __get_id (self): return self.__id 
    def __set_id (self,value): self.__id  = value
    Id = property(fget=__get_id, fset=__set_id, doc='Get/Set the Id.')

    # Payee
    def __get_payee (self): return self.__payee 
    def __set_payee (self,value): self.__payee  = value
    Payee = property(fget=__get_payee, fset=__set_payee, doc='Get/Set the payee.')


    # DueDate
    def __get_dueDate(self):
        return self.__dueDate

    def __set_dueDate(self, value):
        #assert isinstance(value, float)
        self.__dueDate = value

    DueDate = property(fget=__get_dueDate, fset=__set_dueDate, doc='Get/Set the due date.')


    # AmountDue
    def __get_amountDue (self):
        return self.__amountDue

    def __set_amountDue (self, value):
        #assert isinstance(value, float)
        self.__amountDue  = value

    AmountDue = property(fget=__get_amountDue, fset=__set_amountDue, doc='Get/Set the amount for the bill.')


    # Notes
    def __get_notes(self): return self.__notes
    def __set_notes(self,value): self.__notes = value
    Notes = property(fget=__get_notes, fset=__set_notes, doc='Get/Set notes.')


    # Paid
    def __get_paid(self):
        return self.__paid

    def __set_paid(self,value):
        #assert isinstance(value, int)
        #assert 0 <= value <= 1
        self.__paid = value

    Paid = property(fget=__get_paid, fset=__set_paid, doc='Get/Set if package was paid.')

    # Dictionary
    def __get_dictionary(self):
        return dict({
            'Id': self.__id,
            'Payee': self.__payee,
            'DueDate': self.__dueDate,
            'AmountDue': self.__amountDue,
            'Notes': self.__notes,
            'Paid': self.__paid})

    Dictionary = property(fget=__get_dictionary, doc='Gets a dictionary representation of bill.')

    def __repr__(self):
        return self.__payee
