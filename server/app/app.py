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
database_file = "sqlite:///{}".format(os.path.join(project_dir, "app.db"))

app = Flask(__name__, static_folder='../../static/dist', template_folder='../../static/client')
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

fr = Fred(api_key='9191e886eb8b7e932d92df410fbf0c9e',response_type='df')

#Create Table
class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    date = db.Column(db.DateTime)
    value = db.Column(db.Float)
    title = db.Column(db.String(200))
    y_axis_label = db.Column(db.String(200))
    y_axis_low = db.Column(db.Float)
    y_axis_high = db.Column(db.Float)

    def __repr__(self):
        return '<Graph %r>' % self.id
#Create Table
#SQLdata.to_sql('User', con=db.engine, index=False, if_exists='replace')

#SQLdata = pd.DataFrame(fr.series.observations('A191RL1Q225SBEA'))



def some_plot2():
            plot = figure(y_range=[-100, 100], plot_height=350, x_axis_type='datetime', sizing_mode='scale_width')
            plot.line(x=Graph.query.with_entities(Graph.date).all(), y=Graph.query.with_entities(Graph.value).all(), line_width=2)

            plot.toolbar.logo = None
            plot.xaxis.axis_label = "Year"
            plot.xaxis.axis_label_standoff = 10
            plot.xaxis.axis_label_text_font_style = "normal"
            plot.yaxis.axis_label = 'Graph.query.with_entities(Graph.y_axis_label).first()'
            plot.xaxis.axis_label_standoff = 10
            plot.yaxis.axis_label_text_font_style = "normal"
            plot.add_tools(hover)

            plot.add_layout(Title(text='a'), "above")

            script, div = components(plot)
            return script, div


#Render Webpage#
@app.route('/', methods=['GET', 'POST'])

def show_dashboard():
    plots = []
#Call Graph Function
    if some_plot2():
        plots.append(some_plot2())

    if (request.form):
        api = request.form['api']
        datasource= fr.series.observations(api)
        #datasource.to_sql(name='Graph', con=database_file, if_exists='replace')
        print(datasource)
        #api_plot = Graph(apiCol=str(api))
    #    for d in datasource['date']
    #        d.dt
        date = Graph(date=datasource['date'].iloc[0])

        value = Graph(value= float(datasource['value'].iloc[0]))
        title = Graph(title=str(fr.series.details(api).title.values).replace("[", "").replace("]", "").replace("''", "").replace("'", ""))

        #title= str(fr.series.details(api).title.values)
        #title=title.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        y_axis_label = Graph(y_axis_label=str(fr.series.details(api).units.values).replace("[", "").replace("]", "").replace("''", "").replace("'", ""))
        #y_axis_label=y_axis_label.replace("[", "").replace("]", "").replace("''", "").replace("'", "")
        y_axis_low=Graph(y_axis_low=(min(fr.series.observations(api)['value']) - (min(fr.series.observations(api)['value']) * 5)))
        y_axis_high=Graph(y_axis_high=(max(fr.series.observations(api)['value']) + (max(fr.series.observations(api)['value']) * 1.5)))

        #db.session.add(id)
        db.session.add(date)
        db.session.add(value)
        db.session.add(title)
        db.session.add(y_axis_label)
        db.session.add(y_axis_low)
        db.session.add(y_axis_high)
        db.session.commit()

        #multiple= float(request.form['multiple'])
        #datasource['value']*=multiple

    return render_template('index.html', plots=plots)


#Tool Parameters

hover = HoverTool(tooltips=[
("Date", "@date{'%F'}"),  ("Value", "@value"), ],
 formatters={
        'date' : 'datetime', # use 'datetime' formatter for 'date' field
    })


if __name__ == '__main__':
    app.run(debug=True)
