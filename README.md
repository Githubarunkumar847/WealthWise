# WealthWise

WealthWise is a budgeting tool that provides insights into your expenses and income through visualizations. It also includes a developer contact page for feedback and queries.

## Features
- Expense and income tracking with visual charts.
- Developer contact form for queries and feedback.
- Simple and intuitive user interface.

---

## Installation Guide

Follow these steps to set up the project locally:

### Prerequisites
- Python 3.8+
- Virtual environment (`venv`)
- Pip (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/WealthWise.git
   cd WealthWise
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Set up the database:
   ```bash
   python manage.py migrate
5. Run the development server:
   ```bash
   python manage.py runserver
6. Open the application in your browser at:
   ```bash
   http://127.0.0.1:8000/
## How to Use
1. Navigate to the home page to start managing your budget.
2. Use the "Add Expense" or "Add Income" sections to record transactions.
3. View detailed visualizations of your finances.
4. Use the Contact Developer page to send feedback or queries.
