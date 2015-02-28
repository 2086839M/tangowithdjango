from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
	
    category_list = Category.objects.order_by('-likes')[:5]
    view_list = Page.objects.order_by('-views')[:5]
        
    context_dict = {'categories': category_list, 'pages': view_list}
    
    visits = request.session.get('visits')

    if not visits:
	visits = 1
	
    reset_last_visit_time = False
		
    last_visit = request.session.get('last_visit')
    if last_visit:
	last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
	if (datetime.now() - last_visit_time).seconds > 0:
		visits = visits + 1
		reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    response = render(request, 'rango/index.html', context_dict)
        
    return response
                

def about(request):
    context2_dict = {'boldmessage' : "Picture below"}

    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
        
    context2_dict['visits'] = count
    return render(request, 'rango/about.html', context2_dict)

def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
        
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat, 'category_name_slug':category_name_slug}

    return render(request, 'rango/add_page.html', context_dict)
	

		
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

