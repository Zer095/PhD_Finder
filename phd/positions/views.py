from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django import forms
from django.contrib.auth.models import User
from users.forms import CustomUserCreationForm, CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Profile, CustomUser
from users.forms import ProfileForm
from .forms import AddPositionForm
from django.contrib.postgres.fields import ArrayField
# Create your views here.



from .models import Position

# Registration view
def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("positions:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = CustomUserCreationForm()
    return render(request=request, template_name="positions/register.html", context={"register_form": form})

# Login view
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("positions:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="positions/login.html", context={"login_form": form})

# Logout view
@login_required
def logout_request(request):
    logout(request)
    return redirect('positions:index')
        

# Index view
class IndexView(generic.ListView):
    template_name = 'positions/base.html'
    context_object_name = 'latest_position_list'

    def get_queryset(self):
        """Return the last five published positions."""
        return Position.objects.filter(
            pos_pub_date__lte=timezone.now()
        ).order_by('-pos_pub_date')[:3]

# Detail view    
class RegionView(generic.ListView):

    template_name = 'positions/detail.html'
    context_object_name = 'positions_in_region'
    def get_queryset(self):
        """Return the positions filetered by region"""

        return Position.objects.filter(pos_country__contains=[self.kwargs['region']]
        ).order_by('-pos_pub_date')

class LastPositionView(generic.ListView):
    template_name = 'positions/latest.html'
    context_object_name = 'latest_position_all'
    def get_queryset(self):
        """Return the latest position ordered by pub date"""
        return Position.objects.filter().order_by('-pos_pub_date')

# Description view
class DescriptionView(generic.DetailView):
    model = Position
    template_name = 'positions/description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddPositionForm()
        context['saved'] = False

        user_profile = Profile.objects.filter(user=self.request.user).first()
        if user_profile and self.object.id in user_profile.saved:
            context['saved'] = True

        return context

    def post(self, request, *args, **kwargs):
        form = AddPositionForm(request.POST)
        if form.is_valid():
            user_profile = Profile.objects.filter(user=self.request.user).first()
            if not user_profile:
                return HttpResponse('User profile not found')

            position_id = request.POST.get('position_pk')
            if not position_id:
                return HttpResponse('Position not found')
            

            if Profile.objects.all().filter(user=self.request.user).filter(saved__contains=[position_id]):
                print('Position Finded')
                position_id = int(position_id)
                user_profile.saved.remove(position_id)
                user_profile.save()
            else:
                print('Position NOT finded')
                user_profile.saved.append(position_id)
                user_profile.save()

            return HttpResponseRedirect(self.request.path_info)

        return HttpResponse('Form is not valid')

class AddPositionForm(forms.Form):
    pass

# User view
@login_required
def user(request):
    return render(request, 'positions/user.html')


def AboutView(request):
    return render(request, template_name='positions/about.html')