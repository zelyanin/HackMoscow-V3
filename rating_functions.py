from math import exp


def warehouse_ratings(pause, amount):
    """
    По параметрам рассчитать рейтинг конкретного склада в данный момент времени
    По функции нормирования в 0-1
    :type pause: float в часах
    :param pause: Максимальный временной простой среди всех заказов
    :param amount: Кол-во заказов на складе в данный момент времени
    :return: Нормированный рейтинг склада от 0 до 1
    TODO: Нормирование для эмаунта проработать лучше
    """

    # Веса задаются в зависимости от приоритета
    weight_1 = 0.6  # Вес для макс простоя среди заказов
    weight_2 = 0.4  # Вес для кол-ва заказов на складе

    f_pause = lambda s: (exp(s/20)-1)/(exp(s/20)+1)
    f_amount = lambda s: (exp(s)-1)/(exp(s)+1)

    return weight_1 * f_pause(pause) + weight_2 * f_amount(amount)


def courier_ratings(timeout, delivery_rating, distances):
    """
    Формирование рейтинга клиента
    Получает параметры, рассчитывает их и выдает массив рейтингов определенного курьера
    :param timeout: время простоя курьера без заказа
    :param delivery_rating: сколько курьеров раз зафейлил (прибавлет, если доставил воврем, вычитает, если опоздал)
    :param distances: массив минут, до каждого склада
    distance - сколько курьеру понадобится времени доставить товар (количество минут)
    :return: Выдает массив, каждое значение из которых рейтинг для каждого склада
    """

    f_timeout = lambda s: (exp(s / 10) - 1) / (exp(s / 10) + 1)       # Функция активации для timeout
    f_delivery_rating = lambda s: 1 / (1 + exp(-s / 10))              # Функция активности для ценности курьера
    f_distance = lambda s: 1 - (exp(s / 75) - 1) / (exp(s / 75) + 1)  # Функция активации для distance

    # Нормирование
    timeout_value = f_timeout(timeout)
    delivery_rating_value = f_delivery_rating(delivery_rating)
    for i in range(len(distances)):
        distances[i] = f_distance(distances[i])

    # Веса задаются в зависимости от приоритета
    weight_1 = 0.08  # Вес для параметра простоя курьера
    weight_2 = 0.09  # Вес для параметра фейлов курьера
    weight_3 = 0.83  # Вес для расстония курьера

    ratings = []
    # Сумма всех райтингов с учетом весов
    for distance_value in distances:
        rating = timeout_value * weight_1 + delivery_rating_value * weight_2 + distance_value * weight_3
        ratings.append(rating)
    return ratings
