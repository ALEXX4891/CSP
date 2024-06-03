import collections
from   ortools.linear_solver import pywraplp
import pandas as pd
import math
model = pywraplp.Solver.CreateSolver('CLP')
#      Данные для расчета
data = [['frez_1','frez','prod_1',10], ['frez_1','frez','prod_2',20],
       ['frez_2','frez','prod_1',10], ['frez_2','frez','prod_2',20],
       ['frez_3','frez','prod_1',10], ['frez_3','frez','prod_2',20],
       ['rev_1','rev','prod_1',20], ['rev_1','rev','prod_2',30],
       ['rev_2','rev','prod_1',20], ['rev_2','rev','prod_2',30],
       ['rev_3','rev','prod_1',20], ['rev_3','rev','prod_2',30],
       ['avt_1','avt','prod_1',30], ['avt_1','avt','prod_2',80],]  
init_data = pd.DataFrame(data, columns =['EQUIP_ID', 'EQUIP_TYPE', 'PROD_ID', 'OUTPUT']).reset_index()
equip_dict = init_data.EQUIP_ID.unique()
equip_type_dict = init_data.EQUIP_TYPE.unique()
prod_dict = init_data.PROD_ID.unique()
type_equip_prod_dict = init_data.groupby(['EQUIP_TYPE','PROD_ID']).size().reset_index().rename(columns={0:'COUNT'})
#      Переменные
vars_list = collections.defaultdict(list)
#      Блок ограничений
equipment_cons = collections.defaultdict(list)
equality_cons = []
first_case_cons = collections.defaultdict(list)
#      Целевая функция
objective = []
#      Суммарный объем  производства
equipment_type_production = collections.defaultdict(list)
total_production = collections.defaultdict(list)

for index, row in init_data.iterrows():
       time_var = model.NumVar(lb=0, ub=1, name=f"fraction_day_{row['EQUIP_ID']}_{row['PROD_ID']}")
       vars_list[row['EQUIP_ID'],row['PROD_ID']].append(time_var)
       equipment_cons[row['EQUIP_ID']].append(time_var)
       objective.append(time_var*row['OUTPUT'])
       if row['PROD_ID'] == 'prod_1':
              equality_cons.append(time_var*row['OUTPUT'])
              first_case_cons[row['EQUIP_TYPE']].append(time_var*row['OUTPUT'])
       else:
              equality_cons.append(-1*time_var*row['OUTPUT'])
              first_case_cons[row['EQUIP_TYPE']].append(-1*time_var*row['OUTPUT'])      

#      Блок ограничений
#2) Сумма времени, затраченного на производство деталей для каждого станка, не должна превышать времени, доступного в одном рабочем дне.
for equip_id in equip_dict:
       model.Add(sum(equipment_cons[equip_id]) <= 1)
#3) Обеспечение комплектности финального продукта. Сумма производства деталей каждого типа равны.
model.Add(sum(equality_cons) == 0)
#4) Ограничение для "равного выпуска" продукции. Сумма производства каждого типа деталей для каждого типа оборудования равны.
# for equip_type in equip_type_dict:
#        model.Add(sum(first_case_cons[equip_type]) == 0)
#      Целевая функция
model.Maximize(sum(objective))
#      Запуск расчета
model.EnableOutput()
model.Solve()
#      Выгрузка результатов
for index, row in init_data.iterrows():
       time = round(vars_list[row['EQUIP_ID'],row['PROD_ID']][0].solution_value(),2)
       total_production[row['PROD_ID']].append(math.floor(time*row['OUTPUT']))
       equipment_type_production[row['EQUIP_TYPE'],row['PROD_ID']].append(math.floor(time*row['OUTPUT']))
for index, row in type_equip_prod_dict.iterrows():
       print('Тип оборудования',row['EQUIP_TYPE'],'Деталь',row['PROD_ID'],'Выработка',sum(equipment_type_production[row['EQUIP_TYPE'],row['PROD_ID']]))
for prod_id in prod_dict:
       print('Деталь',prod_id,'Суммарный объем выпуска',sum(total_production[prod_id]))