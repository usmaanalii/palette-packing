import csv
import itertools
from itertools import repeat
from collections import Counter
from copy import deepcopy

# data.py


# convert the order csv file into a dict
def order_to_dict(order_file):
    order_list = {}
    with open(order_file, 'r') as my_file:
        reader = csv.reader(my_file)
        for row in reader:
            value = {}
            value['Qty'] = int(row[1])
            value['Warehouse'] = row[2]
            order_list[row[0]] = value
    return order_list


order_list = (order_to_dict('order.csv'))


# convert the order product information file into a dict
def products_to_dict(order_file):
    product_info = {}
    with open(order_file, 'r') as my_file:
        reader = csv.reader(my_file)
        for row in reader:
            value = {}
            value['Qty'] = int(row[1])
            value['Length'] = int(row[2])
            value['Width'] = int(row[3])
            value['Descr'] = row[4]
            product_info[row[0]] = value
    return product_info


product_info = (products_to_dict('products.csv'))

# processor1.py


# produces a subset of the products dict only the items on the order
def order_data_retrieval(products, order):
    wanted_keys = order.keys()
    return dict((k, products[k]) for k in wanted_keys if k in products)


order = order_data_retrieval(product_info, order_list)
# {'BA5': {'Width': 200, 'Length': 800, 'Descr': 'Bap White x 32', 'Qty': 16}..


# produce two tuple lists containing the lengths and widths
# with the product code

def dimension_lists(order):
    lengths = []
    for key in sorted(order):
        item_count = min(order_list[key]['Qty'], product_info[key]['Qty'])
        lengths.extend(repeat((key, order[key]['Length']),
                              item_count))

    widths = []
    for key in sorted(order):
        item_count = min(order_list[key]['Qty'], product_info[key]['Qty'])
        widths.extend(repeat((key,
                              order[key]['Width']), item_count))

    return lengths, widths


lengths = dimension_lists(order)[0]  # [('AA1': 220), (...)]
widths = dimension_lists(order)[1]  # [('AA1': 120), (...)]

# processor2.py


# produces a list with the accumulated measurements
def accumulator_gen(measurement_list):

    if len(measurement_list) == 0:
        measurement_list = [0]

    accumulated_measurements_list = []
    total = 0
    for x in measurement_list:
        total = total + x
        accumulated_measurements_list.append(total)

    return accumulated_measurements_list


# used to find the number of items it takes to exceed the max length/width
def index_at_value(acc_list, max_val):
    for i in acc_list:
        if i >= max_val:
            return acc_list.index(i)
    if len(acc_list) > 0:
        if max_val > acc_list[len(acc_list) - 1]:
            return len(acc_list)
    else:
        return 999  # dummy to prevent index error (points to end of list)

# processor3.py


lengths_list = [length[1] for length in lengths]
widths_list = [width[1] for width in widths]


# returns a list containing the indexes to slice the order
# and is used to find the indexes for both width and length
def index_retrievaL(acc_list, max_val):
    p1_end = (index_at_value(acc_list, max_val))
    p2_end = (index_at_value(acc_list, acc_list[p1_end - 1] + max_val))
    p3_end = (index_at_value(acc_list, acc_list[p2_end - 1] + max_val))
    p4_end = (index_at_value(acc_list, acc_list[p3_end - 1] + max_val))
    p5_end = (index_at_value(acc_list, acc_list[p4_end - 1] + max_val))
    p6_end = (index_at_value(acc_list, acc_list[p5_end - 1] + max_val))
    p7_end = (index_at_value(acc_list, acc_list[p6_end - 1] + max_val))
    p8_end = (index_at_value(acc_list, acc_list[p7_end - 1] + max_val))

    return [p1_end, p2_end, p3_end, p4_end, p5_end, p6_end, p7_end, p8_end]


# returns the correct index to slice the order (between the indexes
# generated from length and width measurements)
def lowest_index(l_indexes, w_indexes):
    indexes = []
    for i in zip(l_indexes, w_indexes):
        indexes.append(min(i))

    return indexes


# processor4.py

# find the correct index to split the current palette with
def index_generator(ll, wl):
    acc_lengths_list = accumulator_gen(ll)
    acc_widths_list = accumulator_gen(wl)

    length_indexes = index_retrievaL(acc_lengths_list, 2001)
    width_indexes = index_retrievaL(acc_widths_list, 1201)

    low_indexes = lowest_index(length_indexes, width_indexes)

    remaining_lengths = ll[low_indexes[len(length_indexes) - 2]:]
    remaining_widths = wl[low_indexes[len(width_indexes) - 2]:]

    return low_indexes, remaining_lengths, remaining_widths


