from django.shortcuts import render
from mediashare.models import Photo
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

# Create your views here.



def user_profile(request, pk):

    user = User.objects.get(id=int(pk))

    user_photos = Photo.objects.filter(logged_user=int(pk)).order_by('-id')

    try:
        socialaccount_obj = SocialAccount.objects.filter(provider='google', user_id=int(pk))[0].extra_data['picture']
        if len(socialaccount_obj) > 0:
            profile_picture = socialaccount_obj
    except :
        profile_picture = "/images/profile/profile.jpg"

    paginator = Paginator(user_photos, 9, orphans=2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user':user,
        'user_photos': user_photos,
        'profile_picture': profile_picture,
        'user_paginator_photos': page_obj
    }

    return render(request, 'users/user_profile.html', context=context)