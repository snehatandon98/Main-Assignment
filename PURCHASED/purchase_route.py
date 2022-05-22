import uuid
import config
from config import session
from model import Purchased as purchase
from flask import Flask, request, jsonify

session=session()

app = Flask(__name__)
app.config['SECRET_KEY']=config.SECRET_KEY

#ADD INVOICE DETAILS IN DATABASE
@app.route('/checkout/<user_id>/<prod_name>/<prod_quantity>/<int:amount>',methods=['POST'])
def checkout(user_id,prod_name,prod_quantity,amount):
    invoice=purchase(invoice_id=uuid.uuid4(),user_id=user_id,prod_name=prod_name,prod_quantity=prod_quantity,total_amount_paid=amount)
    session.add(invoice)
    session.commit()

    response  = jsonify({'message' : 'Invoice added!'})
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
