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
    def __init__(self, payee, dueDate, amountDue, notes=None):
        self.payee = payee
        if not dueDate:
            self.dueDate = time.time()
        else:
            self.dueDate = dueDate
        self.amountDue = amountDue
        self.notes = notes

    def Payee(self):
        return self.payee

    def DueDate(self):
        return self.dueDate

    def AmountDue(self):
        return self.amountDue

    def Notes(self):
        return self.notes

    def __repr__(self):
        return self.payee
