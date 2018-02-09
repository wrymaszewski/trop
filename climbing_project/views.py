from django.views.generic import TemplateView, RedirectView

class Homepage(TemplateView):
    template_name = 'index.html'
