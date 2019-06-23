from flask import Flask,render_template,request

import pandas as pd
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.util.string import encode_utf8

from bokeh.plotting import figure
from bokeh.io import show, output_notebook

import datetime as dt
import pandas as pd

import pandas_datareader.data as web

import os

app_stock = Flask(__name__)

app_stock.vars={}




def create_figure(ticker, show_open, show_close):
    
    imported_df = pd.read_csv('StockData.csv')
    
    # Create figure
    p = figure(plot_width = 600, plot_height = 600, 
               title = 'Stock prices for %s:' % (ticker),
               y_axis_label = '$', x_axis_type='datetime')

    # Plot requested data
    if show_open == 'True':
        p.line(x = pd.to_datetime(imported_df.Date), y = imported_df.Open, color = 'navy', line_width = 4, alpha = 0.6)

    if show_close == 'True':
        p.line(x = pd.to_datetime(imported_df.Date), y = imported_df.Close, color = 'green', line_width = 4, alpha = 0.6)

    return p



@app_stock.route('/index',methods=['GET','POST'])
def index():
    nquestions=5
    

    if request.method == 'GET':
        return encode_utf8(render_template('index.html',num=nquestions))
    else: 
        app_stock.vars['ticker'] = request.form['ticker_input']
        
        if request.form.get('stat_options1'):
            app_stock.vars['show_open'] = 'True'
        else: 
            app_stock.vars['show_open'] = 'False'
            
            
        if request.form.get('stat_options2'):
            app_stock.vars['show_close'] = 'True'
        else: 
            app_stock.vars['show_close'] = 'False'
            
        start = dt.datetime(2019,1,1)
        end = dt.datetime(2019,1,31)
        
        df = web.DataReader(app_stock.vars['ticker'], 'yahoo', start, end)
    
        df[['Open','Close']].to_csv('StockData.csv')
        
        
        f=open('booltest.txt', 'w')
        f.write(app_stock.vars['show_open'])
        f.close()
        
        
        plot = create_figure(app_stock.vars['ticker'], app_stock.vars['show_open'], app_stock.vars['show_close'])
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        script, div = components(plot)

        
        return render_template('stock_plot.html',num=nquestions,plot_script=script,
        plot_div=div,js_resources=js_resources,css_resources=css_resources)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app_stock.run(host='127.0.0.0', port=port)