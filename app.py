from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from datetime import datetime
from twilio_helper import generate_otp, send_otp

app = Flask(__name__)
app.secret_key = 'orda_rides_secret_key'  # For session management

# Mock data for riders
MOCK_RIDERS = [
    {
        "id": 1,
        "name": "Kwame Mensah",
        "avatar": "https://randomuser.me/api/portraits/men/32.jpg",
        "bike": "Yamaha YBR 125",
        "rating": 4.8,
        "completedRides": 342,
        "distance": 0.8,
        "arrivalTime": "3 min",
        "price": "GH₵ 15"
    },
    {
        "id": 2,
        "name": "Ama Serwaa",
        "avatar": "https://randomuser.me/api/portraits/women/44.jpg",
        "bike": "Honda CG 150",
        "rating": 4.6,
        "completedRides": 208,
        "distance": 1.2,
        "arrivalTime": "5 min",
        "price": "GH₵ 12"
    },
    {
        "id": 3,
        "name": "Kofi Addo",
        "avatar": "https://randomuser.me/api/portraits/men/55.jpg",
        "bike": "Bajaj Boxer 150",
        "rating": 4.9,
        "completedRides": 512,
        "distance": 1.5,
        "arrivalTime": "7 min",
        "price": "GH₵ 10"
    }
]

