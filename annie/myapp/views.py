# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from forms import SignUpForm,LoginForm,PostForm
from imgurpython import ImgurClient
from annie.settings import BASE_DIR
from datetime import  datetime
from django.contrib.auth.hashers import make_password,check_password
from .models import User,SessionToken,PostModel
# Create your views here.


def signup_view(request):
    today = datetime.now()
    if request.method== "GET":
        form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #hashed_password=make_password(password)
            user=User(email=email,username=username,name=name,password=password)
            user.save()
            return render(request, 'success.html')
    return  render(request,"index.html",{'today':today,'method':request.method,'form':form})


def login_view(request):
    if request.method=='GET':
        form=LoginForm
        return render(request,"login.html",{'method':request.method,'form':form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=User.objects.filter(username=username).first()
            if user:
                session=SessionToken(user=user)
                session.create_token()
                session.save()
                response=redirect("/feed ")
                response.set_cookie(key='session_token', value=session.session_token)
                return response
                if check_password(password, user.password):
                    print 'User is valid'
                else:
                    print 'User is invalid'


def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
      return session.user
  else:
    return None

def feed(request):
    user=check_validation()
    if user:
        posts=PostModel.objects.all().order_by("created on")
        return render(request,'feed.html',{'posts':posts})
    else:
        return redirect("/login")



def post_view(request):
    user = check_validation(request)
    if user:
        print 'Authentic user'
    else:
        return redirect('/login/')
    if request.method == 'GET':
        form = PostForm
        return render(request,'post.html',{'method':request.method,'form':form})
    elif request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
           # image_url=form.cleaned_data.get('image_url')
            post=PostModel(user=user, image=image, caption=caption)
            client = ImgurClient('bd84b67278a7591', 'c483c64ae0633b56919911bac65cd07a37f7eb2d')
            path =str( BASE_DIR +"\\"+ post.image_url)
            post.image_url = client.upload_from_path(path, anon=True)['link']
            post.save()
            return redirect("/feed")


def like_view(request):
user = check_validation(request)
if user and request.method == 'POST':
    form = LikeForm(request.POST)
    if form.is_valid():
        post_id = form.cleaned_data.get('post').id

        existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

        if not existing_like:
            LikeModel.objects.create(post_id=post_id, user=user)
        else:
            existing_like.delete()

        return redirect('/feed/')

else:
    return redirect('/login/')

