from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

# Data structure to represent a contact


class Contact:
    def __init__(self, name, email, address, phone):
        self.name = name
        self.email = email
        self.address = address
        self.phone = phone

# MainContacts class represents the main window


class MainContacts(QMainWindow):
    def __init__(self):
        super(MainContacts, self).__init__()
        loadUi("main_contacts.ui", self)
        self.show()

        # List to store contacts
        self.contacts = []

        # Set up the table widget
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Name"])
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setColumnWidth(0, 230)

        # Set up UI elements and connect signals to slots
        self.lineEdit.setPlaceholderText("Search...")
        self.lineEdit.textChanged.connect(self.search)

        self.add_btn.clicked.connect(self.add_button)
        self.view_btn.clicked.connect(self.view_button)
        self.upd_btn.clicked.connect(self.update_button)
        self.del_btn.clicked.connect(self.delete_button)
        self.clr_btn.clicked.connect(self.clear_button)

    # Slot for the "Add" button
    def add_button(self):
        dialog = ContAdd(self)
        if dialog.exec_() == QDialog.Accepted:
            contact = dialog.get_contact()
            if contact:
                self.contacts.append(contact)
                self.update_table()

    # Slot for the "View" button
    def view_button(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        if not selected_rows:
            self.show_warning("No Selection", "Please select a contact.")
            return

        row = selected_rows[0].row()
        dialog = ViewCont(self, contact=self.contacts[row])
        dialog.exec_()

    # Slot for the "Update" button
    def update_button(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        if not selected_rows:
            self.show_warning("No Selection", "Please select a contact.")
            return

        row = selected_rows[0].row()
        dialog = ContAdd(self, contact=self.contacts[row])
        dialog.exec_()
        updated_contact = dialog.get_contact()

        if updated_contact:
            self.contacts[row] = updated_contact
            self.update_table()

    # Slot for the "Delete" button
    def delete_button(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        if not selected_rows:
            self.show_warning("No Selection", "Please select a contact.")
            return

        row = selected_rows[0].row()
        del self.contacts[row]
        self.update_table()

    # Slot for the "Clear" button
    def clear_button(self):
        self.contacts = []
        self.update_table()

    # Update the table with current contacts
    def update_table(self):
        self.tableWidget.setRowCount(len(self.contacts))
        for row, contact in enumerate(self.contacts):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(contact.name))

    # Slot for the search functionality
    def search(self):
        query = self.lineEdit.text().lower()

        for row in range(self.tableWidget.rowCount()):
            hide_row = True
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item and query in item.text().lower():
                    hide_row = False
                    break
            self.tableWidget.setRowHidden(row, hide_row)

    # Show a warning dialog
    def show_warning(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

# ContAdd class represents the dialog for adding or updating a contact


class ContAdd(QDialog):
    def __init__(self, parent, contact=None):
        super().__init__(parent)
        loadUi("cont_add.ui", self)
        self.contact = contact
        if self.contact:
            self.load_contact_data()

        self.accepted = False

    # Load existing contact data into the dialog
    def load_contact_data(self):
        self.lineEdit_name.setText(self.contact.name)
        self.lineEdit_email.setText(self.contact.email)
        self.lineEdit_add.setText(self.contact.address)
        self.lineEdit_contact.setText(self.contact.phone)

    # Get the contact information from the dialog
    def get_contact(self):
        name = self.lineEdit_name.text()
        email = self.lineEdit_email.text()
        address = self.lineEdit_add.text()
        phone = self.lineEdit_contact.text()

        if not name or not email or not address or not phone:
            self.show_warning("Input Error", "Please fill in all fields.")
            return None

        self.accepted = True

        return Contact(name, email, address, phone)

    # Show a warning dialog
    def show_warning(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

# ViewCont class represents the dialog for viewing a contact


class ViewCont(QDialog):
    def __init__(self, parent, contact=None):
        super().__init__(parent)
        loadUi("view_contact.ui", self)
        self.contact = contact
        if self.contact:
            self.load_contact_data()

        self.close_btn.clicked.connect(lambda: self.close())

    # Load contact data into the view dialog
    def load_contact_data(self):
        self.view_name.setText(self.contact.name)
        self.view_email.setText(self.contact.email)
        self.view_add.setText(self.contact.address)
        self.view_contact.setText(self.contact.phone)


# Instantiate the application and main window
app = QApplication([])
window = MainContacts()
app.exec_()
