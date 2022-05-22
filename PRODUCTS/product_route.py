import uuid
import config
from config import session
from model import Products as prods
from flask import Flask, request, jsonify

session=session()

app = Flask(__name__)
app.config['SECRET_KEY']=config.SECRET_KEY

#GET ALL PRODUCTS
@app.route('/get_product',methods=['GET'])
def get_product():
    products=session.query(prods).all()
    output = []
    for product in products:
        prod_data = {}
        prod_data['prod_name'] = product.prod_name
        prod_data['prod_quantity'] = product.prod_quantity
        prod_data['prod_price'] = product.prod_price
        prod_data['prod_category'] = product.prod_category
        prod_data['prod_rating'] = product.prod_rating
        output.append(prod_data)

    response = jsonify({'PRODUCTS' : output})
    return response

#GET ALL PRODUCT BY PRODUCT NAME
@app.route('/get_product_by_name/<prod_name>',methods=['GET'])
def get_product_by_name(prod_name):
    product=session.query(prods).filter(prods.prod_name==prod_name).first()
    prod_data = {}
    prod_data['prod_name'] = product.prod_name
    prod_data['prod_quantity'] = product.prod_quantity
    prod_data['prod_price'] = product.prod_price
    prod_data['prod_category'] = product.prod_category
    prod_data['prod_rating'] = product.prod_rating

    response = jsonify(prod_data)
    return response

#GET ALL PRODUCTS UNDER A PARTICULAR CATEGORY
@app.route('/get_product/<prod_category>',methods=['GET'])
def get_product_category(prod_category):
    products=session.query(prods).filter(prods.prod_category==prod_category).all()
    output = []
    for product in products:
        prod_data = {}
        prod_data['prod_name'] = product.prod_name
        prod_data['prod_quantity'] = product.prod_quantity
        prod_data['prod_price'] = product.prod_price
        prod_data['prod_category'] = product.prod_category
        prod_data['prod_rating'] = product.prod_rating
        output.append(prod_data)

    response = jsonify({'PRODUCTS' : output})
    return response


#GET ALL PRODUCTS IN A PARTICULAR PRICE RANGE
@app.route('/price_filter', methods=['GET'])
def prod_by_price_filter():
    data=request.get_json()
    prod=session.query(prods).filter(prods.prod_price.between(data['low_price'],data['high_price'])).order_by(prods.prod_price.asc()).all()
    output = []
    for product in prod:
        prod_data = {}
        prod_data['prod_name'] = product.prod_name
        prod_data['prod_quantity'] = product.prod_quantity
        prod_data['prod_price'] = product.prod_price
        prod_data['prod_category'] = product.prod_category
        prod_data['prod_rating'] = product.prod_rating
        output.append(prod_data)

    response = jsonify({'prods' : output})
    return response


#GET ALL PRODUCTS SORTED BY RATING
@app.route('/sort_by_rating', methods=['GET'])
def sort_by_rating():
    data=request.get_json()
    prod=session.query(prods).filter(prods.prod_category==data['prod_category']).order_by(prods.prod_rating.desc()).all()
    output = []
    for product in prod:
        prod_data = {}
        prod_data['prod_name'] = product.prod_name
        prod_data['prod_quantity'] = product.prod_quantity
        prod_data['prod_price'] = product.prod_price
        prod_data['prod_category'] = product.prod_category
        prod_data['prod_rating'] = product.prod_rating
        output.append(prod_data)

    response = jsonify({'prods' : output})
    return response

#GET ALL PRODUCTS SORTED BY PRICE
@app.route('/sort_by_price', methods=['GET'])
def sort_by_price():
    data=request.get_json()
    prod=session.query(prods).filter(prods.prod_category==data['prod_category']).order_by(prods.prod_price.desc()).all()
    output = []
    for product in prod:
        prod_data = {}
        prod_data['prod_name'] = product.prod_name
        prod_data['prod_quantity'] = product.prod_quantity
        prod_data['prod_price'] = product.prod_price
        prod_data['prod_category'] = product.prod_category
        prod_data['prod_rating'] = product.prod_rating
        output.append(prod_data)

    response = jsonify({'PRODUCTS' : output})
    return response

#ADD PRODUCT IN A PRODUCT DATABASE
@app.route('/add_product', methods=['POST'])
def add_product():

    data = request.get_json()
    print(data)
    new_prod = prods(
            prod_id=uuid.uuid4(),prod_name=data["prod_name"],
            prod_quantity=data['prod_quantity'], prod_price=data['prod_price'], 
            prod_category=data['prod_category'],prod_rating=data['prod_rating']
            )
    session.add(new_prod)
    session.commit()

    response  = jsonify({'message' : 'New product added!'})
    return response

#UPDATE PRODUCT QUANTITY IN DATABASE
@app.route('/update_quantity/<prod_name>/<int:prod_quantity>', methods=['PUT'])
def update_product(prod_name,prod_quantity):
    prod=session.query(prods).filter(prods.prod_name==prod_name).first()
    quantity_db = prod.prod_quantity
    prod.prod_quantity = quantity_db - prod_quantity
    session.commit()
    response  = jsonify({'message' : 'Product quantity updated successfully!'})
    return response


#DELETE PRODUCT FROM DATABSE
@app.route('/delete_prod', methods=['DELETE'])
def delete_prod():
    data=request.get_json()
    try:
        prod=session.query(prods).filter(prods.prod_name==data['prod_name']).first()
        if not prod:
            response = jsonify({'message' : 'This product does not exist in the list.'})
            return response
        session.delete(prod)
        session.commit()
        response= jsonify({'message' : 'Product has been deleted!'})
    except Exception as error:
        response = jsonify({'message':'Some error occured!!!'})
        
    return response



if __name__ == '__main__':

    app.run(host='127.0.0.1', port=5001, debug=True)