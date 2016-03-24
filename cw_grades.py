from PyQt5 import QtCore, QtWidgets, QtGui
from dialog import Ui_Dialog as Form
import loginUI
import login
import sys
import bisect


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self, data):
        QtWidgets.QMainWindow.__init__(self)
        self.data = data
        self.tabList, self.tableList, self.labelList, self.labelList2 = ([] for _ in range(4))
        self.perclist = []
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.moduleTab = QtWidgets.QTabWidget()
        self.moduleTab.insertTab(0, QtWidgets.QWidget(), "Summary")
        self.table_summary = QtWidgets.QTableWidget()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(630, 400)

        self.centralwidget.setObjectName("centralwidget")
        layoutList, frameList, frame_labelList, layout_labelList = ([] for _ in range(4))

        layout = QtWidgets.QVBoxLayout()
        aWidget = QtWidgets.QWidget()

        columnNames = ["Due Date", "Coursework Title", "Weight", "Mark", "Final Mark"]
        stylesheet = """
        QScrollBar:vertical, QScrollBar:horizontal {
            b.order: solid #999999;
            width:12px;
            height:12px;
        }
        QHeaderView::section{Background-color:rgb(34,221,81); font:bold}
        QTableView{gridline-color: rgb(107, 107, 107)}
        """

        for i in range(len(self.data)):
            self.tabList.append(QtWidgets.QWidget())
            frame_labelList.append(QtWidgets.QFrame())
            frame_labelList[i].setGeometry(QtCore.QRect(100, 285, 400, 65))
            layout_labelList.append(QtWidgets.QVBoxLayout(frame_labelList[i]))
            self.labelList.append(QtWidgets.QLabel(frame_labelList[i]))
            self.labelList2.append(QtWidgets.QLabel(frame_labelList[i]))
            self.moduleTab.addTab(self.tabList[i], self.data[i]['Module'][0])
            self.tableList.append(QtWidgets.QTableWidget(self.tabList[i]))

            layoutList.append(QtWidgets.QVBoxLayout(self.tabList[i]))

            self.tableList[i].setColumnCount(len(columnNames))
            self.tableList[i].setRowCount(int(len(self.data[i]["Module"])))


            self.tableList[i].setMaximumHeight(280)

            self.tableList[i].setHorizontalHeaderLabels(columnNames)
            self.tableList[i].horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            self.tableList[i].setColumnWidth(0, 90)
            self.tableList[i].setColumnWidth(1, 170)

            self.tableList[i].verticalHeader().setVisible(False)
            self.tableList[i].setStyleSheet(stylesheet)
            layout_labelList[i].addWidget(self.labelList[i])
            layout_labelList[i].addWidget(self.labelList2[i])
            self.labelList[i].setAlignment(QtCore.Qt.AlignCenter)
            self.labelList2[i].setAlignment(QtCore.Qt.AlignCenter)
            self.labelList[i].setGeometry(180,300,400,30)


            layoutList[i].addWidget(self.tableList[i], 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            frame_labelList[i].setParent(self.tabList[i])
            self.tableList[i].setAlternatingRowColors(True)

        def average_exam_mark(column):
            total = 0
            count = 0
            for row in range(self.table_summary.rowCount()):
                try:
                    total += int(self.table_summary.item(row, column).text())
                    count += 1
                except (AttributeError, ValueError):
                    average_label.setText("")
                    pass
            if count != 0:
                average_label.setText("Average mark needed for a " + self.table_summary.horizontalHeaderItem(column).text() + ": " + str(round(total/count, 1)))


        self.table_summary.cellPressed.connect(lambda: average_exam_mark(self.table_summary.currentColumn()))

        self.moduleTab.setCurrentIndex(0)

        layout_summary = QtWidgets.QGridLayout(self.moduleTab.widget(0))
        self.table_summary.setAlternatingRowColors(True)
        self.table_summary.verticalHeader().setVisible(False)
        self.table_summary.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table_summary.setColumnCount(8)
        self.table_summary.setStyleSheet(stylesheet)
        self.table_summary.setHorizontalHeaderLabels(["Module", "Current %", "Current Grade", "C/W Weight", "First", "2:1", "2:2", "Pass"])
        self.table_summary.setRowCount(len(self.data))
        self.table_summary.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_summary.horizontalHeaderItem(1).setToolTip("Assumes you have at least attempted all of the coursework so far<p style='white-space:pre'>If there is a coursework that you didn't do and the deadline has passed, then you will need to manually set that coursework mark to 0 in the respective module tab")
        for i in range(9):
            self.table_summary.setItemDelegateForColumn(i,NotEditableTableItem(self.table_summary))
        layout_summary.addWidget(self.table_summary, 1, 0, QtCore.Qt.AlignCenter)
        weights_btn = QtWidgets.QPushButton(self.moduleTab.widget(0))
        layout_summary.addWidget(weights_btn, 0, 0, QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)
        weights_btn.setText("Get coursework weights")
        weights_btn.setToolTip("Grabs the percentage that coursework makes up for each module. This is a requirement to calculate the marks needed in the exam")
        weights_btn.adjustSize()
        hide_btn = QtWidgets.QPushButton(self.moduleTab.widget(0))
        layout_summary.addWidget(hide_btn, 0, 0, QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
        hide_btn.setText("Hide exam marks")
        hide_btn.adjustSize()
        show_btn = QtWidgets.QPushButton(self.moduleTab.widget(0))
        layout_summary.addWidget(show_btn, 0, 0, QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
        show_btn.setText("Show exam marks")
        show_btn.setToolTip("Displays the marks needed in the exam to obtain the grade shown")
        show_btn.adjustSize()
        average_label = QtWidgets.QLabel(self.moduleTab.widget(0))
        layout_summary.addWidget(average_label, 2, 0, QtCore.Qt.AlignHCenter)

        timer = QtCore.QTimer()
        timer.setSingleShot(True)

        hide_btn.clicked.connect(lambda:hideC())
        show_btn.clicked.connect(lambda:showC())
        weights_btn.clicked.connect(lambda:add_weights(0))

        def hideC():
            self.table_summary.hideColumn(4)
            self.table_summary.hideColumn(5)
            self.table_summary.hideColumn(6)
            self.table_summary.hideColumn(7)
            MainWindow.setFixedSize(630,400)
            show_btn.show()
            hide_btn.hide()
            if weights_btn.isVisible():
                show_btn.hide()
        hideC()

        def showC():
            self.table_summary.showColumn(4)
            self.table_summary.showColumn(5)
            self.table_summary.showColumn(6)
            self.table_summary.showColumn(7)
            MainWindow.setFixedSize(self.moduleTab.sizeHint().width() + 20, 400)
            hide_btn.show()
            show_btn.hide()

        def add_weights(row):
            if row<len(self.data):
                weight = login.get_weights(self.data[row]['Module'][0])
                if weight=="Session Error":
                    dialog = QtWidgets.QDialog(None, QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)
                    dialog.ui = Form()
                    dialog.ui.setupUi(dialog)
                    dialog.ui.label.setText("To get coursework weights, you must log in again. Click OK to continue.")
                    dialog.exec_()
                    dialog.show()
                    global form
                    form = LoginApp()
                    form.show()
                    MainWindow.close()
                    return
                self.table_summary.setItem(row,3,QtWidgets.QTableWidgetItem(weight))

                timer.singleShot(0, lambda:add_weights(row+1))
            else:
                timer.stop()
                timer.deleteLater()
                weights_btn.hide()
                self.fillSummary()
                show_btn.show()

                list_of_cw_weights = [self.table_summary.item(i,3).text() for i in range(len(self.data))]

                weights_file_w = open("weights", "wb")
                pickle.dump(list_of_cw_weights, weights_file_w)
                weights_file_w.close()

        try:
            import pickle
            weights_file_r = open("weights", "rb")
            pickle_weights = pickle.load(weights_file_r) #have to unwrap layers of pickle
            if len(pickle_weights)==len(self.data):
                for x in range(len(self.data)):
                    self.table_summary.setItem(x,3,QtWidgets.QTableWidgetItem(pickle_weights[x]))
            weights_file_r.close()
            weights_btn.hide()
        except (FileNotFoundError, EOFError):
            show_btn.hide()
            pass

        self.moduleTab.currentChanged.connect(lambda:hideC())

        layout.addWidget(self.moduleTab)
        aWidget.setLayout(layout)

        MainWindow.setCentralWidget(aWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def fillSummary(self):
        for i in range(len(self.data)):
            self.table_summary.setItem(i,0,QtWidgets.QTableWidgetItem(self.data[i]['Module'][0]))
            if self.perclist[i]!=0:
                item = QtWidgets.QTableWidgetItem(str(self.perclist[i]))
                self.table_summary.setItem(i,1,item)
            self.marks_needed(i)

            grade = self.mark_to_grade(self.perclist[i])
            if grade in ("First Class","Fail","Pass") and self.perclist[i]!=0:
                self.table_summary.setItem(i,2,QtWidgets.QTableWidgetItem(grade))
            else:
                self.table_summary.setItem(i,2,QtWidgets.QTableWidgetItem(grade[5:17]))
            self.color_cell_value(self.table_summary.item(i, 1))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.dict2table()
        self.currPc()
        self.paintcell()
        self.fillSummary()
        for table in self.tableList:
            table.cellChanged.connect(lambda:self.currPc())
            table.cellChanged.connect(lambda:self.paintcell())
            table.cellChanged.connect(lambda:self.fillSummary())

        MainWindow.setWindowTitle(_translate("MainWindow", "Grades"))

    def dict2table(self):
        for table in self.tableList:
            for x in range(len(self.data)):
                for row, item in enumerate(self.data[x]["Due Date"]):
                    new_item = QtWidgets.QTableWidgetItem(item)
                    self.tableList[x].setItem(row, 0, new_item)
                for row, item in enumerate(self.data[x]["Coursework Title"]):
                    new_item = QtWidgets.QTableWidgetItem(item)
                    self.tableList[x].setItem(row, 1, new_item)
                for row, item in enumerate(self.data[x]["Weight"]):
                    new_item = QtWidgets.QTableWidgetItem(item)
                    self.tableList[x].setItem(row, 2, new_item)
                for row, item in enumerate(self.data[x]["Mark"]):
                    new_item = QtWidgets.QTableWidgetItem(item)
                    new_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableList[x].setItem(row, 3, new_item)
                for row, item in enumerate(self.data[x]["Final Mark"]):
                    new_item = QtWidgets.QTableWidgetItem(item)
                    new_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableList[x].setItem(row, 4, new_item)
            for y in range(4):
                table.setItemDelegateForColumn(y,NotEditableTableItem(table))

            table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)

    @staticmethod
    def perc_to_float(percentage):
        """ Takes a percentage of form int% and returns it as a float """
        return float(percentage.strip('%'))/100

    @staticmethod
    def check_mark(entry):
        """ Checks if the table entry is a valid mark. Returns the float if it is and returns None if it is not."""
        try:
            return float(entry)
        except ValueError:
            return None

    def currPc(self):
        markList, weightList, sumprods, sumweights = ([] for _ in range(4))
        blockdict = {}
        block = {}
        del self.perclist[:]

        total = 0
        for i,table in enumerate(self.tableList):
            for x in range(table.rowCount()):
                markList.append(self.check_mark(table.item(x, 4).text()))
                weightList.append(self.perc_to_float(table.item(x,2).text()))
                blockdict[i] = table.rowCount()
        for v in blockdict:
            total += blockdict[v]
            block[v] = total
        try:
            for y in range(len(block)):
                sumprods.append(sum(j*k if isinstance(j,float) else 0 for j, k in zip(markList[block[y]:block[y+1]], weightList[block[y]:block[y+1]])))
                sumweights.append(sum(k if isinstance(j,float) else 0 for j, k in zip(markList[block[y]:block[y+1]], weightList[block[y]:block[y+1]])))
        except KeyError:
            pass
        sumprods.insert(0,sum(j*k if isinstance(j,float) else 0 for j, k in zip(markList[0:block[0]], weightList[0:block[0]])))
        sumweights.insert(0,sum(k if isinstance(j,float) else 0 for j, k in zip(markList[0:block[0]], weightList[0:block[0]])))
        for x in range(len(sumprods)):
            if sumprods[x] in ("","-") or sumweights[x]==0:
                self.perclist.append(0.0)
                self.labelList[x].setText("")
                self.labelList2[x].setText("")
            else:
                self.perclist.append(round((sumprods[x] / sumweights[x]), 2))
                if self.perclist[x] != 0.0 and sumweights[x]<1.001:
                    self.labelList[x].setText("<span style='font-size:12pt; font-weight:500;'>Your current percentage is: </span><span style='font-size:12pt'>" + str(self.perclist[x]) + "%</span>")
                    self.labelList2[x].setText("<span style='font-size:12pt; font-weight:500;'>Your current grade is: </span><span style='font-size:12pt'>" + self.mark_to_grade(self.perclist[x]) + "</span>")
                elif sumweights[x]>1.001:
                    self.labelList[x].setText("<span style='font-size:12pt; font-weight:500;'>(Sum of weights is >100%): </span><span style='font-size:12pt'>" + str(self.perclist[x]) + "%</span>")

    def paintcell(self):
        """ Feeds every mark from the table to the color_cell_value function """
        for table in self.tableList:
            table.blockSignals(True)
            for x in range(len(self.data)):
                for row, item in enumerate(self.data[x]["Final Mark"]):
                    tableitem = table.item(row,4)
                    self.color_cell_value(tableitem)
            table.blockSignals(False)

    @staticmethod
    def color_cell_value(tableitem):
        """ Sets tableitem cell background to a colour based on its value unless it has an invalid value"""
        if hasattr(tableitem, "text"):
            try:
                f = float(tableitem.text())
            except ValueError:
                tableitem.setBackground(QtGui.QBrush())
                return
            background = QtGui.QLinearGradient(0, 0, f, 0)
            background.setColorAt(1.00, QtGui.QColor('#fafafa'))
            if float(tableitem.text()) < 40:
                if float(tableitem.text()) == 0:
                    background = QtGui.QLinearGradient(0, 0, 0.01, 0)
                    background.setColorAt(1.00, QtGui.QColor('#fafafa'))
                background.setColorAt(0.00, QtGui.QColor('#ff0000'))
                background.setColorAt(0.99, QtGui.QColor('#ff0000'))
            if 40 <= float(tableitem.text()) < 50:
                background.setColorAt(0.00, QtGui.QColor('#ffdd00'))
                background.setColorAt(0.99, QtGui.QColor('#ffdd00'))
            if 50 <= float(tableitem.text()) < 60:
                background.setColorAt(0.00, QtGui.QColor('#eaff00'))
                background.setColorAt(0.99, QtGui.QColor('#eaff00'))
            if 60 <= float(tableitem.text()) < 70:
                background.setColorAt(0.00, QtGui.QColor('#b7ff00'))
                background.setColorAt(0.99, QtGui.QColor('#b7ff00'))
            if 70 <= float(tableitem.text()) < 500:
                background.setColorAt(0.00, QtGui.QColor('#00ff00'))
                background.setColorAt(0.99, QtGui.QColor('#00ff00'))
            elif float(tableitem.text()) >= 500:
                tableitem.setBackground(QtGui.QBrush((QtGui.QPixmap("kappa.png"))))
                return

            tableitem.setBackground(QtGui.QBrush(background))

    @staticmethod
    def mark_to_grade(mark, breakpoints=[40, 50, 60, 70], grades=["Fail","Pass","2:2, Lower Second-Class","2:1, Upper Second-Class","First Class"]):
        """ Checks mark against breakpoints and returns the appropriate grade """
        i = bisect.bisect(breakpoints, mark)
        return grades[i]

    def marks_needed(self, row):
        """ Calculates mark needed using a formula when given the weight of the coursework and current percentage """
        try:
            curr_perc = float(self.table_summary.item(row,1).text())/100
            for i,j in zip(range(4,8), reversed(range(4,8))):
                cw_weight = self.perc_to_float(self.table_summary.item(row, 3).text())
                mark = int(round(100*(i/10 -(curr_perc * cw_weight))/(1.0-cw_weight)))
                item = QtWidgets.QTableWidgetItem(str(mark))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_summary.setItemDelegateForColumn(j,NotEditableTableItem(self.table_summary))
                self.table_summary.setItem(row,j,item)
                if mark>100:
                    self.table_summary.item(row, j).setForeground(QtGui.QColor('#ff0000'))
                elif mark<=0:
                    self.table_summary.item(row, j).setForeground(QtGui.QColor('#00ff00'))
        except (AttributeError, ValueError) as e:
            pass


class NotEditableTableItem(QtWidgets.QItemDelegate):
    """
    Create a readOnly QTableWidgetItem
    """
    def __init__(self, parent):

        QtWidgets.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        item = QtWidgets.QLineEdit(parent)
        item.setReadOnly(True)
        return item

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())


class LoginApp(QtWidgets.QMainWindow, loginUI.Ui_LoginWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_login.clicked.connect(self.login)
        self.lineEdit_password.returnPressed.connect(self.login)

    def login(self):
        self.setWindowTitle("Logging in...")
        doLogin_return = login.startLogin()
        dialog = QtWidgets.QDialog(None, QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)
        dialog.ui = Form()
        dialog.ui.setupUi(dialog)

        if doLogin_return == "Fail":
            self.setWindowTitle("Login")
            dialog.ui.label.setText("Login failed. Please try again.")
            dialog.exec_()
            dialog.show()
        elif doLogin_return == "Empty Fail":
            self.setWindowTitle("Login")
            dialog.ui.label.setText("Please enter your login details and try again.")
            dialog.exec_()
            dialog.show()
        elif doLogin_return == "Connection Fail":
            self.setWindowTitle("Login")
            dialog.ui.label.setText("Failed to establish a connection. Please check your network settings and the status of SEMS Intranet.")
            dialog.exec_()
            dialog.show()
        else:
            data = login.FormatData()
            dialog.close()
            self.close()

            import main
            file = open("data", "wb")
            main.pickle.dump(main.datetime.datetime.today(), file)
            main.pickle.dump(data, file)
            file.close()

            OpenMainWindow(data)

    def input_user(self):
        user = self.lineEdit_username.text()
        return user
    def input_pass(self):
        passw = self.lineEdit_password.text()
        return passw


def OpenMainWindow(data):
    global MainWindow
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(data)
    ui.setupUi(MainWindow)
    MainWindow.show()

def main_window():
    return form

def main():
    global form
    app = QtWidgets.QApplication(sys.argv)
    form = LoginApp()
    form.show()
    sys.exit(app.exec_())