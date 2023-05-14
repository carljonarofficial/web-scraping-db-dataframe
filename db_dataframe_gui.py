import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableView, QWidget
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
import mysql.connector

class DataFrameModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data.iloc[:, 1:-1]  # Exclude the first and last columns
    
    def rowCount(self, parent):
        return len(self._data)
    
    def columnCount(self, parent):
        return len(self._data.columns)
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, (int, float)):
                return format(value, ',')
            return str(value)
        return QVariant()
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return QVariant()
    
    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        col_name = self._data.columns[column]
        self._data.sort_values(col_name, ascending=order == Qt.AscendingOrder, inplace=True)
        self.layoutChanged.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MySQL to DataFrame GUI")
        self.resize(800, 600)
        
        # Create a QWidget as the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Create a QVBoxLayout to arrange the widgets vertically
        layout = QVBoxLayout(central_widget)
        
        # Create a QTableView widget to display the DataFrame
        self.table_view = QTableView()
        layout.addWidget(self.table_view)
        
        # Connect to the MySQL database and retrieve data
        self.retrieve_data()
    
    def retrieve_data(self):
        # Replace 'host', 'user', 'password', and 'database' with your MySQL connection details
        db_connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )
        
        query = "SELECT * FROM your_table"
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=cursor.column_names)

        cursor.close()
        db_connection.close()
        
        # Create a custom model from the DataFrame
        model = DataFrameModel(df.head(5))
        
        # Set the model for the QTableView
        self.table_view.setModel(model)
        
        # Set table properties
        self.table_view.setSortingEnabled(True)
        self.table_view.sortByColumn(0, Qt.AscendingOrder)
        # self.table_view.horizontalHeader().setStretchLastSection(True)

def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()
