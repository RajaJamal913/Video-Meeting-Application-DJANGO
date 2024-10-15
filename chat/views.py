from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Meeting  # Ensure this imports your Meeting model
import random  # Import random for meeting code generation
import string 
# Home page view
def index(request):
    return render(request, 'index.html')

# User registration view
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'register.html')

# User login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('dashboard')  # Redirect to the dashboard after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form input.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# Dashboard view
def dashboard_view(request):
    # Generate a random meeting code
    meeting_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Create a new Meeting object
    meeting = Meeting.objects.create(code=meeting_code, created_by=request.user)
    
    return render(request, 'dashboard.html', {
        'meeting_code': meeting_code,
    })

# Video Call View
def video_call_view(request, meeting_code):
    meeting = get_object_or_404(Meeting, code=meeting_code)
    user_name = request.user.username  # Get the logged-in user's username

    # Render the video call template and pass the necessary context
    return render(request, 'video_call.html', {
        'meeting': meeting,
        'name': user_name,  # Pass the username to the template
    })
from django.shortcuts import render, get_object_or_404
from .models import Meeting

def join_meeting_view(request, meeting_code):
    meeting = get_object_or_404(Meeting, code=meeting_code)
    return render(request, 'join_meeting.html', {'meeting': meeting})
