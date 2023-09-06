from aqt import Qt,mw,QDialogButtonBox, QWidget, QFormLayout, QDoubleSpinBox, QCheckBox
import aqt
import locale
isChinese = locale.getdefaultlocale()[0] == "zh_CN"

def config(key,value=None):
    "使用它来获取变量后记得强制转换"
    addon = aqt.mw.addonManager.getConfig(__name__)
    if value is None:
        return addon.get(key)
    else:
        addon[key] = value
        return aqt.mw.addonManager.writeConfig(__name__,addon)
class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__(mw.window(),Qt.WindowType.Window)
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle('配置界面' if isChinese else 'Configure')

        # 创建表单布局
        formLayout = QFormLayout()

        # 创建组件
        self.widthSpin = QDoubleSpinBox()
        self.widthSpin.setRange(0.1, 1.0)
        self.widthSpin.setValue(config('width')) 
        self.widthSpin.setSingleStep(0.1)

        self.autoCheck = QCheckBox('自动' if isChinese else 'Auto')
        self.autoCheck.setChecked(config('auto'))

        self.marginSpin = QDoubleSpinBox()
        self.marginSpin.setRange(0, 100)
        self.marginSpin.setValue(config('margin'))
        self.marginSpin.setSingleStep(5)

        self.opacitySpin = QDoubleSpinBox()
        self.opacitySpin.setRange(0.1, 1.0)
        self.opacitySpin.setValue(config('opacity'))
        self.opacitySpin.setSingleStep(0.1)

        self.framelessCheck = QCheckBox('无边框' if isChinese else 'Frameless') 
        self.framelessCheck.setChecked(config('frameless'))
        
        self.toolbarlessCheck = QCheckBox('无工具栏' if isChinese else 'No Toolbar')
        self.toolbarlessCheck.setChecked(config('toolbarless'))

        self.ignoreTaskbar = QCheckBox('忽视任务栏高度' if isChinese else 'Ignore taskbar height')
        self.ignoreTaskbar.setChecked(config('ignoreTaskbar'))

        # 添加组件到表单布局
        formLayout.addRow('宽度' if isChinese else 'Width', self.widthSpin)
        formLayout.addRow('自动' if isChinese else 'Auto', self.autoCheck)  
        formLayout.addRow('边距' if isChinese else 'Margin', self.marginSpin)
        formLayout.addRow('透明度' if isChinese else 'Opacity', self.opacitySpin)
        formLayout.addRow(self.framelessCheck,self.toolbarlessCheck)
        formLayout.addRow(self.ignoreTaskbar)
        
        # 添加确认和取消按钮
        buttonBox = QDialogButtonBox(Qt.Orientation.Horizontal)
        buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)

        # 设置表单布局
        formLayout.addRow(buttonBox)
        buttonBox.accepted.connect(self.onConfirm) 
        buttonBox.rejected.connect(self.close)

        # 设置表单布局
        self.setLayout(formLayout)
    def onConfirm(self):
        config('width', self.widthSpin.value())
        config('auto', self.autoCheck.isChecked())
        config('margin', self.marginSpin.value())
        config('opacity', self.opacitySpin.value())
        config('frameless', self.framelessCheck.isChecked())
        config('toolbarless', self.toolbarlessCheck.isChecked())
        config('ignoreTaskbar', self.ignoreTaskbar.isChecked())
        self.close()
