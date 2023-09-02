from aqt import gui_hooks
from aqt.utils import tooltip
#from anki import hooks
import aqt
import threading
import time
import os.path
import codecs
from aqt.qt import QTimer
from threading import Timer
from anki.cards import Card
#aqt.mw.toolbar.create_link("testcmd","test",lambda:tooltip("test"),"testtip","testcmd")
toolbarHeight = aqt.mw.toolbar.web.height()
bottomHeight = aqt.mw.bottomWeb.height()

config = aqt.mw.addonManager.getConfig(__name__)

jsdata = ""
with codecs.open(os.path.join( os.path.dirname( __file__),'common.js') , 'r' ,'utf-8') as file:
    jsdata = file.read().replace("</script>","")



#config.setdefault("width",0.3)
autoMode = bool(config.get("auto"))
windowWidth = float(config.get("width"))
lock_simple_mode = False
orgshow = aqt.mw.bottomWeb.show
aqt.mw.bottomWeb.show = lambda *args:orgshow(*args) if not lock_simple_mode else None
#tooltip(windowWidth)

def scrw():
    return aqt.QGuiApplication.primaryScreen().size().width()
def scrh():
    return aqt.QGuiApplication.primaryScreen().size().height()
def winw():
    return windowWidth*scrw()

def simple_mode_enable(enable=True):
    global lock_simple_mode
    lock_simple_mode = enable
    if not enable:
        aqt.mw.show_menubar()
        aqt.mw.form.menubar.show()
        aqt.mw.toolbar.web.setFixedHeight(toolbarHeight)
        
        #aqt.mw.mainLayout.addWidget(aqt.mw.bottomWeb)
        aqt.mw.bottomWeb.show()
        #aqt.mw.bottomWeb.setMinimumHeight(0)
        
        aqt.mw.setWindowFlag(aqt.Qt.WindowType.FramelessWindowHint | aqt.Qt.WindowType.WindowStaysOnTopHint,False)
        aqt.mw.setWindowOpacity(1)
        aqt.mw.setMinimumHeight(0)
        aqt.mw.setMinimumWidth(0)
        aqt.mw.setMaximumHeight(scrh())
        aqt.mw.setMaximumWidth(scrw())
        aqt.mw.show()

        
        #tooltip("关闭极简模式")
        return
    #tooltip("启动极简模式")
    aqt.mw.hide_menubar()
    aqt.mw.form.menubar.hide()
    aqt.mw.toolbar.web.setFixedHeight(0)

    
    #aqt.mw.bottomWeb.setMaximumHeight(0)

    aqt.mw.setWindowFlag(aqt.Qt.WindowType.FramelessWindowHint | aqt.Qt.WindowType.WindowStaysOnTopHint)
    aqt.mw.setWindowOpacity(0.65)
    aqt.mw.show()

    aqt.mw.setFixedWidth(winw())
    aqt.mw.setFixedHeight(scrh())
    aqt.mw.move(scrw()-winw(),0)
    
    
    def delayMover():
        #延迟一会儿是为了防止titlebar还没被关闭
        #time.sleep(0.6)
        aqt.mw.move(scrw()-winw(),0)
        aqt.mw.bottomWeb.hide()
        #aqt.mw.mainLayout.removeWidget(aqt.mw.bottomWeb)    
        #aqt.mw.form.centralwidget.setLayout(aqt.mw.mainLayout)
        #aqt.mw.bottomWeb.setFixedHeight(0)
        
        

    QTimer.singleShot(300,delayMover)
    #threading.Thread(None,delayMover).start()
    

def simple_mode():
    if aqt.mw.toolbar.web.maximumHeight()==0:
        simple_mode_enable(False)
        return
    simple_mode_enable(True)

def toggleop():
    if aqt.mw.windowOpacity()<1.0:
        aqt.mw.setWindowOpacity(1.0)
    else:
        aqt.mw.setWindowOpacity(0.65)

def togglefs():
    if aqt.mw.width() == scrw():
        aqt.mw.move(scrw()-winw(),0)
        aqt.mw.setFixedWidth(winw())
        aqt.mw.setFixedHeight(scrh())
    else:
        aqt.mw.move(0,0)
        aqt.mw.setFixedWidth(scrw())
        aqt.mw.setFixedHeight(scrh())


def on_menu_show(a,menu:aqt.QMenu):
    menu.addAction(
        "开关浮窗模式"
        ,simple_mode
    )
    menu.addAction(
        "开关半透明模式"
        ,toggleop
    )
    menu.addAction(
        "开关全屏幕模式"
        ,togglefs
    )
    menu.addAction(
        "回到主界面",
        lambda:aqt.mw.moveToState("overview")
    )

def on_js_msg(a,message: str, context):
    if(message=="undo"):
        aqt.mw.undo()
    if(message=="init-window" and autoMode and (not (aqt.mw.windowFlags() & aqt.Qt.WindowType.FramelessWindowHint))):
        simple_mode_enable()
        #Timer(0.3,simple_mode_enable).start()
    return a
def on_state_change(state,old_state):
    global lock_simple_mode
    if(state=="overview"):
        simple_mode_enable(False)
    return
    if(state=="review"):
        lock_simple_mode = True
        #simple_mode_enable()
    #if(state=="")
    #tooltip(state)

isUndo = False

def prepare(html, card:Card, context):
    global isUndo 
    prefix = "<script>document.documentElement.classList.remove('common_back');document.documentElement.classList.remove('common_front');</script>" if isUndo else ""
    isUndo = False
    return prefix + ("<script>\n{}\n</script>\n<script>pycmd('init-window');</script>").format(jsdata)+html

def mode_locker(*args):
    return
    if lock_simple_mode and autoMode:
        simple_mode_enable(True)

gui_hooks.card_will_show.append(prepare)
gui_hooks.webview_did_receive_js_message.append(on_js_msg)
gui_hooks.webview_will_show_context_menu.append(on_menu_show)
gui_hooks.state_did_change.append(on_state_change)
gui_hooks.reviewer_did_show_question.append(mode_locker)
def undo_handler(*args):
    global isUndo
    isUndo = True
gui_hooks.review_did_undo.append(undo_handler)
