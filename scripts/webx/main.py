"""
Original repository link: https://github.com/Jiusoft/webx
"""
# Importing Libraries This Browser Needs
import os, sys, socket, platform, subprocess, sqlite3
from contextlib import contextmanager
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtGui import *
from download import download_file
from datetime import datetime
from history import compile_sqlte3_to_html_history
from bookmark import compile_sqlte3_to_html_bookmark

windows = platform.system() == "Windows"
linux = platform.system() == "Linux"
args = sys.argv[1:]


# Setting Up This Browser
def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False


try:
    history_conn = sqlite3.connect(f"{os.path.dirname(os.path.realpath(__file__))}/history/search_history.db")
    history_c = history_conn.cursor()
    history_c.execute(
        "CREATE TABLE IF NOT EXISTS history(date date, time time, link text)")
    history_conn.commit()
    history_conn.close()

    bookmark_conn = sqlite3.connect(f"{os.path.dirname(os.path.realpath(__file__))}/bookmarks/bookmarks.db")
    bookmark_c = bookmark_conn.cursor()
    bookmark_c.execute(
        "CREATE TABLE IF NOT EXISTS bookmark(date datetime, link text)")
    bookmark_conn.commit()
    bookmark_conn.close()
except:
    print(
        "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")

version = "1.0.0"


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


