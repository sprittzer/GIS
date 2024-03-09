import csv
import os.path

from main import get_week_number

year = 2021
name_of_the_column = ['id_field', 'x', 'y'] + list(map(lambda x: f'NDV{x}', range(1, 53)))
ready_made_points = []
path_of_all_files_ndvi = f'C:/Users/User/coding/qgis postgresql/amyrka/DF_2021/DF/'
flag = True
xs_and_ys = []
not_found_fields = set()

path = f'{year}_fields_id_and_reestrnum.csv'
with open(path, encoding='utf-8') as file:
    file_reader = csv.reader(file, delimiter=';')
    data = list(filter(lambda x: x[0].isdigit(), file_reader))
    field_ids = dict(list(map(lambda x: (x[1], int(x[0])), data)))

for filename in os.listdir(path_of_all_files_ndvi):
    with open(f'{path_of_all_files_ndvi}/{filename}') as file:
        field = filename.replace(f'{year}_DF_', '').replace('.csv', '')
        if field in field_ids:
            file_reader = csv.reader(file, delimiter=';')
        for line in file_reader:
            if line[0] == 'x' and flag:
                flag = False
                columns = []
                for day in line[2:]:
                    columns.append(f'NDV{get_week_number(year, int(day))}')
            elif line[0] != 'x':
                xy = list(map(float, line[:2]))
                if xy not in xs_and_ys:
                    xs_and_ys.append(xy)
                    new_line = [field_ids[field]] + xy + [0.0] * (len(name_of_the_column) - 3)
                    for j in range(1, 53):
                        name = f'NDV{j}'
                        if name in columns:
                            new_line[name_of_the_column.index(name)] = float(line[columns.index(name) + 2])
                    ready_made_points.append(new_line)
    print(field)
with open(f'point_{year}.csv', 'a') as f:
    writer = csv.writer(f, delimiter = ";", lineterminator="\r")
    writer.writerow(name_of_the_column)
    writer.writerows(ready_made_points)