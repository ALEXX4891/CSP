# a = 5 # int
# b = 5.6 # float
# c = 'ALEXX' # str
# d = True # bool
# # print (a)
# # print (b)
# # print (c)
# # print (d)
# # print ('Text')
# print (len(c))

# # Экранирование
# # print ('hi плохой человек')


# Данный код на Python реализует алгоритм оптимизации задачи раскроя (cutting stock problem) с использованием библиотеки OR-Tools от Google. Вот краткое описание того, что делает каждая часть кода:

# 1. Импорт необходимых библиотек: ortools.linear_solver для работы с линейным программированием, pandas для работы с данными в виде таблицы, и numpy для работы с массивами.

# 2. Определение входных данных, таких как фиксированная ширина рулона (W) и информация о ширине рулона по заказам и их количестве (data).

# 3. Создание DataFrame из входных данных с использованием библиотеки Pandas.

# 4. Определение функции cutting_stock_relaxed, которая выполняет расслабленную задачу RMP (Relaxed Master Problem) для задачи раскроя. В этой функции используется библиотека OR-Tools для создания модели линейного программирования или целочисленного программирования, в зависимости от параметра is_relaxed.

# 5. Определение функции pricing_problem, которая решает проблему ценообразования для добавления в модель. В этой функции также используется библиотека OR-Tools для создания модели целочисленного программирования.

# 6. Определение функции cutting_stock_col_gen, которая реализует алгоритм генерации столбцов для задачи раскроя в случае неявного задания схем раскроя.

# Общий подход в этом коде заключается в использовании линейного программирования и целочисленного программирования для оптимизации задачи раскроя, а также в использовании алгоритма генерации столбцов для нахождения оптимальной схемы раскроя.

# Импортируем необходимые библиотеки




from ortools.linear_solver import pywraplp
import pandas as pd
import numpy as np
import random
import pickle
import json
import datetime

# import time
# json = json.dumps('result')
# print(json)


start = datetime.datetime.now()
# print('Время старта: ' + str(start))

# Входные данные
# W = 5600  # Фиксированная ширина рулона, результат единицы производства
# W = 1600  # Фиксированная ширина рулона, результат единицы производства
# W = 1150  # Фиксированная ширина рулона, результат единицы производства


# Ширина рулона по заказам и их кол-во
# data = [(1380, 22),
#         (1520, 25),
#         (1560, 12),
#         (1710, 14),
#         (1820, 18),
#         (1880, 18),
#         (1930, 20),
#         (2000, 10),
#         (2050, 12),
#         (2100, 14),
#         (2140, 16),
#         (2150, 18),
#         (2200, 20)]

# data = [(600, 104),
#         (450, 156),
#         (340, 52)]
# data = [ # ширина полоски / количество полосок
#   (140, 143),
#   (150, 143),
#   (160, 286),
#   (170, 286),
#   (180, 286)
# ]



#откроем нашу книгу и проверим содержимое
book = open("order.txt", 'r')
text = book.readlines()
# print('text: ', text)
data = []
W = 0


for i in range(len(text)):
  if i == 0:
    W = int(text[i])
  if i > 0:
    str = text[i].split(' ')
    str[1] = int(str[1])
    str[0] = int(str[0])
    data.append(tuple(str))

# print('data: ', data)
# print('W: ', W)

indexShems = []
quontityShems = []
shems = []
allShems = []
usingShems = []
result = []

data_df = pd.DataFrame(data, columns=['w', 'q'])
w = np.array(data_df['w'])  # Ширина рулона по каждому из заказов
q = np.array(data_df['q'])  # Кол-во рулонов по заказам
# print(data_df)
# print(w)
# print(q)

indexCol = []

