import numpy as np
import os
from ezodf import newdoc, Sheet


def part_of_signal_to_file(signal, output_folder,
                           output_name):
    """
    Функция записи участка данных сигнала в текстовый dat файл
    :param signal: одномерный массив numpy
    :param output_folder: папка сохранения результата
    :param output_name: имя файла (без расширения)
    :return: None

    """
    export_path = os.path.join(output_folder, output_name + '.dat')
    np.savetxt(fname=export_path, X=signal, fmt='%i')


def correlation_to_file(devices, correlation_matrix, output_folder,
                        output_name):
    """
    Функция для записи корреляционной матрицы в файл
    :param devices: список приборов
    :param correlation_matrix: корреляционная матрица
    :param output_folder: папка, куда будет сохранен файл
    :param output_name: имя файла (без расширения)
    :return: None
    """
    # формирование заголовка столбцов
    header = 'NULL\t' + '\t'.join(devices) + '\n'
    # сборка строк для записив файл
    write_lines = list()
    write_lines.append(header)
    for i in range(correlation_matrix.shape[0]):
        t = list()
        t.append(devices[i])
        for j in range(correlation_matrix.shape[1]):
            t.append(str(correlation_matrix[i, j]))
        s = '\t'.join(t) + '\n'
        write_lines.append(s)
    # запись данных в файл
    export_path = os.path.join(output_folder, output_name + '.dat')
    f = open(export_path, 'w')
    for line in write_lines:
        f.write(line)
    f.close()


def spectrum_to_file(frequency, amplitude, type, output_folder, output_name):
    """
    Функция для экспорта данных сглаженного и НЕсглаженного спектров в виде
    файла
    :param frequency: массив с набором частот
    :param amplitude: массив с набором амплитуд
    :param type: тип спектра (сглаженный или несглаженный)
    :param output_folder: папка экспорта
    :param output_name: имя файла (БЕЗ РАСШИЕРЕНИЯ!)
    :return: None
    """
    if type == 'smooth':
        extension = '.ssc'
    elif type == 'no_smooth':
        extension = '.sc'
    else:
        extension = '.dat'
    export_path = os.path.join(output_folder, output_name + extension)

    temp_array = np.empty(shape=(frequency.shape[0], 2), dtype=float)
    temp_array[:, 0] = frequency
    temp_array[:, 1] = amplitude
    np.savetxt(fname=export_path, X=temp_array, fmt='%f', delimiter='\t')


def energy_to_file(components, points, intervals, data_matrix, output_folder,
                   output_name):
    """
    Функция для экспорта данных энергии в виде ods-файла
    :param components: список компонент
    :param points: данные по точкам (имя, координаты)
    :param intervals: названия временных интервалов
    :param data_matrix: матрица со значениями энергии
    :param output_folder: папка экспорта
    :param output_name: имя выходного файла (без расширения!)
    :return: None
    """
    export_path = os.path.join(output_folder, output_name + '.ods')

    doc = newdoc(doctype='ods',filename=export_path)

    for component_index, component_name in enumerate(components):
        # Создание нового листа
        current_sheet = Sheet(name='Component_{}'.format(component_name))
        # установка количества строк и столбцов
        current_sheet.append_rows(len(points)+1)
        current_sheet.append_columns(len(intervals)+3)
        # заполнение заголовков столбцов
        current_sheet[0, 0].set_value('Point_name')
        current_sheet[0, 1].set_value('x')
        current_sheet[0, 2].set_value('y')
        for interval_index, interval_name in enumerate(intervals):
            current_sheet[0,3+interval_index].set_value(interval_name)

        # заполнение номеров точек и координат
        for data_index, data_value in enumerate(points):
            point_name,x,y = data_value
            current_sheet[1 + data_index, 0].set_value(point_name)
            current_sheet[1 + data_index, 1].set_value(x)
            current_sheet[1 + data_index, 2].set_value(y)

        # заполнение значений энергии
        for row_i in range(len(points)):
            for col_j in range(len(intervals)):
                current_sheet[1 + row_i, 3 + col_j].set_value(data_matrix[component_index,row_i,col_j])

        # добавление листа в книгу
        doc.sheets.append(current_sheet)
    doc.save()
