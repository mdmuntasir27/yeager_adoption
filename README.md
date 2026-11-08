# Yeager Adoption

A Django-based pet adoption and rescue platform where users can browse pets available for adoption, submit adoption requests, and manage their applications. Administrators can manage the entire system through the Django admin panel.

## Features

### User Features

**Authentication**
- User registration with email
- Login and logout
- Profile page with adoption history and favorites

**Pet Browsing**
- Browse all available and adopted pets
- View pet name, image, animal type, breed, age, gender, location, description, and adoption status
- Search pets by name, breed, or type
- Filter by animal type, gender, location, and adoption status
- Paginated pet listings (9 per page)

**Pet Details**
- Dedicated detail page for each pet
- Full information display
- Adoption application button (only shown for available pets)

**Adoption Requests**
- Logged-in users can apply to adopt available pets
- Application includes address, phone, reason for adoption, previous pet experience, and optional message
- Dashboard showing all personal adoption requests with their current status

**Favorites**
- Users can save pets to a favorites list
- Toggle favorites directly from the pet list or detail page
- View favorites from the profile page

### Admin Features

Managed entirely through the Django admin panel at `/admin/`

- Add, edit, delete, and manage pets
- Upload pet images
- Change adoption status
- View all adoption requests
- Approve or reject adoption requests
- When an application is approved, the pet's status automatically changes to Adopted

### Business Logic

- Only pets with status "Available" can receive new adoption requests
- A user cannot submit more than one active (Pending or Approved) request for the same pet
- When an adoption request is approved, the pet is automatically marked as Adopted
- Further applications for an adopted pet are blocked

### REST API

Built with Django REST Framework. Base URL: `/api/`

**Pets**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/pets/` | List all pets |
| GET | `/api/pets/<id>/` | Get a specific pet |
| POST | `/api/pets/` | Create a pet (admin only) |
| PUT | `/api/pets/<id>/` | Update a pet (admin only) |
| DELETE | `/api/pets/<id>/` | Delete a pet (admin only) |

Search and filtering:

```
GET /api/pets/?search=golden
GET /api/pets/?animal_type=Dog
GET /api/pets/?gender=Male
GET /api/pets/?status=Available
GET /api/pets/?page=2
```

**Adoptions** (authentication required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/adoptions/` | List your adoption requests |
| POST | `/api/adoptions/` | Submit a new adoption request |
| GET | `/api/adoptions/<id>/` | Get a specific request |
| PUT | `/api/adoptions/<id>/` | Update a request |

**Token Authentication**

```
POST /api/auth/token/
```

Send username and password in the request body. Use the returned token in subsequent requests as a header:

```
Authorization: Token <your-token>
```

## Tech Stack

- Python 3.14
- Django 6.0
- Django REST Framework 3.18
- SQLite (default database)
- Pillow (image handling)
- django-filter (API filtering)

## Installation and Setup

Clone the repository:

```
git clone <repository-url>
cd yeager_adoption
```

Install dependencies:

```
pip install -r requirements.txt
```

Apply database migrations:

```
python manage.py migrate
```

Create a superuser for admin access:

```
python manage.py createsuperuser
```

Start the development server:

```
python manage.py runserver
```

Open your browser and go to `http://127.0.0.1:8000/`

The admin panel is available at `http://127.0.0.1:8000/admin/`

## Project Structure

```
yeager_adoption/
    accounts/           User authentication and profiles
    adoptions/          Adoption requests and forms
    pets/               Pet listings, detail pages, favorites
    yeager_adoption/    Project settings and main URLs
    templates/          HTML templates
    static/             CSS and JavaScript files
    media/              Uploaded pet images
    manage.py
    requirements.txt
    README.md
```

## Currency

All adoption fees are displayed in BDT (Bangladeshi Taka).

## Dark and Light Mode

The UI supports both dark and light themes. The theme preference is saved in the browser and also respects the system preference automatically. Users can toggle between modes using the button in the navigation bar.

## Notes

- Migrations are included in the repository
- The project uses Django's built-in User model for authentication
- Token authentication is available for API consumers
- Pet images are stored in the `media/pets/` directory

