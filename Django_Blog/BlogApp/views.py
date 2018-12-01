from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

class SingleView(TemplateView):
    template_name = 'single.html'       