from rest_framework import serializers
from .models import User,Event,Ticket

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role',]

    def create(self, validated_data):
        role = validated_data.get('role')
        user = User(
            username=validated_data['username'],
            role=validated_data.get('role', 'User'),
            is_active=validated_data.get('is_active', True),
        )
        user.set_password(validated_data['password'])
        if role == 'Admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        user.save()
        return user


class EventSerializer(serializers.ModelSerializer):
    # Adding 'available_ticket_stock' as a read-only field
    available_ticket_stock = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'total_tickets', 'tickets_sold', 'available_ticket_stock']
        # 'available_ticket_stock' is included as a property field


class TicketPurchaseSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        # Validate if user is authenticated
        if not self.context['request'].user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to purchase tickets.")

        # Validate if user role is 'User'
        if self.context['request'].user.role != 'User':
            raise serializers.ValidationError("Only Users can purchase tickets.")

        # Validate if event exists
        id = self.context['view'].kwargs.get('id')
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event not found.")

        # Check if tickets are sold out
        if event.tickets_sold >= event.total_tickets:
            raise serializers.ValidationError("All tickets are sold out for this event.")

        # Validate quantity of tickets requested
        quantity = data.get('quantity', 0)
        remaining_tickets = event.total_tickets - event.tickets_sold

        if quantity <= 0:
            raise serializers.ValidationError("Invalid ticket quantity.")

        if quantity > remaining_tickets:
            raise serializers.ValidationError(f"Only {remaining_tickets} tickets are available.")

        return data

    def create(self, validated_data):
        # Create ticket instance
        id = self.context['view'].kwargs.get('id')
        event = Event.objects.get(id=id)
        quantity = validated_data['quantity']

        # Update tickets sold count
        event.tickets_sold += quantity
        event.save()

        # Create ticket entry
        ticket = Ticket.objects.create(
            user=self.context['request'].user,
            event=event,
            quantity=quantity
        )

        return ticket
