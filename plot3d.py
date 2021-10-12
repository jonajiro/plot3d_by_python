import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from PyQt5.QtGui import *
from PyQt5.Qt import *
import sys, csv

class Window (QWidget):
    def __init__ (self):
        QWidget.__init__(self, None)


        self.setWindowTitle('Test')

class View (Window):
    def __init__ (self, parent=None):
        super(View, self).__init__()
        self.resize(700, 700)




        self.frame = QFrame()
        # self.frame.setGeometry(QRect(90, 20, 771, 561))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget = QWidget(self.frame)
        # self.verticalLayoutWidget.setGeometry(QRect(30, 30, 701, 501))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_all = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_all.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_all.setObjectName("verticalLayout_all")
        self.horizontalLayout_ctrltable = QHBoxLayout()
        self.horizontalLayout_ctrltable.setObjectName("horizontalLayout_ctrltable")
        self.verticalLayout_ctrl = QVBoxLayout()
        self.verticalLayout_ctrl.setObjectName("verticalLayout_ctrl")
        self.horizontalLayout_com = QHBoxLayout()
        self.horizontalLayout_com.setObjectName("horizontalLayout_com")
        self.comboBox_COM = QComboBox(self.verticalLayoutWidget)
        self.comboBox_COM.setObjectName("comboBox_COM")
        self.horizontalLayout_com.addWidget(self.comboBox_COM)
        self.pushButton_COM = QPushButton(self.verticalLayoutWidget)
        self.pushButton_COM.setObjectName("pushButton_COM")
        self.horizontalLayout_com.addWidget(self.pushButton_COM)
        self.verticalLayout_ctrl.addLayout(self.horizontalLayout_com)
        self.label_status = QLabel(self.verticalLayoutWidget)
        self.label_status.setObjectName("label_status")
        self.verticalLayout_ctrl.addWidget(self.label_status)
        self.label_data = QLabel(self.verticalLayoutWidget)
        self.label_data.setObjectName("label_data")
        self.verticalLayout_ctrl.addWidget(self.label_data)
        self.pushButton_datareq = QPushButton(self.verticalLayoutWidget)
        self.pushButton_datareq.setObjectName("pushButton_datareq")
        self.verticalLayout_ctrl.addWidget(self.pushButton_datareq)
        self.horizontalLayout_add = QHBoxLayout()
        self.horizontalLayout_add.setObjectName("horizontalLayout_add")
        self.pushButton_dataadd = QPushButton(self.verticalLayoutWidget)
        self.pushButton_dataadd.setObjectName("pushButton_dataadd")
        self.pushButton_dataadd.clicked.connect(self.data_add)
        self.horizontalLayout_add.addWidget(self.pushButton_dataadd)
        self.comboBox_plotcolor = QComboBox(self.verticalLayoutWidget)
        self.comboBox_plotcolor.setObjectName("comboBox_plotcolor")
        self.horizontalLayout_add.addWidget(self.comboBox_plotcolor)
        self.verticalLayout_ctrl.addLayout(self.horizontalLayout_add)
        self.horizontalLayout_autoline = QHBoxLayout()
        self.horizontalLayout_autoline.setObjectName("horizontalLayout_autoline")
        self.checkBox_autoline = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_autoline.setObjectName("checkBox_autoline")
        self.horizontalLayout_autoline.addWidget(self.checkBox_autoline)
        self.comboBox_linecolor = QComboBox(self.verticalLayoutWidget)
        self.comboBox_linecolor.setObjectName("comboBox_linecolor")
        self.horizontalLayout_autoline.addWidget(self.comboBox_linecolor)
        self.verticalLayout_ctrl.addLayout(self.horizontalLayout_autoline)
        self.horizontalLayout_ctrltable.addLayout(self.verticalLayout_ctrl)

        #Viewを作成
        self.tableView_main = QTableView()
        self.tableView_main.clicked.connect(self.viewClicked)
        self.tableView_main.setFixedSize(700, 300)
        #Viewの罫をブラックにする
        self.tableView_main.setStyleSheet("QTableView{gridline-color: black}")

        self.headers = ["▽","id", "X", "Y", "Z", "メモ", "点配色", "線配色", "結線先id"]
        tableData0 = [[QCheckBox(''), 0, 0, 0, 0, "基準点A", "黒", "黒",0]]

        #モデルを作成
        self.model = MyTableModel(tableData0, self.headers)
        self.tableView_main.setModel(self.model)

        #Insert、remove用の選択行に行の最大値をセット
        self.selectRow = self.model.rowCount(QModelIndex())

        self.tableView_main.setColumnWidth(0,40)
        self.tableView_main.setColumnWidth(1,40)
        self.tableView_main.setColumnWidth(2,80)
        self.tableView_main.setColumnWidth(3,80)
        self.tableView_main.setColumnWidth(4,80)
        self.tableView_main.setColumnWidth(5,150)
        self.tableView_main.setColumnWidth(6,60)
        self.tableView_main.setColumnWidth(7,60)
        self.tableView_main.setColumnWidth(8,60)
        #csv用のファイルフィルタをセット
        self.filters = "CSV files (*.csv)"

        #ファイル名を初期化
        self.fileName = None

        self.tableView_main.setObjectName("tableView_main")
        self.horizontalLayout_ctrltable.addWidget(self.tableView_main)
        self.verticalLayout_all.addLayout(self.horizontalLayout_ctrltable)

        self.graph_plot3d = gl.GLViewWidget(self)
        self.graph_plot3d.opts['distance'] = 10
        self.graph_plot3d.show()
        self.g = gl.GLGridItem()
        self.graph_plot3d.addItem(self.g)

        self.n=1
        numX, startX, endX = self.n, 1, 0+self.n
        numY, startY, endY = self.n, 1, 0+self.n
        numZ, startZ, endZ = self.n, 1, 0+self.n

        X = np.linspace(startX, endX, numX)
        Y = np.linspace(startY, endY, numY)
        Z = np.linspace(startZ, endZ, numZ)

        #position of scatter in 3D
        pos = np.array([[i,j,k] for i in X for j in Y for k in Z])

        color = (0.7,1,0.1,1)
        size = 0.5

        self.scttrPlt = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
        # self.scttrPlt.translate(5,5,0)
        self.scttrPlt.translate(0,0,0)
        self.graph_plot3d.addItem(self.scttrPlt)

        self.graph_plot3d.setObjectName("graph_plot3d")
        self.verticalLayout_all.addWidget(self.graph_plot3d)

        # _translate = QCoreApplication.translate
        self.setWindowTitle("Widget")
        self.pushButton_COM.setText("接続")
        self.label_status.setText("ステータス：")
        self.label_data.setText("計測データ表示")
        self.pushButton_datareq.setText("計測")
        self.pushButton_dataadd.setText("データ追加")
        self.checkBox_autoline.setText("自動結線")
        # self.QMetaObject.connectSlotsByName()


        self.menubar = QMenuBar()
        self.verticalLayout_all.insertWidget(0,self.menubar)

        self.actionFile = self.menubar.addMenu("ファイル")
        self.actionFile.addAction("新規作成")
        self.actionFile.addAction("読み込み")
        self.actionFile.addAction("保存")
        self.actionFile.addAction("追加")
        self.actionFile.addSeparator()
        self.actionFile.addAction("終了")
        self.menubar.addMenu("ライセンス")
        self.menubar.setFixedHeight(30)

        self.setLayout(self.verticalLayout_all)

    #Viewとモデルに行追加→選択されている行の下に1行追加
    def data_add(self, position, rows=1, index=QModelIndex()):
        print("position: %d"%position)
        print("rows: %d" % rows)
        print("rowCount: %d" % self.model.rowCount(QModelIndex()))
        position = self.selectRow
        self.model.beginInsertRows(QModelIndex(), position, position + rows - 1)
        if self.model.rowCount(QModelIndex()) == 1:
            fid = 0
        else:
            fid = self.model.index(self.model.rowCount(QModelIndex())-1, 1, QModelIndex() ).data( Qt.DisplayRole )
        print(position)
        print(fid)
        for row in range(rows):
            self.model.list.insert(self.model.rowCount(QModelIndex()), [QCheckBox(''), fid+1, 0, 0, 0, "基準点A", "黒", "黒",0])

        self.model.endInsertRows()
        return True

    def plot(self):
        self.n+=1
        numX, startX, endX = self.n, 1, 0+self.n
        numY, startY, endY = self.n, 1, 0+self.n
        numZ, startZ, endZ = self.n, 1, 0+self.n

        X = np.linspace(startX, endX, numX)
        Y = np.linspace(startY, endY, numY)
        Z = np.linspace(startZ, endZ, numZ)

        pos = np.array([[i,j,k] for i in X for j in Y for k in Z])
        color = (0.7,1,0.5,1)
        size = 0.5

        self.scttrPlt.setData(pos=pos,color=color,size=size)

    #保存処理→CSVで保存
    def handleSave(self):
        print("handleSave")
        if self.fileName == None or self.fileName == '':
            self.fileName, self.filters = QFileDialog.getSaveFileName(self, \
            filter=self.filters)
        if(self.fileName != ''):
            with open(self.fileName, 'wt') as stream:
                csvout = csv.writer(stream, lineterminator='\n')
                csvout.writerow(self.headers)
                for row in range(self.model.rowCount(QModelIndex())):
                    print(self.model.rowCount(QModelIndex()))
                    rowdata = []
                    for column in range(self.model.columnCount(QModelIndex())):
                        item = self.model.index( row, column, QModelIndex() ).data( Qt.DisplayRole )
                        if column == 0:
                            rowdata.append('')
                            continue

                        if item is not None:
                            rowdata.append(item)
                        else:
                            rowdata.append('')
                    csvout.writerow(rowdata)
                    print(rowdata)

    #ファイルオープン処理
    def handleOpen(self):
        print("handleOpen")
        self.fileName, self.filterName = QFileDialog.getOpenFileName(self)

        if self.fileName != '':
            with open(self.fileName, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                buf = []
                for row in reader:
                    row[0] = QCheckBox("-")
                    buf.append(row)

                self.model = None
                self.model = MyTableModel(buf, self.headers)
                self.tableView.setModel(self.model)
                self.fileName = ''

    #新規作成
    def handleNew(self):
        print ("handleNew")
        self.fileName = ''

        defaultValue =[[QCheckBox(''), 0, 0, 0, 0, "基準点A", "黒", "黒",0]]
                # self.headers = ["id", "X", "Y", "Z", "メモ", "点配色", "線配色", "結線先id"]
                # tableData0 = [[ "0", "0", "0", "0", "基準点A", "黒", "黒",0]]

        self.model = None
        self.model = MyTableModel(defaultValue, self.headers)
        print(defaultValue)
        self.tableView.setModel(self.model)

    #Viewとモデルに行追加→選択されている行の上に1行挿入します
    def insertRows(self, position, rows=1, index=QModelIndex()):
        # print("position: %d"%position)
        # print("rows: %d" % rows)
        # print("rowCount: %d" % self.model.rowCount(QModelIndex()))

        position = self.selectRow
        self.model.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.model.list.insert(position, [QCheckBox(''), 0, 0, 0, 0, "基準点A", "黒", "黒",0])

        self.model.endInsertRows()
        return True

    #Viewとモデルから行削除→選択位置の行を削除
    def removeRows(self, position, rows=1, index=QModelIndex()):
        print("Removing at position: %s"%position)
        position = self.selectRow
        self.model.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.model.list = self.model.list[:position] + self.model.list[position + rows:]
        self.model.endRemoveRows()
        return True

    #Viewをクリックしたときの行の位置を取得
    def viewClicked(self, indexClicked):
        print('indexClicked() row: %s  column: %s'%(indexClicked.row(), indexClicked.column() ))
        self.selectRow = indexClicked.row()


class MyTableModel(QAbstractTableModel):

    def __init__(self, list, headers = [], parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.list = list
        self.headers = headers

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.list[0])

    def flags(self, index):
        row = index.row()
        column = index.column()
        if column == 0:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):

        row = index.row()
        column = index.column()

        if role == Qt.EditRole:
            return self.list[row][column]

        if role == Qt.CheckStateRole and column == 0:

            if self.list[row][column].isChecked():
                return QVariant(Qt.Checked)
            else:
                return QVariant(Qt.Unchecked)

        """  CheckBoxのテキストを表示させたい場合
        #if role == Qt.DisplayRole and column == 0:
            #return self.list[row][column].text()
        """

        if role == Qt.DisplayRole:

            row = index.row()
            column = index.column()
            value = self.list[row][column]

            return value

    def setData(self, index, value, role = Qt.EditRole):
        row = index.row()
        column = index.column()

        if role == Qt.EditRole:
            self.list[row][column] = value
            self.dataChanged.emit(index, index)
            return True

        if role == Qt.CheckStateRole and column == 0:
            self.list[row][column] = QCheckBox('')
            if value == Qt.Checked:
                self.list[row][column].setChecked(True)
            else:
                self.list[row][column].setChecked(False)
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:

                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return "not implemented"
            else:
                return "%d" % (section + 1)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = View()
    test.show()
    app.exec_()
