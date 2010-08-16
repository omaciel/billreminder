from sqlalchemy import Column, Integer, String, Numeric, Text, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255, convert_unicode=True))
    color = Column(String(length=6, convert_unicode=True))

    def __init__(self, name, color=None):
        self.name = name
        if color:
            self.color = color

    def __repr__(self):
        return self.name

class Bill(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True)
    payee = Column(String(length=255, convert_unicode=True))
    amount = Column(Numeric)
    dueDate = Column(Date)
    alarmDate = Column(DateTime)
    notes = Column(Text(convert_unicode=True))
    paid = Column(Boolean)
    repeats = Column(Boolean)

    catId = Column(Integer, ForeignKey('categories.id'))
    category = relation(Category, backref=backref('bills', order_by=id))

    def __init__(self, payee, amount, dueDate, alarmDate=None, notes=None, paid=False, repeats=None, category=None):
        self.payee = payee
        self.amount = amount
        self.dueDate = dueDate
        if alarmDate:
            self.alarmDate = alarmDate
        if notes:
            self.notes = notes
        self.paid = paid
        self.repeats = repeats
        	if category:
		self.category = category

    def __repr__(self):
        return self.payee

if __name__ == 'main':
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from datetime import date

    engine = create_engine('sqlite:///:memory:', echo=True)
    Session = sessionmaker(bind=engine)

    # Creates all database tables
    Bill.metadata.create_all(engine)

    dt = date.today()

    # Create a new Bill record
    ht = Bill('Harris Teeter', 123.94, dt)
    # Create a new Category record
    food = Category('Groceries')
    # Add category to bill
    food.bills.append(ht)

    # Session to talk to the database
    session = Session()
    # Add new record to database
    session.add(ht)
    # Commit it
    session.commit()

    # Get all Bill records
    for instance in session.query(Bill).order_by(Bill.dueDate):
        print "Pay %s the amount of %s on %s" % (instance.payee, instance.amount, instance.dueDate)

    # Get all Categories records
    for instance in session.query(Category).all():
        print "Category: %s" % instance

    # Get all Bills with a category of 'Groceries'
    for instance in session.query(Bill).filter(Bill.category==food):
        print instance
