from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm
from django.contrib import messages
from django.views import generic
from positions.models import Position
from .models import Profile
# Create your views here.


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,('Your profile was successfully updated!'))
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, ('Your wishlist was successfully updated!'))
        else:
            messages.error(request,('Unable to complete request'))
        return redirect('users:profile')
    user_form = CustomUserChangeForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    saved = []
    saved_id = request.user.profile.saved
    for id in saved_id:
        saved.append(Position.objects.get(pk=id))
    return render(request=request, template_name='users/profile.html', 
                  context={"user":request.user, "user_form": user_form, "profile_form":profile_form, "saved": saved})


# Detail view to list the saved positions
class SavedView(generic.ListView):

    template_name = 'users/saved.html'
    context_object_name = 'saved_positions'

    def get_queryset(self):
        """Return the positions saved by the user"""
        position = []
        user_profile = Profile.objects.get(user=self.request.user)
        for pos_id in user_profile.saved:
            position.append(Position.objects.get(id = pos_id))
        return position
    
@login_required
def EditProfile(request):
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = CustomUserChangeForm(instance=request.user)
    return render(request=request, template_name='users/prof.html', context={'form': user_form})