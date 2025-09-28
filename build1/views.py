from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseServerError
from .plots import *
from .apis import *
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.htm')

def index(request):
    plot_html = generate_dashboard_plot()
    context = {'plot_html': plot_html}
    data = get_current_data()
    context.update(data)
    return render(request, 'index.htm', context)

def login_register(request):
    if request.method == "POST":
        if 'login' in request.POST:
            # Handle login process
            username = request.POST.get("Username")
            password = request.POST.get("Password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to index page upon successful login
                return redirect('/index/')  
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('/login/')
        
        elif 'register' in request.POST:
            # Handle registration process
            username = request.POST.get("Username")
            contact = request.POST.get("Contact")
            email = request.POST.get("Email")
            password = request.POST.get("Password")
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('/login/')
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('/login/') 

    return render(request, 'login.htm')

def forecast_page(request):
    return render(request, 'forecast.htm')

def forecast_index(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        period = request.POST.get('period')
        timestamps = request.POST.get('timestamps')
        trend_graph = generate_trend(currency)
        forecast_graph = plot_forecast(currency,period,timestamps)
        #component_graph = plot_components(currency,period,timestamp)
        #context = {'forecast_graph': forecast_graph, 'trend_graph' : trend_graph, 'component_graph':component_graph}
        context = {'forecast_graph': forecast_graph, 'trend_graph' : trend_graph}
        return render(request, 'forecastindex.htm', context)
    else:
        return render(request, 'forecastindex.htm')
    
def analysis_page(request):
    return render(request, 'analysis.htm')

def analysis_index(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        trend_graph = generate_trend_plot(currency)
        volume_graph = generate_volume_plot(currency)
        context = {'trend_graph': trend_graph, 'volume_graph':volume_graph}
        return render(request, 'analysisindex.htm', context)
    else:
        return render(request, 'analysisindex.htm')
    
def news_page(request):
    news_articles = fetch_news()
    return render(request, 'news.htm', {'news_articles': news_articles})