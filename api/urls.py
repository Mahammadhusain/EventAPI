from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView,EventManagementView,TicketPurchaseView,BulkEventCreateView,SqlQueryEventFetchView

urlpatterns = [

    # Token related urls
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterAPIView.as_view(), name='user-register'), # User Registration
    path('events/', EventManagementView.as_view(), name='events'), # Manage Event (Create and Read)
    path('events/<int:id>/purchase/', TicketPurchaseView.as_view(), name='purchase_ticket'), # Ticket Purchase Logic


    # Optional 
    path('bulk_events_create/', BulkEventCreateView.as_view(), name='bulk-events-create'), # Create 20 random events
    path('top_three_evets_fetch/', SqlQueryEventFetchView.as_view(), name='top-three-evets-fetch'), # SQL query to get top 3 events by total tickets sold

]
