# Yeager Adoption

A Django web application where users can browse foundation pets available for adoption, submit adoption requests, and post their own pets through a community rehoming board. Foundation pets and incoming requests are managed through the Django admin interface.

## Overview

The platform contains two types of adoption listings:

1. Foundation Pets: Official pets managed by Yeager Adoption that appear on the homepage and the main Browse Pets page.
2. Community Posts: Rehoming posts created by registered users on the community board.

## How to Add Foundation Pets (Homepage Listings)

Foundation pets displayed on the homepage and Browse Pets page are added through the Django admin site.

### Step 1: Create or promote an admin account

Run the following command to create a superuser:

```bash
python manage.py createsuperuser
```

Enter your username, email address, and password.

If you already have a registered account and want to grant it admin access, run:

```bash
python manage.py shell
```

Then execute:

```python
from django.contrib.auth.models import User
user = User.objects.get(username="your_username")
user.is_staff = True
user.is_superuser = True
user.save()
exit()
```

### Step 2: Add pets in Django Admin

1. Start the server with `python manage.py runserver`.
2. Open your browser and navigate to `http://127.0.0.1:8000/admin/`.
3. Log in with your admin credentials.
4. Locate the Pets section and click Add Pet.
5. Provide the pet details:
   * Name
   * Animal type (Dog, Cat, Bird, Rabbit, Other)
   * Breed
   * Age in years
   * Gender (Male, Female)
   * Location
   * Description
   * Image file (optional)
   * Status (Available, Adopted)
6. Click Save.

The new pet will appear immediately on the homepage at `http://127.0.0.1:8000/` and under Browse Pets at `http://127.0.0.1:8000/pets/`.

Foundation pets can also be created programmatically via the REST API endpoint `POST /api/pets/` by authenticating with an admin user token.

## Features

### Authentication

* Registration requires username, full name, email, phone number, and password.
* Login and logout handling with session cookies.
* User profile page displaying foundation adoption requests, community posts, and favorite pets.
* Profile edit page allowing users to update phone number, location, bio, and name.

### Foundation Pet Browsing

* Listings show pet name, image, type, breed, age, gender, location, description, and adoption status.
* Search by name, breed, or animal type.
* Filter by animal type, gender, location, and status.
* Pagination set to 9 pets per page.
* One-click favorite button with asynchronous saving.

### Foundation Adoption Requests

* Logged in users can submit an application for any available pet.
* Application fields: phone, address, reason for adoption, previous pet experience, optional message.
* Dashboard at `/adoptions/my-requests/` tracks application status.
* Rule 1: Adopted pets cannot receive new requests.
* Rule 2: A user cannot submit multiple active requests for the same pet.
* Rule 3: When an admin marks an application as Approved in Django Admin, the pet status automatically switches to Adopted and subsequent requests are blocked.

### Community Adoption Board

* Located at `/community/`.
* Any registered user can publish a post for a pet needing a new home.
* Post fields include name, animal type, breed, age, gender, location, description, and an optional photo.
* Other users can send an adoption inquiry with their phone number, address, and message.
* Post authors receive inquiries on a dedicated page with full contact details to get in touch.
* Post authors can update inquiry status to Pending, Contacted, or Rejected.
* Post authors can visit the applicant profile to view their information.
* Authors can mark their post as Given for Adoption or delete the post completely.
* Public profile page for every user at `/community/user/<username>/`.

### REST API

The application provides a REST API built with Django REST Framework under `/api/`.

Pets endpoints:
* GET `/api/pets/` (List all pets, supports search and filtering)
* GET `/api/pets/<id>/` (Pet detail)
* POST `/api/pets/` (Create pet, admin only)
* PUT `/api/pets/<id>/` (Update pet, admin only)
* DELETE `/api/pets/<id>/` (Delete pet, admin only)

Adoption request endpoints:
* GET `/api/adoptions/` (List requests submitted by the authenticated user)
* POST `/api/adoptions/` (Submit new adoption request)
* GET `/api/adoptions/<id>/` (View request detail)
* PUT `/api/adoptions/<id>/` (Update request)

Authentication endpoint:
* POST `/api/auth/token/` (Submit username and password to obtain an authentication token)

## Technology Stack

* Python 3.14
* Django 6.0
* Django REST Framework 3.18
* SQLite database
* Pillow for image processing
* django-filter for API query filtering

## Setup Instructions

1. Clone or download the repository to your machine.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```bash
   python manage.py migrate
   ```
4. Create an administrator account:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
6. Access the site:
   * Main website: `http://127.0.0.1:8000/`
   * Community board: `http://127.0.0.1:8000/community/`
   * Django admin: `http://127.0.0.1:8000/admin/`
   * REST API root: `http://127.0.0.1:8000/api/`

## Project Structure

* `accounts/`: User registration, profile views, and profile models.
* `pets/`: Foundation pet models, pet browsing views, search, and favorites.
* `adoptions/`: Foundation adoption request handling and dashboard.
* `community/`: User-submitted pet posts, adoption inquiries, and public profiles.
* `yeager_adoption/`: Project settings, root URL configuration, WSGI/ASGI handlers.
* `templates/`: HTML templates for all apps.
* `static/`: CSS stylesheet and JavaScript scripts.
* `media/`: User-uploaded pet and post photos.

## Currency

All adoption fees across the foundation listings are indicated in BDT (Bangladeshi Taka).

## Theme Support

The application includes light and dark display modes. Users can toggle modes using the button in the top navigation bar. Preferences persist in the browser and default to the operating system setting.
