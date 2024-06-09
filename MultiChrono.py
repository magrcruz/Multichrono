import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QToolButton, QSizePolicy, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon
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
        self.status_label.mousePressEvent = self.restart_timer  # Conecta el evento mousePressEvent a la función restart_timer


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

        # Actualizar el estilo del fondo
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

    def restart_timer(self, event):  # Define la función restart_timer para reiniciar el temporizador cuando se hace clic en la etiqueta status_label
        if not self.is_running:  # Solo reinicia el temporizador si está pausado
            self.time_elapsed = 0
            self.update_label()
            self.status_label.setText("")  # Borra el texto "Paused"
            self.status_label.clearFocus()

class MultiTimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.timers = []

        self.layout = QVBoxLayout()

        self.tag_input = QLineEdit(self)
        self.add_timer_button = QToolButton(self)
        self.add_timer_button.setIcon(QIcon("resources/add_icon.png"))  # Reemplaza "add_icon.png" con el nombre de tu archivo de icono
        self.add_timer_button.clicked.connect(self.add_timer)

        # Alineación del botón a la derecha
        self.add_timer_button.setStyleSheet("QToolButton { border: none; }")
        self.add_timer_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Disposición horizontal para colocar el cuadro de entrada de texto y el botón en la misma fila
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.tag_input)
        hbox_layout.addWidget(self.add_timer_button)

        self.layout.addLayout(hbox_layout)
        self.setLayout(self.layout)

        # Conectamos el evento returnPressed del cuadro de texto al método add_timer
        self.tag_input.returnPressed.connect(self.add_timer)

        #for menu 
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)


    def add_timer(self):
        tag = self.tag_input.text() or "Timer"
        timer_widget = TimerWidget(tag)
        self.timers.append(timer_widget)
        self.layout.addWidget(timer_widget)
        self.tag_input.clear()

    def show_context_menu(self, position):
        menu = QMenu(self)
        """
        add_timer_action = QAction("Agregar temporizador", self)
        add_timer_action.triggered.connect(self.add_timer)
        menu.addAction(add_timer_action)
        """

        always_on_top_action = QAction("Always on Top", self)
        always_on_top_action.setCheckable(True)
        always_on_top_action.setChecked(self.windowFlags() & Qt.WindowStaysOnTopHint)
        always_on_top_action.triggered.connect(self.toggle_always_on_top)
        menu.addAction(always_on_top_action)

        restart_all_action = QAction("Reiniciar todos los temporizadores", self)
        restart_all_action.triggered.connect(self.restart_all_timers)
        menu.addAction(restart_all_action)

        clear_all_action = QAction("Eliminar todos los temporizadores", self)
        clear_all_action.triggered.connect(self.clear_all_timers)
        menu.addAction(clear_all_action)

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        menu.addAction(exit_action)

        menu.exec_(self.mapToGlobal(position))

    def toggle_always_on_top(self):
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()

    def restart_all_timers(self):
        for timer in self.timers:
            timer.time_elapsed = 0
            timer.update_label()

    def clear_all_timers(self):
        reply = QMessageBox.question(self, "Eliminar todos los temporizadores", "¿Estás seguro de que deseas eliminar todos los temporizadores?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for timer in self.timers:
                timer.deleteLater()
            self.timers.clear()
        self.add_timer()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('resources/icono.png'))

    window = MultiTimerApp()
    window.add_timer()
    window.setWindowTitle("MultiChrono")
    window.show()
    sys.exit(app.exec_())