# Mock data for shops
SHOPS = {
    # Food Category
    "adeiso-pizza": {
        "id": "adeiso-pizza",
        "name": "Adeiso Pizza",
        "category": "food",
        "subcategory": "Pizza & Fast Food",
        "image": "🍕",
        "banner_color": "#FFC107",
        "rating": 4.5,
        "reviews": 120,
        "delivery_time": "15-25 min",
        "delivery_fee": "GH₵ 5",
        "min_order": "GH₵ 20",
        "description": "Best pizza in Adeiso with fresh ingredients and quick delivery.",
        "menu_categories": ["Pizza", "Sides", "Drinks"],
        "menu_items": [
            {
                "id": "margherita-pizza",
                "name": "Margherita Pizza",
                "category": "Pizza",
                "image": "🍕",
                "description": "Classic pizza with tomato sauce, mozzarella, and basil.",
                "price": "GH₵ 35",
                "sizes": [
                    {"name": "Small", "price": "GH₵ 35"},
                    {"name": "Medium", "price": "GH₵ 45"},
                    {"name": "Large", "price": "GH₵ 55"}
                ],
                "options": [
                    {"name": "Extra Cheese", "price": "GH₵ 5"},
                    {"name": "Mushrooms", "price": "GH₵ 3"},
                    {"name": "Pepperoni", "price": "GH₵ 5"}
                ]
            },
            {
                "id": "pepperoni-pizza",
                "name": "Pepperoni Pizza",
                "category": "Pizza",
                "image": "🍕",
                "description": "Pizza with tomato sauce, mozzarella, and pepperoni slices.",
                "price": "GH₵ 40",
                "sizes": [
                    {"name": "Small", "price": "GH₵ 40"},
                    {"name": "Medium", "price": "GH₵ 50"},
                    {"name": "Large", "price": "GH₵ 60"}
                ],
                "options": [
                    {"name": "Extra Cheese", "price": "GH₵ 5"},
                    {"name": "Mushrooms", "price": "GH₵ 3"},
                    {"name": "Double Pepperoni", "price": "GH₵ 8"}
                ]
            },
            {
                "id": "garlic-bread",
                "name": "Garlic Bread",
                "category": "Sides",
                "image": "🥖",
                "description": "Freshly baked bread with garlic butter.",
                "price": "GH₵ 15",
                "options": [
                    {"name": "Add Cheese", "price": "GH₵ 3"}
                ]
            },
            {
                "id": "cola",
                "name": "Cola",
                "category": "Drinks",
                "image": "🥤",
                "description": "Refreshing cola drink.",
                "price": "GH₵ 5",
                "sizes": [
                    {"name": "Regular", "price": "GH₵ 5"},
                    {"name": "Large", "price": "GH₵ 8"}
                ]
            }
        ]
    },
    "adeiso-chicken": {
        "id": "adeiso-chicken",
        "name": "Adeiso Chicken",
        "category": "food",
        "subcategory": "Chicken & Grill",
        "image": "🍗",
        "banner_color": "#F44336",
        "rating": 4.3,
        "reviews": 95,
        "delivery_time": "10-20 min",
        "delivery_fee": "GH₵ 4",
        "min_order": "GH₵ 15",
        "description": "Delicious fried chicken and grilled specialties.",
        "menu_categories": ["Chicken", "Sides", "Drinks"],
        "menu_items": [
            {
                "id": "fried-chicken",
                "name": "Fried Chicken",
                "category": "Chicken",
                "image": "🍗",
                "description": "Crispy fried chicken pieces.",
                "price": "GH₵ 20",
                "options": [
                    {"name": "2 pieces", "price": "GH₵ 20"},
                    {"name": "4 pieces", "price": "GH₵ 35"},
                    {"name": "6 pieces", "price": "GH₵ 50"}
                ]
            },
            {
                "id": "grilled-chicken",
                "name": "Grilled Chicken",
                "category": "Chicken",
                "image": "🍗",
                "description": "Marinated and grilled chicken.",
                "price": "GH₵ 25",
                "options": [
                    {"name": "Quarter", "price": "GH₵ 25"},
                    {"name": "Half", "price": "GH₵ 45"},
                    {"name": "Whole", "price": "GH₵ 80"}
                ]
            },
            {
                "id": "french-fries",
                "name": "French Fries",
                "category": "Sides",
                "image": "🍟",
                "description": "Crispy golden french fries.",
                "price": "GH₵ 10",
                "sizes": [
                    {"name": "Regular", "price": "GH₵ 10"},
                    {"name": "Large", "price": "GH₵ 15"}
                ]
            }
        ]
    },
    "adeiso-local-food": {
        "id": "adeiso-local-food",
        "name": "Adeiso Local Food",
        "category": "food",
        "subcategory": "Traditional Ghanaian",
        "image": "🍲",
        "banner_color": "#4CAF50",
        "rating": 4.6,
        "reviews": 150,
        "delivery_time": "15-30 min",
        "delivery_fee": "GH₵ 5",
        "min_order": "GH₵ 25",
        "description": "Authentic Ghanaian dishes made with local ingredients.",
        "menu_categories": ["Main Dishes", "Soups", "Sides"],
        "menu_items": [
            {
                "id": "jollof-rice",
                "name": "Jollof Rice",
                "category": "Main Dishes",
                "image": "🍚",
                "description": "Spicy rice dish cooked with tomatoes and spices.",
                "price": "GH₵ 30",
                "options": [
                    {"name": "With Chicken", "price": "GH₵ 40"},
                    {"name": "With Beef", "price": "GH₵ 45"},
                    {"name": "With Fish", "price": "GH₵ 38"}
                ]
            },
            {
                "id": "fufu-soup",
                "name": "Fufu with Soup",
                "category": "Soups",
                "image": "🍲",
                "description": "Traditional fufu served with your choice of soup.",
                "price": "GH₵ 35",
                "options": [
                    {"name": "Light Soup", "price": "GH₵ 35"},
                    {"name": "Groundnut Soup", "price": "GH₵ 38"},
                    {"name": "Palm Nut Soup", "price": "GH₵ 40"}
                ]
            }
        ]
    },
    # Groceries Category
    "fresh-market": {
        "id": "fresh-market",
        "name": "Fresh Market",
        "category": "groceries",
        "subcategory": "Fruits & Vegetables",
        "image": "🥗",
        "banner_color": "#4CAF50",
        "rating": 4.8,
        "reviews": 85,
        "delivery_time": "20-30 min",
        "delivery_fee": "GH₵ 6",
        "min_order": "GH₵ 30",
        "description": "Fresh fruits and vegetables delivered to your doorstep.",
        "menu_categories": ["Fruits", "Vegetables", "Juices"],
        "menu_items": [
            {
                "id": "fruit-basket",
                "name": "Fruit Basket",
                "category": "Fruits",
                "image": "🍎",
                "description": "Assorted fresh fruits.",
                "price": "GH₵ 45",
                "options": [
                    {"name": "Small (5 fruits)", "price": "GH₵ 45"},
                    {"name": "Medium (8 fruits)", "price": "GH₵ 70"},
                    {"name": "Large (12 fruits)", "price": "GH₵ 100"}
                ]
            },
            {
                "id": "vegetable-mix",
                "name": "Vegetable Mix",
                "category": "Vegetables",
                "image": "🥦",
                "description": "Mixed fresh vegetables.",
                "price": "GH₵ 35",
                "options": [
                    {"name": "Small Pack", "price": "GH₵ 35"},
                    {"name": "Family Pack", "price": "GH₵ 60"}
                ]
            },
            {
                "id": "fresh-juice",
                "name": "Fresh Juice",
                "category": "Juices",
                "image": "🍹",
                "description": "Freshly squeezed juice.",
                "price": "GH₵ 15",
                "options": [
                    {"name": "Orange", "price": "GH₵ 15"},
                    {"name": "Pineapple", "price": "GH₵ 15"},
                    {"name": "Mixed Fruit", "price": "GH₵ 18"}
                ]
            }
        ]
    },
    # Pharmacy Category
    "adeiso-pharmacy": {
        "id": "adeiso-pharmacy",
        "name": "Adeiso Pharmacy",
        "category": "pharmacy",
        "subcategory": "Medications & Health",
        "image": "💊",
        "banner_color": "#2196F3",
        "rating": 4.7,
        "reviews": 60,
        "delivery_time": "15-25 min",
        "delivery_fee": "GH₵ 5",
        "min_order": "GH₵ 20",
        "description": "Medications and health products delivered quickly.",
        "menu_categories": ["Medications", "First Aid", "Personal Care"],
        "menu_items": [
            {
                "id": "pain-relievers",
                "name": "Pain Relievers",
                "category": "Medications",
                "image": "💊",
                "description": "Common pain relief medications.",
                "price": "GH₵ 15",
                "options": [
                    {"name": "Paracetamol", "price": "GH₵ 15"},
                    {"name": "Ibuprofen", "price": "GH₵ 18"}
                ]
            },
            {
                "id": "first-aid-kit",
                "name": "First Aid Kit",
                "category": "First Aid",
                "image": "🩹",
                "description": "Basic first aid supplies.",
                "price": "GH₵ 45",
                "options": [
                    {"name": "Basic Kit", "price": "GH₵ 45"},
                    {"name": "Family Kit", "price": "GH₵ 75"}
                ]
            }
        ]
    },
    # Electronics Category
    "tech-hub": {
        "id": "tech-hub",
        "name": "Tech Hub",
        "category": "electronics",
        "subcategory": "Mobile & Accessories",
        "image": "📱",
        "banner_color": "#2196F3",
        "rating": 4.2,
        "reviews": 80,
        "delivery_time": "30-45 min",
        "delivery_fee": "GH₵ 8",
        "min_order": "GH₵ 50",
        "description": "Mobile phones, accessories, and electronic gadgets.",
        "menu_categories": ["Mobile Accessories", "Chargers", "Headphones"],
        "menu_items": [
            {
                "id": "phone-case",
                "name": "Phone Case",
                "category": "Mobile Accessories",
                "image": "📱",
                "description": "Protective cases for smartphones.",
                "price": "GH₵ 25",
                "options": [
                    {"name": "iPhone Case", "price": "GH₵ 30"},
                    {"name": "Samsung Case", "price": "GH₵ 25"},
                    {"name": "Other Brands", "price": "GH₵ 20"}
                ]
            },
            {
                "id": "usb-charger",
                "name": "USB Charger",
                "category": "Chargers",
                "image": "🔌",
                "description": "Fast charging USB adapters.",
                "price": "GH₵ 35",
                "options": [
                    {"name": "Standard", "price": "GH₵ 35"},
                    {"name": "Fast Charging", "price": "GH₵ 50"}
                ]
            }
        ]
    },
    "agya-owusu-electricals": {
        "id": "agya-owusu-electricals",
        "name": "Agya Owusu Electricals",
        "category": "electronics",
        "subcategory": "Electrical & Home Appliances",
        "image": "💡",
        "banner_color": "#FFC107",
        "rating": 4.7,
        "reviews": 125,
        "delivery_time": "25-40 min",
        "delivery_fee": "GH₵ 7",
        "min_order": "GH₵ 40",
        "description": "Quality electrical supplies, home appliances, and car parts for all your needs.",
        "menu_categories": ["Lighting", "Wiring", "Appliances", "Car Parts"],
        "menu_items": [
            {
                "id": "led-bulb",
                "name": "LED Light Bulb",
                "category": "Lighting",
                "image": "💡",
                "description": "Energy-efficient LED light bulbs in various wattages.",
                "price": "GH₵ 15",
                "options": [
                    {"name": "5W", "price": "GH₵ 15"},
                    {"name": "10W", "price": "GH₵ 20"},
                    {"name": "15W", "price": "GH₵ 25"}
                ]
            },
            {
                "id": "lampholder",
                "name": "Lamp Holder",
                "category": "Lighting",
                "image": "💡",
                "description": "Standard lamp holders for various bulb types.",
                "price": "GH₵ 12",
                "options": [
                    {"name": "Standard", "price": "GH₵ 12"},
                    {"name": "Decorative", "price": "GH₵ 18"},
                    {"name": "Waterproof", "price": "GH₵ 25"}
                ]
            },
            {
                "id": "electrical-wire",
                "name": "Electrical Wire",
                "category": "Wiring",
                "image": "💪",
                "description": "High-quality electrical wires and cables.",
                "price": "GH₵ 30",
                "options": [
                    {"name": "1.5mm (5m)", "price": "GH₵ 30"},
                    {"name": "2.5mm (5m)", "price": "GH₵ 45"},
                    {"name": "4.0mm (5m)", "price": "GH₵ 65"}
                ]
            },
            {
                "id": "extension-cord",
                "name": "Extension Cord",
                "category": "Wiring",
                "image": "🔌",
                "description": "Multi-socket extension cords with surge protection.",
                "price": "GH₵ 35",
                "options": [
                    {"name": "3-Socket (2m)", "price": "GH₵ 35"},
                    {"name": "5-Socket (3m)", "price": "GH₵ 50"},
                    {"name": "8-Socket (5m)", "price": "GH₵ 75"}
                ]
            },
            {
                "id": "electric-iron",
                "name": "Electric Iron",
                "category": "Appliances",
                "image": "👕",
                "description": "Reliable electric irons for home use.",
                "price": "GH₵ 85",
                "options": [
                    {"name": "Standard", "price": "GH₵ 85"},
                    {"name": "Steam Iron", "price": "GH₵ 120"}
                ]
            },
            {
                "id": "car-battery",
                "name": "Car Battery",
                "category": "Car Parts",
                "image": "🚗",
                "description": "Reliable car batteries for various vehicle models.",
                "price": "GH₵ 250",
                "options": [
                    {"name": "Standard", "price": "GH₵ 250"},
                    {"name": "Heavy Duty", "price": "GH₵ 350"}
                ]
            }
        ]
    }
}

