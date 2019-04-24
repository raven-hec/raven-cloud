# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter

# 部门基本情况信息
class departmentSummary(pTypes.GroupParameter):
    def __init__(self,  **opts):
        opts['type'] = 'group'
        pTypes.GroupParameter.__init__(self,  **opts)
        
        df = pd.read_excel(r'data\summary.xlsx')
        df.columns = ['kpi_index', 'act_value']
        
        i = 0
        while i < len(df):
             sr = df.iloc[i]
             print(sr)
             self.addChild({'name': sr[0],  'type': 'str',  'value': sr[1],  'readonly': True})
             i += 1
    
class departmentIncome(pTypes.GroupParameter):
    def __init__(self,  **opts):
        opts['type'] = 'group'
        pTypes.GroupParameter.__init__(self,  **opts)
        
        df = pd.read_excel(r'data\summary.xlsx',  sheet_name='income_profit')
        df.columns = ['kpi_index',  'act_value']
        
        for row_index,row in df.iterrows():
            self.addChild({'name': row.kpi_index,  'type': 'str',  'value': row.act_value, 'readonly':True})
            print(row_index,  row)

#部门参数树的信息
params = [
     departmentSummary(name='部门基本情况'), 
     departmentIncome(name='部门损益情况')
]

## 创建参数对象树
p = Parameter.create(name='params',  children=params,  type='group')

