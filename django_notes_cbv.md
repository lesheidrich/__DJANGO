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