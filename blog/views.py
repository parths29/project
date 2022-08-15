from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from .models import *
import requests
from .tasks import *
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from blog.forms import SignUpForm
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils.crypto import get_random_string


# Create your views here.
def home(request):
    request.session.modified = True
    news_cat = ''
    trending_loaded = cache.get('trending_loaded')
    if request.GET.get('category') is not None:
        news_cat = request.GET.get('category')
        if news_cat != cache.get('news_cat'):
            trending_loaded = requests.get(f'https://inshorts.deta.dev/news?category={news_cat}').json()['data']
            cache.set('trending_loaded', trending_loaded, 600)
            cache.set('news_cat', news_cat, 600)
    if trending_loaded is None:
        trending_loaded = requests.get(f'https://inshorts.deta.dev/news?category={news_cat}').json()['data']
        cache.set('trending_loaded', trending_loaded, 600)
    all_posts = Blog.objects.filter(hidden=False).order_by('id').reverse()
    paginator = Paginator(all_posts, 10, orphans=3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts': posts, 'trending': trending_loaded}
    return render(request, 'index.html', context=context)


def contact(request):
    request.session.modified = True
    return render(request, 'contact.html')


def login_handle(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_email_verified:
                login(request, user)
                return redirect("/")
            else:
                messages.add_message(request, messages.INFO, message='Please verify your email.')
        else:
            messages.add_message(request, messages.ERROR, message="email or password is incorrect. please try again")
    return render(request, 'registration/login.html')


def signup(request):
    request.session.modified = True
    form = SignUpForm()
    if request.method == 'POST':
        try:
            Account.objects.get(username=request.POST.get('username'))
            messages.add_message(request, messages.ERROR, "username already exist, please pick different one.")
        except ObjectDoesNotExist:
            try:
                Account.objects.get(email=request.POST.get('email'))
                messages.add_message(request, messages.ERROR, "email is already in use. please give another one.")
            except ObjectDoesNotExist:
                form = SignUpForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password1 = form.cleaned_data['password']
                    password2 = request.POST.get('password2')
                    email = form.cleaned_data['email']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    gender = request.POST.get('gender')
                    terms_agreed = request.POST.get('terms_agreed')
                    if password1 == password2:
                        user = Account.objects.create_user(username=username, email=email, password=password1)
                        user.termsAgreed = terms_agreed
                        user.gender = gender
                        user.first_name = first_name
                        user.last_name = last_name
                        user.verification_code = get_random_string(18)
                        user.save()
                        send_verification_code(username, user.verification_code, user.email)
                        messages.add_message(request, messages.INFO,
                                             message="Your account has been created successfully. Please verify your "
                                                     "email.")
                        return redirect("/")
                    else:
                        messages.add_message(request, messages.ERROR,
                                             'Password and confirm password does not match. Please try again!')

    context = {'form': form}
    return render(request, 'registration/signup.html', context=context)


@login_required()
def add_post(request):
    request.session.modified = True
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = slugify(title)
        author = Account.objects.get(id=request.POST.get('author'))
        img_file = request.FILES.get('img_file')
        content = request.POST.get('content')
        try:
            cat = Category.objects.get(name=request.POST.get('category'))
        except ObjectDoesNotExist:
            cat = Category.objects.create(name=request.POST.get('category'))
        post = Blog(title=title, slug=slug, author=author, img_file=img_file, content=content, category=cat)
        post.save()
        messages.add_message(request, messages.SUCCESS, message="Post has been added successfully!")
        send_emails.delay(author.id, slug)
        return redirect('/')
    return render(request, 'addpost.html')


def blog_post(request, slug):
    request.session.modified = True
    is_following = False
    post = Blog.objects.get(slug=slug)
    if request.user.is_authenticated:
        post.viewers.add(request.user)
    comments = Comment.objects.filter(post=post)
    replies = Reply.objects.filter(post=post)
    followers_data = list(Subscriber.objects.filter(following_user_id=post.author_id).values("follower_user_id"))
    followers = [i["follower_user_id"] for i in followers_data]
    if request.user.id in followers:
        is_following = True
    context = {'post': post, 'comments': comments, 'replies': replies, 'is_following': is_following}

    return render(request, 'single.html',
                  context=context)


@login_required()
def delete_post(request):
    request.session.modified = True
    if request.method == "GET":
        post_id = request.GET.get('post_id')
        post = Blog.objects.get(id=post_id)
        post.delete()
    return redirect("/")


@login_required()
def hide_post(request):
    request.session.modified = True
    if request.method == "GET":
        post_id = request.GET.get('post_id')
        post = Blog.objects.get(id=post_id)
        post.hidden = True
        post.save()
    return redirect("/")


@login_required()
def un_hide_post(request):
    request.session.modified = True
    post_id = request.GET.get('post_id')
    post = Blog.objects.get(id=post_id)
    post.hidden = False
    post.save()
    return redirect("/")


@login_required()
def edit_post(request):
    request.session.modified = True
    if request.method == 'POST':
        new_title = request.POST['new_title']
        new_content = request.POST['new_content']
        post_id = request.POST.get('post_id')
        post = Blog.objects.get(id=post_id)
        post.title = new_title
        post.slug = slugify(new_title)
        post.content = new_content
        post.last_edit = datetime.now()
        post.save()
        return redirect("/")
    post_id = request.GET.get('post_id')
    selected_post = Blog.objects.get(id=post_id)
    context = {'selected_post': selected_post}
    return render(request, 'editpost.html', context=context)


@login_required()
def post_comment(request):
    request.session.modified = True
    if request.method == 'POST':
        user = Account.objects.get(id=request.POST.get('user_id'))
        post = Blog.objects.get(id=request.POST.get('post_id'))
        comment_text = request.POST['comment_text']
        comment = Comment(user=user, post=post, comment=comment_text)
        comment.save()
        comments = list(Comment.objects.filter(post=post).values())
        return JsonResponse({'comments': comments})


@login_required()
def comment_reply(request):
    request.session.modified = True
    if request.method == 'POST':
        user = Account.objects.get(id=request.POST.get('user_id'))
        post = Blog.objects.get(id=request.POST.get('post_id'))
        comment = Comment.objects.get(id=request.POST.get('comment_id'))
        reply_text = request.POST['reply_text']
        reply = Reply(user=user, post=post, comment=comment, reply=reply_text)
        reply.save()
        replies = list(Reply.objects.filter(post=post).values())
        return JsonResponse({'replies': replies})


def search(request):
    request.session.modified = True
    query = request.GET.get('query')
    matching_title = Blog.objects.filter(title__icontains=query)
    matching_content = Blog.objects.filter(content__icontains=query)
    matching_posts = matching_title.union(matching_content)
    paginator = Paginator(matching_posts, 10, orphans=3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts': posts}
    return render(request, 'search.html', context=context)


def category(request, cat):
    request.session.modified = True
    cat_posts = Blog.objects.filter(category=cat)
    paginator = Paginator(cat_posts, 10, orphans=3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts': posts}
    return render(request, 'category.html', context=context)


def profile(request, username):
    request.session.modified = True
    if request.method == "POST":
        new_f_name = request.POST.get('newFname')
        new_l_name = request.POST.get('newLname')
        new_profession = request.POST.get('newProfession')
        new_city = request.POST.get('newCity')
        new_email = request.POST.get('newEmail')
        new_phone = request.POST.get('newPhone')
        new_address = request.POST.get('newAddress')
        new_dob = request.POST.get('newDOB')
        new_profile_image = request.FILES.get('newProfilePic')
        my_user = Account.objects.get(username=username)
        my_user.first_name = new_f_name
        my_user.last_name = new_l_name
        my_user.profession = new_profession
        my_user.city = new_city
        my_user.email = new_email
        my_user.phone = new_phone
        my_user.address = new_address
        if new_dob != "":
            my_user.dob = new_dob
        if len(request.FILES) != 0:
            my_user.profile_image = new_profile_image
        my_user.save()
        messages.add_message(request, messages.SUCCESS, "Your profile has been updated successfully. Enjoy!")
        return redirect(f"/profile/{username}")
    my_user = Account.objects.get(username=username)
    posts = Blog.objects.filter(author_id=my_user.id)
    count = posts.count()
    context = {'count': count, 'req_user': my_user, 'posts': posts}
    return render(request, 'profile.html', context=context)


@login_required()
def subscribe(request):
    request.session.modified = True
    is_following = False
    if request.method == "POST":
        post_id = request.POST['post_id']
        post = Blog.objects.get(id=post_id)
        follower_id = request.POST.get('user_id')
        following_id = request.POST.get('author_id')
        follower_user_id = Account.objects.get(id=follower_id)
        following_user_id = Account.objects.get(id=following_id)
        if following_user_id != follower_user_id:
            subscriber = Subscriber(following_user_id=following_user_id, follower_user_id=follower_user_id)
            subscriber.save()

        followers_data = list(Subscriber.objects.filter(following_user_id=post.author_id).values("follower_user_id"))
        followers = [i["follower_user_id"] for i in followers_data]
        if request.user.id in followers:
            is_following = True
        return JsonResponse({'is_following': is_following})


@login_required()
def unsubscribe(request):
    request.session.modified = True
    is_following = True
    if request.method == "POST":
        follower_id = request.POST.get('user_id')
        following_id = request.POST.get('author_id')
        follower_user_id = Account.objects.get(id=follower_id)
        following_user_id = Account.objects.get(id=following_id)
        if following_user_id != follower_user_id:
            subscriber = Subscriber.objects.get(following_user_id=following_user_id, follower_user_id=follower_user_id)
            subscriber.delete()
            is_following = False
    return JsonResponse({'is_following': is_following})


def verify_email(request, username, verification_code):
    user = Account.objects.get(username=username)
    if user.verification_code == verification_code:
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             message="Your email has been verified successfully.Please login to your account.")
    return redirect('/login')


def forgot_password(request):
    if request.GET.get('email') is not None:
        if request.method == 'GET':
            try:
                user = Account.objects.get(email=request.GET.get('email'))
                user.password_reset_code = get_random_string(18)
                user.save()
                send_password_reset_link(username=user.username, email=user.email,
                                         password_reset_code=user.password_reset_code)
                messages.add_message(request, messages.INFO,
                                     message="Password reset link has been sent to your registered email address. "
                                             "Please verify")
                return redirect('/login')
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, message="Account does not exist.")
    return render(request, 'registration/forgot_password.html')


def reset_password(request, username, password_reset_code):
    user = Account.objects.get(username=username)
    if user.password_reset_code == password_reset_code:
        return render(request, 'registration/change_password.html')
    else:
        messages.add_message(request, messages.ERROR,
                             message='Password reset code is wrong or expired. Please try again.')
        return redirect('/')


@login_required()
def change_password(request):
    user = Account.objects.get(username=request.user.username)
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        if password1 == password2:
            user.set_password(password2)
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 message='Your password has been changed successfully. Please login again')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR,
                                 message="Password and confirm password are not same. Please try again")
    return render(request, 'registration/change_password.html')
