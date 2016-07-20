# coding: utf-8

import pyodbc
import os
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as plticker
matplotlib.style.use('ggplot')
import numpy as np
import pandas as pd
import pandas.tools.plotting as pdp
import io
import base64


class Lempica:
    @staticmethod
    def get_figure_image_str(figure):
        buf = io.BytesIO()
        figure.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        data = base64.b64encode(buf.getvalue())
        figure_string = data.decode(encoding='UTF-8')
        return figure_string

    def convert(my_str):
        return my_str.encode('utf-8')


# ********************************************************
# Report generation
# ********************************************************
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('test.html')


accb_path1 = r"F:\debug\web\Anaconda_home\db_cy2_test.accdb"
accb_path2 = r"D:\Data\code\Projets\Anaconda\db_cy2.accdb"
connStr = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;" % accb_path1
cnxn = pyodbc.connect(connStr)
cursor = cnxn.cursor()
query = """select a.tranche, a.nbr as chenaie, b.nbr as pessiere from (select p.tranche, count(*) as nbr from pla90 as p
where p.cy=1 and p.peup_pl = 2 group by p.tranche) as a,
(select p.tranche, count(*) as nbr from pla90 as p
where p.cy=1 and  p.peup_pl = 10 group by p.tranche) as b where a.tranche = b.tranche;"""

df = pd.read_sql(query, cnxn)
# Set title
ttl = 'Nombre par tranche de placettes en chênaie et pessière'

# Rename columns for legend
df.rename(columns={'chenaie': 'Chênaie', 'pessiere': 'Pessière'}, inplace=True)

plotSql = df.plot(kind='bar', x='tranche', rot=0,
                  fontsize=10, alpha=0.5, legend=True, table=False, title=ttl)

# plotSql.xaxis.set_label_coords(0, -0.05)
plotSql.set_xlabel("Tranche")
plotSql.set_ylabel("Nombre")
plotSql.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=False, ncol=2)

# This locator puts ticks at regular intervals
major_loc = plticker.MultipleLocator(base=50.0)
minor_loc = plticker.MultipleLocator(base=25.0)
plotSql.yaxis.set_major_locator(major_loc)
plotSql.yaxis.set_minor_locator(minor_loc)
plotSql.yaxis.grid(True, which="minor")

figSql = plotSql.get_figure()
str_plot1 = Lempica.get_figure_image_str(figSql)
table = df.values.tolist()

# Plot 2
query = """select p.tranche, p.peup_pl, d.peup_d as name, count(*) as nbr from pla90 as p, dico_peup as d
where p.peup_pl = d.code and p.cy=1 and p.peup_pl is not null group by p.tranche, p.peup_pl, d.peup_d;"""
df2 = pd.read_sql(query, cnxn)
df2.set_index('name')

df_select = df2[df2['nbr'].notnull() & (df2['peup_pl'] < 6)]
df_select.set_index('name')
# [df2['nbr'].notnull() & (df2['peup_pl'] < 6)]
# Remember: DataFrame.pivot([index, columns, values])
# Reshape data (produce a “pivot” table) based on column values.
# Index from tranche, columns from name, values from nbr
pivoted = df_select[['tranche', 'name', 'nbr']].pivot('tranche', 'name', 'nbr')
table2 = pivoted.values.tolist()
# print(table2)
# print(list(pivoted))
# print(pivoted.T)
# print(type(pivoted.T))
# print(pivoted.T.to_html())
print(pivoted.T.to_dict())

pivoted_dict = pivoted.T.to_dict()

# & (pivoted['nationality'] == "USA") pivoted['nbr'].notnull() pivoted.describe()  width=1, bar
plotSql2 = pivoted.plot(kind='line', stacked=False,  lw=2, rot=0, alpha=0.5, legend=True, table=False)
plotSql2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=False, ncol=3)
# box = (pos1.x0 + 0.3, pos1.y0 + 0.3,  pos1.width / 2.0, pos1.height / 2.0)
# pos1 = plotSql2.get_position()
# box = (0.35, -0.67, pos1.width / 2.0, pos1.height / 2.0)
# pdp.table(ax=plotSql2, data=pivoted.T, loc='bottom left', bbox=box)
# Where bbox is: [left, bottom, width, height]

plotSql2.set_xlabel("Tranche")
plotSql2.set_ylabel("Nombre")
# This locator puts ticks at regular intervals
plotSql2.yaxis.set_major_locator(major_loc)
plotSql2.yaxis.set_minor_locator(minor_loc)
plotSql2.yaxis.grid(True, which="minor")

figSql2 = plotSql2.get_figure()
str_plot2 = Lempica.get_figure_image_str(figSql2)


# Prepare data for Jinja template
dico = {'title': 'Jinja!',
        'text': 'paragraph text',
        'foo': 'Hello World!',
        'plot1': str_plot1,
        'plot2': str_plot2,
        'table': table,
        'table2': pivoted_dict,
        'table2html': pivoted.T.to_html()}
output_html = template.render(d=dico)
output_from_parsed_template = output_html.encode("utf-8")

# to save the results
with open("my_new_file.html", "wb") as fh:
    fh.write(output_from_parsed_template)

# Pandoc test
# os.system("pandoc C:/Users/pitchugin.m/PycharmProjects/Anaconda/my_new_file.html -o C:/Users/pitchugin.m/PycharmProjects/Anaconda/my_new_file.pdf")


# Pdfkit ok
import pdfkit

# options = {
#     'page-size': 'Letter',
#     'margin-top': '0.25in',
#     'margin-right': '0.25in',
#     'margin-bottom': '0.25in',
#     'margin-left': '0.25in',
#     'encoding': "UTF-8",
#     'no-outline': None
# }
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None
}
css = 'print.css'

pdfkit.from_string(output_html, "my_new_file2.pdf", options=options, css=css)

