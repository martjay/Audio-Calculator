import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QFrame, QGraphicsDropShadowEffect, QSizePolicy,
                           QMessageBox, QToolTip, QSystemTrayIcon, QMenu)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QSize
from PyQt6.QtGui import QDoubleValidator, QColor, QPalette, QLinearGradient, QFont, QCursor, QIcon, QAction
from PyQt6.QtCore import QPropertyAnimation, QRect
import pyperclip
import os

def get_resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和打包后的环境"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller打包后的路径
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class ThemeManager:
    DARK_THEME = {
        'bg_color': '#1A1A1A',  # 更深的背景色
        'text_color': '#E0E0E0',  # 浅色文字
        'border_color': 'rgba(100, 181, 246, 0.3)',  # 半透明边框
        'button_gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2C3E50, stop:1 #34495E)',  # 深蓝渐变
        'button_hover': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34495E, stop:1 #3D566E)',  # 稍亮的深蓝
        'button_pressed': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #243342, stop:1 #2C3E50)',  # 更深的蓝
        'table_header': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2C3E50, stop:1 #34495E)',  # 深蓝渐变
        'table_item_bg': '#2D2D2D',  # 稍亮的深色背景
        'input_bg': 'rgba(45, 45, 45, 0.8)',  # 半透明深色
        'frame_bg': '#242424'  # 深色框架背景
    }
    
    LIGHT_THEME = {
        'bg_color': '#EAE6DD',
        'text_color': '#37474F',
        'border_color': 'rgba(100, 181, 246, 0.5)',
        'button_gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #64B5F6, stop:1 #42A5F5)',
        'button_hover': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #90CAF9, stop:1 #64B5F6)',
        'button_pressed': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #42A5F5, stop:1 #2196F3)',
        'table_header': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #90CAF9, stop:1 #64B5F6)',
        'table_item_bg': '#E8F5E9',
        'input_bg': 'rgba(234, 230, 221, 0.8)',
        'frame_bg': '#EAE6DD'
    }

class LanguageManager:
    TRANSLATIONS = {
        'zh': {
            'window_title': '音频计算器',
            'bpm_label': '歌曲速度 (BPM):',
            'manual_bpm': '手动测速',
            'stay_on_top': '窗口置顶',
            'cancel_on_top': '取消置顶',
            'show_delay': '显示延迟参数',
            'hide_delay': '隐藏延迟参数',
            'audio_app': '音频应用',
            'reverb_params': '混响参数(ms)',
            'delay_params': '延迟参数(ms)',
            'reverb_type': '混响类型',
            'pre_delay': 'Pre-Delay',
            'decay_time': 'Decay Time',
            'total_reverb': 'Total Reverb Time',
            'note_value': '音符值',
            'notes': 'Notes',
            'dotted': 'Dotted',
            'triplets': 'Triplets',
            'bpm_calc': 'BPM计算器',
            'bpm_desc': '通过空格键或点击按钮来计算BPM',
            'tap_button': '点击或按空格键',
            'copied': '已复制到剪贴板！',
            'theme_switch': '切换主题',
            'lang_switch': '切换语言',
            'expand': '展开',
            'collapse': '收起',
            'hide_delay_params': '隐藏延迟参数',
            'show_delay_params': '显示延迟参数',
            'show': '显示',
            'quit': '退出'
        },
        'en': {
            'window_title': 'Audio Calculator',
            'bpm_label': 'Song Tempo (BPM):',
            'manual_bpm': 'Manual BPM',
            'stay_on_top': 'Stay on Top',
            'cancel_on_top': 'Cancel on Top',
            'show_delay': 'Show Delay',
            'hide_delay': 'Hide Delay',
            'audio_app': 'Audiobar',
            'reverb_params': 'Reverb Parameters(ms)',
            'delay_params': 'Delay Parameters(ms)',
            'reverb_type': 'Reverb Type',
            'pre_delay': 'Pre-Delay',
            'decay_time': 'Decay Time',
            'total_reverb': 'Total Reverb Time',
            'note_value': 'Note Value',
            'notes': 'Notes',
            'dotted': 'Dotted',
            'triplets': 'Triplets',
            'bpm_calc': 'BPM Calculator',
            'bpm_desc': 'Use spacebar or click button to calculate BPM',
            'tap_button': 'Tap or Press Space',
            'copied': 'Copied to clipboard!',
            'theme_switch': 'Switch Theme',
            'lang_switch': 'Switch Language',
            'expand': 'Expand',
            'collapse': 'Collapse',
            'hide_delay_params': 'Hide Delay Params',
            'show_delay_params': 'Show Delay Params',
            'show': 'Show',
            'quit': 'Quit'
        }
    }

class StyleSheet:
    @staticmethod
    def get_style(theme):
        return f"""
        QMainWindow {{
            background: {theme['bg_color']};
        }}
        QWidget {{
            color: {theme['text_color']};
            font-family: 'Segoe UI', Arial;
        }}
        QLabel {{
            color: {theme['text_color']};
            font-size: 14px;
            padding: 5px;
        }}
        QPushButton {{
            background: {theme['button_gradient']};
            border: none;
            border-radius: 8px;
            color: white;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background: {theme['button_hover']};
        }}
        QPushButton:pressed {{
            background: {theme['button_pressed']};
        }}
        QLineEdit {{
            background: {theme['input_bg']};
            border: 2px solid {theme['border_color']};
            border-radius: 8px;
            padding: 8px;
            color: {theme['text_color']};
            font-size: 14px;
        }}
        QLineEdit:focus {{
            border: 2px solid #64B5F6;
            background: {theme['frame_bg']};
        }}
        QTableWidget {{
            background: {theme['frame_bg']};
            border: 2px solid {theme['border_color']};
            border-radius: 10px;
            gridline-color: {theme['border_color']};
            selection-background-color: rgba(100, 181, 246, 0.2);
        }}
        QTableWidget::item {{
            padding: 8px;
            border-radius: 4px;
            color: {theme['text_color']};
        }}
        QTableWidget::item:hover {{
            background: rgba(100, 181, 246, 0.1);
        }}
        QTableWidget::item:selected {{
            background: rgba(100, 181, 246, 0.2);
            color: {theme['text_color']};
        }}
        QHeaderView::section {{
            background: {theme['table_header']};
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }}
    """

