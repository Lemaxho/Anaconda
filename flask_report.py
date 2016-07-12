# '''Serving dynamic images with Pandas and matplotlib (using flask).'''
import pyodbc
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import base64

from flask import Flask
app = Flask(__name__)

html = '''
<html>
    <body>
        <img src="data:image/png;base64,{img1}" />
        <div class='matplotlib'>
            <img src="data:image/png;base64,{img2}" />
        </div>
    </body>
</html>
'''

@app.route("/")
def hello():
    df = pd.DataFrame(
        {'y':np.random.randn(10), 'z':np.random.randn(10)},
        index=pd.period_range('1-2000',periods=10),
    )
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df.plot(ax=ax)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    data = base64.b64encode(buf.getvalue())
    str = data.decode(encoding='UTF-8')


    accb = r"F:\debug\web\Anaconda_home\db_cy2_test.accdb"
    connStr = """
    DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};
    DBQ=F:\debug\web\Anaconda_home\db_cy2_test.accdb;
    """
    cnxn = pyodbc.connect(connStr)
    cursor = cnxn.cursor()
    query = """select count(*) as nbr, d.stru_d as name from pla90 as p, dico_stru as d
    where p.stru_pl = d.code and tranche=12 and dg_pf = 1 group by p.stru_pl, d.stru_d;"""
    # p.stru_pl,
    data = pd.read_sql(query, cnxn)
    # plotSql = data.plot(kind='bar', x='name', y='nbr', fontsize=10,
    #                     rot=60, alpha=0.5, legend=False)
    # plotSql = data.plot(kind='bar', x=data.stru_pl, y='nbr', xticks=data.stru_pl,
    #                     fontsize=10, rot=60, alpha=0.5, legend=False)
    # , x='stru_pl', x='name', y='nbr' figsize=(6, 6)
    # plotSql.set_xticks(data.stru_pl)
    # plotSql.set_xticklabels(data.name, rotation=60)
    # plotSql.set_xticks(np.array(data.stru_pl))
    # plotSql.set_xticklabels(np.array(data.name), rotation=50) unorderable types

    plotSql = data.plot(kind='bar', fontsize=10, rot=60, alpha=0.5, legend=False)
    plotSql.set_xticks(data.index)
    plotSql.set_xticklabels(data.name, rotation=90)

    # DPI = fig.get_dpi()
    # fig.set_size_inches(2400.0 / float(DPI), 1220.0 / float(DPI))

    figSql = plotSql.get_figure()
    figSql.tight_layout()

    buf = io.BytesIO()
    figSql.savefig(buf, format='png')
    data = base64.b64encode(buf.getvalue())
    str2 = data.decode(encoding='UTF-8')

    return html.format(
        img1=str,
        img2=str2)

if __name__ == '__main__':
    app.run()
