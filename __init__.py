from aqt import gui_hooks
#from aqt.utils import show_info,tooltip
#from anki import hooks
import aqt
import threading
import time
import os.path
#aqt.mw.toolbar.create_link("testcmd","test",lambda:tooltip("test"),"testtip","testcmd")
toolbarHeight = aqt.mw.toolbar.web.height()
bottomHeight = aqt.mw.bottomWeb.height()

windowWidth = 0.25
windowWidth = windowWidth*aqt.QGuiApplication.primaryScreen().size().width()

jsdata = ""
with open(os.path.join( os.path.dirname( __file__),'common.js') , 'r') as file:
    jsdata = file.read().replace("</script>","")

def simple_mode_enable(enable=True):
    if not enable:
        aqt.mw.show_menubar()
        aqt.mw.form.menubar.show()
        aqt.mw.toolbar.web.setFixedHeight(toolbarHeight)
        aqt.mw.setWindowFlag(aqt.Qt.WindowType.FramelessWindowHint | aqt.Qt.WindowType.WindowStaysOnTopHint,False)
        aqt.mw.setWindowOpacity(1)
        aqt.mw.show()
        return
    aqt.mw.hide_menubar()
    aqt.mw.form.menubar.hide()
    aqt.mw.toolbar.web.setFixedHeight(0)
    aqt.mw.setWindowFlag(aqt.Qt.WindowType.FramelessWindowHint | aqt.Qt.WindowType.WindowStaysOnTopHint)
    aqt.mw.setWindowOpacity(0.65)
    aqt.mw.show()

    screenSize = aqt.QGuiApplication.primaryScreen().size()
    aqt.mw.setFixedWidth(windowWidth)
    aqt.mw.setFixedHeight(screenSize.height())

    def delayMover():
        #延迟一会儿是为了防止titlebar还没被关闭
        time.sleep(1)
        aqt.mw.move(screenSize.width()-windowWidth,0)
    threading.Thread(None,delayMover).start()
    
    

def simple_mode():
    if aqt.mw.toolbar.web.maximumHeight()==0:
        simple_mode_enable()
        return
    simple_mode_enable(False)

def on_menu_show(a,menu:aqt.QMenu):
    menu.addAction(
        "开关浮窗模式"
        ,simple_mode,
        
    )
    menu.addAction(
        "回到主界面",
        lambda:aqt.mw.moveToState("overview")
    )

def on_js_msg(a,message: str, context):
    if(message=="undo"):
        aqt.mw.undo()
    ##tooltip(message)
    return a
def on_state_change(state,old_state):
    if(state=="overview"):
        simple_mode_enable(False)
    if(state=="review"):
        simple_mode_enable()
    #if(state=="")
    #tooltip(state)

def prepare(html, card, context):
    return ("<script>\n{}\n</script>").format(jsdata)+html

gui_hooks.card_will_show.append(prepare)
gui_hooks.webview_did_receive_js_message.append(on_js_msg)
gui_hooks.webview_will_show_context_menu.append(on_menu_show)
gui_hooks.state_did_change.append(on_state_change)