# Location coordinates in Adeiso
LOCATION_COORDINATES = {
    "Adeiso Market Square": {"lat": 5.8003, "lng": -0.5103},
    "Adeiso Health Center": {"lat": 5.7978, "lng": -0.5089},
    "Adeiso Secondary School": {"lat": 5.8012, "lng": -0.5120},
    "Adeiso Police Station": {"lat": 5.7995, "lng": -0.5110},
    "Asamankese-Adeiso Road": {"lat": 5.7980, "lng": -0.5090},
    "Adeiso Lorry Park": {"lat": 5.7988, "lng": -0.5098}
}

# Routes
@app.route('/')
def index():
    # Redirect to home if logged in, otherwise to login
    if session.get('logged_in'):
        return render_template('index.html', page='home', title='OrDa Rides')
    return render_template('login.html', page='login', title='Login - OrDa Rides')

@app.route('/login')
def login():
    return render_template('login.html', page='login', title='Login - OrDa Rides')

@app.route('/signup')
def signup():
    return render_template('signup.html', page='signup', title='Sign Up - OrDa Rides')

@app.route('/verify-otp')
def verify_otp():
    return render_template('verify_otp.html', page='verify_otp', title='Verify Phone - OrDa Rides')

@app.route('/api/send-otp', methods=['POST'])
def send_otp_api():
    data = request.json
    phone = data.get('phone')
    
    if not phone:
        return jsonify({'success': False, 'message': 'Phone number is required'})
    
    # Generate OTP
    otp = generate_otp()
    
    # Store OTP in session
    session['otp'] = otp
    session['otp_phone'] = phone
    
    # Send OTP via Twilio
    message_id = send_otp(phone, otp)
    
    if message_id:
        return jsonify({
            'success': True, 
            'message': 'OTP sent successfully',
            'otp': otp  # In a real app, you wouldn't send this back to client
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP'})

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp_api():
    data = request.json
    otp_input = data.get('otp')
    
    if not otp_input:
        return jsonify({'success': False, 'message': 'OTP is required'})
    
    # Get stored OTP from session
    stored_otp = session.get('otp')
    
    if not stored_otp:
        return jsonify({'success': False, 'message': 'No OTP found, please request a new one'})
    
    # Verify OTP
    if otp_input == stored_otp:
        # Clear OTP from session
        session.pop('otp', None)
        
        # Mark phone as verified
        session['phone_verified'] = True
        
        return jsonify({'success': True, 'message': 'OTP verified successfully'})
    else:
        return jsonify({'success': False, 'message': 'Invalid OTP'})


@app.route('/home')
def home():
    # Set a session flag to simulate login
    session['logged_in'] = True
    return render_template('index.html', page='home', title='OrDa Rides')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return render_template('login.html', page='login', title='Login - OrDa Rides')

# Popular locations in Ghana with coordinates
POPULAR_LOCATIONS = {
    # Adeiso locations
    "Adeiso Market Square": [5.8003, -0.5103],
    "Adeiso Health Center": [5.7980, -0.5080],
    "Adeiso Police Station": [5.8020, -0.5110],
    "Adeiso Community Center": [5.7990, -0.5095],
    "Adeiso School": [5.8010, -0.5120],
    
    # Accra locations
    "Accra Mall": [5.6357, -0.1869],
    "Kotoka International Airport": [5.6052, -0.1669],
    "University of Ghana": [5.6500, -0.1870],
    "Labadi Beach": [5.5568, -0.1463],
    "Makola Market": [5.5461, -0.2173],
    
    # Kumasi locations
    "Kejetia Market": [6.6913, -1.6285],
    "Kumasi City Mall": [6.6887, -1.6095],
    "KNUST": [6.6746, -1.5697],
    "Manhyia Palace": [6.7060, -1.6156],
    "Kumasi Zoo": [6.7018, -1.6233],
    
    # Tamale locations
    "Tamale Central Market": [9.4075, -0.8430],
    "Tamale Teaching Hospital": [9.4338, -0.8520],
    "University for Development Studies": [9.4032, -0.8497],
    "Tamale Stadium": [9.4154, -0.8584],
    "Tamale Cultural Center": [9.4101, -0.8455]
}

@app.route('/rides')
def rides():
    return render_template('rides.html', page='rides', title='Book a Ride', 
                           locations=POPULAR_LOCATIONS)

@app.route('/orders')
def orders():
    return render_template('orders.html', page='orders', title='Order Food & Items', shops=SHOPS)

@app.route('/shop/<shop_id>')
def shop_detail(shop_id):
    if shop_id in SHOPS:
        shop = SHOPS[shop_id]
        return render_template('shop_detail.html', page='orders', title=shop['name'], shop=shop)
    else:
        return render_template('404.html', message='Shop not found'), 404

@app.route('/cart')
def cart():
    return render_template('cart.html', page='orders', title='Your Cart')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html', page='orders', title='Checkout')

@app.route('/order/confirm')
def order_confirm():
    return render_template('order_confirmation.html', page='orders', title='Order Confirmed')

@app.route('/order/track/<order_id>')
def order_track(order_id):
    return render_template('order_tracking.html', page='orders', title='Track Order', order_id=order_id)

@app.route('/community')
def community():
    return render_template('community.html', page='community', title='Community')

@app.route('/profile')
def profile():
    return render_template('profile.html', page='profile', title='My Profile')

# API endpoints
@app.route('/api/riders')
def get_riders():
    return jsonify(MOCK_RIDERS)

@app.route('/api/shops')
def get_shops():
    return jsonify(SHOPS)

@app.route('/api/locations', methods=['GET'])
def get_locations():
    return jsonify(LOCATION_COORDINATES)

@app.route('/api/start_ride', methods=['POST'])
def start_ride():
    data = request.json
    # Store ride info in session
    session['active_ride'] = {
        'rider': data.get('rider'),
        'pickup': data.get('pickup'),
        'destination': data.get('destination'),
        'status': data.get('status', 'confirmed'),
        'start_time': datetime.now().isoformat()
    }
    return jsonify({'success': True})

@app.route('/api/update_ride_status', methods=['POST'])
def update_ride_status():
    data = request.json
    if 'active_ride' in session:
        session['active_ride']['status'] = data.get('status')
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'No active ride found'})

@app.route('/api/end_ride', methods=['POST'])
def end_ride():
    if 'active_ride' in session:
        session.pop('active_ride')
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'No active ride found'})

@app.route('/api/active_ride', methods=['GET'])
def get_active_ride():
    if 'active_ride' in session:
        return jsonify({'success': True, 'ride': session['active_ride']})
    else:
        return jsonify({'success': False, 'message': 'No active ride found'})

@app.route('/api/cancel_ride', methods=['POST'])
def cancel_ride():
    # Clear the active ride from session
    if 'active_ride' in session:
        session.pop('active_ride', None)
        return jsonify({'success': True, 'message': 'Ride cancelled successfully'})
    else:
        return jsonify({'success': False, 'message': 'No active ride found'})

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# For Vercel serverless deployment
app.debug = False
