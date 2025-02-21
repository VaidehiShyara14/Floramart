from fastapi import FastAPI
import fm_backend_db as fm_db
import json
import schemas
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import base64
import io
import pandas as pd

app = FastAPI()

@app.post("/save_user_signup_details")
def save_user_signup_details(signup_details: schemas.UsersignUp):
    print("Received signup details: ", signup_details)
    
    # Call database function and store its result
    result = fm_db.save_user_signup_details(signup_details.dict())
    print("result from backend",result)
    if result == "Success":
        # Return success response
        return {"status": "Signup Successful", "message": "User registered successfully"}
    else:
        # Return failure response
        return {"status": "Signup Failed", "message": result}

@app.post("/attempt_to_login")
def attempt_to_login(login_data:schemas.LoginUser):
    print(login_data)
    valid_user_login = ""
    valid_user = fm_db.validate_login_details(login_data.dict())
    if(valid_user):
        valid_user_login = "Login Successful"
    else:
        valid_user_login = "Login Failed"

    response = {
        "status" : valid_user_login,
        "email"  : login_data.email
    }
    print("response",response)
    return JSONResponse(content=response, status_code=200)

@app.post("/get_submit_contact_form_data")
def get_submit_contact_form_data(contact_data: schemas.ContactForm):
    print("Received contact form data: ", contact_data)
    
    # Save the data to the database using the backend function
    result = fm_db.save_contact_message(contact_data.dict())
    
    if result == "Success":
        return {"status": "Success", "message": "Message submitted successfully"}
    else:
        return {"status": "Error", "message": result}
    
@app.post("/get_plant_image_data")
def get_plant_image_data(filter_data:schemas.FilterPlant):
    # print("From backend.py:",filter_data)
    result = fm_db.get_plant_image_data(filter_data.dict())
    
    # print("Result",result)
    response = {
        "data" : result
    }
    return response
    # return json.dumps(response)   

@app.post("/save_image")
def save_image(image_data:schemas.ImageData):
    result = fm_db.upload_image(image_data.dict())
    response = {
        "data" : result
    }
    return json.dumps(response)

@app.post("/get_add_cart_data")
def get_add_cart_data(cart_data: schemas.ATC_Btn):
    # print("Received carydetails form data: ", cart_data)
    
    # Save the data to the database using the backend function
    result = fm_db.save_cart_details(cart_data.dict())

@app.post("/get_cart_details_data")
def get_cart_details_data(cart_data:schemas.CartIcon):
    
    # print("Received cart data:", cart_data)
    result = fm_db.get_cart_details_data(cart_data.dict())
    
    # print("Result",result)
    response = {
        "data" : result
    }
    return response

# @app.route("/get_update_cart_quantity")
# def update_cart_quantity(cart_data:schemas.UpdateCartQuantityRequest):
    
#     print("Received cart data:", cart_data)
#     result = fm_db.update_cart_quantity(cart_data['id'], cart_data['quantity'])
#     return json({"message": "Quantity updated successfully"})

#     return json
    
# @app.route("/get_remove_cart_item")
# def remove_cart_item(cart_data:schemas.RemoveCartItemRequest):
    
#     print("Received cart data:", cart_data)
#     result = fm_db.remove_cart_item(cart_data['id'])
#     return json({"message": "Item removed successfully"})
    
#     return json
# @app.post("/get_update_cart_quantity_data")
# def get_update_cart_quantity(cart_data:schemas.UpdateCartQuantityRequest):
#     # cart_data = request.get_json()  # Parse JSON from request
#     print("Received cart data:", cart_data)
#     result = fm_db.get_update_cart_quantity_data((cart_data.dict()))
#     return json({"message": "Quantity updated successfully"})
    
@app.post("/get_remove_cart_item_data")
def get_remove_cart_item(remove_cart_data:schemas.RemoveCartItemRequest):
    # cart_data = request.get_json()  # Parse JSON from request
    # print("Received cart data:", remove_cart_data)
    result = fm_db.get_remove_cart_item_data((remove_cart_data.dict()))
    return JSONResponse(content={"message": "Item removed successfully"})

@app.post("/get_submit_order_details_data")
def get_submit_order_details_data(ordere_data: schemas.OrderForm):
    print("Received contact form data: ", ordere_data)
    
    # Save the data to the database using the backend function
    result = fm_db.save_submit_order_details(ordere_data.dict())
    
    if result == "Success":
        return {"status": "Success", "message": "Message submitted successfully"}
    else:
        return {"status": "Error", "message": result}
    










                                        