from django.shortcuts import get_object_or_404, redirect, render

from user.forms import ProfileUpdateForm
from django.contrib import messages
from user.models import Profile, User
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def profile(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.POST:
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()

            messages.success(request, f'Your Account has been Updated')
            return redirect('profile')
        else:
            messages.error(
                request, "Unable to update the account, check the details")
            return redirect('profile')

    p_form = ProfileUpdateForm(instance=request.user.profile)
    profile = get_object_or_404(Profile,user=user)
    context = {
        'form': p_form,
        'title': "Profile",
        'profile' : profile
    }
    return render(request, 'account/profile.html', context=context)
