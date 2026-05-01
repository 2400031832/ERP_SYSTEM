from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser


def login_view(request):
    """Handle user login with role selection"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', 'student').lower()
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            # Verify role matches
            role_map = {
                'student': 'student',
                'faculty': 'teacher',
                'teacher': 'teacher',
                'admin': 'admin',
                'administrator': 'administrator',
            }
            expected_role = role_map.get(role, 'student')
            
            if user.role == expected_role:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, f'This account is not a {role} account')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


def register_view(request):
    """Handle user registration with role-based forms"""
    selected_role = _get_selected_role(request)
    
    if request.method == 'POST':
        try:
            role = _get_selected_role(request)
            password = request.POST.get('password')
            password_confirm = request.POST.get('password2')
            
            # Validate passwords match
            if password != password_confirm:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'register.html', _get_registration_context(role))
            
            # Get or create username
            username = request.POST.get('username') or request.POST.get('registration_number')
            if not username:
                messages.error(request, 'Username or Registration Number is required!')
                return render(request, 'register.html', _get_registration_context(role))
            
            # Check if username already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'This username is already registered!')
                return render(request, 'register.html', _get_registration_context(role))
            
            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                email=request.POST.get('email'),
                password=password,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                role=role,
                phone=request.POST.get('phone', '')
            )
            
            # Create role-specific profile if student
            if role == 'student':
                from students.models import Student
                Student.objects.create(
                    user=user,
                    roll_number=request.POST.get('roll_number') or username,
                    registration_number=request.POST.get('registration_number') or username,
                    date_of_birth=request.POST.get('date_of_birth', None),
                    phone=request.POST.get('phone', ''),
                    address=request.POST.get('address', ''),
                    department=request.POST.get('department', ''),
                    year=request.POST.get('year') or 0,
                    semester=request.POST.get('semester') or 0
                )
            
            messages.success(
                request, 
                f'{_get_role_config(role)["title"]} created successfully! Please login with your credentials.'
            )
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Registration error: {str(e)}')
    
    return render(request, 'register.html', _get_registration_context(selected_role))


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')


@login_required
def profile_view(request):
    """Show the logged-in user's profile details."""
    student = None
    if getattr(request.user, 'role', '') == 'student':
        try:
            from students.models import Student
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None

    return render(request, 'profile.html', {
        'profile_user': request.user,
        'student': student,
    })


def _get_selected_role(request):
    """Extract and normalize the selected role from request"""
    raw_role = (request.POST.get('role') or request.GET.get('role') or 'student').strip().lower()
    
    role_map = {
        'student': 'student',
        'faculty': 'teacher',
        'teacher': 'teacher',
        'admin': 'admin',
        'administrator': 'administrator',
    }
    
    return role_map.get(raw_role, 'student')


def _get_role_config(role):
    """Get configuration for a specific role"""
    roles = {
        'student': {
            'title': 'Student Sign Up',
            'subtitle': 'Create your student account for the ERP system',
            'submit_label': 'Create Student Account',
            'show_student_fields': True,
        },
        'teacher': {
            'title': 'Faculty Sign Up',
            'subtitle': 'Create your faculty account for the ERP system',
            'submit_label': 'Create Faculty Account',
            'show_student_fields': False,
        },
        'admin': {
            'title': 'Admin Sign Up',
            'subtitle': 'Create an admin account for the ERP system',
            'submit_label': 'Create Admin Account',
            'show_student_fields': False,
        },
        'administrator': {
            'title': 'Administrator Sign Up',
            'subtitle': 'Create an administrator account for the ERP system',
            'submit_label': 'Create Administrator Account',
            'show_student_fields': False,
        },
    }
    return roles.get(role, roles['student'])


def _get_registration_context(role):
    """Build context dictionary for registration template"""
    config = _get_role_config(role)
    return {
        'selected_role': role,
        'title': config['title'],
        'subtitle': config['subtitle'],
        'submit_label': config['submit_label'],
        'show_student_fields': config['show_student_fields'],
    }
