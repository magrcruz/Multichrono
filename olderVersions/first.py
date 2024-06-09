import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QTimer

class TimerWidget(QWidget):
    def __init__(self, tag, parent=None):
        super().__init__(parent)
        self.tag = tag
        self.is_running = False
        self.time_elapsed = 0

        self.label = QLabel(self.tag + ": 00:00:00", self)
        self.start_stop_button = QPushButton("Start", self)
        self.reset_button = QPushButton("Reset", self)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_stop_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.start_stop_button.clicked.connect(self.start_stop_timer)
        self.reset_button.clicked.connect(self.reset_timer)

    def start_stop_timer(self):
        if self.is_running:
            self.timer.stop()
            self.start_stop_button.setText("Start")
        else:
            for timer in self.parent().timers:
                if timer != self and timer.is_running:
                    timer.start_stop_timer()
            self.timer.start(1000)
            self.start_stop_button.setText("Pause")
        self.is_running = not self.is_running

    def reset_timer(self):
        self.time_elapsed = 0
        self.update_label()

    def update_timer(self):
        self.time_elapsed += 1
        self.update_label()

    def update_label(self):
        hours = self.time_elapsed // 3600
        minutes = (self.time_elapsed % 3600) // 60
        seconds = self.time_elapsed % 60
        self.label.setText(self.tag + ": {:02d}:{:02d}:{:02d}".format(hours, minutes, seconds))


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
    window = MultiTimerApp()
    window.add_timer()
    window.setWindowTitle("MultiTimer App")
    window.show()
    sys.exit(app.exec_())
