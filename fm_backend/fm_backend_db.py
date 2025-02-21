import psycopg2
import json
import psycopg2.extras
from decimal import Decimal 
from datetime import datetime

def connection():
    try:
        conn = psycopg2.connect(
            database="floramart_db",
            user='fm_user',
            password='147200',
            host='127.0.0.1',
            port='5432'
        )
        print("Connection successful")
        return conn
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

def save_user_signup_details(signup_details):
    role = signup_details['role']
    conn = connection()
    cursor = conn.cursor()

    try:
        if role == "user":
            print("Signup Details: ", signup_details)

            # Fetch new user ID for `user_info`
            FETCH_MAX_ID_QUERY = '''
                SELECT COALESCE(MAX(id), 0) + 1 AS new_user_id
                FROM fm_schema.user_info
            '''
            cursor.execute(FETCH_MAX_ID_QUERY)
            new_user_id = cursor.fetchone()[0]
            print("New User ID (user_info):", new_user_id)

            # Insert into `user_info`
            INSERT_USER_INFO_QUERY = '''
                INSERT INTO fm_schema.user_info (id, full_name, email, password) 
                VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(INSERT_USER_INFO_QUERY, (
                new_user_id,
                signup_details['full_name'],
                signup_details['email'],
                signup_details['password']
            ))
            conn.commit()

            # Fetch new user ID for `user_login`
            FETCH_MAX_LOGIN_ID_QUERY = '''
                SELECT COALESCE(MAX(id), 0) + 1 AS new_user_id
                FROM fm_schema.user_login
            '''
            cursor.execute(FETCH_MAX_LOGIN_ID_QUERY)
            new_user_id = cursor.fetchone()[0]
            print("New User ID (user_login):", new_user_id)

            # Insert into `user_login`
            INSERT_USER_LOGIN_QUERY = '''
                INSERT INTO fm_schema.user_login (id, email, password) 
                VALUES (%s, %s, %s)
            '''
            cursor.execute(INSERT_USER_LOGIN_QUERY, (
                new_user_id,
                signup_details['email'],
                signup_details['password']
            ))
            conn.commit()

        elif role == "admin":
            print("Signup Details: ", signup_details)

            # Fetch new admin ID for `admin_info`
            FETCH_MAX_ID_QUERY = '''
                SELECT COALESCE(MAX(id), 0) + 1 AS new_admin_id
                FROM fm_schema.admin_info
            '''
            cursor.execute(FETCH_MAX_ID_QUERY)
            new_admin_id = cursor.fetchone()[0]
            print("New Admin ID (admin_info):", new_admin_id)

            # Insert into `admin_info`
            INSERT_ADMIN_INFO_QUERY = '''
                INSERT INTO fm_schema.admin_info (id, full_name, email, password) 
                VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(INSERT_ADMIN_INFO_QUERY, (
                new_admin_id,
                signup_details['full_name'],
                signup_details['email'],
                signup_details['password']
            ))
            conn.commit()

            # Fetch new admin ID for `admin_login`
            FETCH_MAX_LOGIN_ID_QUERY = '''
                SELECT COALESCE(MAX(id), 0) + 1 AS new_admin_id
                FROM fm_schema.admin_login
            '''
            cursor.execute(FETCH_MAX_LOGIN_ID_QUERY)
            new_admin_id = cursor.fetchone()[0]
            print("New Admin ID (admin_login):", new_admin_id)

            # Insert into `admin_login`
            INSERT_ADMIN_LOGIN_QUERY = '''
                INSERT INTO fm_schema.admin_login (id, email, password) 
                VALUES (%s, %s, %s)
            '''
            cursor.execute(INSERT_ADMIN_LOGIN_QUERY, (
                new_admin_id,
                signup_details['email'],
                signup_details['password']
            ))
            conn.commit()

        return "Success"

    except Exception as e:
        print("Error occurred:", str(e))
        return f"Error: {str(e)}"

    finally:
        if conn:
            cursor.close()
            conn.close()



def validate_login_details(login_data):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    valid_user = False

    try:
        print("from_db", login_data)

        if login_data['role'] == "user":
            QUERY = '''
                SELECT email, password
                FROM fm_schema.user_login
                WHERE email = %s
            '''
        elif login_data['role'] == "admin":
            QUERY = '''
                SELECT email, password
                FROM fm_schema.admin_login
                WHERE email = %s
            '''
        else:
            print("Invalid role provided")
            return False  # Immediately return if role is incorrect

        # Execute the query using parameterized input (to prevent SQL injection)
        cursor.execute(QUERY, (login_data['email'],))
        reg_records = cursor.fetchall()
        print(reg_records)

        if reg_records:
            for row in reg_records:
                stored_password = row['password']
                stored_email = row['email']

            print(stored_password, stored_email)

            if login_data['email'] == stored_email and login_data['password'] == stored_password:
                valid_user = True

    except Exception as e:
        print("Error:", str(e), "Occurred")

    finally:
        if conn:
            cursor.close()
            conn.close()

    return valid_user