# Расслабленная задача RMP
def cutting_stock_relaxed(A, q, is_relaxed=True):
    """
      A - текущая матрица схем раскроя
      q - кол-во рулонов по заказам
      is_relaxed - параметр переключения между LP и MIP задачами
    """
    m, n = A.shape
    # print('m:', m, 'n:', n, 'q:', w)
    # print('A:', A)


    if is_relaxed:
      model = pywraplp.Solver.CreateSolver('GLOP')
      # print('Relaxed Master Problem:', model)
    else:
      model = pywraplp.Solver.CreateSolver('SCIP')  # На случай RMP MIP
      # print('Master Problem:', model)

    # Инициализация переменных
    x_vars = []
    for i in range(n):
        if is_relaxed:
          x_vars.append(model.NumVar(0, model.infinity(), name=f"x_{i}"))
        else:
          x_vars.append(model.IntVar(0, 100, name=f"x_{i}"))

    # print('x_vars:', x_vars)

    # Добавление ограничений в модель
    constraints = []
    for i in range(m):
        constr = model.Add(A[i] @ x_vars >= q[i])
        constraints.append(constr)

    # Целевая функция
    # print('x_vars:', x_vars)
    model.Minimize(sum(x_vars))
    model_str = model.ExportModelAsLpFormat(False)

    status = model.Solve()
    # print('cutting_stock_relaxed Значение целевой функции = %f' % model.Objective().Value())

    solution = {f"x_{i}": var.solution_value()
                for i, var in enumerate(x_vars)
               if var.solution_value() }

    # print('--solution:', solution)
    # print('--solution.keys():', solution.keys())

    shems = list(solution.keys()) # все ключи схем
    global quontityShems
    quontityShems = []
    quontityShems = list(solution.values()) # все количества схем
    quontityShems = list(map(int, quontityShems)) # преобразование в int 
    # print('quontityShems:', quontityShems)
    global indexShems
    indexShems = []
    for i in range(len(shems)):
      indexShems.append(shems[i][2:])
      # print('shems[i]:', shems[i])
    # print('shems:', shems)
    # print('----x_vars:', x_vars)
    # usingShems = []
    # for i in range(len(indexShems)):
    #    usingShems.append(C)
       

    # print('--solution--:', solution[1])
    solution_vect = np.array([var.solution_value() for var in x_vars])
    if is_relaxed:
      dual_solution_vect = np.array([constr.dual_value() for constr in constraints])
    else: 
      dual_solution_vect = []

    return solution_vect, dual_solution_vect, model_str


# Оптимизация схемы раскроя для добавления в модель
def pricing_problem(u, w, W):
    """
      u - вектор значений двойственных переменных
      w - ширина рулонов в зависимости от заказа
      W - ширина производимого рулона для раскроя
    """
    m = len(w)

    model = pywraplp.Solver.CreateSolver('SCIP')

    # Инициализация переменных
    z_vars = []

    for i in range(m):
        z_vars.append(model.IntVar(0, model.infinity(), name=f"z_{i}"))

    # Добавление ограничений в модель
    model.Add(w @ z_vars <= W)

    # Целевая функция
    model.Minimize(1 - u @ z_vars)

    status = model.Solve()

    # print('pricing_problem Значение целевой функции = %f' % model.Objective().Value())

    solution = {f"z_{i}": var.solution_value()
                for i, var in enumerate(z_vars)
                if var.solution_value() }
    # print('z_vars:', z_vars)
    # print(solution)
    solution_vect = np.array([var.solution_value() for var in z_vars])
    return solution_vect, model.Objective().Value()

# Алгоритм генерации столбцов для задачи раскроя в случае неявного задания схем раскроя
def cutting_stock_col_gen(q, w, W):
    # Инициализация решения
    m = q.shape[0]  # кол-во ограничений
    # Инициализируем начальный набор схем: одна схема - один заказ
    A = np.eye(m, dtype=int)
    # print(A)

    iter_count = 0
    while True:
        iter_count += 1
        if iter_count >= 50: # остановка алгоритма, что бы программа не уходила в бесконечный расчет
            # print('Итерация превышена!', iter_count) 
            break
        # print('Итерация', iter_count)

        sol, dual_sol, m_str = cutting_stock_relaxed(A, q)
        new_pattern, obj = pricing_problem(dual_sol, w, W)
        if obj >= 0:
            break
        new_pattern = new_pattern.astype(int)

        new_pattern_matr = new_pattern.reshape((-1, 1))


        A = np.hstack((A, new_pattern_matr))

    finish = datetime.datetime.now()
    # print('Время окончания: ' + str(finish))
    # print('Время работы скрипта: ' + str(finish - start))
    # print('---------------------------------------------------------------------')  

    # print('q:', q)  
    # print('w:', w)  
    # print('W:', W)  
    # print('m:', m)  
    # print('A:', A)
    global allShems
    allShems = []
    # C = []
    # B = A[:, 1] # формируем массив из вторых элементов каждого массива, в массиве А    
    # C = A[:, -1:] # оставляем только один элемент в последней колонке каждого массива, в массиве А
    for i in range(len(A[0])):
        shema = A[:, i]
        allShems.append(shema)
    # print('---shema:', shema)
    # print('allShems:', allShems)
    # print(len(A))






    return A

