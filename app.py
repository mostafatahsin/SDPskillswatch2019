import json

from flask import Flask
from bokeh.plotting import figure, output_notebook, show, save

from bokeh.models.tools import HoverTool
from bokeh.transform import cumsum
from bokeh.models import Text,Label,AnnularWedge
from flask import render_template
from bokeh.embed import components

import pandas as pd
import math

app = Flask(__name__, template_folder='templates')
# 5000
def make_plot():

    pi = math.pi

    data = pd.DataFrame()
    list1=['Telemedicine','Education','Transportation','Banking','Hospitals','Domestic','Exports','Freelancing']
    list2=[200,200,200,200,200,200,200,200]
    data['country'] = list1
    data['value'] =list2

    data1 = pd.DataFrame()
    list3 = ['Frontend firms','Backend firms','Freelancing']
    list4 = [225,90,45]
    data1['color'] = ['#2a88b8', '#c67613', '#cb4c4c']
    data1['country'] = list3
    data1['value'] =list4
    data1['angle'] = data1['value']/data1['value'].sum() * 2*pi

    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = ['#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#fbbb3c','#f0901a','#de5050']
    data['skill_1'] = ["Full-stack developers","IT courses-instructors","Full-stack developers","Hardware and Network system skills","Java, Android and IOS development","Web Application","Web Application",'Software development']
    data['skill_2'] = ['Mobile, Web & Cloud-based App development', 'IT-enabling of administrative services', 'Software Quality Assurance, Testing and Technical support', 'MS Office Suite', 'Linux, Windows and Virtualization (ESXi)', 'Web Design', 'Mobile Application', 'Web design and development' ]
    data['skill_3'] = ['Database administration', 'IT-enabling of accounting services', 'CISCO/Microsoft certification', 'Accessing networks/servers', 'Routing, Switching for Networking', 'Mobile Application','ERP development', 'System architecture' ]
    data['skill_4'] = ['Data analytics', 'Data entry', 'MS office', 'Java and C++', 'V-LAN for Networking', 'Hardware, Server Installation and Maintenance','QA Testing', 'Graphic design']
    data['skill_5'] = ['Problem-solving mindset and adaptability', 'Administrative skills', 'Communication and presentation skills', 'Hardware, Software and Network troubleshooting', 'Basic computer literacy', 'ERP development ','Web Design', 'HTML & JAVA programming language']

    # Add plot
    p = figure(plot_height=600, plot_width=650, title=None, 
                tools="pan,zoom_in,zoom_out,save,reset,wheel_zoom", x_range = (-0.5,1), y_range= (-0.5,1))


    p.annular_wedge(x=0.15, y=0.25, inner_radius=0.21, outer_radius = 0.4, 
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='country', source=data, name = 'foo' )

    #inner wedge
    p.wedge(x=0.15, y=0.25, radius = 0.2,   
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', source=data1, name ='bar')
    #inner_radius = 1, outer_radius = 2,
    #text=['FE firms', 'BE firms','freelancers']



    # citation1 = Label(x=0, y=1.67, x_units='data', y_units='data', text_color = 'white', angle=0,
    #                  text='Front End firms', render_mode='css',
    #                  border_line_color='#2a88b8', border_line_alpha=1.0,
    #                  background_fill_color='#2a88b8', background_fill_alpha=1.0)

    # citation2 = Label(x=0.012, y=0.245, x_units='data', y_units='data', text_color = 'white',
    #                  text='Back End firms', render_mode='css',
    #                  border_line_color='#c67613', border_line_alpha=1.0,
    #                  background_fill_color='#c67613', background_fill_alpha=1.0, name='bar')

    # citation3 = Label(x=0.42, y=0.7, x_units='data', y_units='data', text_color = 'white',angle=1.23,
    #                  text='Freelance', render_mode='css',
    #                  border_line_color='#cb4c4c', border_line_alpha=1.0,
    #                  background_fill_color='#cb4c4c', background_fill_alpha=1.0)

    # #for the annotations
    # p.add_layout(citation1)
    # p.add_layout(citation2)
    # p.add_layout(citation3)


    p.axis.axis_label=None
    p.axis.visible=None
    p.grid.grid_line_color = None

    # p.legend.glyph_height = 1
    # p.legend.glyph_width = 1
    # p.legend.label_height = 0

    # Add Tooltips
    hover = HoverTool(names=['foo'], mode="mouse", point_policy="follow_mouse")
    hover.tooltips = """
      <div>
        <h3>Top Five Skills - @country</h3>
        <div>1. @skill_1</div>
        <div>2. @skill_2</div>
        <div>3. @skill_3</div>
        <div>4. @skill_4</div>
        <div>5. @skill_5</div>
      </div>
    """

    # Add Tooltips
    hover1 = HoverTool(names=['bar'], mode="mouse", point_policy="follow_mouse")
    hover1.tooltips = """
      <div>
        <h3>@country</h3>
      </div>
    """
    p.add_tools(hover)
    p.add_tools(hover1)

    script, div = components(p)
    return script, div

@app.route('/')
def mainPage():

    plots = []
    plots.append(make_plot())   
    return  render_template('dashboard.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True)