class ListWidget(QListWidget):
    def doubleClicked(self, item):
        bookmark_conn = sqlite3.connect(f"{os.path.dirname(os.path.realpath(__file__))}/bookmarks/bookmarks.db")
        bookmark_c = bookmark_conn.cursor()

        current = item.text()
        # database things for removing bookmarks
        listWidget.takeItem(self.row(item))

        # print(current)
        bookmark_c.execute(f"DELETE FROM bookmark WHERE link='{current}'")

        bookmark_conn.commit()
        bookmark_conn.close()

        compile_sqlte3_to_html_bookmark()


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
    def __init__(self, qurl=None):
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
        QShortcut(QKeySequence('Ctrl+W'), self,
                  lambda: self.closetab(self.tabs.currentIndex()))  # Close current tab shortcut

        try:
            self.history_conn = sqlite3.connect(
                f"{os.path.dirname(os.path.realpath(__file__))}/history/search_history.db")
            self.history_c = self.history_conn.cursor()

            self.bookmark_conn = sqlite3.connect(
                f"{os.path.dirname(os.path.realpath(__file__))}/bookmarks/bookmarks.db")
            self.bookmark_c = self.bookmark_conn.cursor()
        except:
            print(
                "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")

        # Navigation Bar
        global navbar
        navbar = QToolBar()
        self.addToolBar(navbar)
        navbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        navbar.setMovable(False)

        # Back Button
        backbtn = QAction(QIcon(f'{os.path.dirname(os.path.realpath(__file__))}/img/back.png'), 'Back', self)
        backbtn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(backbtn)

        # Forward Button
        forwardbtn = QAction(QIcon(f'{os.path.dirname(os.path.realpath(__file__))}/img/forward.png'), 'Forward', self)
        forwardbtn.triggered.connect(
            lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forwardbtn)

        # Reload Button
        reloadbtn = QAction(QIcon(f'{os.path.dirname(os.path.realpath(__file__))}/img/reload.png'), 'Reload', self)
        reloadbtn.setShortcut('Ctrl+R')
        reloadbtn.triggered.connect(self.reload)
        navbar.addAction(reloadbtn)

        # Adding a space between the reload button and URL Bar
        Separatorlabel = QLabel()
        Separatorlabel.setText(" ")
        navbar.addWidget(Separatorlabel)

        # URL Bar
        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText("Type a url or Search")
        self.urlbar.setToolTip(
            "To go to a url, just type the url;\nTo search, please type \"?\" and a space before your query")
        self.urlbar.returnPressed.connect(self.detectsearch)
        navbar.addWidget(self.urlbar)

        # Adding a separator
        navbar.addSeparator()

        # Adding a new tab button
        #self.newtabButton = QPushButton(QIcon(f'{os.path.dirname(os.path.realpath(__file__))}/img/newtab.png'), "New Tab", self)
        self.newtabButton = QAction(QIcon(f'{os.path.dirname(os.path.realpath(__file__))}/img/newtab.png'), "New Tab", self)
        self.newtabButton.setShortcut('Ctrl+T')
        #self.newtabButton.clicked.connect(self.newtab)
        self.newtabButton.triggered.connect(self.newtab)
        navbar.addAction(self.newtabButton)

        # Creating First Tab
        if qurl == None:
            self.newtab()
        else:
            self.newtab(qurl=qurl)

        # Show Everything
        self.show()

        # Setting the Application icon
        self.setWindowIcon(QIcon('img/WebX.png'))

        # Menubar
        # Quick navigate to address bar
        navigateToAddressBarAction = QShortcut(QKeySequence('F4'), self)

        def navigate_to_addr_bar():
            self.urlbar.selectAll()
            self.urlbar.setFocus()

        navigateToAddressBarAction.activated.connect(navigate_to_addr_bar)

        # Open HTML file
        openhtmlfile = QAction('Open &HTML File', self)
        openhtmlfile.setShortcut('Ctrl+O')
        openhtmlfile.triggered.connect(self.openhtmlfile)

        # Open PDF file
        openpdffile = QAction('Open &PDF File', self)
        openpdffile.setShortcut('Ctrl+Shift+O')
        openpdffile.triggered.connect(self.openpdffile)

        # New Window
        newwinAction = QAction('&New Window', self)
        newwinAction.setShortcut('Ctrl+Shift+N')
        newwinAction.triggered.connect(self.newwin)

        # Exit
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Shift+Q')
        exitAction.triggered.connect(self.exit)

        # About WebX
        aboutAction = QAction('&About WebX', self)
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
        clearBookmarkAction = QAction("&Delete Bookmark", self)
        clearBookmarkAction.setShortcut('Ctrl+Shift+V')
        clearBookmarkAction.triggered.connect(self.removeBookmarks)

        # History
        historyAction = QAction("&View Browsing History", self)
        historyAction.setShortcut('Ctrl+H')
        historyAction.triggered.connect(self.checkHistory)

        # Clear History
        clearHistoryAction = QAction("&Clear All History", self)
        clearHistoryAction.setShortcut('Ctrl+Shift+H')
        clearHistoryAction.triggered.connect(self.removeHistory)

        # Seting Up Menubar
        global menubar
        menubar = self.menuBar()
        menubar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openhtmlfile)
        fileMenu.addAction(openpdffile)
        fileMenu.addAction(newwinAction)
        fileMenu.addAction(exitAction)

        bookmarkManagerMenu = menubar.addMenu('&Bookmarks')
        bookmarkManagerMenu.addAction(bookmarkAction)
        bookmarkManagerMenu.addAction(openBookmarksAction)
        bookmarkManagerMenu.addAction(clearBookmarkAction)

        historyMenu = menubar.addMenu('&History')
        historyMenu.addAction(historyAction)
        historyMenu.addAction(clearHistoryAction)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)

    # Defining things
    def reload(self):
        if is_connected:
            self.tabs.currentWidget().reload()
        else:
            url=self.tabs.currentWidget().url()
            self.urlbar.setText("webx:snake")
            self.navigatetourl(nodetectinternet=True)

    def fetchBookmarks(self):
        self.bookmark_c.execute("SELECT DISTINCT link FROM bookmark ORDER BY date DESC")
        bookmarks = []
        for bookmark in self.bookmark_c.fetchall():
            page = bookmark[0]
            bookmarks.append(page)
        return bookmarks

    def detectsearch(self):
        urlorquery = self.urlbar.text()
        if not urlorquery.startswith("? "):
            self.navigatetourl()
        else:
            self.doasearch()

    def openhtmlfile(self):
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

    def openpdffile(self):
        if platform.system() == "Linux" or platform.system() == "Darwin":
            filepath = QFileDialog.getOpenFileName(
                None, "Open File", "/", "PDF Files (*.pdf)")
        else:
            filepath = QFileDialog.getOpenFileName(
                None, "Open File", "C:\\", "PDF Files (*.pdf)")
        filepath2str = str(filepath)
        filepath2str = filepath2str[2:-23]
        if not filepath2str == "":
            self.newtab(qurl=QUrl(f"file:{filepath2str}"))

    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def doasearch(self):
        keyword = self.urlbar.text()[2:]
        if QUrl(keyword).scheme() == "":
            url = QUrl("https://duckduckgo.com/?q=" + keyword)
        elif QUrl(keyword).scheme() == "g":
            url = QUrl("https://google.com/search?q=" + keyword[2:])
        elif QUrl(keyword).scheme() == "google":
            url = QUrl("https://google.com/search?q=" + keyword[7:])
        elif QUrl(keyword).scheme() == "b":
            url = QUrl("https://bing.com/search?q=" + keyword[2:])
        elif QUrl(keyword).scheme() == "bing":
            url = QUrl("https://bing.com/search?q=" + keyword[5:])
        elif QUrl(keyword).scheme() == "y":
            url = QUrl("https://search.yahoo.com/search?p=" + keyword[2:])
        elif QUrl(keyword).scheme() == "yahoo":
            url = QUrl("https://search.yahoo.com/search?p=" + keyword[6:])
        elif QUrl(keyword).scheme() == "ddg":
            url = QUrl("https://duckduckgo.com/?q=" + keyword[4:])
        elif QUrl(keyword).scheme() == "duckduckgo":
            url = QUrl("https://duckduckgo.com/?q=" + keyword[11:])
        elif QUrl(keyword).scheme() == "sp":
            url = QUrl("https://www.startpage.com/sp/search?query=" +
                       keyword[3:] + "&cat=web&pl=opensearch&language=english")
        elif QUrl(keyword).scheme() == "startpage":
            url = QUrl("https://www.startpage.com/sp/search?query=" +
                       keyword[10:] + "&cat=web&pl=opensearch&language=english")
        elif QUrl(keyword).scheme() == "aiu":
            url = QUrl("https://jiu-soft.com/aiu/nonav.html?q=" + keyword[4:])
        elif QUrl(keyword).scheme() == "yt":
            url = QUrl(
                "https://www.youtube.com/results?search_query=" + keyword[3:])
        elif QUrl(keyword).scheme() == "youtube":
            url = QUrl(
                "https://www.youtube.com/results?search_query=" + keyword[8:])
        self.tabs.currentWidget().setUrl(url)
        browser.setFocus()

    def exit(self):
        self.close()
        self.history_conn.close()
        self.bookmark_conn.close()

    def newwin(self):
        MainWindow()

    def about(self):
        aboutwebx = QMessageBox()
        aboutwebx.setWindowTitle("About")
        aboutwebx.setText(f"""WebX Version {version}

© The Jiusoft Team. All rights reserved.""")
        aboutwebx.setIcon(QMessageBox.Icon.Information)
        aboutwebx.setWindowIcon(QIcon('img/WebX.png'))
        x = aboutwebx.exec()

    def newtab(self, *args, qurl=None, label="about:blank"):
        if qurl is None:
            qurl = QUrl.fromLocalFile(f"{os.path.dirname(os.path.realpath(__file__))}/home/home.html")
        global browser
        browser = QWebEngineView()
        browser.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        page = WebEnginePage(browser)
        browser.setPage(page)
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.updateurl(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))
        browser.loadFinished.connect(self.updatetitle)
        browser.page().profile().downloadRequested.connect(download_file)
        browser.page().fullScreenRequested.connect(
            lambda request, browser=browser: self.handle_fullscreen_requested(
                request, browser
            )
        )

        # Keyboard Shortcuts
        browser.page().profile().setHttpUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)

    def handle_fullscreen_requested(self, request, browser):
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
        self.updatetitle()

    def closetab(self, i):
        if self.tabs.count() < 2:
            self.tabs.currentWidget().setUrl(
                QUrl.fromLocalFile(f"{os.path.dirname(os.path.realpath(__file__))}/home/home.html"))
        else:
            self.tabs.removeTab(i)

    def navigatetourl(self, nodetectinternet=False):
        url = QUrl(self.urlbar.text())
        if self.urlbar.text() == "chrome:dino" or self.urlbar.text() == "chrome://dino":
            self.urlbar.setText("webx://snake")
        if self.urlbar.text() == "webx:history" or self.urlbar.text() == "webx://history":
            url = QUrl.fromLocalFile(f"{os.path.dirname(os.path.realpath(__file__))}/history/history.html")
        if self.urlbar.text() == "webx:home" or self.urlbar.text() == "webx://home" or self.urlbar.text() == "":
            url = QUrl.fromLocalFile(f"{os.path.dirname(os.path.realpath(__file__))}/home/home.html")
        if self.urlbar.text() == "webx:bookmarks" or self.urlbar.text() == "webx://bookmarks":
            url = QUrl.fromLocalFile(f"{os.path.dirname(os.path.realpath(__file__))}/bookmarks/bookmarks.html")
        if self.urlbar.text() == "webx:links" or self.urlbar.text() == "webx://links":
            url = QUrl.fromLocalFile(f"{os.path.dirname(os.path.realpath(__file__))}/links/links.html")
        if self.urlbar.text() == "webx:snake" or self.urlbar.text() == "webx://snake":
            url = QUrl.fromLocalFile(f"{os.path.dirname(os.path.realpath(__file__))}/snake_game/snake.html")
        if url.scheme() == "":
            url.setScheme("https")
        if url.scheme() == "http":
            url.setScheme("https")
        if nodetectinternet:
            self.tabs.currentWidget().setUrl(url)
        else:
            if is_connected():
                self.tabs.currentWidget().setUrl(url)
            else:
                self.urlbar.setText("webx:snake")
                self.navigatetourl(nodetectinternet=True)
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

        if url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/history/history.html").toString():
            try:
                self.urlbar.setText("webx://history")
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', 'webx://history')")
                self.history_conn.commit()
            except:
                print(
                    "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")
        elif url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/snake_game/snake.html").toString():
            try:
                self.urlbar.setText("webx://snake")
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', 'webx://snake')")
                self.history_conn.commit()
            except:
                print(
                    "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")
        elif url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/home/home.html").toString() or self.url.toString() == QUrl.fromLocalFile(
            f"{os.path.dirname(os.path.realpath(__file__))}/home/home.html").toString() + "?":
            try:
                self.urlbar.setText("")
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', 'webx://home')")
                self.history_conn.commit()
            except:
                print(
                    "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")
        elif url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/links/links.html").toString():
            try:
                self.urlbar.setText("webx://links")
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', 'webx://links')")
                self.history_conn.commit()
            except:
                print(
                    "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")
        elif url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/bookmarks/bookmarks.html").toString():
            try:
                self.urlbar.setText("webx://bookmarks")
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', 'webx://bookmarks')")
                self.history_conn.commit()
            except:
                print(
                    "Cannot access file \"search_history.db\" or \"bookmarks.db\"; most likely because of a wrong directory error.")
        else:
            if str(url.toString()) != "":
                self.history_c.execute(
                    f"INSERT INTO history VALUES ('{year}-{month}-{day}', '{hour}:{minute}:{second}', '{str(url.toString())}')")
                self.history_conn.commit()

        compile_sqlte3_to_html_history()

        if browser != self.tabs.currentWidget():
            return

    def updatetitle(self):
        self.setWindowTitle("%s – WebX" % self.tabs.tabText(self.tabs.currentIndex()))

    def checkHistory(self):
        current = os.path.dirname(os.path.realpath(__file__))
        file_path = current + "/history/history.html"
        qurl = QUrl.fromLocalFile(file_path)
        global browser
        browser = QWebEngineView()
        browser.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
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
        self.urlbar.setText("webx://history")
        browser.page().profile().setHttpUserAgent(f'WebX/{version}')
        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)

    def removeHistory(self):
        self.history_conn.commit()
        self.history_conn.close()

        os.remove(f"{os.path.dirname(os.path.realpath(__file__))}/history/search_history.db")

        try:
            self.history_conn = sqlite3.connect("history/search_history.db")
            self.history_c = self.history_conn.cursor()

            self.history_c.execute(
                "CREATE TABLE IF NOT EXISTS history(date date, time time, link text)")
        except:
            print(
                "Cannot access file \"search_history.db\"; most likely because of a wrong directory error.")

        compile_sqlte3_to_html_history()
        if self.urlbar.text() == "webx:history" or self.urlbar.text() == "webx://history":
            self.tabs.currentWidget().reload()

    def bookmark(self):
        now = datetime.now()

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")

        if self.url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/bookmarks/bookmarks.html").toString():
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', 'webx://bookmarks')")
        elif self.url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/history/history.html").toString():
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', 'webx://history')")
        elif self.url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/snake_game/snake.html").toString():
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', 'webx://snake')")
        elif self.url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/home/home.html").toString() or self.url.toString() == QUrl.fromLocalFile(
            f"{os.path.dirname(os.path.realpath(__file__))}/home/home.html").toString() + "?":
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', 'webx://home')")
        elif self.url.toString() == QUrl.fromLocalFile(
                f"{os.path.dirname(os.path.realpath(__file__))}/links/links.html").toString():
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', 'webx://links')")
        else:
            self.bookmark_c.execute(
                f"INSERT INTO bookmark VALUES ('{year}-{month}-{day} {hour}:{minute}:{second}', '{self.url.toString()}')")
        self.bookmark_conn.commit()

        compile_sqlte3_to_html_bookmark()

    def openBookmarks(self):
        compile_sqlte3_to_html_bookmark()

        current = os.path.dirname(os.path.realpath(__file__))
        file_path = current + "/bookmarks/bookmarks.html"
        qurl = QUrl.fromLocalFile(file_path)
        global browser
        browser = QWebEngineView()
        browser.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
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
        self.urlbar.setText("webx://bookmarks")
        browser.page().profile().setHttpUserAgent(f'WebX/{version}')
        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)

    def removeBookmarks(self):
        global listWidget
        listWidget = ListWidget()
        listWidget.resize(300, 120)
        bms = self.fetchBookmarks()
        for bm in bms:
            listWidget.addItem(bm)
        listWidget.setWindowTitle("Remove Bookmark")
        listWidget.itemDoubleClicked.connect(listWidget.doubleClicked)
        listWidget.show()


