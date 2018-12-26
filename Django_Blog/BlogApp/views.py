from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import article
from .models import author
from .models import category
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import createForm
from django.contrib import messages

'''class IndexView(TemplateView):#Class-based Template View
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(IndexView, self).get_context_data(*args, **kwargs)
		context['post'] = article.objects.all()
		return context'''
def IndexView(request):#Function based View
    post = article.objects.all()
    search = request.GET.get('srch')
    if search:
        post=post.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
        )
    paginator = Paginator(post, 4) # Show 25 post per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        "post":total_article
    }
    return render(request,'index.html',context)

def ProfileView(request, name):
    post_author=get_object_or_404(User, username=name)
    auth=get_object_or_404(author, name=post_author.id)
    post=article.objects.filter(article_author=auth.id)
    context={
        "auth":auth,
        "post":post
    }
    return render(request,'profile.html', context)

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

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password = password)
            if auth is not None:
                login(request,auth)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password Wrong !!')
                return render(request,'login.html')    
    return render(request,'login.html')

def logoutView(request):
    logout(request)
    return redirect('home')

def createView(request):
    if request.user.is_authenticated:
        form = createForm(request.POST or None, request.FILES or None)
        u = get_object_or_404(author, name=request.user.id)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'Article is Created successfully !!')
            return redirect('user')
        return render(request,'create.html',{'form':form}) 
    else:
        return redirect('login') 

def updateView(request, id):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=id)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'Article updated successfully !!')
            return redirect('user')
        return render(request,'create.html',{'form':form}) 
    else:
        return redirect('login') 

def deleteView(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=id)
        post.delete()
        messages.warning(request, 'Article is Deleted')
        return redirect('user')
    else:
        return redirect('login')           

def userView(request):
    if request.user.is_authenticated:
        post = article.objects.filter(article_author=request.user.id)
        profile = get_object_or_404(author, name=request.user.id)
        return render(request,'user.html',{'post':post, 'profile':profile})
    else:
        return redirect('login')     
