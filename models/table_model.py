#----------------------- Imports ---------------------------------#
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant


# ------------------ Dataframe into Model ----------------------- #
class TableModel(QAbstractTableModel):
    def __init__(self,data,columns):
        super().__init__()
        self._data = data
        self._columns = columns

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._columns)

    def data(self, index, role):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            return str(self._data[row][col])
        return None
        
    def headerData(self, section, Qt_Orientation, role=None):
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._columns[section]
        return QVariant()
    
    
