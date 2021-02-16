import random

def read_from_console():
    try:
        
        n = int(input('Введите размерность матрицы от 2 до 20: '))
        if (n > 1 and n <= 20):
                line = []
                values = []
                i = 0
                while i < n:
                    print (str(i+1) + ' из ' + str(n));
                    line = input('Вводите данные в формате: ai1 ai2 ... ain | bi\n')
                    line = line.split()
                    
                    if (len(line) > 1):
                        if (line[-2] == '|' and len(line) == n + 2):
                            line.pop(-2)
                            for j in range(len(line)):
                                line[j] = float(line[j])
                            values.append(line)
                            i = i + 1;
                        else:
                            print('Неправильный ввод данных, попробуйте ещё раз')
                    else:
                        print('Неправильный ввод данных, попробуйте ещё раз')
                        
                e = float(input('Задайте точность вычисления: '))
                print_start_values(n, values, e)
                matrix = Matrix(n, values, e)
                matrix.execute()
                del matrix
                
    except ValueError:
        print('Неправильный ввод данных')

def read_from_file():
    
        try:
            warning()
            path = input('Введите путь к файлу: ')
            f = open(path, 'r')
            start_values = []
            line = []
            values = []
            for i in f:
                start_values.append(i.split())
            n = int(start_values[0][0])
            e = float(start_values[-1][-1])
            if (len(start_values) - 2 == n):
                for i in start_values[1:-1]:
                    line = i
                    if (line[-2] == '|' and len(line) == n + 2):
                        line.pop(-2)
                        for i in range(len(line)):
                            line[i] = float(line[i])
                        values.append(line)
                    else:
                        print('Неправильный ввод данных, исправьте содержимое файла и попробуйте снова')
                        return
            else:
                print('Недостаточное количество строк, исправьте содержимое файла и попробуйте снова')
                return
            print_start_values(n, values, e)

            matrix = Matrix(n, values, e)
            matrix.execute()
            del matrix
                             
        except FileNotFoundError:
            print ('Файла не существует, попробуйте заново')
            read_from_file()
   


def random_matrix():
    n = random.randint(2, 20)
    values = []
    line = []
    for i in range(n):
        for j in range(n+1):
            line.append(round(random.random() * random.randrange(-1000, 1000, 10), 3))
        values.append(line)
        line = []
    e = round(random.random(), 3)
    print_start_values(n, values, e)
    matrix = Matrix(n, values, e)
    matrix.execute()
    del matrix

def print_start_values(n, values, e):
    print()
    print('Размерность матрицы: ' + str(n))
    print('A:')
    for line in values:
        print(' '.join(str(line[:-1])))
    print('B:')
    for line in values:
        print(line[-1])
    print('Погрешность: ' + str(e) + '\n')
        

def warning():
    print('Правила офрмления файла:\n1. В первой строке файла указывается размерность '+
          'матрицы в виде одного целого числа от 2 до 20\n2. Далее описывается сама матрица в формате:\n' +
          'a11 a12 ... a1n | b1\na21 a22 ... a2n | b2\n.\n.\n.\nan1 an2 ... ann | bn\n3. После чего указывается погрешность\n\n'+
          'Обращайте внимание на пробелы!\n')
    print('Пример оформления файла:')
    print('-------------------------')
    print('4\n'+
          '20 2 3 7 | 5\n'+
          '1 12 -2 -5 | 4\n'+
          '5 -3 13 0 | -3\n'+
          '0 0 -1 15 | 7\n'+
          '0.1')
    print('-------------------------')
        
class Matrix:
    n = 0
    values = []
    e = 0

    def __init__(self, n, values, e):
        self.n = n
        self.values = values
        self.e = e

    def diagonal_check(self):
        check = []
        s = 0
        diag_elem = 0
        strict = 0
        
        for i in range(self.n):
            diag_elem = abs(self.values[i][i])
            for elem in self.values[i]:
                s += abs(elem)
            s -= diag_elem + abs(self.values[i][-1])
            if (diag_elem >= s):
                if (diag_elem > s):
                    strict += 1
                check.append(1)
            else:
                check.append(0)
            s = 0
        if (strict > 0):    
            res = 1
            for i in check:
                res *= i
        else:
            res = 0
        return res

    def calculate(self):
        iteration = 1;
        last_results = []
        e_arr = []
        arr = []
        s = 0
        e_local = self.e+1
        for i in range(self.n):
            last_results.append(0)
        while (e_local > self.e):
            results = []
            e_arr = []

            for i in range(self.n):
                s = 0
                for j in range(self.n):
                    s += self.values[i][j]*last_results[j]
                s -= self.values[i][i] * last_results[i]
                results.append((self.values[i][-1] - s)/self.values[i][i])
            
            for i in range(self.n):
                e_arr.append(abs(results[i] - last_results[i]))
            last_results = results
            e_local = max(e_arr)
            if (e_local <= self.e):
                self.print_end_values(results, e_arr, e_local, iteration)
                
            else:
                iteration += 1;
            

    def change_matrix(self):
            columns = []
            new_arr = []
            check = 0
            strict = 0
            for line in self.values:
                abs_line = []
                s = 0
                for elem in line:
                    abs_line.append(abs(elem))
                for elem in abs_line[:-1]:
                    s += elem
                s -= max(abs_line[:-1])
                if (max(abs_line[:-1]) < s):
                    print('Невозможно совершить преобразования')
                    return 0
                else:
                    if (max(abs_line[:-1]) > s):
                        strict += 1
                    columns.append(abs_line.index(max(abs_line[:-1])))

            for i in range(len(columns) - 1):
                for j in range(i+1, len(columns)):
                    if (columns[i] == columns[j]):
                        check = 1
            if (check == 0 and strict != 0):
                for i in range(len(columns)):
                    new_arr.append(self.values[columns.index(i)])
            else:
                print('Невозможно совершить преобразования')
                return 0
          
            self.values = new_arr
            return 1


    
    def execute(self):
        if (self.diagonal_check()):
           self.calculate()
        else:
            answer = ''
            while (answer != 'yes' and answer != 'no'):
                answer = input('Не выполнено условие сходимости, сделать перстановку столбцов/строк до её достижения (yes/no)? ')    
                if (answer == 'yes'):
                    if(self.change_matrix()):
                        self.calculate()
                elif (answer == 'no'):
                    print('Поменяйтяте значения элементов матрицы и повторите попытку')
                    

    def print_end_values(self, results, e_arr, e_local, iteration):
        print('Столбец неизвестных: ')
        for j in range(len(results)):
            print('x' + str(j+1) + ': ' + str(results[j]))
        print('Количество итераций, за которое было найдено решение: ')
        print(iteration)
        print('Столбец погрешностей: ')
        for j in range(len(e_arr)):
            print('e' + str(j+1) + ': ' + str(e_arr[j]))
        print('Погрешность: ')
        print('e = ' + str(e_local))
              
        

