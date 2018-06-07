from flask import Flask, render_template, jsonify, request
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models.sources import AjaxDataSource
from bokeh.models import ColumnDataSource, CDSView, IndexFilter
from fred import Fred
import sys
fr = Fred(api_key='9191e886eb8b7e932d92df410fbf0c9e',response_type='df')


app = Flask(__name__, static_folder='../static/dist', template_folder='../static/client')

def make_plot():
    plot = figure(plot_height=250, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div

def make_plot2():
    plot = figure(plot_height=250, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div

def make_plot3():
    plot = figure(plot_height=250, sizing_mode='scale_width')

    x = [0, 10, 25, 35, 42, 52, 66, 77, 88, 92]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div

def chart():

    fruits = ['A', 'P', 'N', 'B', 'V', 'C', 'D']
    plot = figure(x_range=fruits, plot_height=250, title="Company Performance", sizing_mode='scale_width')
    plot.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9)

    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0

    script, div = components(plot)
    return script, div

    #return render_template("chart.html",)

x, y = 0, 0

@app.route('/data/', methods=['POST'])
def data():
    global x, y
    x += 1
    y = x//1.3
    return jsonify(x=[x], y=[y])

def make_ajax_plot():
    source = AjaxDataSource(data_url=request.url_root + 'data/',
                            polling_interval=20000, mode='append')

    source.data = dict(x=[], y=[])

    plot = figure(x_range=[0,1000], y_range=[10, 2000], plot_height=250, sizing_mode='scale_width')
    plot.line('x', 'y', source=source, line_width=4)

    script, div = components(plot)
    return script, div

params = {
'tag_group_id':'gen',
'limit':10,
'exclude_tag_names':'services',
'sort_order':'asc'
}

res = fr.series.tags('GNPCA')

res1 = res['series_count']
print (res1)

def fred_plot():

#    x=[res['popularity']]
#    y=[res['series_count']]


    plot = figure(x_range=[0,1000], y_range=[0, 200000], plot_height=250, sizing_mode='scale_width')
    plot.line(source=res, x='popularity', y='series_count', line_width=4)



    script, div = components(plot)
    return script, div

@app.route('/dashboard/')
def show_dashboard():
    plots = []
    plots.append(fred_plot())
    plots.append(make_ajax_plot())
    plots.append(make_plot())
    plots.append(make_plot2())
    plots.append(make_plot3())
    plots.append(chart())

    return render_template('index.html', plots=plots)









if __name__ == '__main__':
    app.run(debug=True)
