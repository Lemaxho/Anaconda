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
# figSql.tight_layout()
str_plot1 = Lempica.get_figure_image_str(figSql)

# pivoted = df.pivot('x', 'y')
# table = pivoted.values.tolist()
table = df.values.tolist()
# print(table)

dico = {'title': 'Jinja!',
        'text': 'paragraph text',
        'foo': 'Hello World!',
        'plot1': str_plot1,
        'table': table}
output_from_parsed_template = template.render(d=dico).encode("utf-8")
# print(output_from_parsed_template)

# to save the results
with open("my_new_file.html", "wb") as fh:
    fh.write(output_from_parsed_template)

# from weasyprint import HTML
# HTML(string=output_from_parsed_template).write_pdf("my_new_file.pdf")

# HTML(string=html_out).write_pdf(args.outfile.name, stylesheets=["style.css"])

# Pandoc test
# os.system("pandoc C:/Users/pitchugin.m/PycharmProjects/Anaconda/my_new_file.html -o C:/Users/pitchugin.m/PycharmProjects/Anaconda/my_new_file.pdf")



import pdfkit
path_wkthmltopdf = 'E:/programs/wkhtmltopdf/bin/wkhtmltopdf.exe'
pdfkit.from_string(output_from_parsed_template, "my_new_file2.pdf")



# Passing args to jinja with a dict
# for row in rows:
#     thedict=dict(zip(col_names,row))
#     filename='zzpuma_' + row[0] + '.tex'
#     folder='test3'
#     outpath=os.path.join(folder,filename)
#     outfile=open(outpath,'w')
#     outfile.write(template.render(d=thedict))
#     outfile.close()
#     # os.system("pdflatex -output-directory=" + folder + " " + outpath)
