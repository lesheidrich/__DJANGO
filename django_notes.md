### SETUP

* ``Set-ExecutionPolicy RemoteSigned`` for permissions if needed
* cmd in project dir: ``python -m venv <myEnv>``
* ``<myEnv>\Scripts\activate``  ||  ``deactivate``
* ``pip install django``  <br><br>
* ``django-admin startproject <project_name>`` cd > project_name
* ``python manage.py startapp <app_name>`` || ``django-admin startapp <app_name>``
* ``python manage.py runserver``


### APPS
**./app_name/views** 
```
def index(request):
    return HttpResponse("<emph>Puppyfarts</emph>")
```

**./Project/settings** 
INSTALLED_APPS > add "app_name"

**.Project/urls** 
```
from <app_name> import views
urlpatterns=url("", views.index, name="index")
```

#### Alternatively: Modular In-App Urls
**./Project/urls**
``path('appTwo/', include("appTwo.urls")), ``

**./app_name/urls** 
```
urlpatterns = [
    path('', views.index, name="index"),
]
```


### TEMPLATES
template tags:
```
{% if user.is_authenticated %}
  <p>You are logged in as {{ user.username }}</p> 
  <!--for simple text-->
{% else %}
  <p>Please log in to access this page.</p>
{% endif %}
```
**./Project/settings** 
* ``TEMPLATE_DIR = BASE_DIR / 'templates'`` after ``BASE_DIR``
* ``TEMPLATES['DIRS'] = [TEMPLATE_DIR],``

**./app_name/views**
```
def index(request):
    my_dict = {
        'insert_me': "Hello I'm from views.py!",
    }
    return render(request, 'appTwo\index.html', context=my_dict)
```

### /static/IMAGES
**./Project/settings**
``STATIC_DIR = BASE_DIR / 'static'`` under ``BASE_DIR``
```
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    STATIC_DIR,
]
```
Template tagging:
``{% load static %}`` under doctype html
``<img src="{% static 'images/pic.jpg' %}" alt="">``

### MODELS
```
class Topic(models.Model):
    top_name = models.CharField(max_length=264, unique=True)

    def __str__(self) -> str:
        return self.top_name
    
class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=264, unique=True)
    url = models.URLField(unique=True)

    def __str__(self) -> str:
        return self.name
    
class AccessRecord(models.Model):
    name = models.ForeignKey(Webpage, on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self) -> str:
        return str(self.date)
```
``python manage.py migrate`` DDL and DML > sqlite
``python manage.py makemigrations <app_name>`` register changes to app
``python manage.py migrate`` migrate again

##### Testing
```
python manage.py shell               # open interactive python console
from <app_name>.models import Topic
print(Topic.objects.all())           # --> <QuerySet []>
t = Topic(top_name="Social Network") 
t.save()
print(Topic.objects.all())           # --> <QuerySet [<Topic: Social Network>]>
quit()
```

##### Admin
**./app_name/admin**
registering with admin interface
``admin.site.register(AccessRecord)`` for all classes in Model

``python manage.py createsuperuser``

#### MTV
```
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')

import django
django.setup()

import random
from first_app.models import AccessRecord, Webpage, Topic
from faker import Faker

fakegen = Faker()
topics = ['Search', 'Social', 'Marketplace', 'News', 'Games']

def add_topic():
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t

def populate(N=5):
    for entry in range(N):
        # get the topic for the entry
        top = add_topic()
        
        # create fake data
        fake_url = fakegen.url()
        fake_date = fakegen.date()
        fake_name = fakegen.name()

        # create webpage entry
        webpg = Webpage.objects.get_or_create(topic=top,url=fake_url,name=fake_name,)[0]

        # create fake access record for webpg
        acc_rec = AccessRecord.objects.get_or_create(name=webpg,date=fake_date)[0]

if __name__ == "__main__":
    print("populating script!")
    populate(20)
    print("populating complete!")

```

**./app_name/views**
```
from .models import AccessRecord, Topic, Webpage

# Create your views here.


def index(request):
    webpages_list = AccessRecord.objects.order_by('date')
    date_dict = {"access_records": webpages_list}

    return render(request, 'first_app/index.html', context=date_dict)
```
**./templates/index.html**
```
<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django</title>
    <link rel="stylesheet" href="{% static 'css/style.css'%}">
</head>
<body>
    <h1>Django Header</h1>
    <h2>Access Records</h2>
    <div class="djangtwo"></div>
        {% if access_records %}
            <table>
                <thead>
                    <th>Site Name</th>
                    <th>Data Accessed</th>
                </thead>

                {% for acc in access_records %}
                <tr>
                    <td>{{ acc.name }}</td>
                    <td>{{ acc.date }}</td>
                </tr>
                {% endfor %}
            </table>

        {% else %}
            <p>NO ACCESS RECORDS FOUND!</p>
        {% endif %}
</body>
</html>
```

### FORMS
*review:*
* project/settings
    * template_dir
    * templates[template_dir]
    * static
    * installed apps


**./app_name/forms.py**
 ```
 from django import forms

class FormName(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
```

**./app_name/views**
```
from django.shortcuts import render
from . import forms

# Create your views here.

def index(request):
    return render(request, 'basicapp/index.html')


def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("Validation Success")
            print(form.cleaned_data['name'])
            print(form.cleaned_data['email'])
            print(form.cleaned_data['text'])

    return render(request, 'basicapp/form_page.html', context={'form': form})

```

