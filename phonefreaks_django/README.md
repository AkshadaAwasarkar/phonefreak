# PhoneFreaks - Django Phone Comparison Platform

A Django-based web application for comparing mobile phone prices and specifications with role-based authentication.

## Features

### 🔐 Role-Based Authentication
- **User Login** (`/user-login/`) - Standard user access
- **Admin Login** (`/admin-login/`) - Admin-only access
- Custom role field: `user` or `admin`
- Grant/revoke admin privileges

### 👥 User Management (Admin Only)
- View all users
- Grant admin role to users
- Revoke admin role from users
- Self-protection (cannot modify own role)

### 📱 Phone Management (Admin Only)
- Add new phones with specifications
- Edit existing phone details
- Delete phones
- Manage prices (Amazon & Flipkart)

### 🛍️ User Features
- Browse phone catalog
- Compare phones side-by-side
- Add phones to wishlist
- View detailed specifications

## Tech Stack

- **Backend**: Django 5.2
- **Database**: SQLite
- **Frontend**: HTML, TailwindCSS, JavaScript
- **Icons**: Lucide Icons

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd phonefreaks_django
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: `http://127.0.0.1:8000/`
   - User login: `http://127.0.0.1:8000/user-login/`
   - Admin login: `http://127.0.0.1:8000/admin-login/`
   - Django admin: `http://127.0.0.1:8000/admin/`

## Project Structure

```
phonefreaks_django/
├── core/                      # Main app
│   ├── models.py             # Phone, UserProfile, Review, etc.
│   ├── views.py              # All view functions
│   ├── forms.py              # PhoneForm, AdminLoginForm
│   ├── decorators.py         # @admin_required decorator
│   ├── urls.py               # URL routing
│   └── management/
│       └── commands/
│           └── cleanup_phones.py  # Utility command
├── templates/                # HTML templates
│   ├── base.html            # Base template with navbar
│   ├── admin_base.html      # Admin layout
│   ├── admin_dashboard.html # Phone management
│   ├── manage_users.html    # User role management
│   └── ...
├── phonefreaks_django/       # Project settings
│   ├── settings.py
│   └── urls.py
└── manage.py
```

## User Roles

### Regular Users
- ✅ View phones
- ✅ Compare phones
- ✅ Add to wishlist
- ❌ Cannot access admin features

### Admin Users
- ✅ All user features
- ✅ Add/edit/delete phones
- ✅ Manage user roles
- ✅ Access admin dashboard

## Management Commands

### Clean up invalid phones
```bash
python manage.py cleanup_phones
```

## Security Notes

⚠️ **Before deploying to production:**
1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Set up proper database (PostgreSQL recommended)

## License

This project is for educational purposes.

## Author

Built with Django and ❤️
