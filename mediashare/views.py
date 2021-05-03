import os 
from django.shortcuts import render, redirect
from .models import Category, Photo, ShortnerURL, Like, PhotoComment
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .shortner import shortner
from django.core.paginator import Paginator
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.db.models import Count

# Create your views here.
def home(request):


    photos = Photo.objects.annotate(like_count=Count('liked')).order_by('-like_count')[:6]

    category = request.GET.get('category')

    # if category == None:
    #     photos = Photo.objects.all().order_by('-id')
    # else:
    #     photos = Photo.objects.filter(category__name=category).order_by('-id')

    categories = Category.objects.all()

    context = {
        'categories': categories,
        'photos': photos
    }

    return render(request, 'viral_photos.html', context=context)


def gallery(request):

    category = request.GET.get('category')

    if category == None:
        photos = Photo.objects.all().order_by('-id')
    else:
        photos = Photo.objects.filter(category__name=category).order_by('-id')

    categories = Category.objects.all()

    ## pagination of posts
    paginator = Paginator(photos, 12, orphans=2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'photos': photos,
        'paginator_photos':page_obj,
    }
    return render(request, 'index.html', context = context)


def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    comments = PhotoComment.objects.filter(post=photo).order_by('-sno')
    
    if photo.image == '':
        messages.error(request, "Not Found ... Do not show your foolish creativity here you noob ")

    context = {
        'photo': photo,
        'url': settings.DOMAIN_END_POINT +"/img/" + str(photo.token),
        'comments': comments,
    }

    return render(request, 'photo_view.html', context = context)


def like_photo(request):
    user = request.user
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Photo.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)


        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

        data = {
            'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('/')


@login_required
def addPhoto(request):
    categories = Category.objects.all()


    if request.method == 'POST':
        active_user = request.user.id
        data = request.POST
        images = request.FILES.getlist('images')

        try:
            socialaccount_obj = SocialAccount.objects.filter(provider='google', user_id=active_user)[0].extra_data['picture']
            if len(socialaccount_obj) > 0:
                profile_picture = socialaccount_obj
        except :
            profile_picture = "/images/profile/profile.jpg"

        a = shortner().issue_token()

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                logged_user_id=active_user,
                description=data['description'],
                image=image,
                token=a,
                profile_pic=profile_picture,
            )

            shorten_url = ShortnerURL.objects.create(
                long_url = photo.image.url,
                short_url = a,
            )

        return redirect('gallery')

    else:
        return redirect('gallery')


def shortner_target(request, token):
    long_url = ShortnerURL.objects.filter(short_url=token)[0]
    return redirect(long_url.long_url.replace("%20", ' '))


def post_comment(request):
    
    if request.method == 'POST':
        active_user = request.user.id
        comment = request.POST.get('comment')
        user = request.user
        photo_id = request.POST.get('comment_photo_id')

        try:
            socialaccount_obj = SocialAccount.objects.filter(provider='google', user_id=active_user)[0].extra_data['picture']
            if len(socialaccount_obj) > 0:
                profile_picture = socialaccount_obj
        except :
            profile_picture = '/images/profile/profile.jpg'

        photo = Photo.objects.get(id=photo_id)
        comment = PhotoComment(comment=comment, user=user, post=photo, user_pic=profile_picture)
        comment.save()

    return redirect(f'/photo/{photo_id}/'.format(photo_id=str(photo_id)))


