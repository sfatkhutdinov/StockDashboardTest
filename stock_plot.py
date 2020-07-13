from flask import Flask, render_template


app = Flask(__name__)

@app.route('/plot')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN
    def increase_decrease(close_value, open_value):
        if close_value > open_value:
            value = 'Increase'
        elif close_value < open_value:
            value = 'Decrease'
        else:
            value = 'Equal'
        return value

    start = datetime.datetime(2020,1,1)
    end = datetime.datetime(2020,7,13)

    df = data.DataReader(name='AAPL', data_source = 'yahoo', start = start, end = end)

    df['Status'] = [increase_decrease(c, o) for c, o in zip(df.Close, df.Open)]
    df['Middle'] = (df.Open + df.Close) / 2
    df['Height'] = abs(df.Close - df.Open)
    plot = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_both')
    plot.title.text = 'Apple (APPL)'
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Price'
    plot.grid.grid_line_alpha = 0.3

    hours = 12 * 60 * 60 * 1000 # in milliseconds

    plot.segment(x0=df.index,
                y0=df.High,
                x1=df.index,
                y1=df.Low,
                color='black')

    plot.rect(x=df.index[df.Status=='Increase'], 
            y=df.Middle[df.Status=='Increase'], 
            width=hours, 
            height=df.Height[df.Status=='Increase'],
            fill_color='green',
            line_color='black')

    plot.rect(x=df.index[df.Status=='Decrease'], 
            y=df.Middle[df.Status=='Decrease'], 
            width=hours, 
            height=df.Height[df.Status=='Decrease'],
            fill_color='red',
            line_color='black')

    script1, division1, = components(plot)
    cdn_js = CDN.js_files

    return render_template('plot.html', 
    script1 = script1, 
    division1 = division1,
    cdn_js = cdn_js[0])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)