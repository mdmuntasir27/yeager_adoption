# Yeager Adoption

A Django-based pet adoption and rescue platform where users can browse foundation pets available for adoption, submit adoption requests, and post their own pets for rehoming through a community board. Administrators manage the foundation pets and requests through the Django admin panel.

## Features

### User Authentication

- Register with username, full name, email, phone number, and password
- Login and logout
- Profile page with adoption history, community posts, and favorites
- Edit profile including phone number, bio, and location

### Foundation Pet Browsing (Yeager Adoption Managed Pets)

- Browse all foundation pets with name, image, type, breed, age, gender, location, description, and status
- Search by name, breed, or type
- Filter by animal type, gender, location, and adoption status
- Paginated listings (9 per page)
- Favorite pets with one click

### Adoption Requests (Foundation Pets)

- Logged-in users can apply to adopt available foundation pets
- Application includes address, phone, reason, previous pet experience, and optional message
- Dashboard showing all personal adoption requests with status (Pending / Approved / Rejected)

### Community Adoption Board

Users can post their own pets that need rehoming, and other users can browse these community posts and reach out.

**Posting a pet:**
- Post pet name, animal type, breed, age, gender, location, description, and an optional photo
- Posts are visible to all visitors
- Authors can edit, delete, or mark a post as "Given for Adoption"

**Requesting a community pet:**
- Logged-in users can send an adoption request to any open post (not their own)
- Request includes a message, phone number, and address
- One request per user per post

**Managing requests (post author):**
- Authors see all requests on a dedicated inquiries page
- Full contact info is shown: requester phone, email, and address
- Authors can update request status: Pending, Contacted, or Rejected
- Authors can visit a requester's public profile to learn more about them

**Public profiles:**
- Any logged-in user can view another user's public profile
- Shows name, location, bio, phone number, email, and active posts
- Contact info is only visible to logged-in users

**Post lifecycle:**
- Mark a post as "Given for Adoption" to close it without deleting it
- Or delete the post outright (this removes all associated requests too)

### Admin Features

Managed entirely through the Django admin panel at `/admin/`

- Add, edit, delete, and manage foundation pets
- Upload pet images and change adoption status
- View and manage all foundation adoption requests
- Approve or reject requests (approved requests auto-mark the pet as Adopted)
- Manage community posts and inquiries

### Business Logic

- Only foundation pets with status "Available" can receive new adoption requests
- A user cannot submit more than one active (Pending or Approved) request for the same foundation pet
- When a foundation adoption request is approved, the pet is automatically marked as Adopted
- A user cannot submit an inquiry for their own community post
- A user can only submit one inquiry per community post

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

Send username and password in the request body. Use the returned token in subsequent requests:

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

The community board is at `http://127.0.0.1:8000/community/`

## Project Structure

```
yeager_adoption/
    accounts/           User authentication, profiles, and phone numbers
    adoptions/          Foundation pet adoption requests
    community/          Community adoption posts and inquiries
    pets/               Foundation pet listings, detail pages, favorites
    yeager_adoption/    Project settings and main URLs
    templates/          HTML templates
    static/             CSS and JavaScript files
    media/              Uploaded images
    manage.py
    requirements.txt
    README.md
```

## Currency

All adoption fees are displayed in BDT (Bangladeshi Taka).

## Dark and Light Mode

The UI supports both dark and light themes. The preference is saved in the browser and also respects the system preference automatically. Users can toggle between modes using the button in the navigation bar.

## Notes

- Migrations are included in the repository
- The project uses Django's built-in User model extended with a UserProfile model for phone, bio, and location
- Phone numbers collected at registration are shown on public profiles to logged-in users for contact purposes
- Token authentication is available for API consumers
- Pet and community post images are stored in the `media/` directory
