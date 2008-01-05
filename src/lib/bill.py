#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Bill']

from datetime import datetime
import time

class Bill(object):

    def __init__(self, payee, category='', dueDate='', amountDue='',
                 notes=None, paid=0, id=-1, alarm=-1):

        if isinstance(payee,dict):
            self.__set_id(payee['Id'])
            self.__set_category(payee['catId'])
            self.__set_payee(payee['payee'])
            if not payee['dueDate']:
                self.__set_dueDate(time.time())
            else:
                self.__set_dueDate(payee['dueDate'])

            self.__set_amountDue(payee['amountDue'])
            self.__set_notes(payee['notes'])
            self.__set_paid(payee['paid'])
            self.__set_alarm(payee['alarm'])
        else:
            self.__set_id(id)
            self.__set_payee(payee)
            self.__set_category(category)
            if not dueDate:
                self.__set_dueDate(time.time())
            else:
                self.__set_dueDate(dueDate)
            self.__set_amountDue(amountDue)
            self.__set_notes(notes)
            self.__set_paid(paid)
            self.__set_alarm(alarm)

    # Id
    def __get_id (self): return self.__id
    def __set_id (self, value): self.__id  = value
    Id = property(fget=__get_id, fset=__set_id,
                  doc='Get/Set the Id.')

    # Category
    def __get_category (self): return self.__category
    def __set_category (self, value): self.__category  = value
    Category = property(fget=__get_category, fset=__set_category,
                        doc='Get/Set the category.')

    # Payee
    def __get_payee (self): return self.__payee
    def __set_payee (self, value): self.__payee  = value
    Payee = property(fget=__get_payee, fset=__set_payee,
                     doc='Get/Set the payee.')

    # DueDate
    def __get_dueDate(self): return self.__dueDate
    def __set_dueDate(self, value):
        #assert isinstance(value, float)
        self.__dueDate = value
    DueDate = property(fget=__get_dueDate, fset=__set_dueDate,
                       doc='Get/Set the due date.')

    # AmountDue
    def __get_amountDue (self): return self.__amountDue
    def __set_amountDue (self, value):
        #assert isinstance(value, float)
        self.__amountDue = value
    AmountDue = property(fget=__get_amountDue, fset=__set_amountDue,
                         doc='Get/Set the amount for the bill.')

    # Notes
    def __get_notes(self): return self.__notes
    def __set_notes(self, value): self.__notes = value
    Notes = property(fget=__get_notes, fset=__set_notes,
                     doc='Get/Set notes.')

    # Paid
    def __get_paid(self): return self.__paid
    def __set_paid(self, value):
        #assert isinstance(value, int)
        #assert 0 <= value <= 1
        self.__paid = value
    Paid = property(fget=__get_paid, fset=__set_paid,
                    doc='Get/Set if package was paid.')

    # Alarm
    def __get_alarm(self): return self.__alarm
    def __set_alarm(self, value):
        #assert isinstance(value, int)
        #assert 0 <= value <= 1
        self.__alarm = value
    Alarm = property(fget=__get_alarm, fset=__set_alarm,
                    doc='Get/Set if package has alarm.')

    # Dictionary
    def __get_dictionary(self):
        return dict({
            'Id': self.__id,
            'catId': self.__category,
            'payee': self.__payee,
            'dueDate': self.__dueDate,
            'amountDue': self.__amountDue,
            'notes': self.__notes,
            'paid': self.__paid,
            'alarm': self.__alarm})
    Dictionary = property(fget=__get_dictionary,
                          doc='Gets a dictionary representation of bill.')

    def __repr__(self):
        return self.__payee
