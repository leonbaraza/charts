from _ast import In
from idlelib.idle_test.test_iomenu import S

from flask import Flask, render_template, request, redirect, url_for, flash

import pygal

import psycopg2

from flask_sqlalchemy import SQLAlchemy
from Config.Config import Development


app = Flask(__name__)
app.config.from_object(Development)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Leon@1996@127.0.0.1:5432/sales_demo'
# app.config['SECRET_KEY'] = 'KenyaYetuMoja'
# app.config['DEBUG'] = True
db = SQLAlchemy(app)


from models.inventories import Inventories
from models.sales import Sales

@app.before_first_request
def create_tables():
    db.create_all()

# @app.route('/test/<num1>/<num2>')
# def test(num1,num2):
#
#     print(int(num1)+int(num2))
#     return 'Yes'

@app.route('/salepro/<int:id>', methods=['POST', 'GET'])
def makeSales(id):
    record = Inventories.fetch_one_record(id)
    if record:
        if request.method == 'POST':

            quantity = request.form['quantity']
            newStock = record.stock - int(quantity)

            record.stock = newStock
            db.session.commit()

            sales = Sales(inv_id=id, quantity = quantity)
            sales.add_records()

            flash('You successfully made a sale', 'success')

    return redirect(url_for('hello_world'))

@app.route('/viewsales/<int:id>')
def viewSales(id):

    record = Inventories.fetch_one_record(id)

    return render_template('viewsales.html', record=record)


@app.route('/')
def hello_world():
    x = 'Leon'
    records = Inventories.fetch_all_records()

    return render_template('index.html', records=records, x=x)

@app.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):
    record = Inventories.fetch_one_record(id)

    if request.method == 'POST':
        record.name = request.form['name']
        record.type = request.form['type']
        record.buying_price = request.form['bp']
        record.selling_price = request.form['sp']
        record.stock = request.form['Stock']

        db.session.commit()

        return redirect(url_for('hello_world'))

    return render_template('edit.html', record=record)


@app.route('/add_inventory', methods=['POST', 'GET'])
def add_inventory():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        buying_price = request.form['bp']
        selling_price = request.form['sp']
        stock = request.form['Stock']

        # print(name)
        # print(type)
        # print(buying_price)
        # print(selling_price)

        record = Inventories(name=name, type=type , buying_price=buying_price, selling_price=selling_price, stock=stock)
        record.add_records()

    # return 'Naibei'
    return redirect(url_for('hello_world'))

@app.route('/sale/<int:id>', methods=['POST','GET'])
def makeSale(id):
    rec = Inventories.fetch_one_record(id)

    if rec:
        if request.method == 'POST':
            newStock = rec.stock - int(request.form['quantity'])
            rec.stock = newStock
            db.session.commit()
        # saleRecord = Sales(inv_id=id, quantity=)
    return redirect(url_for('hello_world'))


@app.route('/delete/<int:id>')
def delete(id):
    record = Inventories.fetch_one_record(id)

    db.session.delete(record)
    db.session.commit()
    # flash('You have successfully deeted the inventory', 'danger')
    return  redirect(url_for('hello_world'))


@app.route('/dashboard')
def piechart():

    conn = psycopg2.connect("dbname='sales_demo' user='postgres' host='localhost' password='Leon@1996' ")

    ratios = [('Gentlemen', 5), ('Ladies',9)]
    ratios[0][0]
    # ratios1 = [{},{}]
    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add(ratios[0][0], ratios[0][1])
    pie_chart.add(ratios[1][0], ratios[1][1])
    # pie_chart.add('Chrome', 36.3)
    # pie_chart.add('Safari', 4.5)
    # pie_chart.add('Opera', 2.3)
    pie_data = pie_chart.render_data_uri()

    data = [
        {'month': 'January', 'total': 22},
        {'month': 'February', 'total': 27},
        {'month': 'March', 'total': 23},
        {'month': 'April', 'total': 20},
        {'month': 'May', 'total': 12},
        {'month': 'June', 'total': 32},
        {'month': 'July', 'total': 42},
        {'month': 'August', 'total': 72},
        {'month': 'September', 'total': 52},
        {'month': 'October', 'total': 42},
        {'month': 'November', 'total': 92},
        {'month': 'December', 'total': 102}
    ]
    cur = conn.cursor()

    cur.execute("""SELECT (sum(i.selling_price * s.quatity)) as subtotal, EXTRACT(MONTH FROM s.created_at) as sales_month 
    from sales as s 
    join inventories as i on s.inv_id = i.id
    GROUP BY sales_month
    ORDER BY sales_month
    """)

    rows = cur.fetchall()
    # print(type(rows))
    months = []
    total_sales = []

    for each in rows:
        months.append(each[1])
        total_sales.append(each[0])

    print(months)
    print(total_sales)

    graph = pygal.Line()
    graph.title = '% Change Coolness of programming languages over time.'
    graph.x_labels = months
    graph.add('Total Sales', total_sales)
    # graph.add('Java', [15, 45, 76, 80, 91, 95])
    # graph.add('C++', [5, 51, 54, 102, 150, 201])
    # graph.add('All others combined!', [5, 15, 21, 55, 92, 105])
    graph_data = graph.render_data_uri()
    # return render_template("graphing.html", graph_data=graph_data)

    return render_template('dashboard.html', pie_data=pie_data, graph_data=graph_data)



if __name__ == '__main__':
    app.run()