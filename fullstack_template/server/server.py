from flask import Flask, render_template, jsonify, request
from decimal import Decimal
import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import row, widgetbox
from bokeh.embed import components
from bokeh.models.sources import AjaxDataSource
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, Title, TapTool, HoverTool, CustomJS, Slider
from fred import Fred
import sys
fr = Fred(api_key='9191e886eb8b7e932d92df410fbf0c9e',response_type='df')


app = Flask(__name__, static_folder='../static/dist', template_folder='../static/client')

#Define Graph Data Source
Urban_Index = fr.series.observations('CPIAUCSL')
Real_GDP = fr.series.observations('A191RL1Q225SBEA')

#Create Graph
def Urban_Index_Plot():

    plot = figure(y_range=[0, 280], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
    plot.line(source=Urban_Index, x='date', y='value',  line_width=4)

    plot.xaxis.axis_label = "Year"
    plot.xaxis.axis_label_standoff = 10
    plot.xaxis.axis_label_text_font_style = "normal"
    plot.yaxis.axis_label = "Index 1982-1984=100"
    plot.xaxis.axis_label_standoff = 10
    plot.yaxis.axis_label_text_font_style = "normal"
    plot.add_tools(hover)

    plot.add_layout(Title(text="Consumer Price Index for All Urban Consumers", align="center"), "above")

    script, div = components(plot)
    return script, div

def Real_GDP_Plot():

    plot = figure(y_range=[-15, 20], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
    plot.line(source=Real_GDP, x='date', y='value',  line_width=2)

    plot.xaxis.axis_label = "Year"
    plot.xaxis.axis_label_standoff = 10
    plot.xaxis.axis_label_text_font_style = "normal"
    plot.yaxis.axis_label = "% Change from Preceding Period"
    plot.xaxis.axis_label_standoff = 10
    plot.yaxis.axis_label_text_font_style = "normal"
    plot.add_tools(hover)

    plot.add_layout(Title(text="Real GDP", align="center"), "above")

    script, div = components(plot)
    return script, div

def some_plot():

    if (request.method == 'POST' and file_plot()==False):
        api= request.form['api']
        datasource= fr.series.observations(api)
        title= str(fr.series.details(api).title.values)
        title=title.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        y_axis_label = str(fr.series.details(api).units.values)
        y_axis_label=y_axis_label.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        y_axis_low=min(fr.series.observations(api)['value']) - (min(fr.series.observations(api)['value']) * 3)
        y_axis_high=max(fr.series.observations(api)['value']) + (max(fr.series.observations(api)['value']) * 1.5)


        plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
        plot.line(source=datasource, x='date', y='value',  line_width=2)

        plot.xaxis.axis_label = "Year"
        plot.xaxis.axis_label_standoff = 10
        plot.xaxis.axis_label_text_font_style = "normal"
        plot.yaxis.axis_label = y_axis_label
        plot.xaxis.axis_label_standoff = 10
        plot.yaxis.axis_label_text_font_style = "normal"
        plot.add_tools(hover)

        plot.add_layout(Title(text=title, align="center"), "above")

        some_plot.counter += 1

        script, div = components(plot)
        return script, div
    else:
        return print('string')

some_plot.counter = 0



def file_plot1():

        datasource= pd.read_csv('./DGS10(1).csv')

        datasource['DGS10'] = datasource['DGS10'].apply(pd.to_numeric, errors='coerce')
        #datasource['DGS10']= datasource[pd.notnull(datasource)]
        datasource= datasource.dropna(how='any')
        datasource['DATE']= pd.to_datetime(datasource['DATE'])
        y_axis_low=(float(datasource['DGS10'].min())) - (float(datasource['DGS10'].min() * 3))
        y_axis_high=(float(datasource['DGS10'].max())) + (float(datasource['DGS10'].max() * 1.5))


        plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
        plot.line(x=datasource['DATE'], y=datasource['DGS10'], line_width=2)

        plot.xaxis.axis_label = "Year"
        plot.xaxis.axis_label_standoff = 10
        plot.xaxis.axis_label_text_font_style = "normal"
        plot.xaxis.axis_label_standoff = 10
        plot.yaxis.axis_label_text_font_style = "normal"
        plot.add_tools(hover)

        #plot.add_layout(Title(text=title, align="center"), "above")

        script, div = components(plot)
        return script, div

def file_plot():

    if (request.method == 'POST'):
        file= request.form['file']
        datasource= pd.read_csv(file, index_col=False)
        title= str(file.title.values)
        title=title.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        y_axis_label = str(file.units.values)
        y_axis_label=y_axis_label.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        y_axis_low=min(file['value']) - min((file['value']) * 3)
        y_axis_high=max(file['value']) + max((file['value']) * 1.5)


        plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
        plot.line(source=datasource, x='date', y='value',  line_width=2)

        plot.xaxis.axis_label = "Year"
        plot.xaxis.axis_label_standoff = 10
        plot.xaxis.axis_label_text_font_style = "normal"
        plot.yaxis.axis_label = y_axis_label
        plot.xaxis.axis_label_standoff = 10
        plot.yaxis.axis_label_text_font_style = "normal"
        plot.add_tools(hover)

        plot.add_layout(Title(text=title, align="center"), "above")
        return print(file)
        script, div = components(plot)
        return script, div
    else:
        return print('string')


#Render Webpage#
@app.route('/', methods=['GET', 'POST'])

def show_dashboard():
    plots = []
#Call Graph Function
    plots.append(Urban_Index_Plot())
    plots.append(Real_GDP_Plot())
    plots.append(file_plot1())
    if some_plot():
        plots.append(some_plot())


    return render_template('index.html', plots=plots)

#Tool Parameters

hover = HoverTool(tooltips=[
("Date", "@date{'%F'}"),  ("Value", "@value"), ],
 formatters={
        'date' : 'datetime', # use 'datetime' formatter for 'date' field
    })






if __name__ == '__main__':
    app.run(debug=True)
