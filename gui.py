### INTRO

#Here is not where the logic is, but how we display it

#We want buttons, which can show where to look IE ports, timestamps, packet numbers, types
#There should be a graph at the beginning, which should show some sort of stability

#This is just what I am writing, so feel free to change this as necessary

#This is a prototype, feel free to change this as necessary.

### DEMONSTRATION USAGE

#The General graph button updates the graph and adds errors (for proof of concept more than anything)
#The other buttons print to console.

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import random

# Temporary solution to demonstrate the graph
class NetworkMonitor:
    def __init__(self):
        #TODO add the actual data..
        self.data = [random.randint(1, 10) for _ in range(10)]  # Random resend counts
        self.errors = 0
        self.total_connections = 0
    
    def get_resend_data(self):
        #TODO update with actual data
        self.data = [random.randint(1, 10) for _ in range(10)]
        return self.data

    def get_errors(self):
        #TODO We have this!
        self.errors += random.randint(0, 2)
        return self.errors

    def get_total_connections(self):
        #TODO implement this outside as well, or just count
        self.total_connections += random.randint(1, 3)
        return self.total_connections

# Graph definition
class GraphWidget(pg.PlotWidget):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
        self.plot = self.plot(pen="b")  # Blue line
        self.update_graph()  # Initialize graph

    def update_graph(self):
        """Fetch new data and refresh the graph."""
        new_data = self.monitor.get_resend_data()
        self.plot.setData(new_data)

# Main window
class CallMonitorApp(QMainWindow):
    # Window setup
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CallQual")
        self.setGeometry(100, 100, 1024, 512)

        # PyQt setup
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout()  # Horizontal layout for left, middle, right
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Left Layout (buttons)
        self.left_layout = QVBoxLayout()  # Buttons on the left
        self.main_layout.addLayout(self.left_layout)

        # Right Layout (metrics)
        self.right_layout = QVBoxLayout()  # Metrics on the right
        self.main_layout.addLayout(self.right_layout)

        # Graph setup (middle)
        self.network_monitor = NetworkMonitor()  # Placeholder, but the idea
        self.graph_widget = GraphWidget(self.network_monitor)  # Update with actual data
        self.main_layout.addWidget(self.graph_widget)

        # Buttons
        self.buttons = [
            QPushButton("Errors/Dropped Packets"),
            QPushButton("Connection Quality"),
            QPushButton("General Graph"),
            QPushButton("Overall Log / Wireshark"),
            QPushButton("Settings"),
        ]

        # Assigns *FUNCTION* behavior to buttons
        self.buttons[0].clicked.connect(self.show_errors)
        self.buttons[1].clicked.connect(self.show_quality)
        self.buttons[2].clicked.connect(self.update_graph)
        self.buttons[3].clicked.connect(self.show_log)
        self.buttons[4].clicked.connect(self.show_settings)

        # Left layout (buttons)
        for button in self.buttons:
            self.left_layout.addWidget(button)

        # Right layout (metrics)
        self.errors_label = QLabel(f"Errors: {self.network_monitor.get_errors()}")
        self.total_connections_label = QLabel(f"Total Connections: {self.network_monitor.get_total_connections()}")
        self.right_layout.addWidget(self.errors_label)
        self.right_layout.addWidget(self.total_connections_label)

        # This makes it look like Wireshark
        self.central_widget.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 2px solid #2980b9;
                border-radius: 4px;
                padding: 2px 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
            QLabel {
                font-size: 14px;
                margin: 10px;
            }
        """)

    # Trigger manual graph update
    def update_graph(self):
        """Trigger manual graph update."""
        print("Updating graph...")
        self.graph_widget.update_graph()
        self.update_metrics()

    # Update metrics (errors and total connections)
    def update_metrics(self):
        """Update the metrics on the right side."""
        self.errors_label.setText(f"Errors: {self.network_monitor.get_errors()}")
        self.total_connections_label.setText(f"Total Connections: {self.network_monitor.get_total_connections()}")

    # Dynamic resizing
    def resizeEvent(self, event):
        button_width = max(144, self.width() // 8)
        button_height = max(52, self.height() // 10)

        for button in self.buttons:
            button.setFixedSize(button_width, button_height)

    # Debug functions
    def show_errors(self):
        print("Showing errors...")

    def show_quality(self):
        print("Showing quality...")

    def show_log(self):
        print("Showing log...")

    def show_settings(self):
        print("Showing settings...")

# Run the app
if __name__ == "__main__":
    app = QApplication([])
    window = CallMonitorApp()
    window.show()
    app.exec()
