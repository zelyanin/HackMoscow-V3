import json
import requests

#Алгоритм распределения заказов

#warehouse - массив, в котором находятся рейтинги существующих складов
#warehouse_id - массив id складов
#couriers - массив, в котором находятся рейтинги курьеров (двойной массив)
#couriers_id - массив id курьеров
def choice_of_courier(warehouse, warehouse_id, couriers, couriers_id):
    array_id = {} #Списка id-шников, ключ - id курьеров, значение - id склада
    value_max = -1 #Максимальное число в матрице
    n = len(warehouse)
    array_of_coefficients = [] #Матрица после перемножения (от 0 до 100 - значения)
    try:
        for i in range(len(couriers)):
            if len(couriers[i]) == n:
                array = [] #Рейтинг курьера, после перемножения
                for y in range(n):
                    value = warehouse[y]*couriers[i][y]
                    array.append(value)
                    if value == value_max: #Если значений не одно число, в этот словарь запишетс количество таких значений
                        array_id[i] = y
                    elif value > value_max:
                        value_max = value
                        array_id = {i: y}
                array_of_coefficients.append(array)
    except:
        print('ERROR, разное количество элементов в массивах')
        return False
    
    if len(array_id.keys()) > 1:
        max_r = -1
        for key in array_id.keys():
            if warehouse[array_id[key]] > max_r:
                max_r = warehouse[array_id[key]]
                i_max_r = key #ID курьера, имеющего максимальный рейтинг склада
        array_id = {key: array_id[key]}
    
    r = requests.get("http://172.31.20.207:8000/api/v1/courier/?format=json&username=admin&api_key=228a")
    j = r.json()
    id_c_sql = couriers_id[list(array_id.keys())[0]]
    id_w_sql = warehouse_id[list(array_id.values())[0]]
    for courier in j['objects']:
        if courier['id'] == id_c_sql:
            courier['status'] = 'B'
            w = requests.put(f'http://172.31.20.207:8000{courier["resource_uri"]}?format=json&username=admin&api_key=228a', data=json.dumps({'status': 'B'}), headers={'Content-type': 'application/json'})
            print(courier)
    couriers.pop(list(array_id.keys())[0])
    return id_c_sql, id_w_sql #Выводит id курьера и склада, находщиеся на sql-сервере
