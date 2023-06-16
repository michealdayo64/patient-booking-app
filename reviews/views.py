from django.shortcuts import render, redirect
from .models import Review
from django.contrib import messages
# Create your views here.


def postReview(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        treated_on = request.POST.get('treated_on')
        profile_image = request.FILES.get('profile_image')
        print(profile_image)
        comments = request.POST.get('comments')

        Review.objects.create(firstname = firstname, lastname = lastname, treated_on = treated_on, profile_image = profile_image, comments = comments)
        
        messages.success(request, "Thank you for dropping your review")
        return redirect('index')

    else:
        print("You need to enter a form")
    return render(request, 'review/reviews.html')

