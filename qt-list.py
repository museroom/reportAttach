# Allow access to command-line arguments
import sys
 
# SIP allows us to select the API we wish to use
import sip
 
# use the more modern PyQt API (not enabled by default in Python 2.x);
# must precede importing any module that provides the API specified
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)
 
# Import all of Qt
from PyQt5.Qt import *

# Create a Qt application
app = QApplication(sys.argv)
 
# Our main window will be a QListView
list = QListView()
list.setWindowTitle('Example List')
list.setMinimumSize(600, 400)
 
# Create an empty model for the list's data
model = QStandardItemModel(list)
 
# Add some textual items
foods = [
    'Cookie dough', # Must be store-bought
    'Hummus', # Must be homemade
    'Spaghetti', # Must be saucy
    'Dal makhani', # Must be spicy
    'Chocolate whipped cream' # Must be plentiful
]
 
for food in foods:
    # create an item with a caption
    item = QStandardItem(food)
 
    # add a checkbox to it
    item.setCheckable(True)
 
    # Add the item to the model
    model.appendRow(item)
 
# Apply the model to the list view
list.setModel(model)
 
# Show the window and run the app
list.show()
app.exec_()