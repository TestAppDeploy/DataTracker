from flask import Flask, render_template, jsonify, request, send_from_directory
import datetime as datetime
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

#Create Table
class blank(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    date = db.Column(db.DateTime)
    value = db.Column(db.String(200))
    title = db.Column(db.String(200))
    y_axis_label = db.Column(db.String(200))
    y_axis_low = db.Column(db.Float)
    y_axis_high = db.Column(db.Float)

    def __repr__(self):
        return '<Graph %r>' % self.id




#Render Webpage#
@app.route('/', methods=['GET', 'POST'])

def show_dashboard():
    if (request.form):
        api = request.form['api']
        datasource= fr.series.observations(api)
        labelsource= fr.series.details(api)
        datasource.to_sql('Graph1', con=db.engine, index=False, if_exists='replace')
        labelsource.to_sql('Labels', con=db.engine, index=False, if_exists='replace')

    dataframe=pd.read_sql('Graph1', con=db.engine)
    labelframe=pd.read_sql('Labels', con=db.engine)

    print(labelframe['title'].iloc[0])

    def some_plot2():

                y_axis_low=(min(dataframe['value']) - (min(dataframe['value']) * 5))
                y_axis_high=(max(dataframe['value']) + (max(dataframe['value']) * 1.5))

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
    plots = []

    if some_plot2():
        plots.append(some_plot2())


    return render_template('index.html', plots=plots)




#    print(Graph.query.with_entities(Graph.date).first())




        #title = Graph(title=str(fr.series.details(api).title.values).replace("[", "").replace("]", "").replace("''", "").replace("'", ""))

        #title= str(fr.series.details(api).title.values)
        #title=title.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        #y_axis_label = Graph(y_axis_label=str(fr.series.details(api).units.values).replace("[", "").replace("]", "").replace("''", "").replace("'", ""))
        #y_axis_label=y_axis_label.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        #y_axis_low=Graph(y_axis_low=(min(fr.series.observations(api)['value']) - (min(fr.series.observations(api)['value']) * 5)))
        #y_axis_high=Graph(y_axis_high=(max(fr.series.observations(api)['value']) + (max(fr.series.observations(api)['value']) * 1.5)))

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
("Date", "@date{'%F'}"),  ("Value", "@value"), ],
 formatters={
        'date' : 'datetime', # use 'datetime' formatter for 'date' field
    })


if __name__ == '__main__':
    app.run(debug=True)
