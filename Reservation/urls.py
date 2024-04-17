from django.urls import path
from .views import AppartementListCreateView ,AppartementRetrieveUpdateDestroyView

urlpatterns = [
    path('appartements/', AppartementListCreateView.as_view()),
    path('appartements/<int:pk>/', AppartementRetrieveUpdateDestroyView.as_view()),
]