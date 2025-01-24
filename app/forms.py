from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class TransactionForm(FlaskForm):
    date = StringField("Date", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    amount = FloatField("Amount", validators=[DataRequired()])
    type = SelectField("Type", choices=[("Income", "Income"), ("Expense", "Expense")], validators=[DataRequired()])
    submit = SubmitField("Add Transaction")
