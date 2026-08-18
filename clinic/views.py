from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Booking, Service


# =========================
# HOME
# =========================

def home(request):
    services = Service.objects.all()[:4]

    return render(
        request,
        'home.html',
        {'services': services}
    )


# =========================
# CATALOG (all services)
# =========================

def catalog_view(request):
    services = Service.objects.all()

    return render(
        request,
        'catalog.html',
        {'services': services}
    )


# =========================
# SIGN UP
# =========================

def signup_view(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(request, f"Welcome to MindBloom Therapy, {user.username}!")

            return redirect('catalog')

    else:

        form = UserCreationForm()

    return render(
        request,
        'accounts/signup.html',
        {'form': form}
    )


# =========================
# LOGIN
# =========================

def login_view(request):

    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            next_url = request.POST.get('next') or request.GET.get('next')

            return redirect(next_url or 'catalog')

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


# =========================
# LOGOUT
# =========================

def logout_view(request):

    logout(request)

    return redirect('home')


# =========================
# BOOKING
# =========================

@login_required
def book(request, service_id):

    service = get_object_or_404(
        Service,
        id=service_id
    )

    if request.method == 'POST':

        phone = (request.POST.get('phone') or '').strip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes', '').strip()
        mode = request.POST.get('mode')

        errors = []

        if not phone:
            errors.append('Please provide a phone number.')

        if not date or not time:
            errors.append('Please choose both a date and a time.')
        else:
            try:
                appt_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                if appt_datetime < datetime.now():
                    errors.append('Please choose a date and time in the future.')
            except ValueError:
                errors.append('Please provide a valid date and time.')

        if mode not in ('in_person', 'virtual'):
            errors.append('Please select a session mode.')

        # Prevent double booking: the therapist can only see one client at a time.
        # A cancelled slot frees back up for someone else.
        if date and time and Booking.objects.filter(
            date=date,
            time=time
        ).exclude(status='Cancelled').exists():
            errors.append('This time slot is already booked. Please choose another time.')

        if errors:
            return render(
                request,
                'booking.html',
                {
                    'service': service,
                    'errors': errors,
                    'form_data': request.POST,
                }
            )

        Booking.objects.create(
            user=request.user,
            service=service,
            phone=phone,
            mode=mode,
            date=date,
            time=time,
            notes=notes,
            price=service.price
        )

        return redirect('booking_success')

    return render(
        request,
        'booking.html',
        {'service': service}
    )


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('service').order_by('-date', '-time')

    return render(
        request,
        'dashboard.html',
        {
            'bookings': bookings
        }
    )


# =========================
# CANCEL BOOKING
# =========================

@login_required
@require_POST
def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if booking.can_cancel:
        booking.status = 'Cancelled'
        booking.save(update_fields=['status'])
        messages.success(request, 'Your session has been cancelled.')
    else:
        messages.error(request, 'This session can no longer be cancelled.')

    return redirect('dashboard')


# =========================
# BOOKING SUCCESS
# =========================

def booking_success(request):

    return render(
        request,
        'booking_success.html'
    )
