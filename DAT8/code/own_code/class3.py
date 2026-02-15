# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 19:22:08 2015

@author: user
"""
import csv


movies = ['tt0111161', 'tt1856010', 'tt0096694', 'tt0088763', 'tt1375666']

numbers = [];
for i in movies:
    numbers.append(i[2:])
print(numbers)

numbers2 = [int(i[1:]) for i in movies];
print(numbers2)

int_numbers = [int(i) for i in numbers2];
sum(int_numbers[0:3])
sum(int_numbers)

#####################

f = open('airlines.csv', 'rU')
file_string = f.read()
f.close()

with open('airlines.csv', 'rU') as f:
    file_nested_list = [row for row in csv.reader(f)]
    
header = file_nested_list[0]
data = file_nested_list[1:]


avg_incidents_yr = [(float(airline[2]) + float(airline[5]))/30 for airline in data]
name_clean = [airline[0].replace('*','') for airline in data]
name_star = [0 if airline[0].find('*') == -1 else 1 for airline in data]
dict_airlines = dict(zip(name_clean, avg_incidents_yr))

##################### HW

# cd ~/Desktop/DAT8/data
import csv
with open('chipotle.tsv', 'rU') as f:
    #dialect = csv.Sniffer().sniff(f.read(1024))
    
    file_nested_list = [row for row in csv.reader(f, delimiter='\t')]

header = file_nested_list[0]
data = file_nested_list[1:]

lst_prices = [float(i[4][1:]) for i in data]
sum_prices = sum(lst_prices)
lst_order_ids = [int(i[0]) for i in data]
num_orders = len(set(lst_order_ids))
avg_order_price = sum_prices/num_orders

lst_canned = [item_order[3] for item_order in data if item_order[2].lower().find('canned') >= 0]
lst_canned_unique = set(lst_canned)

lst_burrito_topping = [item_order[3] for item_order in data if item_order[2].lower().find('burrito') >= 0]
count_burrito_topping = [i.count(',') + 1 for i in lst_burrito_topping]
avg_burrito_topping = float(sum(count_burrito_topping))/len(lst_burrito_topping)

lst_chip_names = set([item_order[2] for item_order in data if item_order[2].lower().find('chip') >= 0])

lst_chip_count = []
        
for chip_name in lst_chip_names:
    print(chip_name)
    int_chip_count = 0
    for item_order in data:
        if item_order[2] == chip_name:
            int_chip_count += 1 * int(item_order[1])
    lst_chip_count.append(int_chip_count)
    
dict_chip_count = dict(zip(lst_chip_names, lst_chip_count))

#set([i[3] for i in data])
# lst_item_name = [i[2].lower() for i in data]
'''
for item_order in data:
    int_chip_count = 0
    for chip_name in lst_chip_names:
        if item_order[2] == chip_name:
            int_chip_count += 1
        lst_chip_count.append(int_chip_count)
'''