import os
import sys
import json
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
from helpers.database import DBAccess
from helpers.modal import Modal

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, 'queries')

with open(os.path.join(data_path,'db_data.json'), 'r') as data_file:
    connection_data = json.load(data_file)

xml = ET.parse(os.path.join(data_path,'queries.xml')).getroot()
queries_list = [query.text for query in xml.findall("query")]

class QueryAccess(QMainWindow):
    def __init__(self):
        super().__init__()
        # Creamos un objeto para acceder a la base de datos
        self.db = DBAccess(host = connection_data["host"],user = connection_data["user"], password = connection_data["password"])
        self.db.create_connection()
        self.db.create_cursor()
        self.db.select_database(connection_data["database"])
       # Cargamos el icono y lo asignamos a la ventana principal
        icon = QIcon("img/icon.png")
        self.setWindowIcon(icon)

    def execute_queries(self):
        self.resultado = True
        for query in queries_list:
            result = self.db.set_data(query)
            if not result[0]:
                self.resultado = False
        if self.resultado:
            result_message = "Todas las consultas se han ejecutado correctamente"
        else:
            result_message = "Ha habido un error al ejecutar alguna de las consultas"
        modal = Modal(result=result_message)
        modal.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    acceso = QueryAccess()
    acceso.execute_queries()
    app.quit()


