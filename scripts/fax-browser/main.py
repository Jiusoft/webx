"""
Original repository link: https://github.com/Jiusoft/fax-browser
"""
# Importing Libraries This Browser Needs
import sys
import platform
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
from download import download_file
from datetime import datetime
import os
import sqlite3
from history import compile_sqlte3_to_html_history
from bookmark import compile_sqlte3_to_html_bookmark

if os.name == 'nt':
    os.system("cls")
else:
    os.system("clear")

print("""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/((((((&@((((((((((@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@&@((((((((((((@###@/((((((((((((((%@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@/((((((((((((((@######&((((((((((((((((((@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@((((((((((((((((/@########@((((((((((((((((((((@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@((((((((((((((((((#%##########@(((((((((((((((((((((%&@@@@@@@@@@@@
@@@@@@@@@@@@/((((((((((((((((((@#############&#(((((((((((((((((((((#@@@@@@@@@@@
@@@@@@@@@@((((((((((((((((((((@################&((((((((((((((((((((((@@@@@@@@@@
@@@@@@@@@(((((((((((((((((((/@##################@(((((((((((((((((((((((&@@@@@@@
@@@@@@@&((((((((((((((((((((@########&&&&########@(((((((((((((((((((((((@@@@@@@
@@@@@@&((((((((((((((((((((@@@@@@@@@@@@@@@@@@@@@@@@#((((((((((((((((((((((@@@@@@
@@@@@@(((((((((((((((%@#(/@@@@@@@@@@@@@@@@@@@@@@@@@@(((%@%(((((((((((((((((@@@@@
@@@@@/((((((((((%@(((((((@@@@@@@@@@@@@@@@@@@@@@@@@@@&(((((((/@@((((((((((((#@@@@
@@@@@(((((((@&((((((((((@@@@@@@@@@@@@@  @@@@@@@@@@@@@((((((((((((/@@/(((((((@@@@
@@@@%((@@((((((((/ ((((/@@@@@@@@@@@@@ @  @@@@@@@@@@@@%((/ /(.(((((((((/@@/((@@@@
@@@@@@(((((((((((/ (( ((@@@@@@@@@@@@ @@@  @@@@@@@@@@@&((((. (((((((((((((((/@@@@
@@@@@(((/@@/(((((/ (((((@@@@@@@@@@@ @@@@@  @@@@@@@@@@&((**((  ((((((((&@%(((@@@@
@@@@&(((((((((@@((((((((@@@@@@@@@@ @@@@@@@  @@@@@@@@@#(((((((((((@@/(((((((//@@@
@@@@@%(((((((((((((#@&((%@@@@@@@@@@@@@@@@@@@@@@@@@@@&((((((@@/(((((((((((((@@@@@
@@@@@@(((((((((((((((((((@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&/((((((((((((((((((#@@@@@
@@@@@@@(((((((((((((((((((@.,,,,.*@@@@@@@@@@@@,.,,@((((((((((((((((((((((/@@@@@@
@@@@@@@@(((((((((((((((((((@,,,,,,,,,,,,,,,,,,,,,@(((((((((((((((((((((((@@@@@@@
@@@@@@@@@(((((((((((((((((((&*,,,,,,,,,,,,,,,,,,@((((((((((((((((((((((@@@@@@@@@
@@@@@@@@@@@((((((((((((((((((/@,,,,,,,,,,,,,,,,@((((((((((((((((((((((@@@@@@@@@@
@@@@@@@@@@@@@((((((((((((((((((@.,,,,,,,,,,,,*%(((((((((((((((((((((@@@@@@@@@@@@
@@@@@@@@@@@@@@@/((((((((((((((((#(,,,,,,,,,,@((((((((((((((((((((%&@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@/(((((((((((((((@,,,,,,,.@(((((((((((((((((((@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%(((((((((((((@*,,,,*%((((((((((((((((@&@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@(@(((((((((((@,,@/((((((((((((&@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#//&@((//(#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
""")

print("Thank you for using the Fax Browser!\n")

# Setting Up This Browser

