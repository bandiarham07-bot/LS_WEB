from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view()),
    path('progress/', views.UpdateProgressView.as_view()),
    path('pages/<str:section>/', views.SectionPagesView.as_view()),
    path('page/<uuid:id>/', views.PageDetailView.as_view()),
    path('assignments/<uuid:assignment_id>/submit/', views.AssignmentSubmitView.as_view()),
]
