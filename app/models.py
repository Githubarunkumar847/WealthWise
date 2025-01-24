from . import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    category = db.Column(db.String(100))
    amount = db.Column(db.Float)
    type = db.Column(db.String(10))  # 'Income' or 'Expense'

    def __repr__(self):
        return f'<Transaction {self.id} - {self.date} - {self.category} - {self.amount}>'
