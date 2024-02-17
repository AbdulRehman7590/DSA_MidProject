# ----------------------- Modules -------------------------------- #
import sys, os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
import pandas as pd
import csv

# Change the path to the project root directory to import files from utils
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(project_root)

from utils.searching_algorithms import *
from models.table_model import TableModel
from utils.scrape_threading import ScrapingThread
from utils.sort_threading import SortingThread
from utils.read_Data import read_file


# ---------------------- Program -------------------------------- #
class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("views/scraping_GUI.ui", self)


        # ---------------------- Defaults ------------------------ #
        self.setWindowTitle("READERS HUB") 
        self.columns = ['Title','Price','Seller','Sold_Items','Country','Status','Seller_Rank','Shipping']

        self.counter = 0                    # Counter for timer
        self.isSorting = False              # Flag for checking if sorting is running
        self.sortingThread = None           # Thread for sorting
        self.multiLevel_attributes = []     # List for multi-level sorting attributes
        self.scrappingThread = None         # Thread for scrapping
        self.scrappedData = []              # List for scrapped data
        self.timer = QTimer()               # Timer for counting time
        self.timer.timeout.connect(self.updateCounter)

        self.outer_Stack = self.findChild(QStackedWidget, "main_Stack")
        self.inner_Stack = self.findChild(QStackedWidget, "pageContent_Stack")
        self.changeOuterStackedPage(0)
        self.changeInnerStackedPage(0)

        self.algorithmAttributes = {
            "Bubble Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Selection Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Insertion Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Merge Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Heap Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Quick Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Shell Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Brick Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Cocktail Sort": ["Title", "Price", "Seller", "Sold_Items", "Country", "Status", "Seller_Rank", "Shipping"],
            "Count Sort": ["Sold_Items"],
            "Radix Sort": ["Price", "Sold_Items", "Shipping"],
            "Bucket Sort": ["Price", "Sold_Items", "Shipping"]
        }


        # ---------------------- Table --------------------------- #
        self.df = read_file("unique_data.csv")
        self.table = self.findChild(QTableView, "sorting_table")
        self.loadUniqueData(self.table)
        self.table2 = self.findChild(QTableView, "searching_table")
        self.loadMillionData()
        self.table3 = self.findChild(QTableView, "scraping_table")


        # ----------------------- Buttons ------------------------ #
        self.continue_Btn.clicked.connect(lambda: self.changeOuterStackedPage(1))
        self.home_Btn.clicked.connect(lambda: self.changeInnerStackedPage(0))
        self.sorting_Btn.clicked.connect(lambda: self.changeInnerStackedPage(1))
        self.searching_Btn.clicked.connect(lambda: self.changeInnerStackedPage(2))
        self.scraping_Btn.clicked.connect(lambda: self.changeInnerStackedPage(3))
        self.exit_Btn.clicked.connect(lambda: sys.exit())



    # ---------------------- Button Functions -------------------- #
    def changeOuterStackedPage(self, index):
        self.outer_Stack.setCurrentIndex(index)

    def changeInnerStackedPage(self, index):
        self.inner_Stack.setCurrentIndex(index)
        # Setting up the sorting page
        if index == 1:
            self.sorting()
        # Setting up the searching page
        elif index == 2:
            self.search()
        # Setting up the scraping page
        elif index == 3:
            self.scraping()



    # ---------------------- Loading Data ------------------------ #
    def loadUniqueData(self,tabl):
        self.loadTable(read_file("unique_data.csv"),tabl)

    def loadMillionData(self):
        self.loadTable(read_file("million_data.csv"),self.table2)



    # ---------------------- Timer ------------------------------- #
    def updateCounter(self):
        self.counter += 1
        hours = self.counter // 3600
        minutes = (self.counter // 60) % 60
        seconds = self.counter % 60
        counterText = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        self.time_Show.setText(counterText)



    # ---------------------- Clearing ---------------------------- #
    def clearingData(self):
        self.attribute_box.setCurrentIndex(0)
        self.algorithm_box.setCurrentIndex(0)
        self.ascending_Check.setChecked(True)


    def clearingData2(self):
        self.columnNames_box.setCurrentIndex(0)
        self.filters_box.setCurrentIndex(0)
        self.input_Box.clear()
        self.input_Box.setPlaceholderText("Enter your key to search, here")
        self.columnNames_box_2.setCurrentIndex(0)
        self.filters_box_2.setCurrentIndex(0)
        self.input_Box_2.clear()
        self.input_Box_2.setPlaceholderText("Enter your key to search, here")
        self.And_button.setChecked(False)
        self.Or_button.setChecked(False)
        self.Not_button.setChecked(False)



    # ---------------------- Loading Table ----------------------- #
    def loadTable(self, df, tabl):
        tabl.setModel(TableModel(df,self.columns))
        header = tabl.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)



    # ---------------------- Sorting ----------------------------- #
    def sorting(self):
        algo = self.findChild(QComboBox, "algorithm_box")
        col = self.findChild(QComboBox, "attribute_box")

        def updateAttribute():
            selectedAlgo = algo.currentText()
            col.clear()
            col.addItems(
                self.algorithmAttributes.get(selectedAlgo, []))
        
        updateAttribute()
        algo.currentIndexChanged.connect(updateAttribute)
        
        self.start_Btn_2.clicked.connect(self.startSorting)
        self.clear_Btn.clicked.connect(self.clearingData)

        self.multiLevel_Btn.clicked.connect(self.openDialogueBox)


    def startSorting(self):
        self.counter = 0
        self.algo = self.findChild(QComboBox, "algorithm_box")
        self.colu = self.findChild(QComboBox, "attribute_box")

        algorithm = self.algo.currentText()
        column = []
        column.append(self.colu.currentText())

        if self.ascending_Check.isChecked():
            sort_type = True
        elif self.descending_Check.isChecked():
            sort_type = False

        self.isSorting = True
        self.sortingThread = SortingThread(self.df, column, sort_type, algorithm)
        self.sortingThread.finished.connect(lambda: self.sortingFinished())
        self.sortingThread.start()
        self.timer.start(1000)


    def sortingFinished(self):
        self.isSorting = False
        self.timer.stop()
        self.loadTable(self.df, self.table)



    # ---------------------- Multi-level Sorting ----------------- #
    def openDialogueBox(self):
        dialog = QDialog()
        loadUi("views/multi_level.ui", dialog)

        Table = dialog.findChild(QtWidgets.QTableWidget, 'tableWidget')
        Table.setRowCount(10)
        Table.setHorizontalHeaderLabels(["Attributes"])
        header = Table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        dialog.add_Btn.clicked.connect(lambda: self.addButton(dialog, Table))
        dialog.delete_Btn.clicked.connect(lambda: self.deleteButton(dialog, Table))
        dialog.multisort_Btn.clicked.connect(lambda: self.startsort_CloseDialog(dialog))
        dialog.exec_()


    def loadAttributesToTable(self, dialog, table):
        table.setRowCount(len(self.multiLevel_attributes))
        table.resizeRowsToContents()
        for row, attribute in enumerate(self.multiLevel_attributes):
            table.setItem(row, 0, QTableWidgetItem(attribute))


    def addButton(self, dialog, table):
        dialog_attributes = dialog.findChild(QtWidgets.QComboBox, 'DialogueAttribute')
        if dialog_attributes.currentText() != "--Select Attribute--" and not self.multiLevel_attributes.__contains__(dialog_attributes.currentText()):
            self.multiLevel_attributes.append(dialog_attributes.currentText())
            self.loadAttributesToTable(dialog, table)


    def deleteButton(self, dialog, table):
        currentRow = table.currentRow()
        if currentRow >= 0:
            deletedAttribute = self.multiLevel_attributes.pop(currentRow)
            self.loadAttributesToTable(dialog, table)


    def startsort_CloseDialog(self, dialog):
        if len(self.multiLevel_attributes) == 0:
            dialog.close()
            return

        if dialog.multi_ascending_Check.isChecked():
            sort_type = True
        elif dialog.multi_descending_Check.isChecked():
            sort_type = False

        sortingThread = SortingThread(self.df, self.multiLevel_attributes, sort_type, "Multi Sort")
        sortingThread.finished.connect(self.sortingFinished)
        sortingThread.start()
        sortingThread.wait()

        self.multiLevel_attributes.clear()
        self.loadTable(self.df, self.table)
        dialog.close()



    # ---------------------- Searching --------------------------- #
    def search(self):
        self.col1 = self.findChild(QtWidgets.QComboBox, 'columnNames_box')  
        self.col2 = self.findChild(QtWidgets.QComboBox, 'columnNames_box_2')
        
        self.filter1 = self.findChild(QtWidgets.QComboBox, 'filters_box')
        self.filter2 = self.findChild(QtWidgets.QComboBox, 'filters_box_2')
        
        self.input1 = self.findChild(QtWidgets.QLineEdit, 'input_Box')
        self.input1.setPlaceholderText("Enter your key to search, here")
        
        self.input2 = self.findChild(QtWidgets.QLineEdit, 'input_Box_2')
        self.input2.setPlaceholderText("Enter your key to search, here")

        self.or_b = self.findChild(QtWidgets.QRadioButton, 'And_button')
        self.and_b = self.findChild(QtWidgets.QRadioButton, 'Or_button')
        self.not_b = self.findChild(QtWidgets.QRadioButton, 'Not_button')

        self.start_Btn.clicked.connect(self.startSearching)
        self.millionData_Btn.clicked.connect(self.loadMillionData)
        self.uniqueData_Btn.clicked.connect(lambda: self.loadUniqueData(self.table2))
        self.clear_Btn_2.clicked.connect(self.clearingData2)


    def startSearching(self):
        col = self.col1.currentIndex()-1
        key = self.input1.text()
        filter_Type = self.filter1.currentIndex()

        if col == -1 or filter_Type == 0 or key == "":  
            self.showErrorMessage("To perform a search operation, you need to select an attribute, a search key, and a filter.")
        else:
            
            if not self.or_b.isChecked() and not self.and_b.isChecked() and not self.not_b.isChecked():
                indexes = LinearSearch(self.df,col,key,filter_Type)
                if len(indexes) == 0:
                    self.showErrorMessage("No data found")
                else:
                    self.loadTable(indexes,self.table2)
            
            else:

                operator = None
                if self.or_b.isChecked():
                    operator = "Or"
                elif self.and_b.isChecked():
                    operator = "And"
                elif self.not_b.isChecked():
                    operator = "Not"
                
                col1 = self.col2.currentIndex()-1
                key2 = self.input2.text()
                filter_Type2 = self.filter2.currentIndex()
                
                if col1 == -1 or filter_Type2 == -1 or key2 == "":
                    self.showErrorMessage("To perform a multi search, you need to select both attribute properties.")
                else:
                    indexes = MultiLinearSearch(self.df, col, key, filter_Type, col1, key2, filter_Type2, operator)
                    if len(indexes) == 0:
                        self.showErrorMessage("No data found")
                    else:
                        self.loadTable(indexes,self.table2)


    def showErrorMessage(self, message):
        p_widget = QMainWindow()
        QMessageBox.warning(p_widget, "Warning", message, QMessageBox.Ok)



    # ---------------------- Scraping ---------------------------- #
    def scraping(self):
        self.progress_Bar = self.findChild(QtWidgets.QWidget, 'progressBar')
        self.progress_Bar.setValue(0)
        self.books = self.findChild(QtWidgets.QWidget, 'books_Scraped')

        self.start_scrap.clicked.connect(lambda: self.startScraping())
        self.pause_scrap.clicked.connect(lambda: self.pauseScraping())
        self.stop_scrap.clicked.connect(lambda: self.stopScraping())
        self.resume_scrap.clicked.connect(lambda: self.resumeScraping())


    def startScraping(self):
        self.scrapingThread = ScrapingThread()
        self.scrapingThread.scrapingIterationFinished.connect(self.handleScrapedData)
        self.scrapingThread.start()


    def pauseScraping(self):
        if hasattr(self, 'scrapingThread'):
            self.scrapingThread.pause()


    def stopScraping(self):
        if hasattr(self, 'scrapingThread'):
            self.scrapingThread.stop()
            self.scrapingThread.wait()


    def resumeScraping(self):
        if hasattr(self, 'scrapingThread'):
            self.scrapingThread.resume()


    def updateProgressBar(self):
        self.books.setText(str(len(self.scrappedData))+" Books Scrapped")
        value = len(self.scrappedData)//100
        self.progress_Bar.setValue(value)


    def handleScrapedData(self, scrappedData):
        self.scrappedData+=scrappedData
        self.updateProgressBar()
        if self.scrappedData != []:
            self.loadTable(self.scrappedData, self.table3)



# ------------------------- Main --------------------------------- #
def Start():
    try:
        app = QApplication(sys.argv)
        window = Mainwindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("An error occured: ", str(e))


if __name__ == "__main__":
    Start()