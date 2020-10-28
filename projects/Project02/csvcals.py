import sys
import os
import datetime
import csv

def table_of_file(filename):
    with open(filename) as c:
        r = csv.reader(c)
        next(r)
        table = {}
        for row in r:
            table[row[0]] = row[1:]
        return table

# List the weights, or foods eaten for a day. List calories by calculation.
# calscsv list eaten <name> <date>
# calscsv list weights <name>
def list_eaten(name, date):
    for k, vs in table_of_file(os.path.join(name, date) + '.csv').items():
        print(f'{k} {vs[0]}')

def list_weights(name):
    for k, vs in table_of_file(os.path.join(name, 'weight.csv')).items():
        print(f'{k} {vs[0]}')

# List the dates for which we have calorie counts
# calscsv list dates
def list_dates(name):
    for filename in sorted(os.listdir(name)):
        if filename != 'weight.csv': print(filename[:-4])

# List the calorie data itself.
# calscsv list foods
def list_foods():
    for k, vs in table_of_file('calories.csv').items():
        print(k, end=' ')
        for v in vs: print(v, end=' ')
        print('')

# lookup a) calories for a type of food b) weight for a day. Today if missing.
# calscsv lookup calories <food>
# calscsv lookup weight <date>
def lookup_calories(food):
    table = table_of_file('calories.csv')
    vs = table[food]
    if vs == None:
        print(f'Food {food} not found')
    else:
        if len(vs) > 1:
            weight = vs[0]
            calories = vs[1]
            print(f'There are {calories} calories in {weight}g of {food}')
        else:
            print(f'Malformed calorie entry for {food} in calories file')

def lookup_weight(name, date):
    table = table_of_file(os.path.join(name, 'weight.csv'))
    vs = table[date]
    if vs == None:
        print(f'No weight found for {date}')
    elif len(vs) > 0:
        print(f'Weight at {date} was {vs[0]}')

# Print the total calories for just a given day.
# csvcals total <date>
def total_date(name, date):
    calories = table_of_file('calories.csv')
    table = table_of_file(os.path.join(name, date) + '.csv')
    total = 0
    for k, vs in table.items():
        weight_and_calories = calories[k]
        reference_weight = int(weight_and_calories[0])
        reference_calories = int(weight_and_calories[1])
        calories_per_gram = reference_calories / reference_weight
        total += int(vs[0]) * calories_per_gram
    print(f'Total calories for {date}: {int(total)}')

# Create and initialise new user
# csvcals newuser <name>
def new_user(name):
    os.mkdir(name)
    with open(os.path.join(name, 'weight.csv'), 'w') as f:
        print('Date,Weight', file=f)

def date_today():
    d = datetime.datetime.now()
    return f'{d.day:02}-{d.month:02}-{d.year}'

# Add data for today - food and grams
# csvcals eaten <name> <food> <grams>
def eaten(name, food, grams):
    filename = os.path.join(name, date_today()) + '.csv'
    is_new = not os.path.exists(filename)
    with open(filename, 'a') as f:
        if is_new: print('Food,Weight', file=f)
        print(f'"{food}",{grams}', file=f)

# Add weight for today
# csvcals weighed <name> <weight>
def weighed(name, weight):
    filename = os.path.join(name, 'weight.csv')
    is_new = not os.path.exists(filename)
    with open(filename, 'a') as f:
        if is_new: print('Date,Weight', file=f)
        print(f'{date_today()},{weight}', file=f)

# Main program. Read args and dispatch.
arg = sys.argv

if len(arg) > 1:
    cmd = arg[1]
    if cmd == 'list':
        if len(arg) > 3 and arg[2] == 'eaten':
            list_eaten(arg[3], arg[4])
        else:
            if arg[2] == 'weights' and len(arg) > 3:
                list_weights(arg[3])
            elif arg[2] == 'dates' and len(arg) > 3:
                list_dates(arg[3])
            elif arg[2] == 'foods':
                list_foods()
    elif cmd == 'lookup':
        if len(arg) > 2:
            if arg[2] == 'calories':
                lookup_calories(arg[3])
            elif arg[2] == 'weight' and len(arg) > 3:
                lookup_weight(arg[3], arg[4])
    elif cmd == 'total':
        if len(arg) > 3:
            total_date(arg[2], arg[3])
    elif cmd == 'newuser':
        if len(arg) > 2:
            new_user(arg[2])
    elif cmd == 'eaten':
        if len(arg) > 4:
            eaten(arg[2], arg[3], arg[4])
    elif cmd == 'weighed':
        if len(arg) > 3:
            weighed(arg[2], arg[3])
    else:
        print('Command not understood')
