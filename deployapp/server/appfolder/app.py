from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import row, widgetbox
from bokeh.embed import components
from bokeh.models.sources import AjaxDataSource
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, Title, TapTool, HoverTool, CustomJS, Slider
from fred import Fred
import os


project_dir = os.path.dirname(os.path.abspath(__file__))



app = Flask(__name__, static_folder='../../static/dist', template_folder='../../static/client')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'



db = SQLAlchemy(app)

fr = Fred(api_key='9191e886eb8b7e932d92df410fbf0c9e',response_type='df')

#Render Webpage#
@app.route('/', methods=['GET', 'POST'])

def show_dashboard():
    if (request.form and request.form['select'] == '1'):
        api = request.form['api']
        datasource= fr.series.observations(api)
        labelsource= fr.series.details(api)
        datasource.to_sql('Graph1', con=db.engine, index=False, if_exists='replace')
        labelsource.to_sql('Labels', con=db.engine, index=False, if_exists='replace')

    dataframe=pd.read_sql('Graph1', con=db.engine)
    labelframe=pd.read_sql('Labels', con=db.engine)

    def graph1():

                y_axis_low=(min(dataframe['value']) - (min(dataframe['value']) * 5))
                y_axis_high=(max(dataframe['value']) + (max(dataframe['value']) * 1.3))

                plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
                plot.line(x=dataframe['date'], y=dataframe['value'], line_width=2)

                plot.toolbar.logo = None
                plot.xaxis.axis_label = "Year"
                plot.xaxis.axis_label_standoff = 10
                plot.xaxis.axis_label_text_font_style = "normal"
                plot.yaxis.axis_label = labelframe['units'].iloc[0]
                plot.xaxis.axis_label_standoff = 10
                plot.yaxis.axis_label_text_font_style = "normal"
                plot.add_tools(hover)

                plot.add_layout(Title(text=labelframe['title'].iloc[0], align="center"), "above")

                script, div = components(plot)
                return script, div

    if (request.form and request.form['select'] == '2'):
        api2 = request.form['api']
        datasource2= fr.series.observations(api2)
        labelsource2= fr.series.details(api2)
        datasource2.to_sql('Graph2', con=db.engine, index=False, if_exists='replace')
        labelsource2.to_sql('Labels2', con=db.engine, index=False, if_exists='replace')

    dataframe2=pd.read_sql('Graph2', con=db.engine)
    labelframe2=pd.read_sql('Labels2', con=db.engine)

    def graph2():

                y_axis_low=(min(dataframe2['value']) - (min(dataframe2['value']) * 5))
                y_axis_high=(max(dataframe2['value']) + (max(dataframe2['value']) * 1.3))

                plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
                plot.line(x=dataframe2['date'], y=dataframe2['value'], line_width=2)

                plot.toolbar.logo = None
                plot.xaxis.axis_label = "Year"
                plot.xaxis.axis_label_standoff = 10
                plot.xaxis.axis_label_text_font_style = "normal"
                plot.yaxis.axis_label = labelframe2['units'].iloc[0]
                plot.xaxis.axis_label_standoff = 10
                plot.yaxis.axis_label_text_font_style = "normal"
                plot.add_tools(hover)

                plot.add_layout(Title(text=labelframe2['title'].iloc[0], align="center"), "above")

                script, div = components(plot)
                return script, div

    if (request.form and request.form['select'] == '3'):
        api3 = request.form['api']
        datasource3= fr.series.observations(api3)
        labelsource3= fr.series.details(api3)
        datasource3.to_sql('Graph3', con=db.engine, index=False, if_exists='replace')
        labelsource3.to_sql('Labels3', con=db.engine, index=False, if_exists='replace')

    dataframe3=pd.read_sql('Graph3', con=db.engine)
    labelframe3=pd.read_sql('Labels3', con=db.engine)

    def graph3():

                y_axis_low=(min(dataframe3['value']) - (min(dataframe3['value']) * 5))
                y_axis_high=(max(dataframe3['value']) + (max(dataframe3['value']) * 1.3))

                plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
                plot.line(x=dataframe3['date'], y=dataframe3['value'], line_width=2)

                plot.toolbar.logo = None
                plot.xaxis.axis_label = "Year"
                plot.xaxis.axis_label_standoff = 10
                plot.xaxis.axis_label_text_font_style = "normal"
                plot.yaxis.axis_label = labelframe3['units'].iloc[0]
                plot.xaxis.axis_label_standoff = 10
                plot.yaxis.axis_label_text_font_style = "normal"
                plot.add_tools(hover)

                plot.add_layout(Title(text=labelframe3['title'].iloc[0], align="center"), "above")

                script, div = components(plot)
                return script, div

    if (request.form and request.form['select'] == '4'):
        api4 = request.form['api']
        datasource4= fr.series.observations(api4)
        labelsource4= fr.series.details(api4)
        datasource4.to_sql('Graph4', con=db.engine, index=False, if_exists='replace')
        labelsource4.to_sql('Labels4', con=db.engine, index=False, if_exists='replace')

    dataframe4=pd.read_sql('Graph4', con=db.engine)
    labelframe4=pd.read_sql('Labels4', con=db.engine)

    def graph4():

                y_axis_low=(min(dataframe4['value']) - (min(dataframe4['value']) * 5))
                y_axis_high=(max(dataframe4['value']) + (max(dataframe4['value']) * 1.3))

                plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
                plot.line(x=dataframe4['date'], y=dataframe4['value'], line_width=2)

                plot.toolbar.logo = None
                plot.xaxis.axis_label = "Year"
                plot.xaxis.axis_label_standoff = 10
                plot.xaxis.axis_label_text_font_style = "normal"
                plot.yaxis.axis_label = labelframe4['units'].iloc[0]
                plot.xaxis.axis_label_standoff = 10
                plot.yaxis.axis_label_text_font_style = "normal"
                plot.add_tools(hover)

                plot.add_layout(Title(text=labelframe4['title'].iloc[0], align="center"), "above")

                script, div = components(plot)
                return script, div

    if (request.form and request.form['select'] == '5'):
        api5 = request.form['api']
        datasource5= fr.series.observations(api5)
        labelsource5= fr.series.details(api5)
        datasource5.to_sql('Graph5', con=db.engine, index=False, if_exists='replace')
        labelsource5.to_sql('Labels5', con=db.engine, index=False, if_exists='replace')

    dataframe5=pd.read_sql('Graph5', con=db.engine)
    labelframe5=pd.read_sql('Labels5', con=db.engine)

    def graph5():

                y_axis_low=(min(dataframe5['value']) - (min(dataframe5['value']) * 5))
                y_axis_high=(max(dataframe5['value']) + (max(dataframe5['value']) * 1.3))

                plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
                plot.line(x=dataframe5['date'], y=dataframe5['value'], line_width=2)

                plot.toolbar.logo = None
                plot.xaxis.axis_label = "Year"
                plot.xaxis.axis_label_standoff = 10
                plot.xaxis.axis_label_text_font_style = "normal"
                plot.yaxis.axis_label = labelframe5['units'].iloc[0]
                plot.xaxis.axis_label_standoff = 10
                plot.yaxis.axis_label_text_font_style = "normal"
                plot.add_tools(hover)

                plot.add_layout(Title(text=labelframe5['title'].iloc[0], align="center"), "above")

                script, div = components(plot)
                return script, div

    if (request.form and request.form['select'] == '6'):
        api6 = request.form['api']
        datasource6= fr.series.observations(api6)
        labelsource6= fr.series.details(api6)
        datasource6.to_sql('Graph6', con=db.engine, index=False, if_exists='replace')
        labelsource6.to_sql('Labels6', con=db.engine, index=False, if_exists='replace')

    dataframe6=pd.read_sql('Graph6', con=db.engine)
    labelframe6=pd.read_sql('Labels6', con=db.engine)

    def graph6():

                y_axis_low=(min(dataframe6['value']) - (min(dataframe6['value']) * 5))
                y_axis_high=(max(dataframe6['value']) + (max(dataframe6['value']) * 1.3))

                plot = figure(y_range=[y_axis_low, y_axis_high], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
                plot.line(x=dataframe6['date'], y=dataframe6['value'], line_width=2)

                plot.toolbar.logo = None
                plot.xaxis.axis_label = "Year"
                plot.xaxis.axis_label_standoff = 10
                plot.xaxis.axis_label_text_font_style = "normal"
                plot.yaxis.axis_label = labelframe6['units'].iloc[0]
                plot.xaxis.axis_label_standoff = 10
                plot.yaxis.axis_label_text_font_style = "normal"
                plot.add_tools(hover)

                plot.add_layout(Title(text=labelframe6['title'].iloc[0], align="center"), "above")

                script, div = components(plot)
                return script, div
    plots = []

    if graph1():
        plots.append(graph1())
    if graph2():
        plots.append(graph2())
    if graph3():
        plots.append(graph3())
    if graph4():
        plots.append(graph4())
    if graph5():
        plots.append(graph5())
    if graph6():
        plots.append(graph6())

    return render_template('index.html', plots=plots)




#    print(Graph.query.with_entities(Graph.date).first())




        #title = Graph(title=str(fr.series.details(api).title.values).replace("[", "").replace("]", "").replace("''", "").replace("'", ""))

        #title= str(fr.series.details(api).title.values)
        #title=title.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        #y_axis_label = Graph(y_axis_label=str(fr.series.details(api).units.values).replace("[", "").replace("]", "").replace("''", "").replace("'", ""))
        #y_axis_label=y_axis_label.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        #y_axis_low=Graph(y_axis_low=(min(fr.series.observations(api)['value']) - (min(fr.series.observations(api)['value']) * 5)))
        #y_axis_high=Graph(y_axis_high=(max(fr.series.observations(api)['value']) + (max(fr.series.observations(api)['value']) * 1.3)))

        #db.session.add(id)


        #db.session.add(title)
        #db.session.add(y_axis_label)
        #db.session.add(y_axis_low)
        #db.session.add(y_axis_high)
        #db.session.commit()

        #multiple= float(request.form['multiple'])
        #datasource['value']*=multiple





#Tool Parameters

hover = HoverTool(tooltips=[
("Date", "@x{%F}"),  ("Value", "@y"), ],
 formatters={
        '@x' : 'datetime', # use 'datetime' formatter for 'date' field
    })


if __name__ == '__main__':
    app.run(debug=True)
    freezer.freeze()
    from elsa import cli
    cli(app, base_url='http://datatracker.github.io')
