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

        #サイズ固定
        # self.setFixedSize(850, 500)

        #Viewを作成
        self.tableView = QTableView()
        self.tableView.clicked.connect(self.viewClicked)
        self.tableView.setFixedSize(700, 300)
        #Viewの罫をブラックにする
        self.tableView.setStyleSheet("QTableView{gridline-color: black}")

        self.headers = ["▽", "1", "2", "3", "4", "5", "6", "7"]
        tableData0 = [
                     [QCheckBox(''), "1", "2", "3", "4", "5", "6", 1],
                     ]

        #モデルを作成
        self.model = MyTableModel(tableData0, self.headers)
        self.tableView.setModel(self.model)

        #Insert、remove用の選択行に行の最大値をセット
        self.selectRow = self.model.rowCount(QModelIndex())

        #csv用のファイルフィルタをセット
        self.filters = "CSV files (*.csv)"

        #ファイル名を初期化
        self.fileName = None

        #ボタン作成
        self.buttonNew = QPushButton('NEW', self)
        self.buttonOpen = QPushButton('Open', self)
        self.buttonSave = QPushButton('Save', self)
        self.buttonAdd = QPushButton('add', self)
        self.buttonDell = QPushButton('Dell', self)

        #ボタングループをセット
        self.group = QButtonGroup()
        self.group.addButton(self.buttonNew)
        self.group.addButton(self.buttonOpen)
        self.group.addButton(self.buttonSave)
        self.group.addButton(self.buttonAdd)
        self.group.addButton(self.buttonDell)

        #Signal、Slotを設定
        self.buttonNew.clicked.connect(self.handleNew)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonSave.clicked.connect(self.handleSave)
        self.buttonAdd.clicked.connect(self.insertRows)
        self.buttonDell.clicked.connect(self.removeRows)

        #水平レイアウトを設定
        layout = QHBoxLayout()

        layout.addWidget(self.buttonNew)
        layout.addWidget(self.buttonOpen)
        layout.addWidget(self.buttonSave)
        layout.addWidget(self.buttonAdd)
        layout.addWidget(self.buttonDell)

        #Plotボタン
        self.buttonPlot = QPushButton('PLOT', self)
        self.buttonPlot.clicked.connect(self.plot)

        #Plotボタン
        self.graph = gl.GLViewWidget(self)
        self.graph.opts['distance'] = 10
        self.graph.show()
        self.g = gl.GLGridItem()
        self.graph.addItem(self.g)

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
        self.graph.addItem(self.scttrPlt)

        #垂直レイアウトを設定
        Vlayout = QVBoxLayout()
        # Vlayout.addWidget(self.tableView)
        Vlayout.addWidget(self.buttonPlot)
        Vlayout.addWidget(self.graph)
        Vlayout.addWidget(self.tableView)
        Vlayout.addLayout(layout)

        #全体のレイアウトをセット
        self.setLayout(Vlayout)

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

        defaultValue =[
        [QCheckBox(''), "1", "2", "3", "4", "5", "6", 1]
        ]

        self.model = None
        self.model = MyTableModel(defaultValue, self.headers)
        print(defaultValue)
        self.tableView.setModel(self.model)

    #Viewとモデルに行追加→選択されている行の上に1行挿入します
    def insertRows(self, position, rows=1, index=QModelIndex()):
        print("position: %d"%position)
        print("rows: %d" % rows)
        print("rowCount: %d" % self.model.rowCount(QModelIndex()))

        position = self.selectRow
        self.model.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.model.list.insert(position, [QCheckBox(''), "1", "2", "3", "4", "5", "6", 1])

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
