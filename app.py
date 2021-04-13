from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'World'})


basedir = os.path.abspath(os.path.dirname(__file__))

# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    desc = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    # invoke constructor
    def __init__(self, name, desc, price, qty):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desc', 'price', 'qty')


# init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# create route
@app.route('/product', methods=['post'])
def add_product():
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, desc, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# get all products
@app.route('/product', methods=['GET'])
def get_products():
    x = ""
    pro = ""
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    print(type(result))
    print(result)
    return jsonify(result)


# run server
if __name__ == '__main__':
    app.run(debug=True)
