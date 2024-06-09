import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QInputDialog
from PyQt5.QtCore import QTimer, Qt


class TimerWidget(QWidget):
    def __init__(self, tag, parent=None):
        super().__init__(parent)
        self.tag = tag
        self.is_running = False
        self.time_elapsed = 0

        self.tag_label = QLabel(self.tag, self)
        self.tag_label.setAlignment(Qt.AlignCenter)
        self.tag_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.time_label = QLabel("00:00:00", self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 24px;")

        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tag_label)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.tag_label.mousePressEvent = self.edit_tag
        self.time_label.mousePressEvent = self.start_stop_timer

    def start_stop_timer(self, event):
        if self.is_running:
            self.timer.stop()
            self.status_label.setText("Paused")
        else:
            for timer in self.parent().timers:
                if timer != self and timer.is_running:
                    timer.start_stop_timer(event)
            self.timer.start(1000)
            self.status_label.setText("Running")
        self.is_running = not self.is_running
        self.update_background_style()

    def edit_tag(self, event):
        self.tag_label.clearFocus()
        self.tag_label.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.tag_label.setLineWidth(2)
        self.tag_label.setMargin(5)
        self.tag_label.setContentsMargins(0, 0, 0, 0)
        self.tag_label.setScaledContents(False)
        new_tag, ok = QInputDialog.getText(self, "Edit Timer", "Enter new timer name:", QLineEdit.Normal, self.tag)
        if ok and new_tag:
            self.tag = new_tag
            self.tag_label.setText(new_tag)


    def update_timer(self):
        self.time_elapsed += 1
        self.update_label()

    def update_label(self):
        hours = self.time_elapsed // 3600
        minutes = (self.time_elapsed % 3600) // 60
        seconds = self.time_elapsed % 60
        self.time_label.setText("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds))

    def update_background_style(self):
        if self.is_running:
            self.tag_label.setStyleSheet("font-size: 18px; font-weight: bold; background-color: #90EE90;")
        else:
            self.tag_label.setStyleSheet("font-size: 18px; font-weight: bold; background-color: none;")


class MultiTimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.timers = []

        self.layout = QVBoxLayout()

        self.tag_input = QLineEdit(self)
        self.add_timer_button = QPushButton("Add Timer", self)
        self.layout.addWidget(self.tag_input)
        self.layout.addWidget(self.add_timer_button)

        self.add_timer_button.clicked.connect(self.add_timer)

        self.setLayout(self.layout)

    def add_timer(self):
        tag = self.tag_input.text() or "Timer"
        timer_widget = TimerWidget(tag)
        self.timers.append(timer_widget)
        self.layout.addWidget(timer_widget)
        self.tag_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar el archivo de estilo QSS
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MultiTimerApp()
    window.add_timer()
    window.setWindowTitle("MultiTimer App")
    window.show()
    sys.exit(app.exec_())
