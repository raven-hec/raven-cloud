# --*coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import plotly.offline as pyof
import plotly.graph_objs as go
from plotly import figure_factory as ff

class Kpi_Plotly():
    def __init__(self):
        plotly_dir = 'plotly_html'
        if not os.path.isdir(plotly_dir):
            os.makedirs(plotly_dir)
            
        self.path_dir_plotly_html = os.getcwd() + os.sep + plotly_dir

    ## 生成月度部门收入走势图 
    def get_income_year_plolty_path(self, file_name='income_year.html'):
        path_plotly = self.path_dir_plotly_html + os.sep + file_name
        
        df1 = pd.read_excel(r'data\kpidata.xlsx', col_index=[0],  sheet_name='income2',  header=0)
        df1.columns= ['month', 'project_income', 'hr_in', 'hr_out', 'income_adjust', 'department_income', 'none_contract_income', 'deduct_income', 'assess_income']
        df1.set_index(['month'])
        print(df1.index)
#        df1.dropna(inplace=True)
        df2 = df1.stack()
        print(df2)
        
        data = [
                 go.Scatter(
                     x = df1.month, 
                     y = df1.project_income, 
                 #    text = df1.project_income, 
                 #    textposition = 'top center', 
                     name = '项目收入'
                 ), 
                 go.Scatter(
                     x = df1.month, 
                     y = df1.department_income, 
                     name = '部门收入'
                     ), 
                go.Scatter(
                     x = df1.month, 
                     y = df1.assess_income, 
                     name = '考核收入'
                )
        ]
        layout = go.Layout(
             title = '月度收入分析', 
             yaxis = dict( 
                 title = '月度收入（万元）', 
                 titlefont=dict(color='rgb(148, 103, 189)',size=12), 
                 showticklabels = True
             )
        )
        
        fig = go.Figure(data = data,  layout = layout)
        pyof.plot(fig,  filename=path_plotly,  auto_open=False)
        return path_plotly

    ## 获取业绩展望表    
    def get_department_kpi_status(self, file_name='kpi_status.html'):
        path_plotly = self.path_dir_plotly_html + os.sep + file_name
        df = pd.read_excel(r'data\2019年业绩分析及跟踪.xlsx', sheet_name='业绩展望2')
        df = df.fillna('')
        print(df)
        table = ff.create_table(df, index=False, index_title='指标')

        pyof.plot(table, filename=path_plotly, auto_open=False)
        return path_plotly
        