A_schemes = cutting_stock_col_gen(q, w, W)
res_vec, _, _ = cutting_stock_relaxed(A_schemes, q, is_relaxed=False)
# res_vec, val1, val2 = cutting_stock_relaxed(A_schemes, q, is_relaxed=False)

# print(res_vec)
# print(val1)
# print(val2)
# print('indexShems:', indexShems)

# for i in range(len(allShems)):
    # print('shema:', allShems[i])


# usingShems = []

for i in indexShems:
    # print('i:', i)
    # print('allShems[i]:', allShems[i])


    usingShems.append(allShems[int(i)])
# 
# usingShems.append(allShems[8])
# usingShems.append(allShems[9])

# for i in range(len(usingShems)):

# print('Ширина листа: ', W)
# print('Заказ: ширина - количество', data)
# print('Зданные ширины: ', w)


# print('usingShems: ', usingShems)
# print('quontityShems:', quontityShems)

pattern = []
resShems = []
# sortedShems1 = []

for i in range(len(usingShems)):
   pattern = []
   for j in range(len(usingShems[i])):
       if usingShems[i][j]:
            # print('usingShems[i][j]: ', usingShems[i][j])
            # print('w.index[j]: ', w.index[j])
            # print('w[j]: ', w[j])
            # print('j: ', j)

            for x in range(usingShems[i][j]):
                pattern.append(w[j])
  #  print ('shem1: ', shem1)
   resShems.append(pattern)
            # shem1.append(w[j])
        #  for x in range(w.index[j]):
            # print(w.index[j])
          #  shem1.append(usingShems[i][j])
        #  global shems1
        #  shems1.append(usingShems[i][j]) * w[j]
        #  print('shems1: ', shems1)

        #  print('usingShems[i][j]: ', usingShems[i][j])
      #  print('usingShems[i][j]: ', usingShems[i][j])

result.append(quontityShems)
# print('quontityShems: ', quontityShems)
result.append(resShems)
# print('resShems: ', resShems)
# print('result: ', result)
# result.append(data)

# result.append(W)


# json = json.dumps(result)

# класс нужен для того что бы можно было сериализовать в json список списков
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
# Your codes ....

# y = [1, 2, 3]
# z = [[1, 2, 3], [1, 2, 3]]
# x = []
# x.append(y)
# x.append(z)


json = json.dumps(result, cls=NpEncoder)
print(json)



# sortedShems1 = sorted(shems1, key=lambda x: x[0]) # сортировка списка списков по вервому элементу
# res = []

# print('res: ', res)
# print('quontityShems[0]: ', quontityShems[0])

# print('sortedShems1: ', sortedShems1)
# print('allShems: ', allShems[8])


# print('-----------------')
# print(A_schemes)
# print('-----------------')

# print('---------------------------------------------------------------------')  


# #начнём с первой главы
# #создадим файл с книгой в текущей папке
# my_book = open("my_book.txt", 'w')
# my_book.write('Количество листов:\n')

# for item in quontityShems:
#     my_book.write("%s\n" % item)
# my_book.write('-------------------------------------------\n')
# my_book.write('матрица раскроя:\n')
# for item in resShems:
#     my_book.write("%s\n" % item)

# # my_book.write('Chapter 1: Hello, Python!\n')
# # pickle.dump(quontityShems, my_book)
# # my_book.write('quontityShems:'.join(quontityShems).join('\n'))
# # my_book.write('To be continued...\n')
# #закроем поток записи
# my_book.close()


# #откроем нашу книгу и проверим содержимое
# book = open("my_book.txt", 'r')
# text = book.read()
# print(text)
