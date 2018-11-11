# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 23:03:16 2018

@author: Ghema
"""

import pandas as pd
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.layouts import widgetbox, column
from bokeh.io import curdoc
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Set2_7
from bokeh.models import Slider
tr = pd.read_csv('top250-00-19.csv')

tr['transfer_fee_M']= tr['Transfer_fee'].map(lambda x : str(x/1000000)+' M')

tr['Year']= tr['Season'].map(lambda x : x.split('-')[0])
tr['Year'] = tr['Year'].astype(int)

tr = tr.sort_values('Transfer_fee', ascending=False)

tr_yearly_10 = tr.groupby('Year').head(10).reset_index(drop=True)
tr_max_100 = tr.head(100).reset_index(drop=True)
tr_max_20 = tr.head(20).reset_index(drop=True)


tr_plot = tr_yearly_10

# Save the minimum and maximum values of the fertility column: xmin, xmax
xmin, xmax = min(tr_plot.Age), max(tr_plot.Age)

# Save the minimum and maximum values of the life expectancy column: ymin, ymax
ymin, ymax = min(tr_plot.Transfer_fee), max(tr_plot.Transfer_fee)

yr=2000
data_init = {
        'x'        : tr_plot[tr_plot['Year']==yr].Age,
        'y'        : tr_plot[tr_plot['Year']==yr].Transfer_fee,
        'position' : tr_plot[tr_plot['Year']==yr].Position,
        'league_from'     : tr_plot[tr_plot['Year']==yr].League_from,
        'league_to': tr_plot[tr_plot['Year']==yr].League_to,
        'name'        : tr_plot[tr_plot['Year']==yr].Name,
        'team_to' : tr_plot[tr_plot['Year']==yr].Team_to,
        'team_from'     : tr_plot[tr_plot['Year']==yr].Team_from,
        'transfer_fee_M': tr_plot[tr_plot['Year']==yr].transfer_fee_M,
        }
source = ColumnDataSource(data=data_init)

hover = HoverTool(tooltips = [('Player', '@name'), ('From (Team)', '@team_from'),
                             ('To (Team)', '@team_to'), ('Transfer Fee', '@transfer_fee_M')])



plot = figure(title='Transfers', plot_width=700, plot_height = 450 )

# Make a color mapper: color_mapper
league_list = tr_plot.League_to.unique().tolist()
color_mapper = CategoricalColorMapper(factors=league_list, palette=Set2_7)

c = plot.circle(x='x', y='y', fill_alpha=1, source=source, size=10,
            color=dict(field='league_to', transform=color_mapper), legend='league_to',
            hover_fill_color='firebrick', hover_alpha=1,
            hover_line_color='red')

plot.legend.location = 'top_right'

year_slider = Slider(start=2000, end=2018, value=2000, step=1, title="Year") 

def callback (attr, old, new):
    new_yr = new
    new1 = {
        'x'        : tr_plot[tr_plot['Year']==new_yr].Age,
        'y'        : tr_plot[tr_plot['Year']==new_yr].Transfer_fee,
        'position' : tr_plot[tr_plot['Year']==new_yr].Position,
        'league_from'     : tr_plot[tr_plot['Year']==new_yr].League_from,
        'league_to': tr_plot[tr_plot['Year']==new_yr].League_to,
        'name'        : tr_plot[tr_plot['Year']==new_yr].Name,
        'team_to' : tr_plot[tr_plot['Year']==new_yr].Team_to,
        'team_from'     : tr_plot[tr_plot['Year']==new_yr].Team_from,
        'transfer_fee_M': tr_plot[tr_plot['Year']==new_yr].transfer_fee_M
        }
    source.data=new1
    
year_slider.on_change('value', callback)

layout = column(widgetbox(year_slider), plot)

curdoc().add_root(layout)

#output_file('Transfer.html')
show(layout)