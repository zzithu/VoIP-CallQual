#Here is not where the logic is, but how we display it

#We want buttons, which can show where to look IE ports, timestamps, packet numbers, types
#There should be a graph at the beginning, which should show some sort of stability

#This is just what I am writing, so feel free to change this as necessary


from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

## THIS IS A PROTOTYPE AND SHOULD BE CHANGED. I wanted to get this out so we had an idea for monday

class CallMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CallQual")
        self.setGeometry(100, 100, 1024, 512)

        central_widget = QWidget()
        layout = QVBoxLayout()

        #I have to look more into layouts, I want the buttons on the left in the future.

        # Error Button
        self.error_button = QPushButton("Errors/Dropped Packets")
        self.error_button.clicked.connect(self.show_errors)
        layout.addWidget(self.error_button)

        # Connection Quality Button
        self.quality_button = QPushButton("Connection Quality")
        self.quality_button.clicked.connect(self.show_quality)
        layout.addWidget(self.quality_button)

        # General Graph Button
        self.graph_button = QPushButton("General Graph")
        self.graph_button.clicked.connect(self.show_graph)
        layout.addWidget(self.graph_button)

        # Wireshark Log Button
        self.log_button = QPushButton("Overall Log / Wireshark")
        self.log_button.clicked.connect(self.show_log)
        layout.addWidget(self.log_button)

        # Status Label // We want to put a graph here
        self.status_label = QLabel("Status: Monitoring...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Set Layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    #We can open additional windows for mode context dpending on the button
    def show_errors(self):
        print("Showing Errors/Dropped Packets")
        error_window = QMainWindow(self)
        error_window.setWindowTitle("Error Log")
        error_window.setGeometry(200, 200, 400, 300)
        error_window.show()

    #These are all debug right now
    def show_quality(self):
        print("Showing Connection Quality")

    def show_graph(self):
        print("Showing General Graph")

    def show_log(self):
        print("Opening Overall Log / Wireshark")

# Consider moving this into the actual main class, as it would make development and integration easier.
def main():
    app = QApplication([])
    window = CallMonitorApp()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
