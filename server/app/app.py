from flask import Flask, render_template, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import send_from_directory
from decimal import Decimal
import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import row, widgetbox
from bokeh.embed import components
from bokeh.models.sources import AjaxDataSource
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, Title, TapTool, HoverTool, CustomJS, Slider
from fred import Fred
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, DATA, DOCUMENTS
import sys

app = Flask(__name__, static_folder='../../static/dist', template_folder='../../static/client')
db = SQLAlchemy(app)

from config import Config

app.config.from_object(Config)

migrate = Migrate(app, db)

UPLOAD_FOLDER = './Uploads'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xml', 'json'])

fr = Fred(api_key='9191e886eb8b7e932d92df410fbf0c9e',response_type='df')

data = UploadSet('data', DATA)

app.config['UPLOADED_DATA_DEST'] = './Uploads'
configure_uploads(app, data)


#Define Graph Data Source
Urban_Index = fr.series.observations('CPIAUCSL')
Real_GDP = fr.series.observations('A191RL1Q225SBEA')
SQLdata = pd.DataFrame(fr.series.observations('A191RL1Q225SBEA'))
SQLdata.to_sql('users', con=engine)

#Create Graph
def Urban_Index_Plot():

    plot = figure(y_range=[0, 280], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
    plot.line(source=Urban_Index, x='date', y='value',  line_width=4)

    plot.toolbar.logo = None
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

    plot.toolbar.logo = None
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

    if 'select' in request.form:
        if (request.method == 'POST'):
            api= request.form['api']
            datasource= fr.series.observations(api)
            title= str(fr.series.details(api).title.values)
            title=title.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
            y_axis_label = str(fr.series.details(api).units.values)
            y_axis_label=y_axis_label.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
            y_axis_low=min(fr.series.observations(api)['value']) - (min(fr.series.observations(api)['value']) * 5)
            y_axis_high=max(fr.series.observations(api)['value']) + (max(fr.series.observations(api)['value']) * 1.5)

            #multiple= float(request.form['multiple'])
            #datasource['value']*=multiple

            plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
            plot.line(source=datasource, x='date', y='value',  line_width=2)

            plot.toolbar.logo = None
            plot.xaxis.axis_label = "Year"
            plot.xaxis.axis_label_standoff = 10
            plot.xaxis.axis_label_text_font_style = "normal"
            plot.yaxis.axis_label = y_axis_label
            plot.xaxis.axis_label_standoff = 10
            plot.yaxis.axis_label_text_font_style = "normal"
            plot.add_tools(hover)

            plot.add_layout(Title(text=title, align="center"), "above")

            script, div = components(plot)
            return script, div
        else:
            return print('string')
    else:
        return print('some_plot did not run')



def some_plot1():
    if 'select' in request.form:
        if (request.method == 'POST' and request.form['select'] == '2'):
            api= request.form['api']
            datasource= fr.series.observations(api)
            title= str(fr.series.details(api).title.values)
            title=title.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
            y_axis_label = str(fr.series.details(api).units.values)
            y_axis_label=y_axis_label.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
            y_axis_low=min(fr.series.observations(api)['value']) - (min(fr.series.observations(api)['value']) * 5)
            y_axis_high=max(fr.series.observations(api)['value']) + (max(fr.series.observations(api)['value']) * 1.5)

            multiple= float(request.form['multiple'])
            datasource['value']*=multiple

            plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
            plot.line(source=datasource, x='date', y='value',  line_width=2)

            plot.toolbar.logo = None
            plot.xaxis.axis_label = "Year"
            plot.xaxis.axis_label_standoff = 10
            plot.xaxis.axis_label_text_font_style = "normal"
            plot.yaxis.axis_label = y_axis_label
            plot.xaxis.axis_label_standoff = 10
            plot.yaxis.axis_label_text_font_style = "normal"
            plot.add_tools(hover)

            plot.add_layout(Title(text=title, align="center"), "above")

            script, div = components(plot)
            return script, div
        else:
            return print('string')
    else:
        return print('some_plot1 did not run')




def file_plot():

    if (request.method == 'POST' and 'file' in request.files):

        file = request.files['file']

        filename = data.save(file)
        url = data.url(filename)

        datasource= pd.read_csv(url)

        print(datasource)


        datasource['CPIAUCSL'] = datasource['CPIAUCSL'].apply(pd.to_numeric, errors='coerce')
        #datasource['DGS10']= datasource[pd.notnull(datasource)]
        datasource = datasource.dropna(how='any')
        datasource['DATE']= pd.to_datetime(datasource['DATE'])
        y_axis_low=(float(datasource['CPIAUCSL'].min())) - (float(datasource['CPIAUCSL'].min() * 3))
        y_axis_high=(float(datasource['CPIAUCSL'].max())) + (float(datasource['CPIAUCSL'].max() * 1.5))


        plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
        plot.line(x=datasource['DATE'], y=datasource['CPIAUCSL'], line_width=2)

        plot.toolbar.logo = None
        plot.xaxis.axis_label = "Year"
        plot.xaxis.axis_label_standoff = 10
        plot.xaxis.axis_label_text_font_style = "normal"
        plot.xaxis.axis_label_standoff = 10
        plot.yaxis.axis_label_text_font_style = "normal"
        plot.add_tools(hover)

        #plot.add_layout(Title(text=title, align="center"), "above")

        script, div = components(plot)
        return script, div
    else:
        return print ('string')


#Render Webpage#
@app.route('/', methods=['GET', 'POST'])

def show_dashboard():
    plots = []
#Call Graph Function
    plots.append(Urban_Index_Plot())
    plots.append(Real_GDP_Plot())
    if some_plot():
        plots.append(some_plot())
    #if some_plot1():
    #    plots.append(some_plot1())
    #if file_plot():
    #    plots.append(file_plot())



    return render_template('index.html', plots=plots)

#Tool Parameters

hover = HoverTool(tooltips=[
("Date", "@date{'%F'}"),  ("Value", "@value"), ],
 formatters={
        'date' : 'datetime', # use 'datetime' formatter for 'date' field
    })






if __name__ == '__main__':
    app.run(debug=True)
