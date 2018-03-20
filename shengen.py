SHENGEN = 180

#меню
def menu():
    print('--------------------------')
    print('p - показать список визитов')
    print('n - добавить новый визит')
    print('d - удалить визит')
    print('c - расчитать отдых')
    print('a - запланировать поездку')
    print('r - прочитать список визитов из файла')
    print('s - сохранить список визитов в файл')
    print('e - выход')
    print('--------------------------')

#показать визиты
def print_visit(vis):
    if len(vis) != 0:
        print(vis)
    else:
        print('Список визитов пуст')

#проверка правильности данных
def audit_days(day1,day2,vis):
    if day1 > day2:
        print('День въезда должен быть раньше дня выезда!')
        return False
    elif day1 > SHENGEN or day2 > SHENGEN:
        print('Сроки визита не должны превышать срока Шенгенской визы!')
        return False
    elif len(vis) != 0 and day1 < vis[-1][1]:
        print('Сроки визитов не должны пересекаться!')
        return False
    else:
        return True

#добавление визита
def add_visit(vis):
    while True:
        arrive = int(input('Введите день прибытия: '))
        leave = int(input('Введите день отправления: '))
        if audit_days(arrive,leave,vis) == True:
            vis.append([arrive,leave])
            break

#удаление визита:
def remove_visit(vis):
    if empty_list(visits) == False:
        pass
    else:
        s = 1
        print('Список визитов:')
        for visit in visits:
            print('{} - {}'.format(s,visit))
            s += 1
        vis.pop(int(input('Введите номер удаляемого визита: ')) - 1)

#подсчет общего количества дней пребывания
def all_days(vis):
    days = []
    count = 0
    for visit in vis:
        count += visit[1] - visit[0] + 1
        days.append(count)
    return days

#проверка превышения лимита прибывания
def limit_visits(vis):
    for day, visit in zip(all_days(vis),vis):
        if residence_limit < day:
            print('Вы превысили лимит пребывания на {} дней в поездку {}!'.format(day - residence_limit,visit))
            return False
    return True

#проверка пустого списка:
def empty_list(vis):
    if len(vis) == 0:
        print('Нет введенных визитов!')
        return False
    else:
        return True

#расчет поездок
def calc_visit(vis):
    if empty_list(vis) == False or limit_visits(vis) == False:
        pass
    else:
        print('Планируемое время в ЕС - {} дней'.format(all_days(vis)[-1]))
        print('Можно запланировать поездку еще на {} дней'.format(residence_limit - all_days(vis)[-1]))

#расчет запланированной поездки
def future_visit(vis):
    if empty_list(vis) == False or limit_visits(vis) == False:
        pass
    else:
        while True:
            future = int(input('Введите дату планируемого въезда: '))
            if audit_days(future,future,vis) == True:
                break
        if future + (residence_limit - all_days(vis)[-1]) >= SHENGEN:
            print('Вам нужно будет выехать в {} день'.format(SHENGEN))
        else:
            print('Вам нужно будет выехать в {} день'.format(future + (residence_limit - all_days(vis)[-1])))

#создание списка визитов из файла
def read_visit(vis):
    try:
        with open ('visits.txt', 'r') as v:
            for line in v:
                i = line.split()
                i[0] = int(i[0])
                i[1] = int(i[1])
                vis.append(i)
    except:
        pass

#сохранение списка визитов в файл
def save_visit(vis):
    with open('visits.txt', 'w') as v:
        for visit in vis:
            v.write('{} '.format(visit[0]))
            v.write('{}\n'.format(visit[1]))

#функция выхода:
def exit_function(x):
    print('Bye bye!')
    raise SystemExit


print('Здравствуйте! Давайте расчитаем ваш отдых в ЕС')
print('Шенгенская виза - {} дней'.format(SHENGEN))
residence_limit = int(input('Введите максимальную длительность визы: '))
visits = [] #инициализация списка визитов

function_tab = {
    'p' : print_visit,
    'n' : add_visit,
    'd' : remove_visit,
    'c' : calc_visit,
    'a' : future_visit,
    'r' : read_visit,
    's' : save_visit,
    'e' : exit_function
}

while True:
    menu()
    change = input('Выберите действие: ')
    if change not in function_tab:
        continue
    function_tab[change](visits)
