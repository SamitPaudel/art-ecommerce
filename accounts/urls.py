from django.urls import path

from accounts import views
from accounts.views import reset_password

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update_profile/', views.update_profile, name='update_profile'),
    path('dashboard/chat_history/', views.chat_history, name='chat_history'),
    path('dashboard/chat_history/<int:room_id>/', views.chat_detail, name='chat_detail'),
    path('dashboard/submit_portfolio/', views.submit_portfolio, name='submit_portfolio'),
    path('dashboard/upload_artwork/', views.upload_artwork, name='upload_artwork'),
    path('dashboard/view_my_artwork/', views.view_my_artworks, name='view_my_artwork'),
    path('dashboard/edit_artwork/<int:artwork_id>/', views.edit_artwork, name='edit_artwork'),
    path('dashboard/delete_artwork/<int:artwork_id>/', views.delete_artwork, name='delete_artwork'),
    path('start-auction/<int:artwork_id>/', views.start_auction, name='start_auction'),
    path('resetpassword_validate/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
]
