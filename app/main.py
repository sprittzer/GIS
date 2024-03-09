
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QTableWidgetItem, QFileDialog, QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

import sys
import pyqtgraph as pg

from constants import *
import numpy as np

import psycopg2
import pandas as pd
import umap.umap_ as umap
import joblib


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # загрузка файла пользовательского интерфейса
        loadUi('ui_files/main.ui', self)

        self.setWindowTitle('ГИС')
        self.setWindowIcon(QIcon('icons/eath_black.svg'))  # Устанавливаем иконку
        self.full_sidebar.hide()
        self.stackedWidget.setCurrentIndex(4)
        self.home_btn_1.setChecked(True)
        self.graphicsView.showGrid(x=True, y=True)
        self.graphicsView.setBackground((50, 50, 50))  # Черный фон
        self.update_data_ids_fields()

        self.visualization_bnt_1.clicked.connect(self.on_visualization_toggled)
        self.visualization_bnt_2.clicked.connect(self.on_visualization_toggled)
        self.classification_btn_1.clicked.connect(self.on_classification_toggled)
        self.classification_btn_2.clicked.connect(self.on_classification_toggled)

        self.home_btn_1.clicked.connect(self.on_home_toggled)
        self.home_btn_2.clicked.connect(self.on_home_toggled)
        
        self.start_classification_btn.clicked.connect(self.classification)
        self.graph_btn.clicked.connect(self.graph)
        self.export_btn.clicked.connect(self.exportGraph)
        self.clear_graph_btn.clicked.connect(self.clear_graphic)
        self.result_catboost.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_naive_bayes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.year_box.currentIndexChanged.connect(self.update_data_ids_fields)

    def update_data_ids_fields(self):
        self.clear_graphic()
        year = self.year_box.currentText()

        conn = psycopg2.connect(
            host=HOST,
            user=USER, 
            password=PASSWORD,
            database=DATABASE
        )

        cursor = conn.cursor()
        cursor.execute(f'SELECT DISTINCT id_field FROM "{year}"."{year}_NDVI_20"')
        rows = [i[0] for i in cursor.fetchall()]
        cursor.execute(f'SELECT DISTINCT id_crop_fact FROM "{year}"."{year}_NDVI_20"')
        cultures = sorted([CULTURES[i[0]] for i in cursor.fetchall()])
        self.ids_fields.clear()
        self.ids_fields_classific.clear()
        for item in ['-'] + sorted(rows):
            self.ids_fields.addItem(str(item))
            self.ids_fields_classific.addItem(str(item))
            
        self.cultures.clear()
        for item in cultures:
            self.cultures.addItem(item)

        if self.stackedWidget.currentIndex() == 3:
            self.stackedWidget.setCurrentIndex(4)
        elif self.stackedWidget.currentIndex() == 4:
            self.stackedWidget.setCurrentIndex(3)

    def graph(self):
        self.error_label_v.setText('')
        year = self.year_box.currentText()
        id_field = self.ids_fields.currentText()
        cultures = self.cultures.currentText()
        if (id_field == '-' and cultures == '-') or (id_field != '-' and id_field != '-'):
            self.error_label_v.setText('Выберите либо номер поля, либо с/х культуру')
            return
        conn = psycopg2.connect(
            host=HOST,
            user=USER, 
            password=PASSWORD,
            database=DATABASE
        )
        cursor = conn.cursor()
        if id_field != '-':
            cursor.callproc(f'"{year}".avg_ndvi_{year[2:]}_20', ['', id_field])
        else:
            cursor.callproc(f'"{year}".avg_ndvi_{year[2:]}_20', [cultures, ''])
        # Получение результатов
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        x_data = [int(x) for x, y in results]
        y_data = [float(y) for x, y in results]
        color = set(np.random.randint(0, 255, size=3))
        pen = pg.mkPen(color=color, width=2)  # Красная линия толщиной 2 пикселя
        self.graphicsView.plot(x_data, y_data, pen=pen, symbol='o', symbolPen=None, symbolBrush=color,
                                name='NDVI', title='График NDVI', xlabel='Неделя', ylabel='NDVI')

    def exportGraph(self):
        # Запрос пути для сохранения файла
        file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить график', '', 'PNG (*.png);;JPEG (*.jpg)')
        if file_path:
            # Сохранение графика в выбранный файл
            self.graphicsView.grab().save(file_path)

