from cameratrap import fdf
from bokeh.plotting import figure, show, output_file

f = figure(x_axis_type='datetime',height=100,width=500,responsive=True,title="Face Detection Events")
q = f.quad(left=fdf["Start"],right=fdf["End"],bottom=0,top=1,color="purple")

output_file("FaceGraph.html")
show(f)
# m = figure(x_axis_type='datetime',height=100,width=500,responsive=True,title="Motion Detection Events")