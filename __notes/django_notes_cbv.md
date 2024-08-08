#### ./app_name/views
```
from django.views.generic import View, TemplateView

class IndexView(TemplateView):
    template_name = 'basic_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['write_this_on_html'] = 'your result'
        return context
```

#### ./Project/urls
```
    path('', views.IndexView.as_view())
```

### List and Detail View
Set up School ORM in model

```
class SchoolListView(ListView):
    # complete table
    model = models.School

class SchoolDetailView(DetailView):
    # 
    model = models.School
    template_name = 'basic_app/school_detail.html'  # Point it to the template
```

### CRUD
#### ./app_name/views
```
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

class SchoolCreateView(CreateView):
    # what fields can be created to
    fields = ('name', 'principal', 'location')
    model = models.School

class SchoolUpdateView(UpdateView):
    # what can be updated to
    fields = ('name', 'principal')
    model = models.School

class SchoolDeleteView(DeleteView):
    model = models.School
    # after deleting it go back to the list and show me all the schools
    success_url = reverse_lazy("app_name:list")
```

#### ./app_name/urls
```
urlpatterns = [
    url('create/', views.SchoolCreateView.as_view(), name='create'),
    url('update/<pk>', views.SchoolUpdateView.as_view(), name='update'),
    url('delete/<pk>', views.SchoolDeleteView.as_view(), name='delete')
]
```

#### ./app_name/templates/app_name/schools_form.html
```
{% extends "app_name/app_name_base.html %}
{% block body_block %}
<h1>
    {% if not form.instance.pk %}
        Create School
    {% else %}
        Update School
    {% endif %}    
</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" class="btn btn-primary" value="Submit">
{% end block %}
```

#### ./app_name/templates/app_name/schools_confirm_delete.html
```
{% extends "app_name/app_name_base.html %}
{% block body_block %}
<h1>Are you sure you want to Delete {{ school.name }}?</h1>
<form method="post"> 
    {% csrf_token %}
    <input type="submit" class="btn btn-danger" value"Delete">

<a href="{% url 'app_name:detail' pk=school.pk  %}">Cancel</a>
</form>
{% end block %}
```

#### ./app_name/models
define get_absolute_url for Schools class
```
from django.core.urlresolvers import reverse 

class Schools(models.Model):
    ...
    def get_absolute_url(self):
        return reverse("app_name:detail", kwargs={'pk': self.pk})

class Student...
```

