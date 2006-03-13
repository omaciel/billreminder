#!/usr/bin/env python

class Bill:
    def __init__(self, payee, dueDate, amountDue, notes):
        self.payee = payee
        self.dueDate = dueDate
        self.amountDue = amountDue
        self.notes = notes
        
    def Payee(self):
        return self.payee
    
    def __repr__(self):
        return self.payee