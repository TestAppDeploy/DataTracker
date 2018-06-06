import random
from flask import Flask, render_template
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__, static_folder='../static/dist', template_folder='../static/client')

@app.route('/dashboard/')
def show_dashboard():
    plots = []
    plots.append(make_plot())

    return render_template('dashboard.html', plots=plots)

def make_plot():
    plot = figure(plot_height=300, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div

if __name__ == '__main__':
    app.run(debug=True)