def save_contact_message(contact_data):
    conn = connection()
    cursor = conn.cursor()

    try:
        print("Contact Details: ", contact_data)

        FETCH_MAX_LOGIN_ID_QUERY = '''
            SELECT COALESCE(MAX(id), 0) + 1 AS new_user_id
            FROM fm_schema.contact_messages
        '''
        cursor.execute(FETCH_MAX_LOGIN_ID_QUERY)
        new_user_id = cursor.fetchone()[0]
        print("New User ID (user_login):", new_user_id)


        # Insert into contact_messages table
        INSERT_CONTACT_MESSAGE_QUERY = '''
            INSERT INTO fm_schema.contact_messages (id,full_name, email, message) 
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(INSERT_CONTACT_MESSAGE_QUERY, (
            new_user_id,
            contact_data['full_name'],
            contact_data['email'],
            contact_data['message']
        ))
        conn.commit()

        return "Success"

    except Exception as e:
        print("Error occurred while saving contact message:", str(e))
        return f"Error: {str(e)}"

    finally:
        if conn:
            cursor.close()
            conn.close()
    return valid_user

def upload_image(image_data):
    conn = connection()
    cursor = conn.cursor()
    try:
        # print(image_data)
        FETCH_MAX_LOGIN_ID_QUERY = '''
            SELECT COALESCE(MAX(plant_id), 0) + 1 AS new_user_id
            FROM fm_schema.plants_images
        '''
        cursor.execute(FETCH_MAX_LOGIN_ID_QUERY)
        new_plant_id = cursor.fetchone()[0]
        # print("New Plant ID (user_login):", new_plant_id)


        QUERY = '''
                INSERT INTO fm_schema.plants_images(plant_id,plant_name,price,description,plant_images,plant_type,plant_product)
                VALUES('{}','{}','{}','{}','{}','{}','{}')
                '''.format(
                    new_plant_id,
                    image_data['plantName'],
                    image_data['plantPrice'],
                    image_data['plantDescription'],
                    image_data['image'],
                    image_data['plantType'],
                    image_data['productType']
                )
        cursor.execute(QUERY)
        conn.commit()

    except Exception as e:
        print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return "Success"

# def get_plant_image_data(filter_data):
#     conn = connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     # json_result = [] 
    
#     try:
#         print(filter_data)
#         QUERY = '''
#                 SELECT 
#                 plant_id,
#                 plant_name,
#                 plant_product,
#                 plant_type,
#                 description,
#                 price,
#                 plant_images
#                 FROM fm_schema.plants_images
#                 WHERE  plant_type= '{}' AND plant_product= '{}'
#                 '''.format(
#                     filter_data['selectPlantType'],
#                     filter_data['selectFertilizerandSeeds']
#                 )
        
#         result = cursor.execute(QUERY)
#         records = cursor.fetchall()
       
#         # Process each record
#         for record in records:
#             if record["plant_images"] is not None:
#                 record["plant_images"] = record["plant_images"].tobytes().decode("utf-8")
            
#             # Convert Decimal type to float
#             if isinstance(record["price"], Decimal):
#                 record["price"] = float(record["price"])
#         print("Records:",records)
#         # json_result.append(records)
            
#         json_result = json.dumps(records, indent=4)
#         # print(json_result)
#     except Exception as e:
#         print("Error:", str(e))
#     finally:
#         if conn:
#             cursor.close()
#             conn.close()
    
#     return json_resul

def get_plant_image_data(filter_data):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # print("Filter Data Received:", filter_data)

        # Base query
        QUERY = '''
            SELECT 
                plant_id,
                plant_name,
                plant_product,
                plant_type,
                description,
                price,
                plant_images
            FROM fm_schema.plants_images
            WHERE 1=1
        '''

        # Add dynamic filters
        filters = []
        params = []

        # Check if filters are provided
        if filter_data.get('selectPlantType'):
            filters.append("plant_type = %s")
            params.append(filter_data['selectPlantType'])

        if filter_data.get('selectFertilizerandSeeds'):
            filters.append("plant_product = %s")
            params.append(filter_data['selectFertilizerandSeeds'])

        # If no filters are applied, all data will be fetched by default
        if filters:
            QUERY += " AND " + " AND ".join(filters)

        print("Constructed Query:", QUERY)
        print("Query Parameters:", params)

        # Execute the query with parameters
        cursor.execute(QUERY, params)
        records = cursor.fetchall()

        # Process the records
        for record in records:
            if record["plant_images"] is not None:
                record["plant_images"] = record["plant_images"].tobytes().decode("utf-8")
            
        
            if isinstance(record["price"], Decimal):
                record["price"] = float(record["price"])
  
        
        # print("Fetched Records:", records)

        # Convert result to JSON
        json_result = json.dumps(records, indent=4)
    except Exception as e:
        print("Error:", str(e))
        json_result = json.dumps({"error": "Error occurred while fetching plant data."})
    finally:
        if conn:
            cursor.close()
            conn.close()

    return json_result

