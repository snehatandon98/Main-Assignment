import jwt
import uuid
import datetime
import config
import requests
import logging
from config import session
from model import Credentials as users
from flask import Flask, request, jsonify, make_response
from functools import wraps

session=session()

app = Flask(__name__)
app.config['SECRET_KEY']=config.SECRET_KEY

logging.basicConfig(level=logging.INFO)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            current_user = session.query(users).filter(users.user_id==data['user_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

#ADD USER IN DATABASE
@app.route('/register', methods=['POST'])
def register_user():

    data = request.get_json()

    new_user = users(user_id=uuid.uuid4(),username=data["username"],password=data['password'])
    session.add(new_user)
    session.commit()

    response  = jsonify({'message' : 'New user created!'})
    logging.info('User successfully registered!!')
    return response

#LOGIN
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization 
    username = auth.username
    password = auth.password
    response = None
    if not username or not password:
        response = make_response('Could not verify, Incorrect username or password', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        return response
    user = session.query(users).filter_by(username=username).first()

    if not user:
        response = make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        logging.info('LOGIN FAILED!!!')
        return response
    if (user.password==password):
        token = jwt.encode({'user_id' : user.user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, app.config['SECRET_KEY'])
        response = jsonify({'token' : token})
        logging.info('Login Successful!!')
    else:
        response = jsonify({'message' : 'Invalid Password!'})
        logging.info('Invalid password, login attempt failed!!!')
    return response

#UPDATE PASSWORD IN DATABASE
@app.route('/update_password', methods=['PUT'])
@token_required
def update_password(current_user):
    data=request.get_json()
    #user=session.query(users).filter(users.username==current_user.username).first()
    current_user.password=data['password']
    session.commit()
    response  = jsonify({'message' : 'Password updated successfully!'})
    logging.info('User password updated Successfuly!!')
    return response

#DELETE USER FROM DATABASE
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data=request.get_json()
    try:
        user=session.query(users).filter(users.username==data['username']).first()
        if not user:
            response = jsonify({'message' : 'This username does not exist'})
            return response
        session.delete(user)
        session.commit()
        response= jsonify({'message' : 'User has been deleted!'})
    except:
        response = jsonify({'message':'Some error occured!!!'})
        
    return response

#VIEW ALL PRODUCTS ON THE APP
@app.route('/view_products',methods = ['GET'])
@token_required
def view_products(current_user):
    res = requests.get('http://127.0.0.1:5001/get_product')
    return res.json()

#ADD PRODUCT TO THE CART
@app.route('/add_to_cart',methods=['POST'])
@token_required
def add_to_cart(current_user):
    data=request.get_json()
    user_id=current_user.user_id
    item_name=data['item_name']
    item_quantity=data['item_quantity']
    get_prod=requests.get('http://127.0.0.1:5001/get_product_by_name/' + item_name)
    product=get_prod.json()
    if get_prod and item_quantity <= product['prod_quantity']:
        item_price=product['prod_price']
        url_str = user_id + "/" + item_name + "/" + str(item_quantity) + "/" + str(item_price)
        res=requests.post('http://127.0.0.1:5002/add_to_cart/' + url_str)
        return res.json()
    else:
        res=jsonify({'message' : 'Quantity not available!!'})
        return res

#VIEW ALL PRODUCTS IN THE CART
@app.route('/view_cart', methods=['GET'])
@token_required
def view_cart(current_user):
    user_id=current_user.user_id
    res = requests.get('http://127.0.0.1:5002/get_cart_details/' + user_id )
    return res.json()

#GET ALL PRODUCTS BETWEEN PARTICULAR PRICE RANGE
@app.route('/price_filter', methods=['GET'])
@token_required
def prod_by_price_filter(current_user):
    data = request.get_json()
    url_str = str(data['low_price']) + "/" + str(data['high_price'])
    res=requests.get('http://127.0.0.1:5001/price_filter/' + url_str)
    return res.json()

#GET ALL PRODUCTS SORTED BY RATING
@app.route('/prod_sorted_by_rating', methods=['GET'])
@token_required
def prod_sorted_by_rating(current_user):
    data = request.get_json()
    res=requests.get('http://127.0.0.1:5001/sort_by_rating/' + data['prod_category'])
    return res.json()

#GET ALL PRODUCTS SORTED BY PRICE
@app.route('/prod_sorted_by_price', methods=['GET'])
@token_required
def prod_sorted_by_price(current_user):
    data = request.get_json()
    res=requests.get('http://127.0.0.1:5001/sort_by_price/' + data['prod_category'])
    return res.json()

#GET ALL PRODUCTS UNDER A PARTICULAR CATEGORY
@app.route('/get_product_by_category', methods=['GET'])
@token_required
def get_product_by_category(current_user):
    data = request.get_json()
    res=requests.get('http://127.0.0.1:5001/get_product/' + data['prod_category'])
    return res.json()

#UPDATE PRODUCT QUANTITY IN CART
@app.route('/update_prod_quantity',methods=['PUT'])
@token_required
def update_prod_quantity(current_user):
    user_id=current_user.user_id
    data=request.get_json()
    item_name=data['item_name']
    item_quantity=data['item_quantity']
    get_prod=requests.get('http://127.0.0.1:5001/get_product_by_name/' + item_name)
    details=get_prod.json()
    if get_prod and item_quantity<=details['prod_quantity']:
        url_str= user_id + "/" + item_name + "/" + str(item_quantity)
        res=requests.put('http://127.0.0.1:5002/update_quantity/' + url_str)
        return res.json()
    else:
        res=jsonify({'message' : 'Quantity not available!!'})
        return res

#DELETE A PRODUCT FROM THE CART
@app.route('/delete_from_cart',methods=['DELETE'])
@token_required
def delete_from_cart(current_user):
    user_id=current_user.user_id
    data=request.get_json()
    item_name=data['item_name']
    res=requests.delete('http://127.0.0.1:5002/remove_item/' + user_id + "/" + item_name)
    return res.json()


#CHECKOUT AND MAKE PAYMENT
@app.route('/checkout', methods=['POST'])
@token_required
def checkout(current_user):
    user_id=current_user.user_id
    details=requests.get('http://127.0.0.1:5002/get_cart_details/' + user_id)
    cart_details=details.json()
    if 'ITEMS' not in cart_details.keys() :
        return cart_details
    amt=cart_details['Total Amount']
    cart=cart_details['ITEMS']
    if len(cart)==0:
        return details.json()
    discount=config.DISCOUNT
    prod_names=""
    prod_quantity=""
    if amt >=config.MINIUMUM_CART_VALUE:
        amt=amt*(100-discount)/100 
    for item in cart:
        prod_names+=item['item_name'] + ","
        prod_quantity+=str(item['item_quantity']) + ","
    url_str=user_id + "/" + prod_names + "/" + prod_quantity + "/" + str(int(amt))
    res=requests.post('http://127.0.0.1:5003/checkout/' + url_str)  

    if res.status_code==200:
        for item in cart :
            item_name=item['item_name']
            str1=item['item_name'] + "/" + str(item['item_quantity'])
            res1=requests.put('http://127.0.0.1:5001/update_quantity/' + str1)
            res2=requests.delete('http://127.0.0.1:5002/remove_item/' + user_id + "/" + item_name)
    return res.json() 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)