**form.html**
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forms</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    <h1>Fill out the form!</h1>

    <div class="container">
        <form action="" method="post">
            {{form.as_p}}   
            {% csrf_token %}
            <input type="submit" class="btn btn_primary" value="Submit">
        </form>

    </div>
</body>
</html>
```

#### Form Validation
Own method - not used
```
class FormName(forms.Form):
    name, email, text, etc..

    # botcheck by honeypot form field
    botcatcher = forms.CharField(required=False,
                                widget=forms.HiddenInput,
                                validators=[validators.MaxLengthValidator(0)])
```

#### Model-Forms
admin, model, urls - same
**./app_name/views**
```
from django.http import HttpResponse
from django.shortcuts import render
from appTwo.forms import NewUserForm

# Create your views here.


def index(request):
    my_dict = {
        'insert_me': "Hello I'm from views.py!",
    }
    return render(request, 'appTwo/index.html', context=my_dict)


def users(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("Error, invalid form!")
    return render(request, 'appTwo/users.html', {'form': form})
```

**html**
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Users</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    <h1>Users</h1>

    <div class="container">
        <h2>Please sign up here!</h2>

        <form action="" method="POST">
            {{form.as_p}}
            {% csrf_token %}
            <input type="submit" class="btn btn-primary" value="Submit">
        </form>
    </div>
</body>
</html>
```

### TEMPLATE TAGS
#### Relative URLs for Template Tags
**./app_name/views**
```
def index(request):
    return render(request, 'basic_app/index.html')

def other(request): 
    return render(request, 'basic_app/other.html')

def relative(request):
    return render(request, 'basic_app/relative_url_templates.html')
```

**./Project/urls**
```
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('basic_app/', include('basic_app.urls'))
]
```

**./app_name/urls**
```
from django.urls import path
from basic_app import views

app_name = 'basic_app'  # actual app name for template tagging

urlpatterns = [
    path('relative/', views.relative, name='relative'),
    path('other/', views.other, name='other'),
]
```

**html**
```
    <a href="{% url 'basic_app:other' %}">OTHER PAGE</a>
    <a href="{% url 'admin:index' %}">ADMIN</a>
    <a href="{% url 'index' %}">HOME</a>
```

### TEMPLATE INHERITANCE
**base.html**
```
<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link rel="stylesheet" href="{% static 'css/style.css' %}"/>

</head>
<body>
    <nav class="navbar navbar-default navbar-static-top">
        <div class="container">
            <ul class="nav navbar-nav">
                <li><a class="navbar-brand" href="{% url "index" %}">BRAND</a></li>
                <li><a class="navbar-link" href="{% url "admin:index" %}">Admin</a></li>
                <li><a class="navbar-link" href="{% url "basic_app:other" %}">Other</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        {% block body_block %}
        {% endblock %}
    </div>
    
</body>
</html>
```

**other.html**
```
<!DOCTYPE html>
{% extends "basic_app/base.html" %}
{% block body_block %}
    <h1>Welcome to other</h1>

    <p>This is an example of template inheritance</p>
{% endblock%}
```

##### Template Filters
* manages context dictionary contet passed to renders context in views
* you're calling existing python built-in methods like string.upper() on the html template tag
``{{ text|upper }}`` make sure there's no space before/after the |  
``{{ number|add:"99" }}``

##### Custom Filters
**./app_name/templatetags/**
* make __init__.py
* make my_extras.py custom filter module
```
from django import template

register = template.Library()

def cut(value, arg):
    """
    This cuts out all values of arg from the string.
    """
    return value.replace(arg, '')

register.filter('cut', cut)  # name to call, function
```
* html
``{{ text|cut:"hello" }}``
* using decorators
```
@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')
```

### MEDIA
```
MEDIA_DIR = Path / 'media'
...after static:
# MEDIA
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
```

### LOGIN
##### Password Authentication
* Built in apps (migrate if you add them)
    ```
    INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    ]
    ```
* `pip install django[argon2]`
* set up hashers
    ```
    # Password validation
    # https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher',        # Recommended for better security
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',  # A good alternative
        'django.contrib.auth.hashers.BCryptPasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',        # Default in Django
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    ]
    ```
* modify built-in password validation settings
    ```
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    ```

#### Registration
hook up forms-model-admin

**./app_name/models**
```
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional classes
    portfolio_site = models.URLField(blank=True)
    # save people's images in ./basic_app/media/profile_pics/
    # DON't FOGET TO INSTALL PILLOW
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self) -> str:
        return self.user.username

```

**./app_name/admin**
```
from django.contrib import admin
from basic_app.models import UserProfileInfo

# Register your models here.


admin.site.register(UserProfileInfo)
```

**./app_name/forms**
```
from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
```

**./app_name/views**
```
from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# Create your views here.


def index(request):
    return render(request, 'basic_app/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request, 'basic_app/registration.html', 
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})
```

**html**
```
{% extends "basic_app/base.html" %}
{% block body_block %}

<div class="jumbotron">
    {% if registered %}
        <h1>Thank you for registering!</h1>
    {% else %}
        <h1>Register here!</h1>
        <p>Fill out the form:</p>
        <form action="" method="post" enctype="multipart/form-data">
            {% csrf_token %}
            {{ user_form.as_p }}
            {{ profile_form.as_p }}
            <input type="submit" value="Register" name="register">
        </form>
    {% endif %}
</div>

{% endblock %}
```

#### Login
**./Project/settings**
after media url
`LOGIN_URL = 'basic_app/user_login'`



***

``pip freeze > requirements.txt``
``pip install -r requirements.txt``
