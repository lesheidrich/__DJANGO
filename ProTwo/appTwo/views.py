"""
appTwo views
"""

from django.http import HttpResponse
from django.shortcuts import render
from appTwo.forms import NewUserForm

# Create your views here.


def index(request):
    # return HttpResponse("<emph>Puppyfarts</emph>")
    my_dict = {
        'insert_me': "Hello I'm from views.py!",
    }
    return render(request, 'appTwo/index.html', context=my_dict)

def help(request):
    man = {
        'help_insert': "bar",
    }
    return render(request, 'appTwo/help.html', context=man)

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

# def users(request):
#     user_list = User.objects.order_by('first_name')
#     user_dict = {
#         "user_records": user_list,
#     }
#     return render(request, 'appTwo/users.html', context=user_dict)