from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from .models import article
from .models import author
from .models import category
from .models import Comment
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import createForm, registrationForm, authorForm, CommentForm, createTopicsForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token

'''class IndexView(TemplateView):#Class-based Template View
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(IndexView, self).get_context_data(*args, **kwargs)
		context['post'] = article.objects.all()
		return context'''
def IndexView(request):# Function based View
    post = article.objects.all()
    search = request.GET.get('srch')
    if search:
        post=post.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
        )
    paginator = Paginator(post, 9) # Show 25 post per page
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
    get_comment = Comment.objects.filter(post=id)
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    form = CommentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.post = post
        instance.save()
    context = {
        "post":post,
        "first":first,
        "last":last,
        "related":related,
        "form":form,
        "comment":get_comment,
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
        profile = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=profile.id)
        if author_profile:
            authorUser = get_object_or_404(author,name=request.user.id)
            post = article.objects.filter(article_author=authorUser.id)
            return render(request,'user.html',{'post':post, 'profile':authorUser})
        else:
            form=authorForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = profile
                instance.save()
                return redirect('user')
            return render(request,'author_form.html',{"form":form})
    else:
        return redirect('login')  


def registerView(request):
    form = registrationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_active = False
        instance.save()
        site = get_current_site(request)
        mail_subject = "Confirmation message for blog"
        message = render_to_string("confirm_message.html",{
            'user': instance,
            'domain': site.domain,
            'uid': instance.id,
            'token': activation_token.make_token(instance)
            })
        to_email = form.cleaned_data.get('email')
        to_list = [to_email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
        return HttpResponse('<h1>A Confirmation email has sent</h1>')
    return render(request,'register.html',{"form":form})  

def topicsView(request):
    query = category.objects.all()
    return render(request,'topics.html',{"topic":query})

def createTopicsView(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form =  createTopicsForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('topics')
            return render(request,'createTopics.html',{"form":form})
        else:
            raise Http404('Permision denied !!') 
    else:
        return redirect('login')  

def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except:
        raise Http404("No user found")
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("<h1>Account is activated. Now you can <a href='/login'>login</a></h1>")
    else:
        return HttpResponse("<h3>Invalid activation link</h3>")        
