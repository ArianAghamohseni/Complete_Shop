from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os


# INIT APP
app = Flask(__name__)

# CONFIG DATABASE
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# MODELS
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_path = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path


class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity


# CREATE MODELS IN DATABASE
with app.app_context():
    db.create_all()


# PRODUCT APIs
@app.route('/', methods=['GET'])
def index():
    products = Product.query.all()
    return render_template('product.html', products=products)


@app.route('/product', methods=['POST'])
def add_product():
    name = request.form.get("name")
    price = request.form.get("price")
    image_path = request.form.get("image_path")

    product = Product(name=name, price=price, image_path=image_path)
    db.session.add(product)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    product = Product.query.filter_by(id=product_id).first()
    cart_item = CartItem.query.filter_by(product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('index'))


# CART ITEM APIs
@app.route('/cart_item', methods=['GET'])
def cart():
    cart_items = CartItem.query.all()
    items = []
    for cart_item in cart_items:
        product = Product.query.filter_by(id=cart_item.product_id).first()
        cart_item.name = product.name
        cart_item.price = product.price
        items.append(cart_item)

    return render_template('cart.html', cart_items=items)


@app.route('/cart_item/total', methods=['GET'])
def cart_total():
    cart_items = CartItem.query.all()
    total = 0
    for cart_item in cart_items:
        item = Product.query.filter_by(id=cart_item.product_id).first()
        total += item.price * cart_item.quantity

    return {"total": total}


@app.route('/cart_item/<int:product_id>', methods=['POST'])
def add_item_to_cart(product_id: int):
    quantity = request.get_json()['quantity']
    cart_item = CartItem.query.filter_by(product_id=product_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
    else:
        cart_item = CartItem(product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/cart_item/<int:cart_item_id>', methods=['PUT'])
def edit_cart_item(cart_item_id: int):
    quantity = request.get_json()['quantity']
    cart_item = CartItem.query.filter_by(id=cart_item_id).first()
    cart_item.quantity = quantity
    db.session.commit()

    return redirect(url_for('cart'))


@app.route('/cart_item/<int:cart_item_id>', methods=['DELETE'])
def delete_cart_item(cart_item_id: int):
    cart_item = CartItem.query.filter_by(id=cart_item_id).first()
    db.session.delete(cart_item)
    db.session.commit()

    return redirect(url_for('cart'))


# RUN APP
if __name__ == '__main__':
    app.run(debug=True)
