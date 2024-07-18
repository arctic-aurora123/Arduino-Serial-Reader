import sys
import csv
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QComboBox, QMessageBox, QLineEdit, QLabel, QHBoxLayout, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal

# Serial reader thread
class SerialThread(QThread):
    data_received = pyqtSignal(str)
    
    def __init__(self, port, baudrate=9600, parent=None):
        super().__init__(parent)
        self.serial_port = serial.Serial(port, baudrate)
        self.running = True
        self.paused = False
        self.data_buffer = []
    
    def run(self):
        while self.running:
            if not self.paused and self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode().strip()
                self.data_received.emit(data)
                self.data_buffer.append(data)
    
    def pause_reading(self):
        self.paused = True
    
    def resume_reading(self):
        self.paused = False
    
    def stop(self):
        self.running = False
        self.wait()
    
    def save_data_to_csv(self, filename, headers):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header_list = headers.split(',')
            writer.writerow(header_list)
            for item in self.data_buffer:
                writer.writerow(item.split(','))  # Split each data item by comma and write to CSV

# Main application window
class SerialReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Serial Reader')
        self.setGeometry(100, 100, 600, 400)
        
        self.serial_thread = None
        self.available_ports = []
        
        # GUI elements
        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        
        self.port_combobox = QComboBox()
        self.scan_button = QPushButton('Scan Ports')
        self.scan_button.clicked.connect(self.scan_serial_ports)
        
        self.baudrate_combobox = QComboBox()
        self.baudrate_combobox.addItems(['9600', '19200', '38400', '57600', '115200'])
        
        self.header_edit = QLineEdit()
        self.header_edit.setPlaceholderText('Enter CSV Headers (comma separated)')
        
        start_button = QPushButton('Start Reading')
        start_button.clicked.connect(self.start_serial_reading)
        
        pause_button = QPushButton('Pause Reading')
        pause_button.clicked.connect(self.pause_serial_reading)
        
        stop_button = QPushButton('Stop Reading')
        stop_button.clicked.connect(self.stop_serial_reading)
        
        # Layout
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel('CSV Headers:'))
        header_layout.addWidget(self.header_edit)
        
        layout = QVBoxLayout()
        layout.addWidget(self.data_display)
        layout.addWidget(self.port_combobox)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.baudrate_combobox)
        layout.addLayout(header_layout)
        layout.addWidget(start_button)
        layout.addWidget(pause_button)
        layout.addWidget(stop_button)
        
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
        # Initial scan for available ports
        self.scan_serial_ports()
    
    def scan_serial_ports(self):
        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combobox.clear()
        self.port_combobox.addItems(self.available_ports)
    
    def start_serial_reading(self):
        port_name = self.port_combobox.currentText()
        baudrate = int(self.baudrate_combobox.currentText())
        
        if port_name:
            if not self.serial_thread or not self.serial_thread.isRunning():
                self.serial_thread = SerialThread(port_name, baudrate)
                self.serial_thread.data_received.connect(self.update_data_display)
                self.serial_thread.start()
            elif self.serial_thread.paused:
                self.serial_thread.resume_reading()
    
    def pause_serial_reading(self):
        if self.serial_thread and self.serial_thread.isRunning():
            self.serial_thread.pause_reading()
    
    def stop_serial_reading(self):
        if self.serial_thread and self.serial_thread.isRunning():
            filename, _ = QFileDialog.getSaveFileName(self, 'Save Serial Data', '', 'CSV Files (*.csv)')
            if filename:
                headers = self.header_edit.text()
                self.serial_thread.save_data_to_csv(filename, headers)
                QMessageBox.information(self, 'Data Saved', 'Serial data saved successfully.')
            self.serial_thread.stop()
    
    def update_data_display(self, data):
        self.data_display.append(data)
    
    def closeEvent(self, event):
        if self.serial_thread and self.serial_thread.isRunning():
            self.serial_thread.stop()
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialReaderApp()
    window.show()
    sys.exit(app.exec_())
