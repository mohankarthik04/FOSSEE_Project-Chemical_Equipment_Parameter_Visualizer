import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QScrollArea, QHBoxLayout, QDialog,
    QLineEdit, QFormLayout
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


# LOGIN
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Required")
        layout = QFormLayout(self)

        self.user = QLineEdit()
        self.pwd = QLineEdit()
        self.pwd.setEchoMode(QLineEdit.Password)

        layout.addRow("Username:", self.user)
        layout.addRow("Password:", self.pwd)

        btn = QPushButton("Login")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)


# CHART CANVAS
class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(6.5, 5))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        fig.tight_layout(pad=3)

    def plot_bar(self, data):
        self.ax.clear()
        labels = list(data.keys())
        values = list(data.values())

        self.ax.bar(labels, values, color="#0d6efd", width=0.5)
        self.ax.set_title("Equipment Type Distribution", fontsize=14, pad=15)
        self.ax.set_xlabel("Equipment Type", fontsize=11, labelpad=10)
        self.ax.set_ylabel("Count", fontsize=11)

        self.ax.set_xticks(range(len(labels)))
        self.ax.set_xticklabels(labels, rotation=35, ha='right', fontsize=10)
        self.ax.set_ylim(0, max(values) + 1)

        self.ax.grid(axis='y', linestyle='--', alpha=0.4)
        self.figure.tight_layout(pad=3)
        self.draw()

    def plot_pie(self, data):
        self.ax.clear()
        labels = list(data.keys())
        values = list(data.values())

        self.ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10},
            wedgeprops={'edgecolor': 'white'}
        )

        self.ax.set_title("Type Share (%)", fontsize=14, pad=15)
        self.ax.axis('equal')
        self.figure.tight_layout(pad=3)
        self.draw()


# MAIN DESKTOP_APP
class App(QWidget):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth
        self.setWindowTitle("⚙ Chemical Equipment Parameter Visualizer")
        self.setGeometry(200, 80, 1350, 850)

        self.setStyleSheet("""
            QWidget { background-color: #f8f9fa; font-family: 'Segoe UI'; }
            QPushButton {
                background-color: #0d6efd; color: white;
                padding: 10px; border-radius: 6px;
                font-weight: 600; font-size: 14px;
            }
            QPushButton:hover { background-color: #0b5ed7; }
            QTableWidget { background: white; border: none; }
            QHeaderView::section {
                background-color: #212529; color: white;
                padding: 6px; font-weight: bold;
            }
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(18)

        title = QLabel("⚙ Equipment Data Analytics Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:32px; font-weight:700;")
        layout.addWidget(title)

        self.summary_label = QLabel("Upload CSV to see analytics")
        self.summary_label.setAlignment(Qt.AlignCenter)
        self.summary_label.setStyleSheet("font-size:20px;")
        layout.addWidget(self.summary_label)

        # Upload Button
        btn = QPushButton("Upload CSV File")
        btn.setFixedWidth(250)
        btn.setStyleSheet("font-size:20px; font-weight:700;")
        btn.clicked.connect(self.upload_csv)

        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(btn)
        btn_container.addStretch()
        layout.addLayout(btn_container)

        # PDF Button
        pdf_btn = QPushButton("Generate PDF Report")
        pdf_btn.setFixedWidth(250)
        pdf_btn.setStyleSheet("background:#198754; font-size:20px; font-weight:700;")
        pdf_btn.clicked.connect(self.generate_pdf)
        layout.addWidget(pdf_btn, alignment=Qt.AlignCenter)

        # Charts + Table
        row = QHBoxLayout()
        self.bar_chart = ChartCanvas(self)
        self.pie_chart = ChartCanvas(self)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Equipment Type", "Count"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        row.addWidget(self.bar_chart, 1)
        row.addWidget(self.pie_chart, 1)
        row.addWidget(self.table, 1)
        layout.addLayout(row)

        # History Table
        history_title = QLabel("History")
        history_title.setAlignment(Qt.AlignCenter)
        history_title.setStyleSheet("font-size:22px; font-weight:700;")
        layout.addWidget(history_title)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Upload Time", "Total Count"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setMinimumHeight(300)
        layout.addWidget(self.history_table)

        scroll.setWidget(container)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.fetch_history()

    # FUNCTIONS
    def upload_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        with open(path, 'rb') as f:
            requests.post("http://127.0.0.1:8000/upload/", files={'file': f}, auth=self.auth)

        res = requests.get("http://127.0.0.1:8000/summary/", auth=self.auth).json()
        self.display_summary(res)
        self.fetch_history()

    def display_summary(self, res):
        self.summary_label.setText(
        f"Total: {res.get('total_count')} | "
        f"Avg. Flow: {res.get('avg_flowrate'):.3f} m³/s | "
        f"Avg. Pressure: {res.get('avg_pressure'):.3f} Pa | "
        f"Avg. Temp: {res.get('avg_temperature'):.3f} °C"
        )
        self.current_summary = res

        types = res.get("type_distribution", {})
        self.bar_chart.plot_bar(types)
        self.pie_chart.plot_pie(types)
        self.populate_table(types)

    def populate_table(self, data):
        self.table.setRowCount(len(data))

        for row, (k, v) in enumerate(data.items()):
            key_item = QTableWidgetItem(str(k))
            key_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, key_item)

            value_item = QTableWidgetItem(str(v))
            value_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, value_item)

    def fetch_history(self):
        try:
            data = requests.get("http://127.0.0.1:8000/history/", auth=self.auth).json()[:5]
            self.history_table.setRowCount(len(data))

            for row, item in enumerate(data):
            # FOR TIME
                time_item = QTableWidgetItem(item['time'])
                time_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row, 0, time_item)

            # FOR TOTAL COUNT
                total_item = QTableWidgetItem(str(item['summary']['total_count']))
                total_item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row, 1, total_item)

        except Exception as e:
            print("History fetch error:", e)

    # PDF GENERATION
    def generate_pdf(self):

        if not hasattr(self, "current_summary"):
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if not path:
            return

        doc = SimpleDocTemplate(path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        s = self.current_summary
        elements.append(Paragraph("Equipment Analytics Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(
    Paragraph(
        f"Total: {s['total_count']} | "
        f"Avg Flow: {s['avg_flowrate']:.3f} m³/s | "
        f"Avg Pressure: {s['avg_pressure']:.3f} Pa | "
        f"Avg Temp: {s['avg_temperature']:.3f} °C",
        styles['Normal']
    )
)
        elements.append(Spacer(1, 12))

        data = [["Equipment Type", "Count"]]
        for k, v in s["type_distribution"].items():
            data.append([k, str(v)])

        t = Table(data)
        t.setStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN', (1,1), (-1,-1), 'CENTER')
        ])

        elements.append(t)
        doc.build(elements)


# STARTING HERE
app = QApplication(sys.argv)
login = LoginDialog()

if login.exec_() == QDialog.Accepted:
    credentials = (login.user.text(), login.pwd.text())
    window = App(credentials)
    window.showMaximized()
    sys.exit(app.exec_())
