from django.urls import include, path
from .views import  ProposalViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'proposals', ProposalViewset, basename='proposal')

urlpatterns = [
    path('', include(router.urls)),
]