from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
import re  # Regular expression module
from .models import *
from django.db.models import Max
from django.utils import timezone
from django.contrib.auth import logout
# Create your views here.
def myapp(request):
    return render(request, "login_page.html")

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            messages.error(request, 'Both Username and password are required.')
            return redirect('login_page')

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)  # Log the user in
            return redirect('home_page')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password')  # Show error message
            return redirect('login_page')

    return render(request, "login_page.html")

def signup_page1(request):
    if request.method == 'POST':
        email = request.POST['email']

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return redirect('signup_page1')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('signup_page1')
        else:
            request.session['email'] = email
            return redirect('signup_page2')

    return render(request, "signup_page1.html")

def signup_page2(request):
    email = request.session.get('email', '')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return redirect('signup_page2')

        # Validate username criteria
        if not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):
            messages.error(request, 'Username must be alphanumeric and 3-30 characters long.')
            return redirect('signup_page2')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return redirect('signup_page2')

        # Validate password criteria
        errors = validate_password(password)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('signup_page2')

        request.session['username'] = username
        request.session['password'] = password
        return redirect('signup_page3')
    
    return render(request, 'signup_page2.html', {'message': email})

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password):
        errors.append('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        errors.append('Password must contain at least one lowercase letter.')
    if not re.search(r'\d', password):
        errors.append('Password must contain at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('Password must contain at least one special character.')
    return errors

def signup_page3(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        birthdate = request.POST['birthdate']
        email = request.session.get('email', '')
        password = request.session.get('password', '')
        username = request.session.get('username', '')
     
        
        if not email or not password or not username:
            messages.error(request, "Session expired. Please restart the signup process.")
            return redirect('signup_page1')

        # Generate a verification code
        verification_code = str(random.randint(100000, 999999))
        
        # Store the verification code and other details in the session
        request.session['verification_code'] = verification_code
        request.session['fullname'] = fullname
        request.session['birthdate'] = birthdate

        # Send the verification email
        send_mail(
            'Your Verification Code',
            f'Your verification code is {verification_code}.',
            'youremail@gmail.com',  # Replace with your email
            [email],
            fail_silently=False,
        )
        
        return redirect('verification')

    return render(request, "signup_page3.html")

def verification(request):
    # Check if required session data is available
    if 'verification_code' not in request.session or not request.session.get('email', ''):
        messages.error(request, "Verification process not started or session expired.")
        return redirect('signup_page1')

    if request.method == 'POST':
        input_code = request.POST.get('input')
        verification_code = request.session.get('verification_code', '')

        if input_code == verification_code:
            # Retrieve session data
            email = request.session.get('email', '')
            password = request.session.get('password', '')
            username = request.session.get('username', '')
            fullname = request.session.get('fullname', '')
            birthdate = request.session.get('birthdate', '')

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create a Profile instance and save fullname and birthdate
            Profile.objects.create(user=user, fullname=fullname, birthdate=birthdate)

            # Completely clear the session after user creation
            request.session.flush()

            # Log a success message
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login_page')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')
            return redirect('verification')

    # Render the verification page with the email to be verified
    email = request.session.get('email', '')
    return render(request, "verification.html", {'email': email})

def resend_verification(request):
    # Retrieve the email from the session
    email = request.session.get('email', '')

    if email:
        # Generate a new verification code
        verification_code = str(random.randint(100000, 999999))

        # Update the session with the new verification code
        request.session['verification_code'] = verification_code

        # Resend the email
        send_mail(
            'Your New Verification Code',
            f'Your new verification code is {verification_code}.',
            'youremail@gmail.com',  # Replace with your email
            [email],
            fail_silently=False,
        )

        messages.info(request, 'A new verification code has been sent to your email.')
    else:
        messages.info(request, 'Session expired. Please sign up again.')
        return redirect('signup_page1')

    return redirect('verification')

@login_required
def profile_view(request):
    profile_data = get_object_or_404(Profile, user=request.user)
    context = {
        'profile_data': profile_data
    }
    return render(request, 'profile.html', context)

@login_required
def home_page(request):
    return render(request, "home_page.html")


@login_required
def service_selection(request):
    """
    Display available services as cards (at most three).
    """
    services = Service.objects.all()  # Create 3 services from admin
    return render(request, "service_selection.html", {"services": services})

@login_required
def service_detail(request, service_id):
    """
    Display the chosen service with three queues in three columns.
    Also check if the user is already in a queue.
    """
    service = get_object_or_404(Service, pk=service_id)
    queue1 = QueueEntry.objects.filter(service=service, queue_choice=1).order_by('position', 'join_time')
    queue2 = QueueEntry.objects.filter(service=service, queue_choice=2).order_by('position', 'join_time')
    queue3 = QueueEntry.objects.filter(service=service, queue_choice=3).order_by('position', 'join_time')

    try:
        user_entry = QueueEntry.objects.get(service=service, user=request.user)
    except QueueEntry.DoesNotExist:
        user_entry = None

    context = {
        "service": service,
        "queue1": queue1,
        "queue2": queue2,
        "queue3": queue3,
        "user_entry": user_entry,
    }
    return render(request, "service_detail.html", context)

@login_required
def join_queue(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == "POST":
        selected_queue = request.POST.get("queue_choice")
        if not selected_queue:
            messages.error(request, "No queue selected.")
            return redirect('service_detail', service_id=service_id)
        
        try:
            selected_queue = int(selected_queue)
            if selected_queue not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            messages.error(request, "Invalid queue selection.")
            return redirect('service_detail', service_id=service_id)

        max_position = QueueEntry.objects.filter(service=service, queue_choice=selected_queue).aggregate(Max('position'))['position__max'] or 0
        
        try:
            entry = QueueEntry.objects.get(service=service, user=request.user)
            if entry.queue_choice == selected_queue:
                messages.info(request, "You are already in that queue.")
            else:
                entry.queue_choice = selected_queue
                entry.join_time = now()
                entry.position = max_position + 1
                entry.save()
                messages.success(request, "Queue changed successfully.")
                send_email_notification(request.user.email, "Queue Changed", f"You have successfully changed to Queue {selected_queue} for {service.name}.")
        except QueueEntry.DoesNotExist:
            QueueEntry.objects.create(
                service=service,
                user=request.user,
                queue_choice=selected_queue,
                position=max_position + 1
            )
            messages.success(request, "Joined the queue successfully.")
            send_email_notification(request.user.email, "Queue Joined", f"You have successfully joined Queue {selected_queue} for {service.name}.")
        
        return redirect('service_detail', service_id=service_id)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('service_detail', service_id=service_id)

def send_email_notification(to_email, subject, message):
    send_mail(
        subject,
        message,
        'youremail@gmail.com',  # Replace with your sender email
        [to_email],
        fail_silently=False,
    )


@login_required
def leave_queue(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    try:
        entry = QueueEntry.objects.get(service=service, user=request.user)
        entry.delete()
        messages.success(request, "You have left the queue.")
        send_email_notification(request.user.email, "Queue Left", f"You have successfully left the queue for {service.name}.")
    except QueueEntry.DoesNotExist:
        messages.error(request, "You are not in any queue for this service.")
    return redirect('service_detail', service_id=service_id)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login_page')  # Adjust 'login_page' if your login URL has a different name.


from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib import messages

