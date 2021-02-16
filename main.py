from execution import read_from_console, read_from_file, random_matrix

print('Welcome!')

while 1:
        print ('\nДоступные команды:\n1. Вычисления из файла\n2. Ввод с консоли\n' +
               '3. Сгенерировать случайную матрицу\n4. Выход\nВведите номер команды')
        comand = input()
        if (comand == '1'):
            read_from_file()
        elif (comand == '2'):
            read_from_console()
        elif (comand == '3'):
            random_matrix()
        elif (comand == '4'):
            print('*Программа завершена*')
            break
        else:
            print('Такой команды нет')
    
