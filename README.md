# Vendor-Manager

Development 👨‍💻 Note : Make sure you have Python version 3.8+

Environment Setup 🚀 $ git clone https://github.com/parv-nangalia/Vendor-Manager.git

If virtualenv is not installed (What is virtualenv!!? You can install different softwares and libraries in a sandboxed environment specific to project.)

$ pip install virtualenv

Create a virtual environment

$ virtualenv venv

Activate the environment everytime you open the project

$ source venv/Scripts/activate

$ cd Vendor-Manager

Install requirements 🛠

$ pip install -r requirements.txt

Run migrations for Database

$ python manage.py makemigrations

$ python manage.py migrate

Create superuser for Admin Login 🔐

$ python manage.py createsuperuser

Enter your desired username, email and password. Make sure you remember them as you'll need them in future.

eg.

Username: admin

Email: admin@admin.com

Password: HighlyConfidentialPassword All Set!

Now you can run the server to see your application up & running 🚀

$ python manage.py runserver

To exit the environment ❎

$ deactivate

Every time you want to open the application in browser, make sure you run:

$ source venv/Scripts/activate