try:
    history_conn = sqlite3.connect("history/search_history.db")
    history_c = history_conn.cursor()
    history_c.execute(
        "CREATE TABLE IF NOT EXISTS history(date date, time time, link text)")
    history_conn.commit()
    history_conn.close()

    bookmark_conn = sqlite3.connect("bookmarks/bookmarks.db")
    bookmark_c = bookmark_conn.cursor()
    bookmark_c.execute(
        "CREATE TABLE IF NOT EXISTS bookmark(date datetime, link text)")
    bookmark_conn.commit()
    bookmark_conn.close()
except:
    print(
        "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")

version = "1.0.0"


class WebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        page = WebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @pyqtSlot(QUrl)
    def on_url_changed(self, url):
        url2str = url.toString()
        notaddslash = url2str.endswith(
            "/" or ".xml*" or ".html*" or ".htm*" or ".shtml*" or ".aspx*" or ".do*" or ".css*" or ".xhtml*" or "*.asp*" or ".xht*")
        if not notaddslash:
            url = QUrl(f"{url2str}/")
            window.newtab(qurl=url)
        else:
            window.newtab(qurl=url)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(QSize(800, 600))
        self.resize(QSize(1200, 800))
        self.count = 0

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.maximize)
        self.tabs.currentChanged.connect(self.tabchanged)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closetab)
        self.setCentralWidget(self.tabs)

        try:
            self.history_conn = sqlite3.connect("history/search_history.db")
            self.history_c = self.history_conn.cursor()

            self.bookmark_conn = sqlite3.connect("bookmarks/bookmarks.db")
            self.bookmark_c = self.bookmark_conn.cursor()
        except:
            print(
                "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")

        # Navigation Bar
        global navbar
        navbar = QToolBar()
        self.addToolBar(navbar)
        navbar.setContextMenuPolicy(Qt.PreventContextMenu)
        navbar.setMovable(False)

        # Back Button
        backbtn = QAction(QIcon('img/back.png'), 'Back', self)
        backbtn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(backbtn)

        # Forward Button
        forwardbtn = QAction(QIcon('img/forward.png'), 'Forward', self)
        forwardbtn.triggered.connect(
            lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forwardbtn)

        # Reload Button
        reloadbtn = QAction(QIcon('img/reload.png'), 'Reload', self)
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
        self.newtabButton = QAction(QIcon('img/newtab.png'), "New Tab", self)
        self.newtabButton.triggered.connect(self.newtab)
        navbar.addAction(self.newtabButton)

        # Creating First Tab
        self.newtab()

        # Show Everything
        self.show()

        # Setting the Application icon
        self.setWindowIcon(QIcon('img/FAX.png'))

        # Menubar
        # Open HTML file
        openfile = QAction('&Open', self)
        openfile.setShortcut('Ctrl+O')
        openfile.triggered.connect(self.openfile)

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

        # Bookmark
        bookmarkAction = QAction("&Bookmark This Tab", self)
        bookmarkAction.setShortcut('Ctrl+B')
        bookmarkAction.triggered.connect(self.bookmark)

        # See Bookmarks
        openBookmarksAction = QAction("&Open Bookmarks", self)
        openBookmarksAction.setShortcut('Ctrl+Shift+B')
        openBookmarksAction.triggered.connect(self.openBookmarks)

        # Clear Bookmarks
        clearBookmarksAction = QAction("&Clear Bookmarks", self)
        clearBookmarksAction.setShortcut('Ctrl+Shift+C')
        clearBookmarksAction.triggered.connect(self.removeBookmarks)

        # History
        historyAction = QAction("&Your Browsing History", self)
        historyAction.setShortcut('Ctrl+H')
        historyAction.triggered.connect(self.checkHistory)

        # Clear History
        clearHistoryAction = QAction("&Clear All History", self)
        clearHistoryAction.setShortcut('Ctrl+Shift+H')
        clearHistoryAction.triggered.connect(self.removeHistory)

        # Seting Up Menubar
        global menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openfile)
        fileMenu.addAction(newwinAction)
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)

        bookmarkManagerMenu = menubar.addMenu('&Bookmark Manager')
        bookmarkManagerMenu.addAction(bookmarkAction)
        bookmarkManagerMenu.addAction(openBookmarksAction)
        bookmarkManagerMenu.addAction(clearBookmarksAction)

        historyMenu = menubar.addMenu('&History')
        historyMenu.addAction(historyAction)
        historyMenu.addAction(clearHistoryAction)

    # Defining things
    def openfile(self):
        if platform.system() == "Linux" or platform.system() == "Darwin":
            filepath = QFileDialog.getOpenFileName(
                None, "Open File", "/", "HTML Files (*.htm, *.html)")
        else:
            filepath = QFileDialog.getOpenFileName(
                None, "Open File", "C:\\", "HTML Files (*.htm, *.html)")
        filepath2str = str(filepath)
        filepath2str = filepath2str[2:-32]
        if not filepath2str == "":
            self.newtab(qurl=QUrl(f"file:{filepath2str}"))

    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def doasearch(self):
        keyword = self.searchbox.text()
        url = QUrl("https://duckduckgo.com/?q=" + keyword)
        self.tabs.currentWidget().setUrl(url)
        self.searchbox.clear()
        browser.setFocus()

    def exit(self):
        self.close()
        self.history_conn.close()
        self.bookmark_conn.close()

    def newwin(self):
        MainWindow()

    def about(self):
        aboutfax = QMessageBox()
        aboutfax.setWindowTitle("About")
        aboutfax.setText("""FAX Version 1.001.000

© The Jiusoft Team. All rights reserved.""")
        aboutfax.setIcon(QMessageBox.Information)
        aboutfax.setWindowIcon(QIcon('img/FAX.png'))
        x = aboutfax.exec_()

    def newtab(self, *args, qurl=None, label="about:blank"):
        if qurl is None:
            qurl = QUrl('https://duckduckgo.com/')
        global browser
        browser = QWebEngineView()
        browser.setContextMenuPolicy(Qt.PreventContextMenu)
        page = WebEnginePage(browser)
        browser.setPage(page)
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.updateurl(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))
        browser.page().profile().downloadRequested.connect(download_file)
        browser.page().fullScreenRequested.connect(
            lambda request, browser=browser: self.handle_fullscreen_requested(
                request, browser
            )
        )
        browser.page().profile().setHttpUserAgent(f'FAX/{version}')
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

    def handle_fullscreen_requested(self, request):
        request.accept()
        if self.isMaximized():
            maximize = True
        else:
            maximize = False
        if request.toggleOn():
            self.showFullScreen()
            menubar.hide()
            navbar.hide()
            self.tabs.tabBar().hide()
        else:
            if maximize:
                self.showMaximized()
            else:
                self.showNormal()
            menubar.show()
            navbar.show()
            self.tabs.tabBar().show()

    def openatab(self, i):
        if i == -1:
            self.newtab()

    def tabchanged(self, i):
        qurl = self.tabs.currentWidget().url()
        self.updateurl(qurl, self.tabs.currentWidget())

    def closetab(self, i):
        if self.tabs.count() < 2:
            self.tabs.currentWidget().setUrl(QUrl('https://duckduckgo.com/'))
        else:
            self.tabs.removeTab(i)

    def navigatetourl(self):
        url = QUrl(self.urlbar.text())
        if self.urlbar.text() == "fax://history":
            url = QUrl.fromLocalFile(f"{os.getcwd()}/history/history.html")
        if self.urlbar.text() == "fax://bookmarks":
            url = QUrl.fromLocalFile(f"{os.getcwd()}/bookmarks/bookmarks.html")
        if url.scheme() == "":
            url.setScheme("https")
        if url.scheme() == "http":
            url.setScheme("https")
        self.tabs.currentWidget().setUrl(url)
        browser.setFocus()

    def updateurl(self, url, browser=None):
        now = datetime.now()

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")

        self.url = url

        if len(url.toString()) > 100:
            self.urlbar.setText(f"{url.toString()[:100]}...")
        else:
            self.urlbar.setText(url.toString())

        if url.toString() != QUrl.fromLocalFile(f"{os.getcwd()}/history/history.html").toString() and url.toString() != QUrl.fromLocalFile(f"{os.getcwd()}/bookmarks/bookmarks.html").toString():
            if str(url.toString()) != "":
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', '{str(url.toString())}')")
                self.history_conn.commit()
                compile_sqlte3_to_html_history()
        elif url.toString() == QUrl.fromLocalFile(f"{os.getcwd()}/history/history.html").toString():
            try:
                self.urlbar.setText("fax://history")
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', 'fax://history')")
                self.history_conn.commit()
                compile_sqlte3_to_html_history()
            except:
                print(
                    "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")
        else:
            try:
                self.urlbar.setText("fax://bookmarks")
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', 'fax://bookmarks')")
                self.history_conn.commit()
                compile_sqlte3_to_html_history()
            except:
                print(
                    "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")

        if browser != self.tabs.currentWidget():
            return

    def checkHistory(self):
        current = os.getcwd()
        file_path = current + "/history/history.html"
        qurl = QUrl.fromLocalFile(file_path)
        global browser
        browser = QWebEngineView()
        browser.setContextMenuPolicy(Qt.PreventContextMenu)
        page = WebEnginePage(browser)
        browser.setPage(page)
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, "History")
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.updateurl(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))
        browser.page().fullScreenRequested.connect(
            lambda request, browser=browser: self.handle_fullscreen_requested(
                request, browser
            )
        )
        self.urlbar.setText("fax://history")
        browser.page().profile().setHttpUserAgent(f'FAX/{version}')
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

    def removeHistory(self):
        self.history_conn.commit()
        self.history_conn.close()

        os.remove("history/search_history.db")

        try:
            self.history_conn = sqlite3.connect("history/search_history.db")
            self.history_c = self.history_conn.cursor()

            self.history_c.execute(
                "CREATE TABLE IF NOT EXISTS history(date date, time time, link text)")
        except:
            print(
                "Cannot access file \"search_history.db\"; most likely because of a wrong directory error.")

        compile_sqlte3_to_html_history()

    def bookmark(self):
        now = datetime.now()

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")

        if self.url.toString() == QUrl.fromLocalFile(f"{os.getcwd()}/bookmarks/bookmarks.html").toString():
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', 'fax://bookmarks')")
        elif self.url.toString() == QUrl.fromLocalFile(f"{os.getcwd()}/history/history.html").toString():
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', 'fax://history')")
        else:
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', '{self.url.toString()}')")
        self.bookmark_conn.commit()

        compile_sqlte3_to_html_bookmark()

    def openBookmarks(self):
        compile_sqlte3_to_html_bookmark()

        current = os.getcwd()
        file_path = current + "/bookmarks/bookmarks.html"
        qurl = QUrl.fromLocalFile(file_path)
        global browser
        browser = QWebEngineView()
        browser.setContextMenuPolicy(Qt.PreventContextMenu)
        page = WebEnginePage(browser)
        browser.setPage(page)
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, "Bookmarks")
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.updateurl(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))
        browser.page().fullScreenRequested.connect(
            lambda request, browser=browser: self.handle_fullscreen_requested(
                request, browser
            )
        )
        self.urlbar.setText("fax://bookmarks")
        browser.page().profile().setHttpUserAgent(f'FAX/{version}')
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

    def removeBookmarks(self):
        self.bookmark_conn.commit()
        self.bookmark_conn.close()

        os.remove("bookmarks/bookmarks.db")

        try:
            self.bookmark_conn = sqlite3.connect("bookmarks/bookmarks.db")
            self.bookmark_c = self.bookmark_conn.cursor()

            self.bookmark_c.execute(
                "CREATE TABLE IF NOT EXISTS bookmark(date datetime, link text)")
        except:
            print(
                "Cannot access file \"bookmarks.db\"; most likely because of a wrong directory error.")

        compile_sqlte3_to_html_bookmark()


# Executing The Browser
app = QApplication(sys.argv)
QApplication.setApplicationName('FAX')
window = MainWindow()
app.exec_()