def save_cart_details(cart_data):
    conn = connection()
    cursor = conn.cursor()

    try:
        # print("Cart Details: ", cart_data)

        FETCH_MAX_LOGIN_ID_QUERY = '''
            SELECT COALESCE(MAX(id), 0) + 1 AS new_cart_id
            FROM fm_schema.cart_details
        '''
        cursor.execute(FETCH_MAX_LOGIN_ID_QUERY)
        new_cart_id = cursor.fetchone()[0]
        # print("New Cart ID (cart_login):", new_cart_id)


        INSERT_CONTACT_MESSAGE_QUERY = '''
            INSERT INTO fm_schema.cart_details (id,email_id,plant_name,price,plant_image) 
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(INSERT_CONTACT_MESSAGE_QUERY, (
            new_cart_id,
            cart_data['email_id'],
            cart_data['name'],
            cart_data['price'],
            cart_data['image']
        ))
        conn.commit()

        return "Success"

    except Exception as e:
        print("Error occurred while saving contact message:", str(e))
        return f"Error: {str(e)}"

    finally:
        if conn:
            cursor.close()
            conn.close()
    return valid_cart

def get_cart_details_data(cart_data):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # print("cart Data Received:", cart_data)

        # Base query
        QUERY = '''
            SELECT 
                id,
                email_id,
                plant_name,
                price,
                plant_image,
                quantity,
                total_price
            FROM fm_schema.cart_details
            WHERE email_id ='{}'
        '''.format(
                    cart_data['email_id']
                 )
        
        cursor.execute(QUERY)
        records = cursor.fetchall()

        for record in records:
            if record["plant_image"] is not None:
                record["plant_image"] = record["plant_image"].tobytes().decode("utf-8")
            
        
            if isinstance(record["price"], Decimal):
                record["price"] = float(record["price"])

            if record["total_price"] is not None and isinstance(record["total_price"], Decimal):
                record["total_price"] = float(record["total_price"])      

        # Convert result to JSON
        json_result = json.dumps(records, indent=4)
        # print(json_result)
    except Exception as e:
        print("Error:", str(e))
        json_result = json.dumps({"error": "Error occurred while fetching plant data."})
    finally:
        if conn:
            cursor.close()
            conn.close()

    return json_result

# def get_update_cart_quantity_data(cart_data):
#     conn = connection()
#     cursor = conn.cursor()
#     try:
#         QUERY = '''
#             UPDATE fm_schema.cart_details
#             SET quantity = '{}'
#            WHERE id = {}'
#         '''.format(
#                     cart_data['itemId']
#                  )
        
#         cursor.execute(QUERY)
#         conn.commit()
#         return "Success"
#     finally:
#         cursor.close()
#         conn.close()

def get_remove_cart_item_data(remove_cart_data):
    conn = connection()
    cursor = conn.cursor()
    try:
        # print("cartdata",remove_cart_data)
        QUERY = '''
             DELETE FROM fm_schema.cart_details 
             WHERE id = '{}'
        '''.format(
                    remove_cart_data['itemId']
                 )
             
        cursor.execute(QUERY)
        conn.commit()
        return "Success"
    finally:
        cursor.close()
        conn.close()        

def save_submit_order_details(order_data):
    conn = connection()
    cursor = conn.cursor()

    try:
        print("Order Details: ", order_data)

        FETCH_MAX_LOGIN_ID_QUERY = '''
            SELECT COALESCE(MAX(order_id), 0) + 1 AS new_order_id
            FROM fm_schema.order_details
        '''
        cursor.execute(FETCH_MAX_LOGIN_ID_QUERY)
        new_order_id = cursor.fetchone()[0]
        print("New Order ID (user_login):", new_order_id)


        # Insert into order table
        INSERT_OREDR_DETAILS_QUERY = '''
            INSERT INTO fm_schema.order_details (order_id,email_or_phone,news_offers_subscription,first_name,last_name,address,apartment_details,city,state,pin_code,phone_number) 
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        '''.format(
            new_order_id,
            order_data['email_or_phone'],
            order_data['news_offers_subscription'],
            order_data['first_name'],
            order_data['last_name'],
            order_data['address'],
            order_data['apartment_details'],
            order_data['city'],
            order_data['state'],
            order_data['pin_code'],
            order_data['phone_number']
        )
        print("Executing Query:", INSERT_OREDR_DETAILS_QUERY)  
        print("With Parameters:")  

        cursor.execute(INSERT_OREDR_DETAILS_QUERY)
        conn.commit()

        return "Success"

    except Exception as e:
        print("Error occurred while saving order:", str(e))
        return f"Error: {str(e)}"

    finally:
        if conn:
            cursor.close()
            conn.close()
    return valid_user


            