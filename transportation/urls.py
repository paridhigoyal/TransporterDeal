from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add-vehicle/', views.add_vehicle, name='add-vehicle'),
    path('vehicles/', views.vehicle_list, name='vehicle-list'),
    path('create-deal/', views.create_deal, name='create-deal'),
    path('edit-profile/<int:id>', views.update_profile, name ='edit-profile'),
    path('edit-vehicle/<int:id>', views.update_vehicle, name ='edit-vehicle'),
    path('delete-vehicle/<int:id>', views.delete_vehicle, name='delete-vehicle'),
    path('deals/', views.deal_list, name='deal-list'),
    path('edit-deal/<int:deal_id>', views.edit_deal, name='edit-deal'),
    path('delete-deal/<int:deal_id>', views.delete_deal, name='delete-deal'),
    path('view-deal/<int:deal_id>', views.view_deal, name='view-deal'),
    path('view-image/<int:id>', views.view_image, name='view-image'),
    path('ask-query/<int:deal_id>', views.ask_query, name='ask-query'),
    path('view-query/<int:deal_id>', views.view_query, name='view-query'),
    path('response-query/<int:request_id>', views.response_query, name='response-query'),
    path('view-response/<int:request_id>', views.view_response, name='view-response'),
    path('give-rating/<int:deal_id>', views.give_rating, name='give-rating'),
    path('view-rating/<int:deal_id>', views.view_rating, name='view-rating'),
    ]
