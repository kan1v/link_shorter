from django.shortcuts import redirect
from functools import wraps

def plan_required(required_plans):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.public_profile.plan not in required_plans:
                return redirect("upgrade_plan")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator