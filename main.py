import sys
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from db_connect import db, cursor

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('cms.ui', self)
    self.id = 0

    self.tb_car.setColumnWidth(0, 50)
    self.tb_car.setColumnWidth(1, 150)
    self.tb_car.setColumnWidth(2, 150)
    self.tb_car.setColumnWidth(3, 100)
    self.tb_car.setColumnWidth(4, 180)

    self.show_all_cars()
    self.btn_add.clicked.connect(self.insert_car)
    self.btn_search.clicked.connect(self.search_car)

    self.btn_clear.clicked.connect(self.search_clear)
    self.tb_.cellClicked.connect(self.search_row)
    self.tb_car.cellClicked.connect(self.search_row)

    self.btn_clear.clicked.connect(self.clear)
    self.btn_update.clicked.connect(self.update_car)
    self.btn_delete.clicked.connect(self.delete_car)
    self.tb_car.cellClicked.connect(self.selected_row)

  def say_hi(self):
    QMessageBox.information(self, 'Information', 'Hello World!')

    def delete_car(self):
      price = int(self.txt_price.text())
      sql = 'update car set price = ? where id = ?'
      values = (price,self.id)

      row = cursor.execute(sql, values)
      db.commit()

      if row.rowcount>0:
        QMessageBox.information(self,'information','Updete car succesful!')
      else:
        pass

    def detete_car(self):
      sql = 'dele from car where id = ?'
      values = (self)
      row = cursor.execute(sql, values)
      db.commit()

      if row.rowcount>0:
        QMessageBox.information(self,'information','Updete car succesful!')


  def selected_row(self):
      row = self.tb_car.currentRow()
      self.id = self.tb_car.item(row,0).text()
      self.txt_brand.setText(self.tb_car.item(row, 1).text())
      self.txt_model.setText(self.tb_car.item(row, 2).text())
      self.txt_year.setText(self.tb_car.item(row, 3).text())
      self.txt_price.setText(self.tb_car.item(row, 4).text())

      self.btn_update.setEnablen(True)
      self.btn_delete.setEnablen(True)
      self.btn_add.setEnablen(False)

      self.txt_update.setEnablen(False)
      self.btn_add.setEnablen(False)
      self.btn_add.setEnablen(False)

  def search_(self):
    brand = self.txt_search.text()
    #print(brand)
    sql = 'select * from car where brand like ?'
    values = (f'%{brand}%',)

    cars = cursor.execute(sql,values).fetchall()
    self.show_cars(cars)

  def update_car(self):
    price = int(self.txt_price.text())
    sql = 'update car set price = ? where id = ?'
    values = (price, self.id)

    row = cursor.execute(sql, values)
    db.commit()

    if row.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Update car successful!')
      self.show_all_cars()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to update car!')
    self.clear()

  def delete_car(self):
    sql = 'delete from car where id = ?'
    values = (self.id, )

    row = cursor.execute(sql, values)
    db.commit()

    if row.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Delete car successful!')
      self.show_all_cars()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to delete car!')
    self.clear()

  def selected_row(self):
    row = self.tb_car.currentRow()
    self.id = self.tb_car.item(row, 0).text()
    self.txt_brand.setText(self.tb_car.item(row, 1).text())
    self.txt_model.setText(self.tb_car.item(row, 2).text())
    self.txt_year.setText(self.tb_car.item(row, 3).text())
    self.txt_price.setText(self.tb_car.item(row, 4).text())

    self.btn_update.setEnabled(True)
    self.btn_delete.setEnabled(True)
    self.btn_add.setEnabled(False)

    self.txt_brand.setEnabled(False)
    self.txt_model.setEnabled(False)
    self.txt_year.setEnabled(False)

  def search_car(self):
    brand = self.txt_search.text()
    # print(brand)
    sql = 'select * from car where brand like ?'
    values = (f'%{brand}%', )

    cars = cursor.execute(sql, values).fetchall()
    self.show_cars(cars)

    self.txt_search.setText('')

  def show_all_cars(self):
    sql = 'select * from car'
    cars = cursor.execute(sql).fetchall()


    n = len(cars)
    self.tb_car.setRowCount(n)
    row = 0
    for car in cars: #car => (1, 'Toyota','Yaris',2025 )
      self.tb_car.setItem(row, 0, QTableWidgetItem(str(car[0])))
      self.tb_car.setItem(row, 1, QTableWidgetItem(car[1]))
      self.tb_car.setItem(row, 2, QTableWidgetItem(car[2]))
      self.tb_car.setItem(row, 3, QTableWidgetItem(str(car[3])))
      self.tb_car.setItem(row, 4, QTableWidgetItem(str(car[4])))

      row += 1
    self.show_cars(cars)

  def show_cars(self, cars):
      n = len(cars)
      self.tb_car.setRowCount(n)
      row = 0
      for car in cars:  #car[0] => (1, 'Toyota', 'Yaris Cross', 2025, 80000)
        self.tb_car.setItem(row, 0, QTableWidgetItem(str(car[0])))
        self.tb_car.setItem(row, 1, QTableWidgetItem(car[1]))
        self.tb_car.setItem(row, 2, QTableWidgetItem(car[2]))
        self.tb_car.setItem(row, 3, QTableWidgetItem(str(car[3])))
        self.tb_car.setItem(row, 4, QTableWidgetItem(str(car[4])))

        row += 1


  def insert_car(self):
    brand = self.txt_brand.text()
    model = self.txt_model.text()
    year = self.txt_year.text()
    price = self.txt_price.text()

    sql = 'insert into car(brand, model, year, price) values(?, ?, ?, ?)'
    values = (brand, model, year, price)

    rs = cursor.execute(sql, values)
    db.commit()
    if rs.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Insert car successful!')
      self.show_all_cars()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to insert car!')

    self.show_all_cars
    self.clear()

  def clear(self):
    self.txt_brand.setText('')
    self.txt_model.setText('')
    self.txt_year.setText('')
    self.txt_price.setText('')

    self.txt_brand.setEnabled(True)
    self.txt_model.setEnabled(True)
    self.txt_year.setEnabled(True)

    self.tb_car.clearSelection()

    self.btn_add.setEnabled(True)
    self.btn_update.setEnabled(False)
    self.btn_delete.setEnabled(False)

    self.show_all_cars()


  
    self.txt_brand.setEnablend('True')
    self.txt_model.setEnablend('True')
    self.txt_year.setEnablend('True')
    self.txt_price.setEnablend('True')

    self.tb_car.clearselection()

    self.btn_brand.setEnablend('True')
    self.btn_model.setEnablend('True')
    self.btn_year.setEnablend('Fales')
    self.btn_price.setEnablend('Fales')

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()