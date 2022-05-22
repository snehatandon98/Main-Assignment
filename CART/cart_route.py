from crypt import methods
from urllib import response
import uuid
import config
from config import session
from model import Cart as items
from flask import Flask, request, jsonify


session=session()

app = Flask(__name__)
app.config['SECRET_KEY']=config.SECRET_KEY

#ADD Item
@app.route('/add_to_cart/<user_id>/<item_name>/<int:item_quantity>/<int:item_price>', methods=['POST'])
def add_to_cart(user_id, item_name, item_quantity,item_price):
    new_item=items(
        user_id=user_id, item_name=item_name, 
        item_quantity=item_quantity, item_price=item_price)
    session.add(new_item)
    session.commit()
    response  = jsonify({'message' : 'Item added to Cart!'})
    return response

#DELETE ITEM
@app.route('/remove_item/<user_id>/<item_name>',methods=['DELETE'])
def remove_item(user_id,item_name):
    try:
        item=session.query(items).filter(items.user_id==user_id ,items.item_name==item_name).first()
        if not item:
            response = jsonify({'message' : 'The item is not added to the cart.'})
            return response
        session.delete(item)
        session.commit()
        response= jsonify({'message' : 'item has been deleted from the cart!'})
    except Exception as error:
        response = jsonify({'message':'Some error occured!!!'})
        
    return response

#UPDATE PRODUCT QUANTITY
@app.route('/update_quantity/<user_id>/<item_name>/<int:quantity>', methods=['PUT'])
def update_quantity(user_id,item_name,quantity):
    item=session.query(items).filter(items.user_id==user_id, items.item_name==item_name).first()
    item.item_quantity=quantity
    session.commit()
    response  = jsonify({'message' : 'Item quantity updated successfully!'})
    return response

#VIEW CART DETAILS
@app.route('/get_cart_details/<user_id>', methods=['GET'])
def get_cart_details(user_id):
    cart=session.query(items).filter(items.user_id==user_id).all()
    output=[]
    sum=0
    for item in cart:
        cart_data={}
        cart_data['item_name']=item.item_name
        cart_data['item_quantity']=item.item_quantity
        cart_data['item_price']=item.item_price
        sum+=item.item_price*item.item_quantity
        output.append(cart_data)
    
    response = jsonify({'ITEMS' : output, 'Total Amount' : sum})
    return response


    
if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5002, debug=True)
