from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def admin_required(view_func):
    def check_admin(user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'admin'
    
    decorated_view_func = user_passes_test(check_admin, login_url='admin_login')(view_func)
    return decorated_view_func
