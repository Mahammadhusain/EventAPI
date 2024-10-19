from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,EventSerializer,TicketPurchaseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event
from django.db import connection
from datetime import datetime,timedelta
import random


# JWT token genaration function
def generate_jwt_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return token


# Signup 
class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt_token_for_user(user)
            data = {"username":serializer.data.get('username'),"token":token}

            return Response({"status":True,"data":data,"message":"Create success"}, status=status.HTTP_201_CREATED)
        
        return Response({"status":False,"message":serializer.errors,}, status=status.HTTP_400_BAD_REQUEST)

# Manage Event (Create and Read)
class EventManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all events and use the EventSerializer to return the data
        events = Event.objects.all().order_by('date')
        serializer = EventSerializer(events, many=True)
        return Response({"status":True,"data":serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # Allow only Admins to create events
        if request.user.role != 'Admin':
            return Response({"status":False,"message": "Only Admin can create events."}, status=status.HTTP_403_FORBIDDEN)

        # Use the serializer to validate and save the event data
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"status":True,"message": "Event created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"status":False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TicketPurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializer = TicketPurchaseSerializer(data=request.data, context={'request': request, 'view': self})
        if serializer.is_valid():
            ticket = serializer.save()
            return Response({"status": True, "message": "Ticket purchased successfully.", "ticket_id": ticket.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Extra endpoint for create 20 random events
class BulkEventCreateView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        if request.user.role != 'Admin':
            return Response({"error": "Only Admin can create events."}, status=status.HTTP_403_FORBIDDEN)
        
        events = []
        base_event_names = [
            "Music Concert", "Art Exhibition", "Tech Conference", "Food Festival", 
            "Film Screening", "Theater Play", "Science Fair", "Book Launch", 
            "Fashion Show", "Charity Gala", "Yoga Retreat", "Dance Workshop", 
            "Photography Exhibition", "Startup Pitch", "Comics Festival", 
            "Game Tournament", "Coding Bootcamp", "Culinary Class", 
            "Children's Play", "Holiday Market"
        ]

        # Create 20 unique events
        for i in range(20):
            event_name = f"{base_event_names[i % len(base_event_names)]}"
            event_date = datetime.now() + timedelta(days=random.randint(1, 30))  # Random date within the next 30 days
            total_tickets = random.randint(50, 200)  # Random ticket count

            events.append(Event(name=event_name, date=event_date, total_tickets=total_tickets))

        # Bulk create events
        Event.objects.bulk_create(events)
        return Response({"status":True,"message": "Event created successfully."}, status=status.HTTP_201_CREATED)

# Extra endpoint for SQL query to get top 3 events by total tickets sold
class SqlQueryEventFetchView(APIView):
        
    def get(self, request, *args, **kwargs):
        try:
            
            query = """
                SELECT  
                    e.id, 
                    e.name, 
                    e.date, 
                    e.total_tickets, 
                    e.tickets_sold,
                    COALESCE(SUM(t.quantity), 0) AS total_tickets_sold
                FROM 
                    api_event AS e
                LEFT JOIN 
                    api_ticket AS t
                    ON e.id = t.event_id
                GROUP BY 
                    e.id, e.name, e.date, e.total_tickets
                ORDER BY 
                    total_tickets_sold DESC
                LIMIT 3;
            """
            
            # Execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

            # Format the results into a list of dictionaries
            events = []
            for row in result:
                event = {
                    "id": row[0],
                    "name": row[1],
                    "date": row[2],
                    "total_tickets": row[3],
                    "total_tickets_sold": row[4]
                }
                events.append(event)

            # Return the top 3 events as a JSON response
            return Response({"status":True,"data":events}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors that occur during execution
            return Response({"status":False,"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
