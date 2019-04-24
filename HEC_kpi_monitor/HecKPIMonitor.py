# -*- coding: utf-8  -*-
# 部门经营情况监控

from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Ui_HecKPIMainform import Ui_MainWindow
from hecDepartmentParamters import  p
from pyqtgraph.parametertree import ParameterTree

from kpiPlotly import Kpi_Plotly

class MainWindow(QMainWindow,  Ui_MainWindow):
    
    def __init__(self,  parent=None):
        super(MainWindow,  self).__init__(parent)
        self.setupUi(self)
        
        t = ParameterTree()
        t.setParameters(p,  showTop=False)
        t.setHeaderLabels(['参数', '参数值'])
        
        layout = QtGui.QGridLayout()
        self.departmentInfo_parameter_tree.setLayout(layout)
        layout.addWidget(t)
        
        self.kpi_plotly = Kpi_Plotly()
        
        #self.kpi_plotly.get_income_year_plolty_path()
        self.widget_PeriodIncome.load(
             QUrl.fromLocalFile(self.kpi_plotly.get_income_year_plolty_path())
        )
        self.widgetf_MajorExpense.load(
             QUrl.fromLocalFile(self.kpi_plotly.get_department_kpi_status())
        )
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.showMaximized()
    sys.exit(app.exec_())
