from flask import render_template, request, redirect, url_for, jsonify, flash, current_app
from werkzeug.utils import secure_filename
import os
from . import db, utils
from .models import Transaction
from .forms import TransactionForm

UPLOAD_FOLDER = 'app/data'
ALLOWED_EXTENSIONS = {'csv'}

current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import render_template, request, redirect, url_for, flash
from .models import Transaction
from . import db
from .forms import TransactionForm  # Add this if you're using Flask-WTF forms

@current_app.route("/", methods=["GET", "POST"])
def home():
    # Initialize the form (if you're using Flask-WTF or similar)
    form = TransactionForm()

    # Get filter parameters from the request
    date_filter = request.args.get("date")
    category_filter = request.args.get("category")

    # Create a base query to fetch all transactions
    query = Transaction.query
    
    # Apply date filter if present
    if date_filter:
        query = query.filter(Transaction.date == date_filter)

    # Apply category filter if present
    if category_filter:
        query = query.filter(Transaction.category.ilike(f"%{category_filter}%"))

    # Get the filtered transactions
    transactions = query.all()

    # Render the template with the transactions and form
    return render_template("home.html", transactions=transactions, form=form)

@current_app.route("/add", methods=["POST"])
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        date = form.date.data
        category = form.category.data
        amount = form.amount.data
        t_type = form.type.data

        new_transaction = Transaction(date=date, category=category, amount=amount, type=t_type)
        db.session.add(new_transaction)
        db.session.commit()
        flash("Transaction added successfully!", "success")
        return redirect(url_for("home"))
    return render_template("home.html", form=form)

@current_app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "error")
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected", "error")
            return render_template("upload.html")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Clear the current data in the database before adding new records
            Transaction.query.delete()  # This deletes all current records
            db.session.commit()

            # Process the file and add transactions
            records = utils.parse_file(filepath)
            if isinstance(records, str):  # If the records are a string, it's an error message
                flash(f"Error parsing file: {records}", "error")
                return render_template("upload.html")
            
            for record in records:
                new_transaction = Transaction(
                    date=record["Date"],
                    category=record["Category"],
                    amount=record["Amount"],
                    type=record["Type"]
                )
                db.session.add(new_transaction)
            db.session.commit()

            flash("File uploaded and processed successfully. To view the analytics Go to Home", "success")
            return render_template("upload.html")
        else:
            flash("Invalid file format. Only CSV files are allowed.", "error")
            return redirect(request.url)
    return render_template("upload.html")

@current_app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    # Fetch the transaction from the database by its ID
    transaction = Transaction.query.get_or_404(transaction_id)

    # Delete the transaction from the database
    db.session.delete(transaction)
    db.session.commit()

    flash("Transaction deleted successfully!", "success")
    return redirect(url_for("home"))

@current_app.route("/batch-delete", methods=["POST"])
def batch_delete():
    # Retrieve filter criteria for batch deletion
    date_filter = request.form.get("date")
    category_filter = request.form.get("category")

    # Apply filters to the query
    query = Transaction.query
    if date_filter:
        query = query.filter(Transaction.date == date_filter)
    if category_filter:
        query = query.filter(Transaction.category.ilike(f"%{category_filter}%"))

    # Delete the filtered transactions
    deleted_transactions = query.all()
    for transaction in deleted_transactions:
        db.session.delete(transaction)
    db.session.commit()

    flash("Transactions deleted successfully!", "success")
    return redirect(url_for("home"))

@current_app.route("/chart-data")
def chart_data():
    transactions = Transaction.query.all()
    data = {"categories": [], "income": [], "expense": []}
    category_sums = {}

    for t in transactions:
        if t.category not in category_sums:
            category_sums[t.category] = {"Income": 0, "Expense": 0}
        category_sums[t.category][t.type] += t.amount

    for category, sums in category_sums.items():
        data["categories"].append(category)
        data["income"].append(sums["Income"])
        data["expense"].append(sums["Expense"])

    return jsonify(data)

@current_app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Process the data (e.g., save to database)
        print(f"Name: {name}, Email: {email}, Message: {message}")

        # Flash a success message
        flash('Thank you for contacting us! We will get back to you soon.')
        return redirect(url_for('contact'))

    return render_template('contact_developer.html')