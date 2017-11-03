from cameratrap import fdf, mdf
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
'''
to get the dataframe data working with the hover tool we need to
convert them to strings. We're just creating 2 additional columns
in each dataframe
where the datetimes from the first two are converted to strings.
'''
fdf["Start_string"]=fdf["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
fdf["End_string"]=fdf["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

mdf["Start_string"]=mdf["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
mdf["End_string"]=mdf["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
'''
these two lines are needed to access the data in the 2 dataframes
for the hover tools later
'''
fcds=ColumnDataSource(fdf)
mcds=ColumnDataSource(mdf)

a = figure(x_axis_type='datetime',height=200,width=500,responsive=True,title="Face and Motion Detection Events", logo=None)
a.title.align='center'
a.title.text_font_size='12pt'
a.title.text_font_style='bold'
a.title.text_font='helvetica'
a.yaxis.minor_tick_line_color=None
a.ygrid[0].ticker.desired_num_ticks=1
'''
This Bokeh code uses the @Start_string and @End_string decorators to pull in
those respective columns from the 2 new dataframe columns
a colon between label and data is added by default
'''
fhover = HoverTool(tooltips=[("Face","@Start_string"),("Face Lost","@End_string")])
a.add_tools(fhover)
mhover = HoverTool(tooltips=[("Motion","@Start_string"),("Motion End","@End_string")])
a.add_tools(mhover)
#creating both quadrangle glyphs on the same chart
q = a.quad(left=fdf["Start"],right=fdf["End"],bottom=0,top=0.5,color="deepskyblue",alpha=0.75, legend= "Face Detected", source=fcds)
v = a.quad(left=mdf["Start"],right=mdf["End"],bottom=0.5,top=2,color="yellow", alpha = 0.8, legend= "Motion Detected",source=mcds)
a.legend.location = "top_left"
output_file("FaceGraph.html")
show(a)
