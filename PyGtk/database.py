import cPickle as pickle

DATABASE_NAME = "data.db"

class Database:
    """
    Database class to store, delete,
    return the bills from the database.
    """
    def _create_database(self):
        """
        Creates a new, empty, file to host
        the database.
        """
        new_database = []
        
        try:
            file = open(DATABASE_NAME, "w")
            pickle.dump(new_database, file)
            file.close()
            
            return True
        except Exception, E:
            return False, E
    
    def _read_database(self):
        """
        Read the file and returns a list containing
        dicts, each dicts representes a bill.
        """
        # loads the database
        file = open(DATABASE_NAME, "r")
        data = pickle.load(file)
        file.close()
        
        return data
    
    def _write_database(self, newData):
        """
        After doing modification on the database, you can
        save those on a file.
        
        """
        # writes to the database the new data content
        try:
            file = open(DATABASE_NAME, "w")
            pickle.dump(newData, file)
            file.close()
            return True
        except:
            return False
       
    def _get_newbill_id(self):
        """
        Gets the id of the new bill to store on the database
        """
        try:
            data = self._read_database()
            
            # we get the last id on the list, than
            # add + 1 to it and we get or new id
            id = data[-1]["id"] + 1
        except:
            id = 0
        
        return id
        
    def addBill(self, bill):
        """
        Adds a bill to the database.
        Just is usable with the new Bill class
        """
        data = self._read_database()
        
        # Pickles has a better support to native python
        # objects, so we create a dict on the instance
        # of the bill that contains de info about de bill.
        billObject = bill.bill_dict
        billObject["id"] = self._get_newbill_id()
        
        # Here, we try to create the bill.
        try:
            data.append(billObject)
            self._write_database(data)
            return True
        except Exception, E:
            return False, E
        
        

    def deleteBill(self, id):
        """
        Deletes a bill based on its id.
        Each bill on de list contains a key "id" that
        has a numeric value, its id.
        """
        # loads the database
        data = self._read_database()
        
        for index, bill_object in enumerate(data):
            if bill_object['id'] == id:
                del data[index]
        
        self._write_database(data)