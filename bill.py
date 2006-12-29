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
