from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.template.defaulttags import register

from .models import User, Review
from .utils import user_logged_in

# Create your views here.


def index(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'sign-up.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password-confirmation']
        errors = False

        if password != password_confirmation:
            errors = True
            messages.error(request, 'Passwords do not match')

        # try:
        #     validate_password(password, User(username=username))
        # except ValidationError as error_list:
        #     errors = True
        #     for error in error_list:
        #         messages.error(request, error)

        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            errors = True
            messages.error(request, 'Username already exists')

        if errors:
            return render(request, 'sign-up.html', {'username': username, 'password': password, 'password_confirmation': password_confirmation})

        # password = make_password(password, hasher='default')
        user = User(username=username, password=password)
        user.save()
        request.session['user'] = username
        messages.success(request, f'Account was created successfully! You are now logged in as {username}')
        return redirect('/')


def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.raw(f'SELECT * FROM pages_user WHERE username = "{username}" AND password = "{password}" LIMIT 1')
        # user = User.objects.filter(username=username).first()
        # if not user or not check_password(password, user.password):
        if not user:
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'login.html', {'username': username, 'password': password})
        request.session['user'] = username
        messages.success(request, f'You are now logged in as {username}')
        return redirect('/')


def log_out(request):
    del request.session['user']
    messages.success(request, 'You have been logged out.')
    return redirect('/')


def reviews(request):
    if not user_logged_in(request, 'You must be logged in to read reviews'):
        return redirect('/login')

    latest_reviews = Review.objects.all().order_by('updated_at').reverse()
    return render(request, 'reviews.html', {'reviews': latest_reviews})


def new_review(request):
    if not user_logged_in(request, 'You must be logged in to create a review'):
        return redirect('/login')
    if request.method == 'GET':
        return render(request, 'new-review.html')
    if request.method == 'POST':
        book_title = request.POST['title']
        book_author = request.POST['author']
        rating = int(request.POST['rating'])
        review_text = request.POST['review']
        user = User.objects.filter(username=request.session['user']).first()
        review = Review(book_title=book_title, book_author=book_author, rating=rating, review_text=review_text, user=user)
        review.save()
        messages.success(request, 'Review was created successfully!')
        return redirect('/reviews')


def edit_review(request, id):
    if not user_logged_in(request, 'You must be logged in to edit a review'):
        return redirect('/login')
    review = Review.objects.filter(id=id).first()
    if not review:
        messages.error(request, 'Review does not exist')
        return redirect('/reviews')
    # if not request.session['user'] == review.user.username:
    #     messages.error(request, 'You can only edit your own reviews')
    #     return redirect('/reviews')
    if request.method == 'GET':
        return render(request, 'edit-review.html', {'id': id, 'review': review})
    if request.method == 'POST':
        review.book_title = request.POST['title']
        review.book_author = request.POST['author']
        review.rating = int(request.POST['rating'])
        review.review_text = request.POST['review']
        review.save()
        messages.success(request, 'Review was updated successfully!')
        return redirect('/reviews')


@register.filter
def get_range(value):
    return range(1, value + 1)


@register.filter
def equalto(value, arg):
    return str(value) == arg
