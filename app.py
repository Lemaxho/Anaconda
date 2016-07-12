import os
import random

from flask import Flask, render_template
import numpy as np
import pandas as pd

# imports for matplotlib plotting
import tempfile
import matplotlib

matplotlib.use('Agg')  # this allows PNG plotting
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def indexPage():
    # generate some random integers, sorted
    exponent = .7 + random.random() * .6
    dta = []
    for i in range(50):
        rnum = int((random.random() * 10) ** exponent)
        dta.append(rnum)
    y = sorted(dta)
    x = range(len(y))

    # generate matplotlib plot
    fig = plt.figure(figsize=(5, 5), dpi=100)
    axes = fig.add_subplot(1, 1, 1)
    # plot the data
    axes.plot(x, y, '-')
    # labels
    axes.set_xlabel('time')
    axes.set_ylabel('size')
    axes.set_title("A matplotlib plot")
    # get the file's name (rather than the whole path)
    plot_name = get_plot_file_name(fig)

    # Second plot
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
    df = df.cumsum()
    plot2 = df.plot(secondary_y=['A', 'B'], mark_right=False).get_figure()
    plot_name2 = get_plot_file_name(plot2)

    return (render_template(
        'figures.html',
        y=y,
        plotPng=plot_name,
        secondPlot=plot_name2
    ))


def get_plot_file_name(plot):
    f = tempfile.NamedTemporaryFile(
        dir='static/temp',
        suffix='.png', delete=False)
    # save the figure to the temporary file
    plot.savefig(f)
    f.close()  # close the file
    # get the file's name (rather than the whole path)
    # plot_dir = os.path.dirname(f.name)
    plot_name = os.path.basename(f.name)

    return plot_name


if __name__ == '__main__':
    app.debug = True
    app.run()
