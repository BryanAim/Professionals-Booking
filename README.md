# Professionals Online booking system

- An online based platform for multiple professional_services. Ability to track, monitor, and share a client's health records between all professional_services. Clients can also see information regarding multiple professional_services and professionals, as well as take appointments via online. Pay laboratory tests via online as well as chat with appointed professionals.

- Django Application

## Tools used:

      1) Front-end: HTML, CSS, Boostrap, Javascript
      2) Back-end: Django (Python web framework)
      3) Database: SQLite
      4) Others: Various APIs, PyPI packages, Ajax

## Features

- **Users:** User, Professional, Service Professional Admin, Client, StoreManager

### User

      1)  Search multiple Profession → Department List → Search for Professionals
      2)  Professional Profile → Book Appointment
      3)  Pay Appointment + Mail Confirmation
      4)  Search all Professionals in all professional_services
      5)  Chat with appointed Professional
      6)  View ServiceRequest, Download ServiceRequest (PDF)
      7)  Choose which tests to pay (Cart System, payment + mail confirmation)
      8)  View Report, Download Report (PDF)
      9)  Give Professional Review
      10) Search for Products in Shop (Store)
      11) Select which medicines to purchase (Cart system), pay total amount for medicines (payment + mail confirmation)

### Professional

      1)  Professional Profile Settings (Add More feature)
      2)  Search multiple Profession → Professional register to professional_service + upload certificate
      3)  (Once registered by admin) accept or reject clients appointment (mail confirmation send to client)
      4)  Search client profile → Create and view ServiceRequest, view report
      5)  Chat with appointed User

### ProfessionalService Admin

      1)  Admin Dashboard
      2)  Accept or reject professional registration (view professional profile to see details)
      3)  CRUD ProfessionalServices (Add more)
      4)  View ProfessionalService List → CRUD Departments within professional_service
      5)  CRUD Technical Specialist
      6)  CRUD StoreManager

### Lab worker

      1)  Technical Specialist Dashboard
      2)  Create Report for client.
      3)  Create Tests for professional_services, View Tests

### StoreManager

      1)  StoreManager Dashboard
      2)  CRUD Medicines
      3)  Search Medicine

## APIs and PyPI packages used:

#### [Django Rest Framework](https://www.django-rest-framework.org/#installation) - toolkit for building web APIs

#### [Django Widget Tweaks](https://pypi.org/project/django-widget-tweaks/) - tweak form field rendering in templates

#### [Pillow](https://pillow.readthedocs.io/en/stable/index.html) - Python imaging library

#### [Mailtrap API](https://mailtrap.io/blog/django-send-email/) - smtp fake testing server

#### [Django Environ](https://django-environ.readthedocs.io/en/latest/) - protecting credentials online (.env file)

#### [SSLCommerz API](https://github.com/sslcommerz/SSLCommerz-Python) - a payment gateway that provides various payment options in Bangladesh (debit card, credit card, mobile banking, etc.)

#### [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html) - configurable set of panels that display various debug information about the current request/response and when clicked

#### [xhtml2pdf](https://xhtml2pdf.readthedocs.io/en/latest/usage.html) - to generate and download pdf documents.

## Installation Details

      1) Create an environment to run django project  (source env/Scripts/activate)
      2) Run app(python manage.py runserver)
      2) Create superuser( python manage.py createsuperuser)
      2) Migrate to create dbsqlite database
      3) Look for .env.example and settings.py files to see what credentials to set up, and then create .env files

      The credentials that you need to set up are: Mailtrap credentials, SSLCommerz Credentials.