# Executing The Browser
if "-v" in args or "-V" in args or "--version" in args:
    print(version)
elif "-h" in args or "--help" in args:
    print(f"""Version: {version}
Arguments Available:
    1. -h or --help
    2. -v, -V, or --version
GitHub Page:
    https://github.com/jiusoft/webx/
Official Website:
    https://webx.jiu-soft.com/
Copyright:
    Jiusoft""")
elif len(args) == 0:
    print("Thank you for using the WebX!")
    if linux:
        os.environ["QT_QPA_PLATFORM"] = "xcb"
    os.environ[
        "QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3 --ignore-certificate-errors --ignore-ssl-errors"
    app = QApplication(sys.argv)
    app.setApplicationName("WebX")
    window = MainWindow()
    app.exec()
else:
    print("Thank you for using the WebX!")
    if linux:
        os.environ["QT_QPA_PLATFORM"] = "xcb"
    os.environ[
        "QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3 --ignore-certificate-errors --ignore-ssl-errors"
    app = QApplication(sys.argv)
    app.setApplicationName('WebX')
    tmp = QUrl(args[0])
    if tmp.scheme() == "":
        tmp.setScheme("https")
    elif tmp.scheme() == "http":
        tmp.setScheme("https")
    window = MainWindow(qurl=tmp)
    app.exec()
