import psycopg2
import csv
import sys
import numpy as np
import os
from datetime import datetime, timedelta




def get_week_number(year, day_of_year):
    january_1 = datetime(year, 1, 1)
    first_thursday = january_1 + timedelta(days=(3 - january_1.weekday() + 7) % 7)
    target_date = january_1 + timedelta(days=day_of_year - 1)
    days_diff = (target_date - first_thursday).days
    week_number = (days_diff // 7) + 1
    return week_number


# Ключевые данные, которые вводит пользователь
year = 2021
dbname = 'geostatic_db'
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'
path_to_folder = f'C:/Users/User/coding/qgis postgresql/amyrka/DF_{year}/DF/' # путь к папке с файлами с вегетационными показателями по полям
# название таблицы для записи данных
table_to_insert = f'{year}_NDVI_20'

# --------------------------------------------------------------------------------
csv_file_name = f'{dbname}_{year}_reestrnums_and_ids.csv'
str_name_of_cols = ', '.join([f'"NDV{i}"' for i in range(1, 53)])
conn = psycopg2.connect(
    dbname=dbname,
    user=user,  
    password=password,  
    host=host,
    port=port
)
cursor = conn.cursor()
table_name = f'{year}_list_of_fields'
query = f'SELECT id, reestr_number FROM "{year}"."{table_name}" WHERE reestr_number IS NOT NULL'
cursor.execute(query)
results = cursor.fetchall()
if results:
    with open(csv_file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerows(results)
    print(f"Данные о названиях полей успешно записаны в файл {csv_file_name}")
else:
    print("Нет данных о названиях полей для записи в CSV-файл")
    sys.close()
conn.close()
# --------------------------------------------------------------------------------
with open(csv_file_name, encoding='utf-8') as file:
  file_reader = csv.reader(file, delimiter=';')
  data = np.array(list(filter(lambda x: x[0].isdigit() and x[1] != '', file_reader)))
  field_ids = dict(list(map(lambda x: (x[1], int(x[0])), data)))
# --------------------------------------------------------------------------------
conn = psycopg2.connect(
    dbname=dbname,
    user=user,  
    password=password,  
    host=host,
    port=port
)
cursor = conn.cursor()

for field in field_ids:
   print(field)
   # заметим, что сейчас код ищет файлы с названием вида ГОД_DF_НОМЕРПОЛЯ.csv
   file_name = path_to_folder + f'/{year}_DF_{field}.csv'
   if not os.path.exists(file_name):
       continue
   check_query = f'SELECT id FROM "{year}"."{table_to_insert}" WHERE id_field = %s'
   cursor.execute(check_query, (field_ids[field],))
   if cursor.fetchone() != None:
      print(field, ' УЖЕ СУЩЕСТВУЕТ')
      continue
   with open(file_name) as file:
       file_reader = csv.reader(file, delimiter=';')
       for line in file_reader:
          if line[0] == 'x':
              columns = []
              for day in line[2:]:
                columns.append(get_week_number(year, int(day)))
          else:
            xy = list(map(float, line[:2]))
            res_line = [field_ids[field]] + xy + [0.0] * 52
            for col in columns:
               res_line[col + 2] = float(line[columns.index(col) + 2])
            insert_query = f'INSERT INTO "{year}"."{table_to_insert}" ("id_field", "X", "Y", {str_name_of_cols}) VALUES ({", ".join(["%s"] * 55)})'
            try:
                cursor.execute(insert_query, res_line)
                conn.commit()            
            except psycopg2.errors.UniqueViolation as e:
               conn.rollback()
               if "duplicate key value violates unique" in str(e):
                  print('Такие данные уже существуют, пропускаем...')
               else:
                  print('Произошла другая ошибка: ', e)
                  raise
conn.close()