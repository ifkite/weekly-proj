# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tweet.ui'
#
# Created: Mon May 26 21:41:24 2014
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from demo import tweibo_test
import MySQLdb

#use singleton
def connectDb():
    cont=MySQLdb.connect(user='root',passwd='calm')#set your user and passwd pairs in your MySQL first
    cont.set_character_set('utf8')
    cur=cont.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    cur.execute('''USE tweet''')
    return (cont,cur)

cont,cur=connectDb()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("TencentWeibo")
        MainWindow.resize(779, 474)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(60, 280, 631, 141))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 629, 139))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 250, 62, 17))
        self.label.setObjectName("label")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(60, 70, 631, 161))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.pushButton = QtGui.QPushButton(self.tab_3)
        self.pushButton.setGeometry(QtCore.QRect(50, 50, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab_3, "")
        self.tabShow = QtGui.QWidget()
        self.tabShow.setObjectName("tabShow")
        self.pushButton_2 = QtGui.QPushButton(self.tabShow)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 50, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtGui.QPushButton(self.tabShow)
        self.pushButton_3.setGeometry(QtCore.QRect(190, 50, 93, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tabWidget.addTab(self.tabShow, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 779, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.setSignal()
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "log", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "scratch", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "scratch", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "subject", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "time", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabShow), QtGui.QApplication.translate("MainWindow", "show result", None, QtGui.QApplication.UnicodeUTF8))
    
    def setSignal(self):
        self.pushButton_2.clicked.connect(self.pr)
        self.pushButton_3.clicked.connect(self.pop)
    def pr(self):
        self.popwin=PopWin()
        # self.popwin.setGeometry(QtCore.QRect(200, 200, 120, 120))
        li=cur.execute('''SELECT subject,count(subject) from tweet_info group by subject ORDER BY count(subject) DESC LIMIT 10''')
        res=cur.fetchall()

        # resColumn=len(res[0])
        # for i in range(resColumn)
        for i in range(2):
            row=0
            for r in res:
                tmp=str(r[i])
                item=QtGui.QTableWidgetItem(tmp.decode('utf-8'))
                self.popwin.tableWidget.setItem(row,i,item)
                row=row+1
        
        # t=u'中文'
        # item=QtGui.QTableWidgetItem(t)
        # self.popwin.tableWidget.setItem(0,0,item)
        self.popwin.show()
        print 'pushbutton clicked [:3]'
            
    def pop(self):
        self.date=DateWin()
        # print self.date.dateEdit.date().day(),self.date.dateEdit.date().month(),self.date.dateEdit.date().year()
        print self.date.dateEdit.date().getDate()
        self.date.show()

class PopWin(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        # self.setGeometry(QtCore.QRect(500, 360, 500, 360))
        self.resize(400,300)
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 62, 17))
        self.label.setObjectName("label")
        self.tableWidget = QtGui.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 351, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0,160)
        self.tableWidget.setColumnWidth(1,160)
        self.tableWidget.setRowCount(10)
        self.retranslateUi()
        
    def retranslateUi(self):
            self.label.setText(QtGui.QApplication.translate("QWidget", "data", None, QtGui.QApplication.UnicodeUTF8))


class DateWin(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(400,300)
        
        self.dateEdit = QtGui.QDateEdit(self)
        self.dateEdit.setGeometry(QtCore.QRect(20, 240, 110, 27))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setCalendarPopup(True)
        
        self.tableWidget = QtGui.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 351, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0,160)
        self.tableWidget.setColumnWidth(1,160)
        self.tableWidget.setRowCount(10)

        self.dateEdit_2 = QtGui.QDateEdit(self)
        self.dateEdit_2.setGeometry(QtCore.QRect(150, 240, 110, 27))
        self.dateEdit_2.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(1752, 9, 14), QtCore.QTime(0, 0, 0)))
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(280, 240, 93, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText(QtGui.QApplication.translate("Form", "show", None, QtGui.QApplication.UnicodeUTF8))
        self.setSignal()

    def setSignal(self):
        self.pushButton.clicked.connect(self.prDate)

    def prDate(self):
        beginDate=self.dateEdit.date().getDate()
        endDate=self.dateEdit_2.date().getDate()
        if beginDate>endDate:
            beginDate,endDate=endDate,beginDate
        from datetime import date
        beginDateStr=date(beginDate[0],beginDate[1],beginDate[2]).isoformat()
        endDateStr=date(endDate[0],endDate[1],endDate[2]).isoformat()
        print beginDateStr,endDateStr
        queryDate="select post_time,count(subject) from tweet_info group by date(post_time) having post_time between date('"+beginDateStr+"') and date('"+endDateStr+"') ORDER BY subject DESC LIMIT 10;"
        # print queryDate
        li=cur.execute(queryDate)
        res=cur.fetchall()
        for i in range(2):
            row=0
            for r in res:
                if isinstance(r[i],long):
                    tmp=str(r[i])
                    
                # elif isinstance(r[i],datetime.datetime):
                else:
                    tmp=str(r[i].date())
                    # pass
                item=QtGui.QTableWidgetItem(tmp.decode('utf-8'))
                self.tableWidget.setItem(row,i,item)
                row=row+1
        
        # cur.execute('select count(subject),post_time from tweet_info group by date(post_time) having post_time between date('2014-05-01') and date('2014-05-28');')
        
        # self.calendarWidget = QtGui.QCalendarWidget(self)
        # self.calendarWidget.setGeometry(QtCore.QRect(20, 40, 280, 172))
        # self.calendarWidget.setObjectName("calendarWidget")
        # self.setSignal()
        # self.label = QtGui.QLabel(self)
        # self.label.setGeometry(QtCore.QRect(10, 260, 62, 17))
        # self.label.setObjectName("label")
        # self.label_2 = QtGui.QLabel(self)
        # self.label_2.setGeometry(QtCore.QRect(190, 260, 62, 17))
        # self.label_2.setObjectName("label_2")
        
        # self.textEdit_2 = QtGui.QTextEdit(self)
        # self.textEdit_2.setGeometry(QtCore.QRect(240, 260, 104, 21))
        # self.textEdit_2.setObjectName("textEdit_2")

        # self.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        # self.label.setText(QtGui.QApplication.translate("Form", "begin", None, QtGui.QApplication.UnicodeUTF8))
        # self.label_2.setText(QtGui.QApplication.translate("Form", "end", None, QtGui.QApplication.UnicodeUTF8))
    
    # def setSignal(self):
    #     self.dateEdit.clicked.connect(self.pr)
    
    # def pr(self):
    #     print 'baidu'
if __name__=='__main__':
    import sys
    app=QtGui.QApplication(sys.argv)
    window=QtGui.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
