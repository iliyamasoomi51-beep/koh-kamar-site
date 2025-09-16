from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import ContactForm
from .models import Contact

@login_required
def contact_page_view(request):
    # Get the logged-in user object
    user = request.user

    # --- This is the key part for auto-filling ---
    # Create a dictionary with the user's data.
    # We use .strip() on the name in case a user only has a first name.
    initial_data = {
        'full_name': f'{user.first_name} {user.last_name}'.strip(),
        'email': user.email,
        # IMPORTANT: The standard User model doesn't have a phone number.
        # You need to adjust the line below to match how you store it.
        # For example, if you have a UserProfile model: 'phone': user.userprofile.phone
        # If it's not available, we'll leave it empty.
        'phone': getattr(user, 'mobile', '')
    }
    # --- End of auto-filling logic ---

    if request.method == 'POST':
        # If the form is submitted, process it with the submitted data
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create a Contact object but don't save it to the database yet
            contact_message = Contact.objects.create(
                contact_fullname=form.cleaned_data['full_name'],
                contact_email=form.cleaned_data['email'],
                contact_phone_number=form.cleaned_data['phone'],
                contact_title=form.cleaned_data['Title'],
                contact_message=form.cleaned_data['message'],
            )

            return redirect('home')
    else:
        # If it's a GET request, create the form instance with the initial_data
        form = ContactForm(initial=initial_data)

    context = {
        'form': form
    }

    return render(request, 'contact_modules/contact_page.html', context)