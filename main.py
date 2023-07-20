import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
import sqlite3

class AddressBookApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adres Defteri")
        self.setGeometry(100, 100, 400, 400)

        self.setup_database()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Ad', 'Soyad', 'E-posta', 'Telefon'])
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table_widget)

        name_label = QLabel("Ad:")
        self.name_input = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        surname_label = QLabel("Soyad:")
        self.surname_input = QLineEdit()
        layout.addWidget(surname_label)
        layout.addWidget(self.surname_input)

        email_label = QLabel("E-posta:")
        self.email_input = QLineEdit()
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)

        phone_label = QLabel("Telefon:")
        self.phone_input = QLineEdit()
        layout.addWidget(phone_label)
        layout.addWidget(self.phone_input)

        add_button = QPushButton("Ekle")
        add_button.clicked.connect(self.add_contact)
        layout.addWidget(add_button)

        delete_button = QPushButton("Sil")
        delete_button.clicked.connect(self.delete_contact)
        layout.addWidget(delete_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        self.load_contacts()

    def add_contact(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()

        if name and surname and email and phone:
            conn = sqlite3.connect("address_book.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contacts (name, surname, email, phone) VALUES (?, ?, ?, ?)", (name, surname, email, phone))
            conn.commit()
            conn.close()

            self.load_contacts()
            self.name_input.clear()
            self.surname_input.clear()
            self.email_input.clear()
            self.phone_input.clear()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")

    def delete_contact(self):
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            contact_id = self.table_widget.item(selected_row, 0).text()
            conn = sqlite3.connect("address_book.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()
            conn.close()
            self.load_contacts()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir kişi seçin.")

    def load_contacts(self):
        conn = sqlite3.connect("address_book.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        conn.close()

        self.table_widget.setRowCount(0)

        for row_number, row_data in enumerate(contacts):
            self.table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data[1:]):  # github.com/seferilgun github.com/seferilgun
                self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def setup_database(self):
        conn = sqlite3.connect("address_book.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Çıkış", "Uygulamadan çıkmak istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    address_book_app = AddressBookApp()
    address_book_app.show()

    sys.exit(app.exec_())
