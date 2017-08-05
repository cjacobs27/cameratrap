from cameratrap import fdf
from bokeh.plotting import figure, show, output_file

f = figure(x_axis_type='datetime',height=100,width=500,responsive=True,title="Face Detection Events")
f.title.align='center'
f.title.text_font_size='12pt'
f.title.text_font_style='bold'
f.title.text_font='helvetica'
f.yaxis.minor_tick_line_color=None
f.ygrid[0].ticker.desired_num_ticks=1
q = f.quad(left=fdf["Start"],right=fdf["End"],bottom=0,top=1,color="purple")

output_file("FaceGraph.html")
# show(f)
# m = figure(x_axis_type='datetime',height=100,width=500,responsive=True,title="Motion Detection Events")