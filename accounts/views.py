from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_POST

from accounts.forms import RegistrationForm, UpdateForm, ArtPortfolioForm
from accounts.models import Account, ArtPortfolio
from artist.forms import ArtworkForm
from artist.models import Artist
from carts.models import Cart, CartItem
from carts.views import _cart_id
from store.models import Artwork


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(full_name=full_name, email=email, phone_number=phone_number, username=username, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.save()

            messages.success(request, "Registration Successful.")
            return redirect('register')
    else:
        form = RegistrationForm()

    form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out!")
    return redirect('login')


@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'dashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            current_site = get_current_site(request)
            mail_subject = 'Link for reseting password for forgotten password.'
            message = render_to_string('accounts/forgotton_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset email has been sent to you email address.")
            return redirect('login')
        else:
            messages.error(request, "Account does not exist!")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetpassword.html')


def update_profile(request):
    context = {}
    user = request.user
    form = UpdateForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("home")

    context.update({
        "form": form,
        "user": user,
        "title": "Update Profile"
    })
    return render(request, "accounts/dashboard/update_profile.html", context)


def submit_portfolio(request):
    if request.method == 'POST':
        form = ArtPortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the ArtPortfolio instance
            art_portfolio = form.save(commit=False)
            art_portfolio.artist = request.user
            art_portfolio.save()
            form.save_m2m()
            return redirect('submit_portfolio')
    else:
        form = ArtPortfolioForm()
    return render(request, 'accounts/dashboard/submit_portfolio.html', {'form': form})


@login_required
def upload_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artist = Artist.objects.get(artist_email=request.user)
            artwork.artist_name = artist
            artwork.save()
            messages.success(request, 'Your artwork has been uploaded.')
            return redirect('dashboard')
    else:
        form = ArtworkForm()

    context = {'form': form}
    return render(request, 'accounts/dashboard/upload_artwork.html', context)


@login_required
def view_my_artworks(request):
    artworks = Artwork.objects.filter(artist_name=request.user.artist).order_by('-date_added')
    context = {'artworks': artworks}
    return render(request, 'accounts/dashboard/view_my_artworks.html', context)

@login_required
def edit_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect('view_my_artwork')
    else:
        form = ArtworkForm(instance=artwork)
    return render(request, 'accounts/dashboard/edit_artwork.html', {'form': form, 'artwork': artwork})

@login_required
@require_POST
def delete_artwork(request, artwork_id):
    try:
        artwork = Artwork.objects.get(id=artwork_id, artist_name=request.user)
        artwork.delete()
        return JsonResponse({})
    except Artwork.DoesNotExist:
        return JsonResponse({"error": "Artwork not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)