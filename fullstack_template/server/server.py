from flask import Flask, render_template, jsonify, request
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models.sources import AjaxDataSource
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, Title
from fred import Fred
import sys
fr = Fred(api_key='9191e886eb8b7e932d92df410fbf0c9e',response_type='df')


app = Flask(__name__, static_folder='../static/dist', template_folder='../static/client')

#Define Graph Data Source
Urban_Index = fr.series.observations('CPIAUCSL')
Real_GDP = fr.series.observations('A191RL1Q225SBEA')


#Create Graph
def fred_plot1():

    plot = figure(y_range=[0, 280], plot_height=300, x_axis_type='datetime', sizing_mode='scale_width')
    plot.line(source=Urban_Index, x='date', y='value',  line_width=4)

    plot.xaxis.axis_label = "Year"
    plot.xaxis.axis_label_standoff = 10
    plot.xaxis.axis_label_text_font_style = "normal"
    plot.yaxis.axis_label = "Index 1982-1984=100"
    plot.xaxis.axis_label_standoff = 10
    plot.yaxis.axis_label_text_font_style = "normal"

    plot.add_layout(Title(text="Consumer Price Index for All Urban Consumers", align="center"), "above")

    script, div = components(plot)
    return script, div

def fred_plot():

    plot = figure(y_range=[-15, 20], plot_height=300, x_axis_type='datetime', sizing_mode='scale_width')
    plot.line(source=Real_GDP, x='date', y='value',  line_width=2)

    plot.xaxis.axis_label = "Year"
    plot.xaxis.axis_label_standoff = 10
    plot.xaxis.axis_label_text_font_style = "normal"
    plot.yaxis.axis_label = "% Change from Preceding Period"
    plot.xaxis.axis_label_standoff = 10
    plot.yaxis.axis_label_text_font_style = "normal"

    plot.add_layout(Title(text="Real GDP", align="center"), "above")

    script, div = components(plot)
    return script, div





#Render Webpage#
@app.route('/dashboard/')
def show_dashboard():
    plots = []
#Call Graph Function
    plots.append(fred_plot())
    plots.append(fred_plot1())

    return render_template('index.html', plots=plots)









if __name__ == '__main__':
    app.run(debug=True)
