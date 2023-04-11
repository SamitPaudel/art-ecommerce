from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_POST

from accounts.forms import RegistrationForm, UpdateForm, ArtPortfolioForm
from accounts.models import Account, ArtPortfolio
from artist.forms import ArtworkForm
from artist.models import Artist
from carts.models import Cart, CartItem
from carts.views import _cart_id
from chat.models import ChatRoom
from store.forms import AuctionForm
from store.models import Artwork, Auction


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(full_name=full_name, email=email, phone_number=phone_number,
                                               username=username, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.save()

            messages.success(request, "Registration Successful.")
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    # check if the email is already registered
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            context['email_already_registered'] = 'This email address is already registered.'

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


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out!")
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            current_site = get_current_site(request)
            mail_subject = 'Link for reseting password for forgotten password.'
            message = render_to_string('accounts/forgotton_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
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
    form = UpdateForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            # handle image upload and save to user model
            if request.FILES.get('profileImage'):
                image_file = request.FILES['profileImage']
                fs = FileSystemStorage()
                filename = fs.save(image_file.name, image_file)
                user.profileImage = filename

            form.save()
            return redirect("home")

    context.update({
        "form": form,
        "user": user,
        "title": "Update Profile"
    })
    return render(request, "accounts/dashboard/update_profile.html", context)


def submit_portfolio(request):
    current_portfolio = ArtPortfolio.objects.filter(artist=request.user).first()

    if current_portfolio:
        message = 'Your portfolio is already pending approval'
        return render(request, 'accounts/dashboard/submit_portfolio.html', {'message': message})
    else:
        form = ArtPortfolioForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                # Save the ArtPortfolio instance
                art_portfolio = form.save(commit=False)
                art_portfolio.artist = request.user
                art_portfolio.save()
                form.save_m2m()
                return redirect('submit_portfolio')
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




def delete_artwork(request, artwork_id):
    try:
        artwork = Artwork.objects.get(id=artwork_id)
        artwork.delete()
        messages.success(request, 'Artwork has been deleted successfully.')
    except Artwork.DoesNotExist:
        messages.error(request, 'Artwork not found.')
    except Exception as e:
        messages.error(request, str(e))

    return redirect('edit_delete_artwork_list')


@login_required
def start_auction(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)

    try:
        auction = Auction.objects.get(artwork=artwork)
    except Auction.DoesNotExist:
        auction = None

    if auction:
        if auction.is_active:
            bids = auction.bids.all().order_by('-amount')
            return render(request, 'accounts/dashboard/start_auction.html',
                          {'bids': bids, 'artwork': artwork, 'auction': auction})
        else:
            messages.error(request, 'Auction has already ended for this artwork')
            return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = AuctionForm(request.POST)
            if form.is_valid():
                auction = form.save(commit=False)
                auction.artwork = artwork
                auction.save()
                return redirect('dashboard')
        else:
            form = AuctionForm(initial={'starting_price': artwork.price})
        return render(request, 'accounts/dashboard/start_auction.html', {'form': form, 'artwork': artwork})


def chat_history(request):
    chatrooms = ChatRoom.objects.filter(Q(user=request.user) | Q(artist=request.user.artist))
    for chatroom in chatrooms:
        chatroom.last_message = chatroom.get_last_message()
    context = {'chatrooms': chatrooms}
    return render(request, 'accounts/dashboard/chat_history.html', context)


def chat_detail(request, room_id):
    chatroom = get_object_or_404(ChatRoom, pk=room_id)
    messages = chatroom.messages.order_by('date_sent')
    context = {'chatroom': chatroom, 'messages': messages, 'room_id': room_id, 'current_user_id': request.user.id}
    return render(request, 'accounts/dashboard/chat_details.html', context)


@login_required
def portfolio_list(request):
    portfolios = ArtPortfolio.objects.filter(isApproved=False)
    return render(request, 'accounts/dashboard/portfolio_list.html', {'portfolios': portfolios})


def view_portfolio(request, pk):
    portfolio = get_object_or_404(ArtPortfolio, pk=pk)
    if request.method == 'POST':
        if 'confirm' in request.POST:
            portfolio.isApproved = True
            portfolio.save()
            return redirect('portfolio_list')
        elif 'reject' in request.POST:
            portfolio.delete()
            return redirect('portfolio_list')
    return render(request, 'accounts/dashboard/view_portfolio.html', {'portfolio': portfolio})


def approve_artwork_list(request):
    artworks = Artwork.objects.filter(isApproved=False)
    return render(request, 'accounts/dashboard/approve_artwork_list.html', {'artworks': artworks})

def edit_delete_artworks_admin(request):
    artworks = Artwork.objects.filter(isApproved=True, isAvailable=True).order_by('-date_added')
    return render(request, 'accounts/dashboard/edit_delete_artwork_list.html', {'artworks': artworks})


def artwork_approval_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    if request.method == 'POST':
        if 'approve' in request.POST:
            artwork.isApproved = True
            artwork.isAvailable = True
            artwork.is_verified = True
            artwork.save()
            return redirect('artwork_list')
        elif 'cancel' in request.POST:
            artwork.delete()
            return redirect('artwork_list')
    return render(request, 'accounts/dashboard/artwork_approval_detail.html', {'artwork': artwork})


@login_required
def upload_artwork_admin(request):
    artists = Artist.objects.all()
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist_name = Artist.objects.get(id=request.POST.get('artist_name'))
            artwork.isApproved = True
            artwork.isVerified = True
            artwork.isAvailable = True
            artwork.save()
            messages.success(request, 'Your artwork has been uploaded.')
            return redirect('dashboard')
    else:
        form = ArtworkForm()

    context = {'form': form, 'artists': artists}
    return render(request, 'accounts/dashboard/add_artwork_admin.html', context)