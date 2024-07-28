# import mysql.connector

# mydb = mysql.connector.connect(
# host='localhost', user='root', passwd='Anisid@684', database='inventory')

# mycursor = mydb.cursor()

# mycursor.execute("create database inventory")
# mycursor.execute("")

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Anisid@684'
app.config['MYSQL_DB'] = 'billing'


mydb = MySQL(app)

print(mydb)


# test route
@app.route('/')
def home():
    return render_template('home.html')


# add product
@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    msg = ''
    if request.method == 'POST':
        product = request.form['product']
        company = request.form['company']
        cp = request.form['cp']
        sp = request.form['sp']
        print(type(cp))
        print(type(product))
        cp1 = float(cp)
        sp1 = float(sp)
        print(type(cp1))
        print(type(sp1))
        cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into product(product_name,company_name,cprice,sprice) values('%s','%s','%f','%f')" % (
            product, company, cp1, sp1))

        mydb.connection.commit()
        msg = 'You have successfully registered'
    return render_template('addproduct.html', msg=msg)


# view products
@app.route('/viewproducts', methods=['GET'])
def viewproducts():
    cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from product')
    res = cursor.fetchall()
    print(res)

    return render_template('viewproduct.html', res=res, z=len(res))


# add customer
@app.route('/addcustomer', methods=['GET', 'POST'])
def addcustomer():
    msg = ''
    if request.method == 'POST':
        cname = request.form['cname']
        ccity = request.form['ccity']
        cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "insert into customer(customer_name,customer_city) values('%s','%s')" % (cname, ccity))
        mydb.connection.commit()
        msg = 'You have successfully registered'
    return render_template('addcustomer.html', msg=msg)


# view customer
@app.route('/viewcustomer', methods=['GET'])
def viewcustomer():
    cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from customer')
    res = cursor.fetchall()
    print(res)
    return render_template('viewcustomer.html', res=res, z=len(res))


# purchase item
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    msg = ""
    cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from product')
    res = cursor.fetchall()
    if request.method == 'POST':
        itempd = request.form['pitems']
        pdate = request.form['pdate']
        pqty = request.form['qty']
        cursor.execute(
            'select company_name from product where product_name= "%s"' % (itempd))
        cmp = cursor.fetchall()
        cursor.execute(
            'select cprice from product where product_name= "%s"' % (itempd))
        cost_price = cursor.fetchall()
        print(cost_price[0]['cprice'])
        print(cmp[0]['company_name'])
        print(pqty)
        print(pdate)
        print(itempd)
        cursor.execute(
            "insert into purchase(pditem,cname,cprice,qty,pdate) values('%s','%s','%f','%f','%s')" % (itempd, cmp[0]['company_name'], float(cost_price[0]['cprice']), int(pqty), pdate))
        mydb.connection.commit()
        msg = 'You have successfully registered'

    return render_template('purchaseitem.html', res=res, z=len(res), msg=msg)


# view purchase
@app.route('/viewpurchase', methods=['GET'])
def viewpurchase():
    cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from purchase')
    res = cursor.fetchall()
    print(res)
    return render_template('viewpurchase.html', res=res, z=len(res))


# Sell item
@app.route('/addorder', methods=['GET', 'POST'])
def order():
    msg = ""
    cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from product')
    res = cursor.fetchall()
    cursor.execute('select * from customer')
    res2 = cursor.fetchall()
    if request.method == 'POST':
        itemsd = request.form['sitem']
        odate = request.form['odate']
        oqty = request.form['oqty']
        customer_name = request.form['scust']
        cursor.execute(
            'select sprice from product where product_name= "%s"' % (itemsd))
        selling_price = cursor.fetchall()
        print(selling_price[0]['sprice'])
        cursor.execute(
            "insert into orders(cname,pname,sprice,qty,odate) values('%s','%s','%f','%f','%s')" % (itemsd, customer_name, float(selling_price[0]['sprice']), int(oqty), odate))
        mydb.connection.commit()
        msg = 'You have successfully registered'

    return render_template('sellitem.html', res=res, z=len(res), msg=msg, res2=res2, z2=len(res2))


# View orders
@app.route('/vieworders', methods=['GET'])
def vieworder():
    cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from orders')
    res = cursor.fetchall()
    print(res)
    return render_template('vieworders.html', res=res, z=len(res))


'''
@app.route('/viewsales')

@app.route('/viewtotalpurchases')

@app.route('/viewprofits')
'''

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
