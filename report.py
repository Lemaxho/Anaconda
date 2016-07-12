import pyodbc
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

from matplotlib.backends.backend_pdf import PdfPages

import numpy as np
import pandas as pd

from pandas.tools.plotting import lag_plot


ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
# ts.plot()
plot0 = ts.plot().get_figure()

df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
df = df.cumsum()
# plt.figure()
# df.plot()
# df.plot(secondary_y=['A', 'B'], mark_right=False)
plot1 = df.plot(secondary_y=['A', 'B'], mark_right=False).get_figure()

df4 = pd.DataFrame({'a': np.random.randn(1000) + 1, 'b': np.random.randn(1000),
                    'c': np.random.randn(1000) - 1}, columns=['a', 'b', 'c'])
# plt.figure()
# df4.plot.hist(alpha=0.5)
plot2 = df4.plot.hist(alpha=0.5).get_figure()

# json = df4.to_json()
# print(json)
# print(df.to_html())

plot3 = plt.figure()
data = pd.Series(0.1 * np.random.rand(1000) +
                 0.9 * np.sin(np.linspace(-99 * np.pi, 99 * np.pi, num=1000)))
lag_plot(data)


accb = r"F:\debug\web\Anaconda_home\db_cy2_test.accdb"
# access_con_string = r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=%s" % accb
# cnxn   = pyodbc.connect(access_con_string)


connStr = """
DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};
DBQ=F:\debug\web\Anaconda_home\db_cy2_test.accdb;
"""
# If 32bit access is installed and we are using a 64bit python,
# download and install AccessDatabaseEngine_x64.exe with the option /passive
# --> have both versions of odbc drivers: 32 and 64 installed

cnxn = pyodbc.connect(connStr)
cursor = cnxn.cursor()

# ign,npl,cy,tranche, dg_pf, stru_pl, peup_pl
query = "select stru_pl from pla90 where tranche=12 and dg_pf = 1;"
# cursor.execute(query)
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

data = pd.read_sql(query, cnxn)
plotSql = data.plot.hist(alpha=0.5).get_figure()

query2 = """select x,y from placette as pl, pla90 as p
where pl.ign = p.ign and pl.npl = p.npl and p.stru_pl is not null and p.cy = 1;"""
data2 = pd.read_sql(query2, cnxn)
# plotSql2 = data2.plot(kind='scatter', x='x', y='y').get_figure()
plotSql2 = data2.plot(kind='hexbin', x='x', y='y', gridsize=50).get_figure()


pp = PdfPages('foo.pdf')
pp.savefig(plot0)
pp.savefig(plot1)
pp.savefig(plot2)
pp.savefig(plot3)
pp.savefig(plotSql)
pp.savefig(plotSql2)
pp.close()

