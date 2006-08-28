class Bill2:
    def __init__(self, payee="", dueDate="", amountDue="", notes=""):
        self.payee = payee
        if (dueDate == ""):
            dueDate = datetime.date.today()
            
        self.dueDate = dueDate
        self.amountDue = amountDue
        self.notes = notes
    
    def getList(self):
        """This function returns a list made up of the 
        bill information."""
        return [self.payee, self.dueDate, self.amountDue, self.notes]

class Bill:
    def __init__(self, payee, dueDate, amountDue, notes):
        # Check if all necessary parameters were passed
        assert payee and dueDate and amount or notes, Exception("You must pass the arguments: \
                                                                payee, due_date and amount.")
        
        self.payee = payee
        self.dueDate =  dueDate
        self.amountDue = amountDue
        self.notes = notes
        
        self.bill_dict = {'payee': self.payee, 'dueDate' : self.dueDate, 'amount' : self.amountDue, \
                          'notes' : self.notes}
        
    def __str__(self):
        return "<Bill object> Payee = %s, Due Date = %s, Amount = %s </Bill object>" \
                                            % (self.payee, self.dueDate, self.amountDue)

