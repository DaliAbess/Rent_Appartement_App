from django.urls import path
from .views import AppartementListCreateView ,AppartementRetrieveUpdateDestroyView ,ReservationCreateView ,VisiteCreateView

urlpatterns = [
    path('appartements/', AppartementListCreateView.as_view()),
    path('appartements/<int:pk>/', AppartementRetrieveUpdateDestroyView.as_view()),
    path('appartements/<int:pk>/reserve', ReservationCreateView.as_view()),
    path('appartements/<int:pk>/visit', VisiteCreateView.as_view()),
]

 