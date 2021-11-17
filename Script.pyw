# Importing Libraries This Browser Needs
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFocusEvent as focus

# Setting Up This Browser
class WebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        page = WebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @pyqtSlot(QUrl)
    def on_url_changed(self, url):
        url2str = url.toString()
        addslash = url2str.endswith("/" or ".html")
        if not addslash == True:
            url = QUrl(url2str + "/")
            window.newtab(qurl=url)
        else:
            window.newtab(qurl=url)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(QSize(480, 360))
        self.resize(QSize(1200, 800))

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.maximize)
        self.tabs.currentChanged.connect(self.tabchanged)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closetab)
        self.setCentralWidget(self.tabs)

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)
        navbar.setContextMenuPolicy(Qt.PreventContextMenu)
        navbar.setMovable(False)

        # Back Button
        backbtn = QAction(QIcon('back.png'), 'Back', self)
        backbtn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(backbtn)

        # Forward Button
        forwardbtn = QAction(QIcon('forward.png'), 'Forward', self)
        forwardbtn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forwardbtn)

        # Reload Button
        reloadbtn = QAction(QIcon('reload.png'), 'Reload', self)
        reloadbtn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reloadbtn)

        # Adding a space between the reload button and URL Bar
        Separatorlabel = QLabel()
        Separatorlabel.setText(" ")
        navbar.addWidget(Separatorlabel)

        # URL Bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigatetourl)
        navbar.addWidget(self.urlbar)

        # Adding a separator
        navbar.addSeparator()

        # Adding a search label and search box
        Searchlabel = QLabel()
        Searchlabel.setText("Search ")
        navbar.addWidget(Searchlabel)
        self.searchbox = QLineEdit()
        self.searchbox.returnPressed.connect(self.doasearch)
        self.searchbox.setFixedWidth(300)
        navbar.addWidget(self.searchbox)

        # Adding a separator
        navbar.addSeparator()

        # Adding a new tab button
        self.newtabButton = QAction("New Tab", self)
        self.newtabButton.triggered.connect(self.newtab)
        navbar.addAction(self.newtabButton)

        # Creating First Tab
        self.newtab()

        # Show Everything
        self.show()

        # Setting the Application icon
        self.setWindowIcon(QIcon('FAX.png'))

        # Menubar
        # New Window
        newwinAction = QAction('&New Window', self)
        newwinAction.setShortcut('Ctrl+Shift+N')
        newwinAction.triggered.connect(self.newwin)

        # Exit
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Shift+Q')
        exitAction.triggered.connect(self.exit)

        # About FAX
        aboutAction = QAction('&About FAX', self)
        aboutAction.setShortcut('F1')
        aboutAction.triggered.connect(self.about)

        # Seting Up Menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newwinAction)
        fileMenu.addAction(exitAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)

    # Defining things
    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def doasearch(self):
        keyword = self.searchbox.text()
        url = QUrl("https://www.duckduckgo.com/?q=" + keyword)
        self.tabs.currentWidget().setUrl(url)
        self.searchbox.clear()
        browser.setFocus()

    def exit(self):
        self.close()

    def newwin(self):
        MainWindow()

    def about(self):
        aboutfax = QMessageBox()
        aboutfax.setWindowTitle("About")
        aboutfax.setText("""FAX Version 1.001.000

(c) The Jiusoft Team. All rights reserved.""")
        aboutfax.setIcon(QMessageBox.Information)
        aboutfax.setWindowIcon(QIcon('FAX.png'))
        x = aboutfax.exec_()

    def newtab(self, *args, qurl=None, label="about:blank"):
        if qurl is None:
            qurl = QUrl('https://www.duckduckgo.com')
        global browser
        browser = QWebEngineView()
        page = WebEnginePage(browser)
        browser.setPage(page)
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.updateurl(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def openatab(self, i):
        if i == -1:
            self.newtab()

    def tabchanged(self, i):
        qurl = self.tabs.currentWidget().url()
        self.updateurl(qurl, self.tabs.currentWidget())
        self.updatetitle(self.tabs.currentWidget())

    def closetab(self, i):
        if self.tabs.count() < 2:
            self.tabs.currentWidget().setUrl(QUrl('https://www.duckduckgo.com'))
        else:
            self.tabs.removeTab(i)

    def updatetitle(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()

    def navigatetourl(self):
        url = QUrl(self.urlbar.text())
        if url.scheme() == "":
            url.setScheme("https")
        if url.scheme() == "http":
            url.setScheme("https")
        self.tabs.currentWidget().setUrl(url)
        browser.setFocus()

    def updateurl(self, url, browser=None):
        self.urlbar.setText(url.toString())
        if browser != self.tabs.currentWidget():
            return


# Executing The Browser
app = QApplication(sys.argv)
QApplication.setApplicationName('FAX')
window = MainWindow()
app.exec_()
