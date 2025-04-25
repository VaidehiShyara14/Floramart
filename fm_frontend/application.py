from flask import Flask,render_template,request,url_for,jsonify,json,session,redirect
from flask_cors import CORS,cross_origin
import json
import pandas as pd
import requests
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import base64
import os

app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  #Cookie Same site attribute
app.config['SESSION_COOKIE_SECURE'] = False
app.secret_key = 'This_is_very_secret'
login_manager = LoginManager()
login_manager.init_app(app)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = 'static/uploads'  

class User(UserMixin):
    def __init__(self, email):
        self.id = email
        
@login_manager.user_loader
def load_user(email):
    if email:
        return User(email)      
    return None

@app.route('/')
def index():
    user_info = session.get('email')
    print('Logged in user',user_info)
    return render_template('homePage.html')

def get_logged_in_user():
    user_login = False
    user_info = session.get('email')
    if(user_info is not None):
        user_logged_in = user_info
    else:
        user_logged_in = None
    if(user_logged_in is not None):
        user_login = True

    return user_login

@app.route('/HomePage')
def HomePage():
    user_login = get_logged_in_user()
    user_role = session.get("role")  
    return render_template('homePage.html',user_login = user_login,user_role=user_role)

@app.route('/login') 
def login():
    user_login = get_logged_in_user()
    user_role = session.get("role")  
    return render_template('loginPage.html',user_login = user_login,user_role=user_role)

@app.route('/signup')
def signup():
    user_login = get_logged_in_user()
    user_role = session.get("role")
    return render_template('signUp.html',user_login = user_login,user_role=user_role)

@app.route('/profile')
def profile():
    user_login = get_logged_in_user()
    user_role = session.get("role")
    return render_template('profile.html',user_login = user_login,user_role=user_role)

@app.route('/plants')
def plants():
    if not session.get('email'):
        return redirect(url_for('login'))
    user_role = session.get("role")  # Correcting session key
    user_login = get_logged_in_user()
    return render_template('plantsPage.html',user_login = user_login,user_role=user_role)

@app.route('/aboutPage')
def aboutPage():
    user_login = get_logged_in_user()
    user_role = session.get("role") 
    return render_template('aboutPage.html',user_login = user_login,user_role=user_role)

@app.route('/plantcaretipsPage')
def plantcaretipsPage():
    # user_info = session.get('user_name')
    # print('Logged in user',user_info)
    # print(session)
    # return render_template('plantcaretipsPage.html')
    user_login = get_logged_in_user()
    user_role = session.get("role")
    return render_template('plantcaretipsPage.html',user_login = user_login, user_role=user_role)

@app.route('/contactPage')
def contactPage():
    # user_info = session.get('user_name')
    # print('Logged in user',user_info)
    # print(session)
    # return render_template('contactPage.html')
    user_login = get_logged_in_user()
    user_role = session.get("role")
    return render_template('contactPage.html',user_login = user_login, user_role=user_role)

@app.route('/uploadplants')
def uploadplants():
    user_login = get_logged_in_user()
    user_role = session.get("role")  # Correcting session key
    print("User Role from Session:", user_role)  # Debugging
    return render_template('uploadplants.html', user_login=user_login, user_role=user_role)

@app.route('/cartPlants')
def cartPlants():
#     cart_items = session.get('cart_items', [])
#     total_items = len(cart_items)
#     subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
#     total_amount = subtotal  # Add any additional costs here (e.g., taxes or shipping)
    user_login = get_logged_in_user()
    user_role = session.get("role")
    return render_template('cartPlants.html',user_login = user_login, user_role=user_role)

@app.route('/buyNowPage')
def buyNowPage():
    user_login = get_logged_in_user()
    user_role = session.get("role")
    return render_template('buyNowPage.html',user_login = user_login, user_role=user_role)

@app.route('/user_profile')
def user_profile():
    if 'email' not in session:
        return redirect(url_for('login'))  # Redirect if not logged in
    user_email = session['email']
    user_role = session.get('role', 'User')  # Default role if not set
    user_role = session.get("role")
    return render_template('profilePage.html', email=user_email, user_role=user_role)

@app.route('/orders')
def orders():
    if 'email' not in session:
        return redirect(url_for('login'))  # Redirect if not logged in
    user_email = session['email']
    user_role = session.get('role', 'User')  # Default role if not set
    user_role = session.get("role")
    return render_template('ordersPage.html', email=user_email, user_role=user_role)


@app.route('/logout')
@login_required
def logout():
    logout_user()  
    session.clear()
    user_login = get_logged_in_user()
    print("User has been logged out.")
    # return redirect(url_for('login')
    return render_template('homePage.html',user_login = user_login)
  
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     session.clear()
#     user_login = get_logged_in_user()
#     return render_template('loginPage.html',user_login = user_login)

