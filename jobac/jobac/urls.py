"""jobac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from jobac.Job.views import JobOfferCreate, JobOfferDelete, JobOfferDetail, JobOfferList, JobOfferUpdate, ListEmployersProposals, SubmitProposal

from jobac.User.views import EditProfileView, SignUpEmployerView, SignUpFreelancerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('rest_framework.urls')),
    path('SignUpEmployer/', SignUpEmployerView.site.urls),
    path('SignUpFreelancer/', SignUpFreelancerView.site.urls),
    path('job/', JobOfferList.as_view()),
    path('job/create/', JobOfferCreate.as_view()),
    path('job/<pk>/', JobOfferDetail.as_view()),
    path('job/<pk>/edit/', JobOfferUpdate.as_view()),
    path('job/<pk>/delete/', JobOfferDelete.as_view()),
    path('proposals/', ListEmployersProposals.as_view()),
    path('propose/', SubmitProposal.as_view()),
    path('profile/', EditProfileView.as_view()),
]