#----------------- МОДУЛЬ КЛАССИФИКАЦИИ --------------------------------
    def classification(self, ):
        year = self.year_box.currentText()
        id_field = self.ids_fields_classific.currentText()
        if id_field == '-' :
            self.flash_label.setText('Выберите номер поля')
        conn = psycopg2.connect(
            host=HOST,
            user=USER, 
            password=PASSWORD,
            database=DATABASE
        )
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{year}_NDVI_20' AND column_name LIKE 'NDV%'
        ''')

        # Получение списка столбцов NDVI
        ndvi_columns = [f'"{row[0]}"' for row in cursor.fetchall()]

        # Формирование SQL-запроса с динамически определенными столбцами NDVI
        columns_str = ", ".join(ndvi_columns)
        query = f'''
            SELECT {columns_str}
            FROM "{year}"."{year}_NDVI_20" WHERE id_field = {id_field}
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        self.flash_label.setText('Загрузка данных из базы данных прошла успешно')
        ndvi_columns = list(map(lambda x: x.replace('"', ''), ndvi_columns))
        df = pd.DataFrame(rows, columns=ndvi_columns)
        df = df.loc[:, (df != 0).any(axis=0)]

        for col in df.columns.tolist():
            df[col] = np.where(df[col] > 1, np.nan, df[col])

        name_cols = df.columns[df.isnull().any()].tolist()
        df = df.fillna(df.mean())
        umap_model_test = umap.UMAP(n_neighbors=200, min_dist=0.1, n_components=2, metric='euclidean')
        # Преобразование данных с использованием UMAP
        umap_result_test = umap_model_test.fit_transform(df)
        # Создание нового DataFrame с редуцированными признаками
        umap_df_test = pd.DataFrame(data=umap_result_test)

        X_test = umap_df_test

        catboostclassifier = joblib.load('static/models/catboostclassifier.pkl')
        predicted_cultures = catboostclassifier.predict(X_test)
        predicted_cultures_flat = np.array(predicted_cultures).flatten()
        predictions_df = pd.DataFrame({'Predicted_Culture': predicted_cultures_flat})
        cultures_counts = predictions_df['Predicted_Culture'].value_counts(normalize=True) * 100
        formatted_strings = [[key, f'{value:.2f}%'] for key, value in cultures_counts.items()]
        self.result_catboost.setRowCount(len(formatted_strings))
        self.result_catboost.setColumnCount(len(formatted_strings[0]))
        self.result_catboost.setHorizontalHeaderLabels(['Культура', 'Процент произрастания'])
        # Заполнение таблицы данными из списка списков
        for i, row in enumerate(formatted_strings):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.result_catboost.setItem(i, j, item)



        X_test = umap_df_test[[0, 1]]
        X_test.columns = [f'feature_{i}' for i in range(X_test.shape[1])]

        best_naive_bayes_classifier = joblib.load('static/models/naive_bayes_classifier.pkl')
        predicted_cultures = best_naive_bayes_classifier.predict(X_test)
        predictions_df = pd.DataFrame({'Predicted_Culture': predicted_cultures})
        cultures_counts_naive_bayes = predictions_df['Predicted_Culture'].value_counts(normalize=True) * 100
        # Преобразование к типу строк и форматирование каждой строки
        formatted_strings = [[key, f'{value:.2f}%'] for key, value in cultures_counts_naive_bayes.items()]
        self.result_naive_bayes.setRowCount(len(formatted_strings))
        self.result_naive_bayes.setColumnCount(len(formatted_strings[0]))
        self.result_naive_bayes.setHorizontalHeaderLabels(['Культура', 'Процент произрастания'])
        # Заполнение таблицы данными из списка списков
        for i, row in enumerate(formatted_strings):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.result_naive_bayes.setItem(i, j, item)


    def clear_graphic(self, ):
        self.graphicsView.clear()

    def on_visualization_toggled(self, ):
        self.stackedWidget.setCurrentIndex(1)

    def on_classification_toggled(self, ):
        self.stackedWidget.setCurrentIndex(0)

    def on_settings_toggled(self, ):
        self.stackedWidget.setCurrentIndex(2)
        self.error_block.hide()
        self.load_data_from_sqlite()

    def on_home_toggled(self, ):
        year = self.year_box.currentText()
        if year == '2021':
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.stackedWidget.setCurrentIndex(4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open(f"static/styles/style.css", 'r') as file:
        app.setStyleSheet(file.read())
    window = MainWindow()
    window.show()

    app.exec()