class IconButton(QPushButton):
    def __init__(self, icon_text, tooltip, parent=None):
        super().__init__(parent)
        self.setText(icon_text)
        self.setToolTip(tooltip)
        self.updateStyle()
        
        # 增强阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
    def updateStyle(self):
        theme = self.parent().current_theme if self.parent() and hasattr(self.parent(), 'current_theme') else ThemeManager.LIGHT_THEME
        if theme == ThemeManager.DARK_THEME:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 89, 152, 0.9),
                        stop:0.4 rgba(44, 62, 80, 0.9),
                        stop:0.6 rgba(44, 62, 80, 0.9),
                        stop:1 rgba(52, 73, 94, 0.9));
                    border: 1px solid rgba(59, 89, 152, 0.3);
                    border-top: 1px solid rgba(59, 89, 152, 0.5);
                    border-bottom: 1px solid rgba(44, 62, 80, 0.5);
                    border-radius: 15px;
                    color: #E0E0E0;
                    padding: 5px;
                    font-size: 14px;
                    font-family: "Segoe UI Symbol";
                    min-width: 30px;
                    max-width: 30px;
                    min-height: 30px;
                    max-height: 30px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(69, 99, 162, 0.95),
                        stop:0.4 rgba(52, 73, 94, 0.95),
                        stop:0.6 rgba(52, 73, 94, 0.95),
                        stop:1 rgba(64, 86, 109, 0.95));
                    border: 1px solid rgba(59, 89, 152, 0.5);
                    border-top: 1px solid rgba(59, 89, 152, 0.7);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(49, 79, 142, 0.9),
                        stop:0.4 rgba(36, 51, 66, 0.9),
                        stop:0.6 rgba(36, 51, 66, 0.9),
                        stop:1 rgba(44, 62, 80, 0.9));
                    border: 1px solid rgba(41, 62, 105, 0.5);
                    padding-top: 6px;
                    padding-bottom: 4px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(25, 118, 210, 0.9),
                        stop:0.4 rgba(21, 101, 192, 0.9),
                        stop:0.6 rgba(21, 101, 192, 0.9),
                        stop:1 rgba(13, 71, 161, 0.9));
                    border: 1px solid rgba(25, 118, 210, 0.5);
                    border-top: 1px solid rgba(33, 150, 243, 0.7);
                    border-bottom: 1px solid rgba(13, 71, 161, 0.7);
                    border-radius: 15px;
                    color: white;
                    padding: 5px;
                    font-size: 14px;
                    font-family: "Segoe UI Symbol";
                    min-width: 30px;
                    max-width: 30px;
                    min-height: 30px;
                    max-height: 30px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(30, 136, 229, 0.95),
                        stop:0.4 rgba(25, 118, 210, 0.95),
                        stop:0.6 rgba(25, 118, 210, 0.95),
                        stop:1 rgba(21, 101, 192, 0.95));
                    border: 1px solid rgba(25, 118, 210, 0.7);
                    border-top: 1px solid rgba(33, 150, 243, 0.9);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(21, 101, 192, 0.9),
                        stop:0.4 rgba(13, 71, 161, 0.9),
                        stop:0.6 rgba(13, 71, 161, 0.9),
                        stop:1 rgba(8, 45, 102, 0.9));
                    border: 1px solid rgba(13, 71, 161, 0.6);
                    padding-top: 6px;
                    padding-bottom: 4px;
                }
            """)

class GlassButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.updateStyle()
        
        # 增强阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
    def updateStyle(self):
        theme = self.parent().current_theme if self.parent() and hasattr(self.parent(), 'current_theme') else ThemeManager.LIGHT_THEME
        if theme == ThemeManager.DARK_THEME:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(59, 89, 152, 0.9),
                        stop:0.3 rgba(44, 62, 80, 0.9),
                        stop:0.7 rgba(44, 62, 80, 0.9),
                        stop:1 rgba(52, 73, 94, 0.9));
                    border: 1px solid rgba(59, 89, 152, 0.3);
                    border-top: 1px solid rgba(59, 89, 152, 0.5);
                    border-bottom: 1px solid rgba(44, 62, 80, 0.5);
                    border-radius: 6px;
                    color: #E0E0E0;
                    padding: 5px 10px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(69, 99, 162, 0.95),
                        stop:0.3 rgba(52, 73, 94, 0.95),
                        stop:0.7 rgba(52, 73, 94, 0.95),
                        stop:1 rgba(64, 86, 109, 0.95));
                    border: 1px solid rgba(59, 89, 152, 0.5);
                    border-top: 1px solid rgba(59, 89, 152, 0.7);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(49, 79, 142, 0.9),
                        stop:0.3 rgba(36, 51, 66, 0.9),
                        stop:0.7 rgba(36, 51, 66, 0.9),
                        stop:1 rgba(44, 62, 80, 0.9));
                    border: 1px solid rgba(41, 62, 105, 0.5);
                    padding-top: 6px;
                    padding-bottom: 4px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(25, 118, 210, 0.9),
                        stop:0.3 rgba(21, 101, 192, 0.9),
                        stop:0.7 rgba(21, 101, 192, 0.9),
                        stop:1 rgba(13, 71, 161, 0.9));
                    border: 1px solid rgba(25, 118, 210, 0.5);
                    border-top: 1px solid rgba(33, 150, 243, 0.7);
                    border-bottom: 1px solid rgba(13, 71, 161, 0.7);
                    border-radius: 6px;
                    color: white;
                    padding: 5px 10px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(30, 136, 229, 0.95),
                        stop:0.3 rgba(25, 118, 210, 0.95),
                        stop:0.7 rgba(25, 118, 210, 0.95),
                        stop:1 rgba(21, 101, 192, 0.95));
                    border: 1px solid rgba(25, 118, 210, 0.7);
                    border-top: 1px solid rgba(33, 150, 243, 0.9);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(21, 101, 192, 0.9),
                        stop:0.3 rgba(13, 71, 161, 0.9),
                        stop:0.7 rgba(13, 71, 161, 0.9),
                        stop:1 rgba(8, 45, 102, 0.9));
                    border: 1px solid rgba(13, 71, 161, 0.6);
                    padding-top: 6px;
                    padding-bottom: 4px;
                }
            """)

class ModernFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ModernFrame")
        self.updateStyle()
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
    def updateStyle(self):
        theme = self.window().current_theme if self.window() and hasattr(self.window(), 'current_theme') else ThemeManager.LIGHT_THEME
        if theme == ThemeManager.DARK_THEME:
            self.setStyleSheet("""
                #ModernFrame {
                    background: #242424;
                    border-radius: 15px;
                    padding: 20px;
                }
            """)
        else:
            self.setStyleSheet("""
                #ModernFrame {
                    background: #EAE6DD;
                    border-radius: 15px;
                    padding: 20px;
                }
            """)