def post_api_function(url, data):
    response = ''
    try:
        response = requests.post(url, json=data)
        print(response)
    except Exception as e:
        print('An exception', e,'Occured')
    return response

def get_api_function(url):
    response = ''
    try:
        response = requests.get(url)
        print(response)
    except Exception as e:
        print('An exception', e,'Occured')
    return response

def get_service_url():
    return 'http://localhost:8000'

def post_api_function(url, data):
    response = ''
    try:
        response = requests.post(url, json=data)
        print(response)
    except Exception as e:
        print('An exception', e,'Occured')
    return response


@app.route('/user_signup', methods=['POST'])
def user_signup():
    url = get_service_url() + '/save_user_signup_details'
    request_data = request.json

    print("Request Data Received:", request_data)

    response = post_api_function(url, request_data)
    try:
        result = response.json()  # Extract JSON from response
        print("Response from Backend:", result)

        # Ensure result is a dictionary before returning
        if isinstance(result, dict):
            return jsonify(result)
        else:
            return jsonify({"status": "Signup Failed", "message": "Unexpected response format"})

    except Exception as e:
        print("Error parsing response:", e)
        return jsonify({"status": "Signup Failed", "message": "Error processing server response"})

@app.route('/user_login', methods=['POST'])
def user_login():
    url = get_service_url() + '/attempt_to_login'
    request_data = request.json
    print("Login Request Data:", request_data)

    response = post_api_function(url, request_data)
    result = response.json()
    print("API Response:", result)

    if result['status'] == 'Login Failed':
        session['email'] = None
        session['role'] = None  # Ensure session role is cleared
    else:
        session['email'] = request_data['email']
        session['role'] = request_data['role']  # Storing role
        print("Assigned Role in Session:", session['role'])  # Debugging

        user = User(request_data['email'])
        login_user(user)

    return response.json()

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    url = get_service_url() + '/get_submit_contact_form_data'
    request_data = request.json
    response = post_api_function(url,request_data)
    return json.dumps(response.json())

@app.route('/upload_image', methods=['POST'])
def upload_image(): 
    print("hello")
    if 'plantImage' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    image_file = request.files['plantImage']
    plantName = request.form['plantName']
    productType = request.form['productType']
    plantType = request.form['plantType']
    plantDescription = request.form['plantDescription']
    plantPrice = request.form['plantPrice']
    print(type(plantPrice))
    
    image = image_file.read()
    base64_obj = base64.b64encode(image).decode('utf-8')
    # print(base64_obj)

    request_data = {
        "image": base64_obj,
        "plantName" : plantName,
        "productType" : productType,
        "plantType" : plantType,  
        "plantDescription" : plantDescription,
        "plantPrice":plantPrice
    }
    # print(request_data)
    url = get_service_url() + '/save_image'
    response = post_api_function(url,request_data)
    return json.dumps(response.json())

@app.route('/get_plant_image', methods=['POST'])
def get_plant_image():
    url = get_service_url() + '/get_plant_image_data'
    request_data = request.json
    # print("Request data:",request_data)
    print(type(request_data))
    response = post_api_function(url,request_data)
    # print("Response:",response)
    return json.dumps(response.json())

@app.route('/add_cart', methods=['POST'])
def add_cart():
    url = get_service_url() + '/get_add_cart_data'
    request_data = request.json
    response = post_api_function(url,request_data)
    return json.dumps(response.json())

@app.route('/get_cart_details', methods=['POST'])
def get_cart_details():
    url = get_service_url() + '/get_cart_details_data'
    request_data = request.json
    # print("Request data:",request_data)
    print(type(request_data))
    response = post_api_function(url,request_data)
    # print("Response:",response.json())
    return json.dumps(response.json())

@app.route('/get_remove_cart_item', methods=['POST'])
def get_remove_cart_item():
    url = get_service_url() + '/get_remove_cart_item_data'
    request_data = request.json
    # print(request_data)
    response = post_api_function(url, request_data)
    return json.dumps(response.json())

# @app.route('/submit_order_details', methods=['POST'])
# def submit_order_details():
#     url = get_service_url() + '/get_submit_order_details_data'
#     request_data = request.json
#     print("Data received at order_details endpoint:", request_data)  
#     print(type(request_data['email_or_phone']))
    
#     response = post_api_function(url, request_data)
#     print("Response from backend service:", response.json())

    return jsonify(response.json())  

if __name__ == '__main__':
    app.run(debug=True, port=1447)

























