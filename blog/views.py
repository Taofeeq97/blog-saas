from django.shortcuts import render, get_object_or_404
from .models import Profile, Tag, Article
from .forms import TenantCreationForm, UserCreateForm, LoginForm
from tenant.models import Tenant, Domain
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from customers.models import Tenant  # Import your Tenant model
from .forms import TenantCreationForm  # Import your TenantCreationForm
from django.shortcuts import render, redirect


@login_required(login_url='blog:login')
def home(request):
    # feature articles on the home page
    featured = Article.articlemanager.filter(featured=True)[0:3]
    print('tenant',request.tenant)

    context = {
        'articles': featured
    }
    print(request.user)
    print(Article.objects.all())
    return render(request, 'index.html', context)


def articles(request):

    # get query from request
    query = request.GET.get('query')
    # print(query)
    # Set query to '' if None
    if query == None:
        query = ''

    # articles = Article.articlemanager.all()
    # search for query in headline, sub headline, body
    articles = Article.articlemanager.filter(
        Q(headline__icontains=query) |
        Q(sub_headline__icontains=query) |
        Q(body__icontains=query)
    )

    tags = Tag.objects.all()

    context = {
        'articles': articles,
        'tags': tags,
    }

    return render(request, 'articles.html', context)


def article(request, article):

    article = get_object_or_404(Article, slug=article, status='published')

    context = {
        'article': article
    }

    return render(request, 'article.html', context)


def create_tenant(request):
    form = TenantCreationForm()

    if request.method == 'POST':
        form = TenantCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            blog_name = form.cleaned_data['blog_name']
            subdomain_name = form.cleaned_data['domain_name']
            password = form.cleaned_data['password']

            superuser = User.objects.create_superuser(
                username=username,
                password=password,
                email=f"{username}@{subdomain_name}.example.com"
            )

            tenant = Tenant(schema_name=subdomain_name,
                            blog_name=blog_name,
                            user = superuser
                            )
            tenant.save()

            # Add one or more domains for the tenant
            domain = Domain()
            domain.domain = subdomain_name+'.localhost'
            domain.tenant = tenant
            domain.is_primary = True
            domain.save()

            # Create a superuser for the tenant
            # superuser = User.objects.create_superuser(
            #     username=username,
            #     password=password,
            #     email=f"{username}@{subdomain_name}.example.com"
            # )

    return render(request, 'create_tenant.html', {'form': form})


def register_user(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create_user(email=email, username=email)
            user.set_password(password=password)
            user.save()
    return render(request, 'createuser.html')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('blog:home')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
