# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 12:14:02 2015

@author: yang
"""
# cd ~/Desktop/DAT8/data
# %reset

## Part 1: Read data
import csv
with open('chipotle.tsv', 'rU') as f:
    dialect = csv.Sniffer().sniff(f.read(1024))
    f.seek(0)
    file_nested_list = [row for row in csv.reader(f, dialect)]

## Part 2: Separate header from data
header = file_nested_list[0]
data = file_nested_list[1:]

## Part 3: Calculate average order price by summing all prices and dividing by number of orders
lst_prices = [float(i[4][1:]) for i in data]
sum_prices = sum(lst_prices)
lst_order_ids = [int(i[0]) for i in data]
num_orders = len(set(lst_order_ids))
avg_order_price = sum_prices/num_orders

## Part 4: Find set of canned drinks from choice description of items with the word canned in them
lst_canned = [item_order[3] for item_order in data if 'canned' in item_order[2].lower()]
set_canned = set(lst_canned)

## Part 5: Calculate average number of burrito toppings by counting commas in choice description and dividing by number of burrito orders
lst_burrito_topping = [item_order[3] for item_order in data if 'burrito' in item_order[2].lower()]
count_burrito_topping = [i.count(',') + 1 for i in lst_burrito_topping]
avg_burrito_topping = round(float(sum(count_burrito_topping))/len(lst_burrito_topping), 2)

## Part 6: Create dictionary of chip orders and their respective quantities by finding set of chip orders and adding up quantities for each order type
set_chip_names = set([item_order[2] for item_order in data if item_order[2].lower().find('chip') >= 0])
lst_chip_count = []
for chip_name in set_chip_names:
    int_chip_count = 0
    for item_order in data:
        if item_order[2] == chip_name:
            int_chip_count += int(item_order[1])
    lst_chip_count.append(int_chip_count)
dict_chip_count = dict(zip(set_chip_names, lst_chip_count))

from collections import defaultdict
dict_chip_count_2 = defaultdict(list)
lst_temp = zip(set_chip_names, lst_chip_count)
for chip, count in lst_temp:
    dict_chip_count_2[chip].append(count)
    
from collections import defaultdict
dchips = defaultdict(int)
for row in data:
    if 'Chips' in row[2]:
        dchips[row[2]] += int(row[1])

print('Part 3 (Average price of an order): {}'.format(avg_order_price))
print('Part 4 (Set of unique canned sodas and drinks): {}'.format(set_canned))
print('Part 5 (Average number of toppings per burrito): {}'.format(avg_burrito_topping))
print('Part 6 (Dictionary of chip orders and their totals): {}'.format(dict_chip_count))
