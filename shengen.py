import xml.etree.ElementTree as etree
SHENGEN = 180

#меню
def menu():
    print('--------------------------')
    print('Список визитов: {} '.format(visits))
    print('--------------------------')
    print('n - добавить новый визит')
    print('d - удалить визит')
    print('c - расчитать отдых')
    print('a - запланировать поездку')
    print('r - прочитать список визитов из файла')
    print('s - сохранить список визитов в файл')
    print('e - выход')
    print('--------------------------')
    return input('Выберите действие: ')

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
    elif day1 > residence_limit or day2 > residence_limit:
        print('Сроки визита не должны превышать срока визы!')
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
            print('Вы превысили лимит пребывания на {} дней в поездку {}!'.format(day - residence_limit, visit))
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
        tree = etree.parse('visits.xml')
        root = tree.getroot()
        vis.clear
        for element in root:
            vis.append([int(element.attrib['arrive']),int(element.attrib['departed'])])
    except:
        print('Неправильный файл визитов! Или его нет. :(')
        pass

#сохранение списка визитов в файл
def save_visit(vis):
    root = etree.Element('list_visits')
    for visit in vis:
        a = etree.SubElement(root, 'visit')
        a.set('arrive', str(visit[0]))
        a.set('departed', str(visit[1]))
    with open('visits.xml', 'w') as v:
        data = etree.tostring(root, pretty_print=True)
        v.write(data.decode())

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
    function_tab[menu()](visits)
