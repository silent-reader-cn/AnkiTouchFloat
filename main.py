import aqt
from aqt.utils import tooltip
import locale,codecs,os,anki.cards
mainWindow = aqt.mw
app = aqt.QApplication
#////////////////////////////////////////////////
# 自定义命令
def config(key,value=None):
    "使用它来获取变量后记得强制转换"
    addon = aqt.mw.addonManager.getConfig(__name__)
    if value is None:
        return addon.get(key)
    else:
        addon[key] = value
        return aqt.mw.addonManager.writeConfig(__name__,addon)
def alwaysOnTop():
    windows = [mainWindow]
    for dclass, instance in aqt.dialogs._dialogs.values():
        if instance:
            windows.append(instance)
    for window in windows:
        windowFlags = window.windowFlags()
        windowFlags ^= aqt.Qt.WindowType.WindowStaysOnTopHint
        window.setWindowFlags(windowFlags)
        window.show()
def titlebarHeight():
    return mainWindow.window().windowHandle().frameGeometry().height() - mainWindow.geometry().height()
def screenSize():
    scr = app.primaryScreen()
    rect = scr.availableGeometry()
    return rect
def windowSize():
    return mainWindow.geometry()
def normalMode():
    # 调整半透明度
    mainWindow.setWindowOpacity(1)
    # 关闭多余控件
    mainWindow.menuBar().show()
    # 显示在最上方
    mainWindow.setWindowFlags(mainWindow.windowFlags() & ~ (aqt.Qt.WindowType.WindowStaysOnTopHint | (aqt.Qt.WindowType.FramelessWindowHint if config("frameless") else 0)))
    mainWindow.show()
def floatMode(forceMode=None):
    if (not forceMode if forceMode is not None else mainWindow.windowOpacity() < 0.99999):
        return normalMode()
    
    # 关闭多余控件
    mainWindow.menuBar().hide()
    if config("toolbarless"):
        mainWindow.toolbar.web.hide()
    # 调整半透明度
    mainWindow.setWindowOpacity(config("opacity"))
    # 显示在最上方
    mainWindow.setWindowFlags(mainWindow.windowFlags() | aqt.Qt.WindowType.WindowStaysOnTopHint | (aqt.Qt.WindowType.FramelessWindowHint if config("frameless") else 0))
    mainWindow.show()

    # 调整位置大小
    def delayMover():
        ss = screenSize()
        w = ss.width() * float(config("width"))
        h = ss.height() - 2 * float(config("margin")) - titlebarHeight()
        x = ss.width() - w - float(config("margin"))
        y = float(config("margin"))
        
        mainWindow.resize(
            w,h
        )
        mainWindow.move( 
            x,y
        )
    aqt.QTimer.singleShot(300,delayMover)

def undo():
    aqt.mw.undo()

def initWindow():
    if config("auto"):
        floatMode(True)
#///////////////////////////////////////////////
# 按钮配置
isChinese = locale.getdefaultlocale()[0] == "zh_CN"
ExtButtons = {
    "浮窗":"Float"
}
# 命令配置
ExtCommands = {
    "Float":floatMode,
    "undo":mainWindow.undo,
    "study":initWindow
}
#///////////////////////////////////////////////
# 注入工具栏
def InjectToolBar(btns):
    old_func = mainWindow.toolbar._centerLinks 
    def new_func(*args,**argsd):
        old_value = old_func(*args,**argsd)
        for title in btns:
            cmd = btns[title]
            if not isChinese:
                title = cmd
            old_value += '\n<a class="hitem" tabindex="-1" aria-label="'+title+'" id="sync" href="#" onclick="return pycmd(\''+cmd+'\')">'+title+'</a>'
        return old_value
    mainWindow.toolbar._centerLinks = new_func

# 注入命令
def InjectCommand(cmds):
    def on_js_msg(a,message: str, context):
        tooltip(message)
        if message in cmds:
            cmds[message]()
        return a
    aqt.gui_hooks.webview_did_receive_js_message.append(on_js_msg)

# 注入js
def InjectJavascript(jsdata):
    def prepare(html, card:anki.cards.Card, context):
        prefix = "<script>document.documentElement.classList.remove('common_question');document.documentElement.classList.remove('common_answer');</script>\n" + "<script>document.documentElement.classList.add('common_"+str(aqt.mw.reviewer.state)+"');</script>\n"
        return prefix + ("<script>\n{}\n</script>\n<script>pycmd('init-window');</script>").format(jsdata)+html
    aqt.gui_hooks.card_will_show.append(prepare)

# 注入菜单
def InjectMenu():
    def togglefs():
        if mainWindow.width() != screenSize().width():
            mainWindow.resize( screenSize().width(),screenSize().height())
            mainWindow.move(0,0)
        else:
            floatMode(True)
    def toggleop():
        if aqt.mw.windowOpacity()<0.999999:
            aqt.mw.setWindowOpacity(1.0)
        else:
            aqt.mw.setWindowOpacity(config("opacity"))
    def on_menu_show(a,menu:aqt.QMenu):
        menu.addAction(
            "开关浮窗模式" if isChinese else "Toggle float mode"
            ,floatMode
        )
        menu.addAction(
            "开关半透明模式" if isChinese else "Toggle opacity mode"
            ,toggleop
        )
        menu.addAction(
            "开关全屏幕模式" if isChinese else "Toggle fullscreen mode"
            ,togglefs
        )
        def back():
            aqt.mw.moveToState("overview")
            if config("auto"):
                floatMode(False)
        menu.addAction(
            "回到主界面" if isChinese else "Return to overview",
            back,
        )
    aqt.gui_hooks.webview_will_show_context_menu.append(on_menu_show)
#////////////////////////////////////////////////

def init():
    InjectToolBar(ExtButtons)
    InjectCommand(ExtCommands)
    InjectMenu()
    mainWindow.setWindowOpacity(1)
    with codecs.open(os.path.join( os.path.dirname( __file__),'common.js') , 'r' ,'utf-8') as file:
        jsdata = file.read().replace("</script>","")
        InjectJavascript(jsdata) 