# creates each palettes split indexes
def index_list(ll, wl):
    pal1_indexes = index_generator(ll, wl)[0]
    pal1_rem = index_generator(ll, wl)[1:]

    pal2_indexes = index_generator(pal1_rem[0], pal1_rem[1])[0]
    pal2_rem = index_generator(pal1_rem[0], pal1_rem[1])[1:]

    pal3_indexes = index_generator(pal2_rem[0], pal2_rem[1])[0]
    pal3_rem = index_generator(pal2_rem[0], pal2_rem[1])[1:]

    pal4_indexes = index_generator(pal3_rem[0], pal3_rem[1])[0]
    pal4_rem = index_generator(pal3_rem[0], pal3_rem[1])[1:]

    pal5_indexes = index_generator(pal4_rem[0], pal4_rem[1])[0]
    pal5_rem = index_generator(pal4_rem[0], pal4_rem[1])[1:]

    pal6_indexes = index_generator(pal5_rem[0], pal5_rem[1])[0]
    pal6_rem = index_generator(pal5_rem[0], pal5_rem[1])[1:]

    pal7_indexes = index_generator(pal6_rem[0], pal6_rem[1])[0]
    remaining = index_generator(pal6_rem[0], pal6_rem[1])[1:]

    return (pal1_indexes, pal2_indexes, pal3_indexes, pal4_indexes,
            pal5_indexes, pal6_indexes, pal7_indexes, remaining)


# order_builder.py

all_indexes = index_list(lengths_list, widths_list)[:-1]

# all of the indexes that will be used to slice the order into palettes
pal1_indexes = all_indexes[0]
pal2_indexes = all_indexes[1]
pal3_indexes = all_indexes[2]
pal4_indexes = all_indexes[3]
pal5_indexes = all_indexes[4]
pal6_indexes = all_indexes[5]
pal7_indexes = all_indexes[6]

remaining = index_list(lengths_list, widths_list)[-1]


# Function to reate each palette
def palette_builder(dimensions, index_list):
    # x represents the tuple ('AA1', 220) which is (code, measurement)
    p1 = [x[0] for x in dimensions[:index_list[0]]]
    p2 = [x[0] for x in dimensions[index_list[0]:index_list[1]]]
    p3 = [x[0] for x in dimensions[index_list[1]:index_list[2]]]
    p4 = [x[0] for x in dimensions[index_list[2]:index_list[3]]]
    p5 = [x[0] for x in dimensions[index_list[3]:index_list[4]]]
    p6 = [x[0] for x in dimensions[index_list[4]:index_list[5]]]
    p7 = [x[0] for x in dimensions[index_list[6]:index_list[7]]]

    palettes = [p1, p2, p3, p4, p5, p6, p7]

    non_empty_palettes = [x for x in palettes if x != []]

    remaining_items = dimensions[index_list[6]:]

    return non_empty_palettes, remaining_items


# Creting the palette stack
pal1 = palette_builder(lengths, pal1_indexes)[0]
rem_lengths = palette_builder(lengths, pal1_indexes)[1]

pal2 = palette_builder(rem_lengths, pal2_indexes)[0]
rem_lengths = palette_builder(rem_lengths, pal2_indexes)[1]

pal3 = palette_builder(rem_lengths, pal3_indexes)[0]
rem_lengths = palette_builder(rem_lengths, pal3_indexes)[1]

pal4 = palette_builder(rem_lengths, pal4_indexes)[0]
rem_lengths = palette_builder(rem_lengths, pal4_indexes)[1]

pal5 = palette_builder(rem_lengths, pal5_indexes)[0]
rem_lengths = palette_builder(rem_lengths, pal5_indexes)[1]

pal6 = palette_builder(rem_lengths, pal6_indexes)[0]
rem_lengths = palette_builder(rem_lengths, pal6_indexes)[1]

pal7 = palette_builder(rem_lengths, pal7_indexes)[0]
rem_lengths = palette_builder(rem_lengths, pal7_indexes)[1]


# Returns the stack full of palettes
def stack_generator(palettes):
    stack = []
    for palette in palettes:
        if len(palette) > 0:
            stack.append(palette)

    return stack


all_palettes = [pal1, pal2, pal3, pal4, pal5, pal6]
stack = stack_generator(all_palettes)

# csv_generator.py


