from django.views.generic import TemplateView
from django.shortcuts import render
from .models import article
from .models import author
from .models import category

class IndexView(TemplateView):#Class-based Template View
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(IndexView, self).get_context_data(*args, **kwargs)
		context['post'] = article.objects.all()
		return context
'''def home(request):#Function based View
    post = article.objects.all()
    context = {
        "post":post
    }
    return render(request,'index.html',context)'''


class ProfileView(TemplateView):
    template_name = 'profile.html'

class SingleView(TemplateView):
    template_name = 'single.html'       