class ExpandableFrame(ModernFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.expanded = False
        self.content = None
        self.animation = None
        self.originalWindowHeight = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.header = QHBoxLayout()
        self.titleLabel = QLabel(title)
        self.titleLabel.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2;")
        self.toggleButton = GlassButton(LanguageManager.TRANSLATIONS[self.window().current_lang if self.window() else 'zh']['expand'])
        self.toggleButton.setMaximumWidth(100)
        self.toggleButton.clicked.connect(self.toggle)
        
        self.header.addWidget(self.titleLabel)
        self.header.addWidget(self.toggleButton)
        layout.addLayout(self.header)
    
    def setContent(self, widget):
        if self.content:
            self.layout().removeWidget(self.content)
            self.content.deleteLater()
        self.content = widget
        self.content.hide()
        self.layout().addWidget(self.content)
    
    def toggle(self):
        mainWindow = self.window()
        if not self.animation:
            self.animation = QPropertyAnimation(self.content, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.animation.finished.connect(self.onAnimationFinished)
        
        if self.expanded:
            # 保存当前窗口高度
            self.originalWindowHeight = mainWindow.height()
            self.animation.setStartValue(self.content.height())
            self.animation.setEndValue(0)
            self.toggleButton.setText(LanguageManager.TRANSLATIONS[self.window().current_lang if self.window() else 'zh']['expand'])
        else:
            # 保存当前窗口高度
            if not self.originalWindowHeight:
                self.originalWindowHeight = mainWindow.height()
            self.content.show()
            contentHeight = self.content.sizeHint().height()
            self.animation.setStartValue(0)
            self.animation.setEndValue(contentHeight)
            self.toggleButton.setText(LanguageManager.TRANSLATIONS[self.window().current_lang if self.window() else 'zh']['collapse'])
            
            # 计算需要的额外空间
            extraHeight = contentHeight - (self.content.maximumHeight() if self.content.maximumHeight() > 0 else 0)
            if extraHeight > 0:
                # 调整窗口高度
                newHeight = mainWindow.height() + extraHeight
                mainWindow.setMinimumHeight(newHeight)
                mainWindow.resize(mainWindow.width(), newHeight)
        
        self.animation.start()
        self.expanded = not self.expanded
    
    def onAnimationFinished(self):
        if not self.expanded:
            self.content.hide()
            # 恢复原始窗口高度
            if self.originalWindowHeight:
                mainWindow = self.window()
                mainWindow.setMinimumHeight(600)  # 恢复原始最小高度
                mainWindow.resize(mainWindow.width(), self.originalWindowHeight)

class CopyableTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cellClicked.connect(self.copyCell)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setShowGrid(True)
        self.setFrameStyle(0)  # 移除边框
        self.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: none;
                gridline-color: rgba(100, 181, 246, 0.2);
            }
            QTableWidget::item {
                border-bottom: none;
                padding: 8px;
            }
            QTableWidget QTableCornerButton::section {
                background: transparent;
                border: none;
            }
        """)
        self.verticalHeader().setMinimumSectionSize(0)
        self.verticalHeader().setDefaultSectionSize(40)
        self.horizontalHeader().setMinimumSectionSize(0)
        
    def copyCell(self, row, column):
        item = self.item(row, column)
        if item and item.text():
            pyperclip.copy(item.text())
            # 获取当前语言并显示相应的提示文本
            window = self.window()
            if isinstance(window, DelayParamsWindow):
                current_lang = window.current_lang
            else:
                current_lang = window.current_lang if window and hasattr(window, 'current_lang') else 'zh'
            tooltip_text = LanguageManager.TRANSLATIONS[current_lang]['copied']
            QToolTip.showText(QCursor.pos(), tooltip_text, self)
            
            # 创建临时高亮效果
            original_bg = item.background()
            item.setBackground(QColor("#B3E5FC"))
            QTimer.singleShot(200, lambda: item.setBackground(original_bg))

class BPMCalculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_lang = self.parent.current_lang if self.parent else 'zh'
        self.current_theme = ThemeManager.LIGHT_THEME
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(LanguageManager.TRANSLATIONS[self.current_lang]['manual_bpm'])
        
        # 设置窗口图标
        icon_path = get_resource_path('icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.taps = []
        self.last_tap_time = 0  # 添加最后一次点击时间记录
        self.sync_timer = None  # 添加同步计时器
        self.initUI()
        
    def initUI(self):
        self.setStyleSheet(StyleSheet.get_style(ThemeManager.LIGHT_THEME))  # 使用亮色主题
        layout = QVBoxLayout()
        
        frame = ModernFrame(self)
        frameLayout = QVBoxLayout(frame)
        
        self.title = QLabel(LanguageManager.TRANSLATIONS[self.current_lang]['bpm_calc'])
        self.updateTitleStyle()
        frameLayout.addWidget(self.title)
        
        self.desc = QLabel(LanguageManager.TRANSLATIONS[self.current_lang]['bpm_desc'])
        self.desc.setStyleSheet(f"color: {self.current_theme['text_color']};")
        frameLayout.addWidget(self.desc)
        
        self.tapButton = GlassButton(LanguageManager.TRANSLATIONS[self.current_lang]['tap_button'])
        self.tapButton.setMinimumHeight(50)
        frameLayout.addWidget(self.tapButton)
        
        self.bpmDisplay = QLabel('0 BPM')
        self.updateBpmDisplayStyle()
        frameLayout.addWidget(self.bpmDisplay)
        
        self.tapButton.clicked.connect(self.recordTap)
        layout.addWidget(frame)
        self.setLayout(layout)
        
    def updateTitleStyle(self):
        """更新标题样式"""
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1565C0;")  # 始终使用亮色主题的颜色

    def updateBpmDisplayStyle(self):
        """更新BPM显示样式"""
        self.bpmDisplay.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1565C0;
            padding: 10px;
        """)

    def updateTheme(self):
        """更新主题"""
        # 不再跟随父窗口主题，始终使用亮色主题
        self.current_theme = ThemeManager.LIGHT_THEME
        self.setStyleSheet(StyleSheet.get_style(self.current_theme))
        
        # 更新所有子组件的主题
        for frame in self.findChildren(ModernFrame):
            frame.updateStyle()
        
        # 更新按钮样式
        self.tapButton.updateStyle()
        
        # 更新标题和BPM显示颜色
        self.updateTitleStyle()
        self.updateBpmDisplayStyle()
        
        # 更新描述文本颜色
        self.desc.setStyleSheet(f"color: {self.current_theme['text_color']};")

    def recordTap(self):
        now = time.time() * 1000
        self.last_tap_time = now  # 记录最后一次点击时间
        self.taps.append(now)
        
        # 保持最近20次点击记录
        if len(self.taps) > 20:
            self.taps.pop(0)
            
        self.calculateBPM()
        
        # 重置同步计时器
        if self.sync_timer:
            self.sync_timer.stop()
        self.sync_timer = QTimer()
        self.sync_timer.setSingleShot(True)
        self.sync_timer.timeout.connect(self.syncBPMToParent)
        self.sync_timer.start(3000)  # 3秒后同步
            
    def calculateBPM(self):
        if len(self.taps) < 2:  # 至少需要2次点击才能开始计算
            self.bpmDisplay.setText('0 BPM')
            return None
            
        # 计算所有相邻点击之间的时间间隔
        intervals = []
        for i in range(1, len(self.taps)):
            intervals.append(self.taps[i] - self.taps[i-1])
        
        # 如果有超过20个间隔，只取最近20个
        if len(intervals) > 20:
            intervals = intervals[-20:]
            
        # 计算平均间隔
        avg_interval = sum(intervals) / len(intervals)
        bpm = round(60000 / avg_interval)  # 保持原有计算公式不变
        
        # 更新显示，添加当前使用的点击次数信息
        self.bpmDisplay.setText(f'{bpm} BPM ({len(intervals)} taps)')
        return bpm

    def syncBPMToParent(self):
        """3秒无操作后同步BPM到主窗口"""
        current_time = time.time() * 1000
        if current_time - self.last_tap_time >= 3000:  # 确保真的已经3秒无操作
            bpm = self.calculateBPM()
            if bpm is not None:  # 修改这里，只要有BPM值就同步
                self.parent.bpmInput.setText(str(bpm))
                self.sync_timer = None  # 清除计时器引用
        else:
            # 如果还没到3秒，重新启动计时器
            if self.sync_timer:
                self.sync_timer.stop()
            self.sync_timer = QTimer()
            self.sync_timer.setSingleShot(True)
            self.sync_timer.timeout.connect(self.syncBPMToParent)
            # 将时间差值转换为整数
            remaining_time = int(3000 - (current_time - self.last_tap_time))
            self.sync_timer.start(max(0, remaining_time))  # 确保时间值不为负

    def resetBPM(self):
        """重置BPM显示和计数器"""
        self.taps = []
        self.last_tap_time = 0
        if self.sync_timer:
            self.sync_timer.stop()
        self.bpmDisplay.setText('0 BPM')
        if self.parent:
            self.parent.bpmInput.setText('')  # 清空主窗口的BPM输入

    def updateTexts(self):
        """更新所有文本"""
        self.current_lang = self.parent.current_lang if self.parent else 'zh'
        texts = LanguageManager.TRANSLATIONS[self.current_lang]
        
        # 更新所有文本元素
        self.title.setText(texts['bpm_calc'])
        self.desc.setText(texts['bpm_desc'])
        self.tapButton.setText(texts['tap_button'])
        self.setWindowTitle(texts['manual_bpm'])  # 添加这行来更新窗口标题
        
    def updateTheme(self):
        """更新主题"""
        self.current_theme = ThemeManager.LIGHT_THEME
        self.setStyleSheet(StyleSheet.get_style(self.current_theme))
        
        # 更新描述文本颜色
        self.desc.setStyleSheet(f"color: {self.current_theme['text_color']};")
        
        # 更新按钮样式
        self.tapButton.updateStyle()
        
        # 更新标题和BPM显示颜色
        self.updateTitleStyle()
        self.updateBpmDisplayStyle()

class DelayParamsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.is_syncing = False
        self.is_animating = False
        self.is_snapped = False  # 添加吸附状态标志
        self.current_theme = self.parent.current_theme if self.parent else ThemeManager.DARK_THEME
        self.current_lang = self.parent.current_lang if self.parent else 'zh'
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(LanguageManager.TRANSLATIONS[self.parent.current_lang]['delay_params'])
        self.setStyleSheet(StyleSheet.get_style(self.current_theme))
        
        # 设置窗口图标
        icon_path = get_resource_path('icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 主窗口部件
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setSpacing(20)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        
        # 延迟参数表格
        delayFrame = ModernFrame(self)  # 添加self作为parent
        delayLayout = QVBoxLayout(delayFrame)
        self.delayTitle = QLabel(LanguageManager.TRANSLATIONS[self.parent.current_lang]['delay_params'])
        self.updateTitleStyle()
        delayLayout.addWidget(self.delayTitle)
        
        self.delayTable = CopyableTableWidget(10, 4)
        self.delayTable.setHorizontalHeaderLabels([
            LanguageManager.TRANSLATIONS[self.parent.current_lang]['note_value'],
            LanguageManager.TRANSLATIONS[self.parent.current_lang]['notes'],
            LanguageManager.TRANSLATIONS[self.parent.current_lang]['dotted'],
            LanguageManager.TRANSLATIONS[self.parent.current_lang]['triplets']
        ])
        self.delayTable.verticalHeader().hide()
        
        for i in range(10):
            self.delayTable.setRowHeight(i, 40)
        
        note_values = ['1/1', '1/2', '1/4', '1/8', '1/16', '1/32', '1/64', '1/128', '1/256', '1/512']
        for i, note in enumerate(note_values):
            item = QTableWidgetItem(note)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(QColor(self.current_theme['table_item_bg']))
            self.delayTable.setItem(i, 0, item)
            
        self.delayTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        delayLayout.addWidget(self.delayTable)
        mainLayout.addWidget(delayFrame)
        
        # 设置窗口位置和大小
        if self.parent:
            self.updateGeometry()
            
    def updateTitleStyle(self):
        """更新标题样式"""
        if self.current_theme == ThemeManager.DARK_THEME:
            self.delayTitle.setStyleSheet("font-size: 18px; font-weight: bold; color: #64B5F6;")
        else:
            self.delayTitle.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2;")
        
    def updateGeometry(self):
        """更新窗口位置和大小以匹配父窗口"""
        if self.parent:
            # 先显示窗口以获取正确的框架尺寸
            if not self.isVisible():
                self.show()
                self.hide()
            
            parentGeometry = self.parent.geometry()
            frameGeometry = self.frameGeometry()
            contentGeometry = self.geometry()
            
            # 计算标题栏高度差异
            titleBarHeight = frameGeometry.height() - contentGeometry.height()
            parentTitleBarHeight = self.parent.frameGeometry().height() - self.parent.geometry().height()
            heightDiff = titleBarHeight - parentTitleBarHeight
            
            # 设置窗口位置和大小
            self.setGeometry(
                parentGeometry.x() + parentGeometry.width(),
                parentGeometry.y() - heightDiff,
                600,
                parentGeometry.height() + heightDiff
            )
    
    def moveEvent(self, event):
        """当延迟参数窗口移动时，处理吸附效果"""
        super().moveEvent(event)
        
        if not (self.parent and self.isVisible() and not self.is_animating):
            return
            
        if self.is_syncing:
            return
            
        try:
            self.is_syncing = True
            
            # 获取当前延迟窗口位置
            delay_pos = self.pos()
            
            # 计算主窗口应该在的位置(延迟窗口左侧)
            parent_target_x = max(0, delay_pos.x() - self.parent.width())
            
            # 移动主窗口到目标位置,保持顶部对齐
            self.parent.move(parent_target_x, delay_pos.y())
            
            # 保持两个窗口高度一致
            if self.height() != self.parent.height():
                self.resize(self.width(), self.parent.height())
                
        finally:
            QTimer.singleShot(50, lambda: setattr(self, 'is_syncing', False))

    def updateTheme(self):
        """更新主题"""
        self.current_theme = self.parent.current_theme
        self.current_lang = self.parent.current_lang  # 更新语言
        self.setStyleSheet(StyleSheet.get_style(self.current_theme))
        # 更新所有子组件的主题
        for frame in self.findChildren(ModernFrame):
            frame.updateStyle()
        # 更新表格项的背景色
        for row in range(self.delayTable.rowCount()):
            item = self.delayTable.item(row, 0)
            if item:
                item.setBackground(QColor(self.current_theme['table_item_bg']))
        self.updateTitleStyle()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.delayWindow = None
        self.stayOnTop = False  # 默认不置顶
        self.slideAnimation = None  # 添加动画属性
        self.current_theme = ThemeManager.DARK_THEME  # 默认使用暗色主题
        self.current_lang = 'zh'  # 默认使用中文
        
        # 创建系统托盘图标
        self.createTrayIcon()
        
        # 创建悬浮窗
        self.floatingWindow = FloatingWindow(self)
        self.floatingWindow.show()
        
        self.initUI()
        
    def createTrayIcon(self):
        # 创建托盘图标
        self.trayIcon = QSystemTrayIcon(self)
        icon_path = get_resource_path('icon.ico')
        if os.path.exists(icon_path):
            self.trayIcon.setIcon(QIcon(icon_path))
        
        # 创建托盘菜单
        self.trayMenu = QMenu()
        
        # 添加显示/隐藏动作
        self.showAction = QAction("显示", self)
        self.showAction.triggered.connect(self.toggleAllWindows)
        self.trayMenu.addAction(self.showAction)
        
        # 添加退出动作
        self.quitAction = QAction("退出", self)
        self.quitAction.triggered.connect(self.realQuit)
        self.trayMenu.addAction(self.quitAction)
        
        # 设置托盘图标的菜单
        self.trayIcon.setContextMenu(self.trayMenu)
        
        # 托盘图标单击事件
        self.trayIcon.activated.connect(self.trayIconActivated)
        
        # 显示托盘图标
        self.trayIcon.show()
        
    def toggleAllWindows(self):
        if self.isVisible():
            # 保存延迟窗口状态
            self.delay_window_was_visible = self.delayWindow and self.delayWindow.isVisible()
            # 隐藏所有窗口
            if self.delayWindow and self.delayWindow.isVisible():
                self.delayWindow.hide()
            if self.bpmCalculator and self.bpmCalculator.isVisible():
                self.bpmCalculator.hide()
            self.hide()
            # 更新托盘菜单文本
            self.showAction.setText("显示" if self.current_lang == 'zh' else "Show")
        else:
            # 显示主窗口
            self.showNormal()
            self.activateWindow()
            # 恢复延迟窗口状态
            if hasattr(self, 'delay_window_was_visible') and self.delay_window_was_visible:
                if self.delayWindow:
                    self.delayWindow.show()
                    self.delayWindow.updateGeometry()
                else:
                    self.toggleDelayWindow()
            # 更新托盘菜单文本
            self.showAction.setText("隐藏" if self.current_lang == 'zh' else "Hide")

    def trayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # 单击
            self.toggleAllWindows()
            
    def closeEvent(self, event):
        # 最小化到系统托盘而不是退出
        if self.trayIcon.isVisible():
            # 保存延迟窗口的状态
            self.delay_window_was_visible = self.delayWindow and self.delayWindow.isVisible()
            # 隐藏所有窗口
            if self.delayWindow and self.delayWindow.isVisible():
                self.delayWindow.hide()
            if self.bpmCalculator and self.bpmCalculator.isVisible():
                self.bpmCalculator.hide()
            self.hide()
            event.ignore()
            
    def realQuit(self):
        # 真正退出程序
        self.trayIcon.hide()
        QApplication.quit()
        
    def showNormal(self):
        # 显示主窗口
        super().showNormal()
        self.activateWindow()
        # 恢复延迟窗口状态
        if hasattr(self, 'delay_window_was_visible') and self.delay_window_was_visible:
            if self.delayWindow:
                self.delayWindow.show()
                self.delayWindow.updateGeometry()
        
    def initUI(self):
        # 设置窗口图标
        icon_path = get_resource_path('icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            # 同时设置为应用程序图标
            QApplication.setWindowIcon(QIcon(icon_path))
            
        self.setWindowTitle(LanguageManager.TRANSLATIONS[self.current_lang]['window_title'])
        self.resize(620, 580)
        
        # 主窗口部件
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setSpacing(20)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        
        # BPM输入区域
        inputFrame = ModernFrame()
        topLayout = QHBoxLayout(inputFrame)
        bpmLabel = QLabel(LanguageManager.TRANSLATIONS[self.current_lang]['bpm_label'])
        self.bpmInput = QLineEdit()
        self.bpmInput.setValidator(QDoubleValidator(1, 999, 2))
        self.bpmInput.textChanged.connect(self.updateAllTables)
        self.bpmInput.setMinimumWidth(100)
        self.manualBpmButton = GlassButton(LanguageManager.TRANSLATIONS[self.current_lang]['manual_bpm'])
        
        topLayout.addWidget(bpmLabel)
        topLayout.addWidget(self.bpmInput)
        topLayout.addWidget(self.manualBpmButton)
        mainLayout.addWidget(inputFrame)
        
        # BPM计算器
        self.bpmCalculator = BPMCalculator(self)
        self.bpmCalculator.hide()
        self.manualBpmButton.clicked.connect(self.toggleBpmCalculator)
        
        # 混响参数表格
        reverbFrame = ModernFrame()
        reverbLayout = QVBoxLayout(reverbFrame)
        self.reverbTitle = QLabel(LanguageManager.TRANSLATIONS[self.current_lang]['reverb_params'])
        self.updateReverbTitleStyle()
        reverbLayout.addWidget(self.reverbTitle)
        
        self.reverbTable = CopyableTableWidget(4, 4)
        self.reverbTable.setHorizontalHeaderLabels([
            LanguageManager.TRANSLATIONS[self.current_lang]['reverb_type'],
            LanguageManager.TRANSLATIONS[self.current_lang]['pre_delay'],
            LanguageManager.TRANSLATIONS[self.current_lang]['decay_time'],
            LanguageManager.TRANSLATIONS[self.current_lang]['total_reverb']
        ])
        self.reverbTable.verticalHeader().hide()
        
        for i in range(4):
            self.reverbTable.setRowHeight(i, 40)
        
        reverb_types = ['Hall', 'Large Room', 'Small Room', 'Tight Ambience']
        for i, reverb_type in enumerate(reverb_types):
            item = QTableWidgetItem(reverb_type)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(QColor(self.current_theme['table_item_bg']))
            self.reverbTable.setItem(i, 0, item)
            
        self.reverbTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        reverbLayout.addWidget(self.reverbTable)
        mainLayout.addWidget(reverbFrame)
        
        # 底部按钮区域
        bottomFrame = ModernFrame()
        bottomLayout = QHBoxLayout(bottomFrame)
        bottomLayout.setContentsMargins(10, 5, 10, 5)
        bottomLayout.setSpacing(10)
        
        # 音频应用链接按钮
        audiobarButton = GlassButton(LanguageManager.TRANSLATIONS[self.current_lang]['audio_app'])
        audiobarButton.setMaximumWidth(120)  # 限制按钮宽度
        audiobarButton.clicked.connect(lambda: self.openUrl('http://audiobar.cn/'))
        bottomLayout.addWidget(audiobarButton)
        
        # 添加图标按钮
        self.themeButton = IconButton('🎨', LanguageManager.TRANSLATIONS[self.current_lang]['theme_switch'])
        self.themeButton.clicked.connect(self.toggleTheme)
        
        self.langButton = IconButton('🌐', LanguageManager.TRANSLATIONS[self.current_lang]['lang_switch'])
        self.langButton.clicked.connect(self.toggleLanguage)
        
        self.stayOnTopButton = IconButton('📌', LanguageManager.TRANSLATIONS[self.current_lang]['stay_on_top'])
        self.stayOnTopButton.clicked.connect(self.toggleStayOnTop)
        
        # 延迟参数按钮
        self.toggleDelayButton = GlassButton(LanguageManager.TRANSLATIONS[self.current_lang]['show_delay'])
        self.toggleDelayButton.setMaximumWidth(120)  # 设置最大宽度为120px
        self.toggleDelayButton.clicked.connect(self.toggleDelayWindow)
        
        bottomLayout.addWidget(self.themeButton)
        bottomLayout.addWidget(self.langButton)
        bottomLayout.addWidget(self.stayOnTopButton)
        bottomLayout.addWidget(self.toggleDelayButton)
        
        mainLayout.addWidget(bottomFrame)
        
        # 应用主题
        self.setStyleSheet(StyleSheet.get_style(self.current_theme))
        for button in self.findChildren(GlassButton):
            button.updateStyle()
        for button in self.findChildren(IconButton):
            button.updateStyle()
        for frame in self.findChildren(ModernFrame):
            frame.updateStyle()
            
    def updateReverbTitleStyle(self):
        """更新混响标题样式"""
        if self.current_theme == ThemeManager.DARK_THEME:
            self.reverbTitle.setStyleSheet("font-size: 18px; font-weight: bold; color: #64B5F6;")
        else:
            self.reverbTitle.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2;")
        
    def toggleTheme(self):
        """切换主题"""
        self.current_theme = ThemeManager.LIGHT_THEME if self.current_theme == ThemeManager.DARK_THEME else ThemeManager.DARK_THEME
        self.setStyleSheet(StyleSheet.get_style(self.current_theme))
        
        # 更新所有 GlassButton
        for button in self.findChildren(GlassButton):
            button.updateStyle()
            
        # 更新所有 ModernFrame
        for frame in self.findChildren(ModernFrame):
            frame.updateStyle()
        
        # 更新延迟参数窗口的主题
        if self.delayWindow:
            self.delayWindow.updateTheme()
            
        # 更新表格项的背景色
        for i in range(4):
            item = self.reverbTable.item(i, 0)
            if item:
                item.setBackground(QColor(self.current_theme['table_item_bg']))
                
        # 更新BPM计算器的主题
        if self.bpmCalculator:
            self.bpmCalculator.updateTheme()
                
    def toggleLanguage(self):
        """切换语言"""
        self.current_lang = 'en' if self.current_lang == 'zh' else 'zh'
        self.updateTexts()
        
        # 更新BPM计算器的语言
        if hasattr(self, 'bpmCalculator'):
            self.bpmCalculator.updateTexts()
            self.bpmCalculator.updateTheme()  # 同时更新主题以确保颜色正确
        
    def updateTexts(self):
        """更新所有文本"""
        texts = LanguageManager.TRANSLATIONS[self.current_lang]
        self.setWindowTitle(texts['window_title'])
        self.themeButton.setToolTip(texts['theme_switch'])
        self.langButton.setToolTip(texts['lang_switch'])
        self.stayOnTopButton.setToolTip(texts['stay_on_top'] if not self.stayOnTop else texts['cancel_on_top'])
        self.manualBpmButton.setText(texts['manual_bpm'])
        self.toggleDelayButton.setText(texts['show_delay'] if not self.delayWindow or self.delayWindow.isHidden() else texts['hide_delay'])
        
        # 更新托盘菜单文本
        self.showAction.setText("显示" if self.current_lang == 'zh' else "Show")
        self.quitAction.setText("退出" if self.current_lang == 'zh' else "Quit")
        
        # 更新标签和表头
        for widget in self.findChildren(QLabel):
            if widget.text() == LanguageManager.TRANSLATIONS['en']['bpm_label'] or widget.text() == LanguageManager.TRANSLATIONS['zh']['bpm_label']:
                widget.setText(texts['bpm_label'])
            elif widget.text() == LanguageManager.TRANSLATIONS['en']['reverb_params'] or widget.text() == LanguageManager.TRANSLATIONS['zh']['reverb_params']:
                widget.setText(texts['reverb_params'])
            
            # 更新音频应用按钮文本
            for button in self.findChildren(GlassButton):
                if button.text() == LanguageManager.TRANSLATIONS['en']['audio_app'] or button.text() == LanguageManager.TRANSLATIONS['zh']['audio_app']:
                    button.setText(texts['audio_app'])
                
        self.reverbTable.setHorizontalHeaderLabels([
            texts['reverb_type'],
            texts['pre_delay'],
            texts['decay_time'],
            texts['total_reverb']
        ])
        
        # 更新延迟参数窗口
        if self.delayWindow:
            self.delayWindow.setWindowTitle(texts['delay_params'])
            self.delayWindow.delayTitle.setText(texts['delay_params'])
            self.delayWindow.delayTable.setHorizontalHeaderLabels([
                texts['note_value'],
                texts['notes'],
                texts['dotted'],
                texts['triplets']
            ])
    
    def toggleStayOnTop(self):
        self.stayOnTop = not self.stayOnTop
        flags = self.windowFlags()
        if self.stayOnTop:
            flags |= Qt.WindowType.WindowStaysOnTopHint
            self.stayOnTopButton.setToolTip(LanguageManager.TRANSLATIONS[self.current_lang]['cancel_on_top'])
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
            self.stayOnTopButton.setToolTip(LanguageManager.TRANSLATIONS[self.current_lang]['stay_on_top'])
        
        # 记录延迟参数窗口的可见状态
        delay_window_visible = self.delayWindow and self.delayWindow.isVisible()
        
        # 更新主窗口状态
        self.setWindowFlags(flags)
        self.show()
        
        # 更新延迟参数窗口状态
        if self.delayWindow:
            delay_flags = self.delayWindow.windowFlags()
            if self.stayOnTop:
                delay_flags |= Qt.WindowType.WindowStaysOnTopHint
            else:
                delay_flags &= ~Qt.WindowType.WindowStaysOnTopHint
            self.delayWindow.setWindowFlags(delay_flags)
            # 如果之前是可见的，就保持可见
            if delay_window_visible:
                self.delayWindow.show()
                self.delayWindow.updateGeometry()
    
    def toggleDelayWindow(self):
        if not self.delayWindow:
            self.delayWindow = DelayParamsWindow(self)
            flags = Qt.WindowType.Tool
            if self.stayOnTop:
                flags |= Qt.WindowType.WindowStaysOnTopHint
            self.delayWindow.setWindowFlags(flags)
            
            # 确保延迟窗口应用正确的主题
            self.delayWindow.updateTheme()
            
            # 设置动画
            self.slideAnimation = QPropertyAnimation(self.delayWindow, b"geometry")
            self.slideAnimation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.slideAnimation.setDuration(300)
        
        try:
            self.slideAnimation.finished.disconnect()
        except:
            pass
            
        if self.delayWindow.isHidden():
            # 先显示窗口以获取正确的框架尺寸
            self.delayWindow.show()
            self.delayWindow.hide()
            
            # 获取屏幕尺寸
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            
            # 获取主窗口的全局位置
            parent_pos = self.mapToGlobal(QPoint(0, 0))
            
            # 设置动画起始和结束位置
            target_rect = QRect(
                parent_pos.x() + self.width(),  # 主窗口右边缘
                parent_pos.y(),                 # 主窗口顶部
                600,
                self.height()                   # 主窗口高度
            )
            
            # 检查是否超出屏幕边界
            if target_rect.right() > screen_geometry.right():
                # 如果超出右边界，将主窗口向左移动
                new_x = screen_geometry.right() - (target_rect.width() + self.width())
                new_pos = self.mapFromGlobal(QPoint(new_x, parent_pos.y()))
                self.move(max(0, new_pos.x()), new_pos.y())
                parent_pos = self.mapToGlobal(QPoint(0, 0))
                target_rect.moveLeft(parent_pos.x() + self.width())
            
            start_rect = QRect(
                target_rect.x() + 600,
                target_rect.y(),
                target_rect.width(),
                target_rect.height()
            )
            
            # 显示窗口并开始动画
            self.delayWindow.setGeometry(start_rect)
            self.delayWindow.show()
            self.calculateDelay()
            self.slideAnimation.setStartValue(start_rect)
            self.slideAnimation.setEndValue(target_rect)
            
            def onShowFinished():
                self.toggleDelayButton.setText(LanguageManager.TRANSLATIONS[self.current_lang]['hide_delay_params'])
                self.delayWindow.is_animating = False
                # 确保动画结束后主题正确应用
                self.delayWindow.updateTheme()
                
            self.slideAnimation.finished.connect(onShowFinished)
            self.delayWindow.is_animating = True
            self.slideAnimation.start()
        else:
            # 设置隐藏动画
            current_rect = self.delayWindow.geometry()
            end_rect = QRect(
                current_rect.x() + 600,  # 向右滑动
                current_rect.y(),        # 保持相同的y坐标
                current_rect.width(),
                current_rect.height()
            )
            
            self.slideAnimation.setStartValue(current_rect)
            self.slideAnimation.setEndValue(end_rect)
            
            def onHideFinished():
                self.delayWindow.hide()
                self.toggleDelayButton.setText(LanguageManager.TRANSLATIONS[self.current_lang]['show_delay_params'])
                self.delayWindow.is_animating = False
                
            self.slideAnimation.finished.connect(onHideFinished)
            self.delayWindow.is_animating = True
            self.slideAnimation.start()
    
    def toggleBpmCalculator(self):
        if self.bpmCalculator.isHidden():
            self.bpmCalculator.show()
            self.bpmCalculator.resetBPM()  # 显示时重置BPM
        else:
            self.bpmCalculator.hide()
            self.bpmCalculator.resetBPM()  # 隐藏时也重置BPM
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space and not self.bpmCalculator.isHidden():
            self.bpmCalculator.recordTap()
            event.accept()
        else:
            super().keyPressEvent(event)
            
    def updateAllTables(self):
        self.calculateReverbParams()
        if self.delayWindow and not self.delayWindow.isHidden():
            self.calculateDelay()
    
    def calculateReverbParams(self):
        try:
            bpm = float(self.bpmInput.text() or 0)
        except ValueError:
            return
            
        if bpm <= 0:
            return
            
        # Hall
        hall_total = 60000 / bpm * 8
        hall_predelay = hall_total / 64
        hall_decay = hall_total - hall_predelay
        
        # Large Room
        largeroom_total = 60000 / bpm * 4
        largeroom_predelay = largeroom_total / 64
        largeroom_decay = largeroom_total - largeroom_predelay
        
        # Small Room
        smallroom_total = 60000 / bpm * 2
        smallroom_predelay = smallroom_total / 64
        smallroom_decay = smallroom_total - smallroom_predelay
        
        # Tight Ambience
        tightambience_total = 60000 / bpm
        tightambience_predelay = tightambience_total / 128
        tightambience_decay = tightambience_total - tightambience_predelay
        
        # 更新表格
        values = [
            [hall_predelay, hall_decay, hall_total],
            [largeroom_predelay, largeroom_decay, largeroom_total],
            [smallroom_predelay, smallroom_decay, smallroom_total],
            [tightambience_predelay, tightambience_decay, tightambience_total]
        ]
        
        for row, row_values in enumerate(values):
            for col, value in enumerate(row_values):
                item = QTableWidgetItem(f'{value:.2f}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.reverbTable.setItem(row, col + 1, item)
                
    def calculateDelay(self):
        try:
            bpm = float(self.bpmInput.text() or 0)
        except ValueError:
            return
            
        if bpm <= 0:
            return
            
        note_values = {
            "1/1": 1, "1/2": 0.5, "1/4": 0.25, "1/8": 0.125, "1/16": 0.0625,
            "1/32": 0.03125, "1/64": 0.015625, "1/128": 0.0078125,
            "1/256": 0.00390625, "1/512": 0.001953125
        }
        
        for row, (note, value) in enumerate(note_values.items()):
            notes_delay = (60 / bpm) * 1000 * 4 * value
            dotted_delay = notes_delay * 1.5
            triplets_delay = notes_delay / 3 * 2
            
            for col, val in enumerate([notes_delay, dotted_delay, triplets_delay]):
                item = QTableWidgetItem(f'{val:.2f}')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.delayWindow.delayTable.setItem(row, col + 1, item)
            
    def openUrl(self, url):
        import webbrowser
        webbrowser.open(url)

    def moveEvent(self, event):
        """当主窗口移动时，更新延迟参数窗口位置"""
        super().moveEvent(event)
        if self.delayWindow and self.delayWindow.isVisible():
            if not self.delayWindow.is_syncing:
                try:
                    self.delayWindow.is_syncing = True
                    
                    # 获取主窗口位置
                    parent_pos = self.pos()
                    
                    # 移动延迟窗口到主窗口右侧,保持顶部对齐
                    self.delayWindow.move(parent_pos.x() + self.width(), parent_pos.y())
                    
                    # 保持两个窗口高度一致
                    if self.delayWindow.height() != self.height():
                        self.delayWindow.resize(self.delayWindow.width(), self.height())
                        
                finally:
                    QTimer.singleShot(50, lambda: setattr(self.delayWindow, 'is_syncing', False))

    def resizeEvent(self, event):
        """当主窗口大小改变时，更新延迟参数窗口"""
        super().resizeEvent(event)
        if self.delayWindow and self.delayWindow.isVisible():
            self.delayWindow.updateGeometry()

class FloatingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(None)  # 不设置父窗口
        self.main_window = parent  # 保存主窗口引用
        self.dragging = False
        self.offset = None
        self.windows_hidden = False
        self.drag_threshold = QApplication.startDragDistance()
        self.drag_started = False
        self.press_pos = None
        
        # 设置窗口标志
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(100, 40)
        
        # 创建右键菜单
        self.context_menu = QMenu(self)
        self.show_action = QAction(LanguageManager.TRANSLATIONS[self.main_window.current_lang]['show'], self)
        self.quit_action = QAction(LanguageManager.TRANSLATIONS[self.main_window.current_lang]['quit'], self)
        self.context_menu.addAction(self.show_action)
        self.context_menu.addAction(self.quit_action)
        
        # 连接菜单动作信号
        self.show_action.triggered.connect(self.toggleMainWindow)
        self.quit_action.triggered.connect(self.main_window.realQuit)
        
        self.initUI()
        self.moveToDefaultPosition()

    def toggleMainWindow(self):
        if not self.main_window:
            return
            
        if not self.windows_hidden:
            # 保存延迟窗口状态
            if hasattr(self.main_window, 'delayWindow'):
                self.main_window.delay_window_was_visible = self.main_window.delayWindow and self.main_window.delayWindow.isVisible()
            # 隐藏所有窗口
            for window in QApplication.topLevelWidgets():
                if window != self and window.isVisible():
                    window.hide()
            self.windows_hidden = True
        else:
            # 显示主窗口
            if self.main_window.isMinimized():
                self.main_window.showNormal()
            else:
                self.main_window.show()
            self.main_window.activateWindow()
            # 恢复延迟窗口状态
            if hasattr(self.main_window, 'delay_window_was_visible') and self.main_window.delay_window_was_visible:
                if self.main_window.delayWindow:
                    self.main_window.delayWindow.show()
                    self.main_window.delayWindow.updateGeometry()
                else:
                    self.main_window.toggleDelayWindow()
            self.windows_hidden = False

    def initUI(self):
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建标签
        self.label = QLabel("音频计算器")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.updateStyle()
        layout.addWidget(self.label)
        
        # 设置初始透明度
        self.setWindowOpacity(0.9)

    def updateStyle(self):
        """更新样式，包括悬停和按下状态"""
        base_style = """
            QLabel {
                background-color: %s;
                color: #F5DEB3;
                font-size: 14px;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #F5DEB3;
            }
        """
        
        if self.dragging:
            bg_color = "#1a2733"  # 更深的颜色
        elif self.drag_started:
            bg_color = "#34495e"  # 稍亮的颜色
        else:
            bg_color = "#2C3E50"  # 基础颜色
            
        self.label.setStyleSheet(base_style % bg_color)

    def moveToDefaultPosition(self):
        screen = QApplication.primaryScreen().geometry()
        # 水平位置改为距离右边缘1/10宽度，垂直位置保持在1/5高度
        self.move(screen.width() - self.width() - screen.width() // 10, screen.height() // 10)

    def contextMenuEvent(self, event):
        # 显示右键菜单
        self.context_menu.popup(event.globalPos())
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.press_pos = event.pos()
            self.dragging = False
            self.drag_started = False
            
    def mouseMoveEvent(self, event):
        if not self.press_pos:
            return
            
        # 计算移动距离
        move_distance = (event.pos() - self.press_pos).manhattanLength()
        
        # 如果超过拖动阈值，开始拖动
        if not self.drag_started and move_distance > self.drag_threshold:
            self.drag_started = True
            self.dragging = True
            self.offset = event.pos()
            
        if self.dragging:
            new_pos = event.globalPosition().toPoint() - self.offset
            # 确保窗口不会移出屏幕
            screen = QApplication.primaryScreen().geometry()
            new_x = max(0, min(new_pos.x(), screen.width() - self.width()))
            new_y = max(0, min(new_pos.y(), screen.height() - self.height()))
            self.move(new_x, new_y)
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 如果没有发生拖动，则触发toggleMainWindow
            if not self.drag_started:
                self.toggleMainWindow()
            self.press_pos = None
            self.dragging = False
            self.drag_started = False
            self.updateStyle()  # 更新样式
            
    def enterEvent(self, event):
        self.setWindowOpacity(1.0)  # 鼠标进入时完全不透明
        
    def leaveEvent(self, event):
        if not self.dragging:  # 只有在不拖动时才改变透明度
            self.setWindowOpacity(0.9)  # 鼠标离开时恢复半透明

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion风格作为基础
    
    # 检查是否支持系统托盘
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, '系统托盘',
                           '找不到系统托盘，程序无法运行。')
        sys.exit(1)
        
    # 设置退出时不自动关闭
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
