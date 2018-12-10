from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import article
from .models import author
from .models import category

'''class IndexView(TemplateView):#Class-based Template View
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(IndexView, self).get_context_data(*args, **kwargs)
		context['post'] = article.objects.all()
		return context'''
def IndexView(request):#Function based View
    post = article.objects.all()
    context = {
        "post":post
    }
    return render(request,'index.html',context)

def ProfileView(request, name):
    return render(request,'pofile.html')

def SingleView(request, id):
    post = get_object_or_404(article, pk=id)
    first = article.objects.first()
    last = article.objects.last()
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    context = {
        "post":post,
        "first":first,
        "last":last,
        "related":related
    }
    return render(request,'single.html',context)      

def CategoryView(request, name):
    cat=get_object_or_404(category, name=name)
    post=article.objects.filter(category=cat.id)
    return render(request, "category.html",{"post":post, "cat":cat})           