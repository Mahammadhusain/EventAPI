# EventAPI

EventAPI is a Django-based API that allows users to register, manage events, and purchase tickets. It is built using Django REST Framework, PostgreSQL, and JWT for secure authentication.

## Features

- **User Registration**: Register users using JWT-based authentication
- **Event Management**: Create, manage, and view events
- **Ticket Purchase**: Purchase tickets for specific events
- **Bulk Event Creation**: Create 20 random events for testing purposes
- **Top Events Retrieval**: Fetch the top 3 events based on total tickets sold

## Technologies Used

- Python (3.12.7)
- Django (5.1.2)
- Django REST Framework (DRF 3.15.2)
- PostgreSQL(17.0.1)
- JWT Authentication

## Prerequisites

Ensure you have the following installed on your machine:
- Python (3.12.7)
- PostgreSQL(17.0.1)
- Git

## Installation

### 1. Clone the Project
```bash
git clone https://github.com/Mahammadhusain/EventAPI.git
```

### 2. Create and Activate Virtual Environment

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

Ensure you have PostgreSQL running and create a database for the project:
```bash
CREATE DATABASE event_api_db;
```

Update the `DATABASES` setting in `settings.py` with your PostgreSQL credentials and use `event_api_db` as the database name.

### 5. Run Migrations
```bash
python manage.py makemigrations api
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

The server will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication
1. **Obtain JWT Token**
   - POST `http://127.0.0.1:8000/token/`

2. **Refresh JWT Token**
   - POST `http://127.0.0.1:8000/token/refresh/`

### User Registration
1. **Register User**
   - POST `http://127.0.0.1:8000/register/`

### Event Management
1. **Create or View Events**
   - GET/POST `http://127.0.0.1:8000/events/`

2. **Purchase Event Ticket**
   - POST `http://127.0.0.1:8000/events/<id>/purchase/`
   - Replace `<id>` with the event ID

### Optional Endpoints
1. **Bulk Event Creation**
   - POST `http://127.0.0.1:8000/bulk_events_create/`
   - Creates 20 random events for testing

2. **Fetch Top 3 Events by Tickets Sold**
   - GET `http://127.0.0.1:8000/top_three_evets_fetch/`

## Testing

You can test all endpoints using the provided Postman collection.

### Here are some points you might consider including:
1. **Early Access for subscribed user (Subscription model)**
   - 3-day early access to ticket purchases
   - Priority queue for high-demand events

2. **Exclusive Discounts**
   - Special promotional prices
   - Seasonal offers
   - Event-specific discounts

### Wallet System
1. **Features**
   - Secure digital wallet
   - Multiple recharge options
   - Real-time balance updates
   - Transaction history

2. **Usage**
   - Direct ticket purchases
   - Store referral rewards
   - Apply earned discounts

### Referral Program
1. **Rewards**
   - ₹100 coupon for every 10 successful referrals
   - Automatic wallet credit
   - No maximum limit on earnings

2. **Terms**
   - Referral counted only after successful ticket purchase
   - Coupons valid for 6 months
   - No minimum purchase requirement for coupon use

## Thank you





