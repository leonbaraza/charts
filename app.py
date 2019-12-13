from flask import Flask, render_template
import pygal
import psycopg2

app = Flask(__name__)


@app.route('/')
def hello_world():
    x = 'Leon'
    return render_template('index.html', x=x)

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

    cur.execute("""SELECT (sum(i.buying_price * s.quatity)) as subtotal, EXTRACT(MONTH FROM s.created_at) as sales_month 
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
