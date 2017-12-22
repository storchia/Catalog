from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Products

app = Flask(__name__)

engine = create_engine('sqlite:///catalogpage.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Categories).all()
    return render_template('categories.html', categories=categories)

# Create New Categories
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        new_category = Categories(name=request.form['categname'])
        session.add(new_category)
        session.commit()
        flash("New Category Created!")
        return redirect(url_for('showCategories'))
    else:
        return render_template("newcategory.html")

# Edit Category
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])

def editCategory(category_id):
    editedcateg = session.query(Categories).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['editcategname']:
            editedcateg.name = request.form['editcategname']
        session.add(editedcateg)
        session.commit()
        flash("Category has Successfully been Edited!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html',
                               category_id=category_id, categ=editedcateg)

# Delete Category
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    deletedcateg = session.query(Categories).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(deletedcateg)
        session.commit()
        flash("Category has Successfully been Deleted!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('deletecategory.html',
                               category_id=category_id, categ=deletedcateg)

# All Products for selected Category
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/products/')
def showProducts(category_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    prods = session.query(Products).filter_by(category_id=category.id)
    return render_template("products.html", category=category, prods=prods)

# Create New Product
@app.route('/categories/<int:category_id>/products/new/',
           methods=['GET', 'POST'])
def newProduct(category_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    if request.method == 'POST':
        newprod = Products(name=request.form['prodname'],
                           description=request.form['proddesc'],
                           category_id=category_id)
        session.add(newprod)
        session.commit()
        flash("New Product Created!")
        return redirect(url_for('showProducts', category_id=category_id))
    else:
        return render_template("newproduct.html", category_id=category_id)

# Edit Product
@app.route('/categories/<int:category_id>/products/<int:id>/edit/',
           methods=['GET', 'POST'])
def editProduct(category_id, id):
    editingprod = session.query(Products).filter_by(id=id).one()
    if request.method == 'POST':
        if request.form['editprodname']:
            editingprod.name = request.form['editprodname']
        if request.form['editproddesc']:
            editingprod.description = request.form['editproddesc']
        session.add(editingprod)
        session.commit()
        flash("Product has successfully been Edited!")
        return redirect(url_for('showProducts', category_id=category_id))
    else:
        return render_template("editproduct.html",
                               category_id=category_id,
                               id=id, editingprod=editingprod)

# Delete Product
@app.route('/categories/<int:category_id>/products/<int:id>/delete/',
           methods=['GET', 'POST'])
def deleteProduct(category_id, id):
    deletingprod = session.query(Products).filter_by(id=id).one()
    if request.method == 'POST':
        session.delete(deletingprod)
        session.commit()
        flash("Product has Successfully been Deleted!")
        return redirect(url_for('showProducts', category_id=category_id))
    else:
        return render_template("deleteproduct.html",
                               category_id=category_id,
                               id=id, deletingprod=deletingprod)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