# Create a dict with each palette item, and the item's count
def prod_count_dict(order_stack):
    stack_dict = {}
    stack = 1
    for palette in order_stack:
        pal_dict = {}
        pal_number = 1
        for i in range(len(palette)):
            c = Counter(palette[i])
            pal_dict[pal_number] = c.items()
            pal_number = pal_number + 1
        stack_dict[stack] = pal_dict
        stack = stack + 1

    return stack_dict


stack_counts = prod_count_dict(stack)


# Create seperate csv's for each palette
def palettes_csv_generator(counts):
    for i in range(1, len(stack) + 1):
        with open('palette_stack_' + str(i) + '.csv', 'w') as out:
            writer = csv.writer(out)
            writer.writerow(['Palette Number',
                             'Product Code', 'Product Quantity'])
            for key in counts[i]:
                for item in counts[i][key]:
                    writer.writerow([key, item[0], item[1]])


palettes_csv_generator(stack_counts)


# Create a single csv for the entire stack
def stack_csv_generator(counts):
    with open('full_order.csv', 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['Stack Number', 'Palette Number',
                         'Product Code', 'Product Quantity'])
        for key in counts:
            for key2 in counts[key]:
                for item in counts[key][key2]:
                    writer.writerow([key, key2, item[0], item[1]])


stack_csv_generator(stack_counts)

# analysis.py

stack_2 = deepcopy(stack)
stack_3 = deepcopy(stack)


# swap all item codes with their length
def length_errors(order):

    for palette in order:
        for pack in palette:
            i = 0
            for item in pack:
                pack[i] = product_info[item]['Length']
                i += 1

    order_lengths = order

    palette_lengths = []
    for palette in order_lengths:
        for pack in palette:
            palette_lengths.append((accumulator_gen(pack)
                                    [len(accumulator_gen(pack)) - 1]))

    pack_errors = 0
    for length in palette_lengths:
        if length > 2000:
            pack_errors += 1

    return palette_lengths, pack_errors


palette_lengths = length_errors(stack_2)[0]


def length_analysis(lengths, max_length):
    max_palette_length = max_length * 7
    total_percent = 0
    result = []
    x = 1
    for i in [0, 7, 14, 21, 28, 35]:
        palette_length = sum(lengths[i:i + 7])
        palette_percent_used = round((palette_length /
                                      float(max_palette_length) * 100), 2)
        result.append('Palette stack ' + str(x) + ' used ' +
                      str(palette_percent_used) + '%' + ' of the total length')
        total_percent = total_percent + palette_percent_used
        x = x + 1

    total_percent_used = total_percent / float(6)

    return result, ('Total order length used is ' +
                    str(total_percent_used) + '%')


palette_length_percentages = length_analysis(palette_lengths, 2000)[0]
stack_length_percentage = length_analysis(palette_lengths, 2000)[1]


# swap all item codes with their length
def width_errors(order):
    for palette in order:
        for pack in palette:
            i = 0
            for item in pack:
                pack[i] = product_info[item]['Width']
                i += 1

    order_widths = order

    palette_widths = []
    for palette in order_widths:
        for pack in palette:
            palette_widths.append((accumulator_gen(pack)
                                   [len(accumulator_gen(pack)) - 1]))

    pack_errors = 0
    for width in palette_widths:
        if width > 1200:
            pack_errors += 1

    return palette_widths, pack_errors


palette_widths = width_errors(stack_3)[0]


def width_analysis(widths, max_width):
    max_palette_width = max_width * 7
    total_percent = 0
    result = []
    x = 1
    for i in [0, 7, 14, 21, 28, 35]:
        palette_width = sum(widths[i:i + 7])
        palette_percent_used = round((palette_width /
                                      float(max_palette_width) * 100), 2)
        result.append('Palette stack ' + str(x) + ' used ' +
                      str(palette_percent_used) + '%' + ' of the total width')
        total_percent = total_percent + palette_percent_used
        x = x + 1

    total_percent_used = total_percent / float(6)

    return result, ('Total order width used is ' +
                    str(total_percent_used) + '%')


# Create analysis.txt file

palette_width_percentages = width_analysis(palette_widths, 1200)[0]
stack_width_percentage = width_analysis(palette_widths, 1200)[1]

palette_length_percentages.insert(0, stack_length_percentage)
palette_width_percentages.insert(0, stack_width_percentage)

analysis = list(itertools.chain.from_iterable(zip(palette_length_percentages,
                                                  palette_width_percentages)))

analysis_file = open('analysis.txt', 'w')

for line in analysis:
    analysis_file.write("%s\n\n" % line)
