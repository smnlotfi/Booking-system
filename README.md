# Booking-system
This is a booking system application.

Setup
Clone the repository:
git clone git@github.com:smnlotfi/Booking-system.git

Install Python 3.X

Create a virtual environment:
python -m venv venv

Activate the virtual environment:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows


Install dependencies:
pip install -r requirements.txt

Make and run migrations:
python manage.py makemigrations
python manage.py migrate

Run the server:
python manage.py runserver


The API docs will be available at http://127.0.0.1:8000/docs/


