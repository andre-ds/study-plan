
# enumarete 
lt = [3, 4, 5, 6, 7]

for index, value in enumerate(lt):
    print(f'index: {index}, value: {value}')

## creating dictionary with enumerate
lt = ['a', 'b', 'c']
elements = {}
for i, v in enumerate(lt):
    elements[v] = i

print(elements)

# zip
### pair two lists in one tuple
lt1 = ['AXS', 'BTC', 'ADA']
lt2 = ['low', 'high', 'neuter']

zip1 = zip(lt1, lt2)
list(zip1)

# Unpairing sequence
tuples_list = [('Jessica', 'Jones'), ('Bruce', 'Banner'), ('Luke', 'Cage')]
first_name, last_name = zip(*tuples_list)
print(first_name)
print(last_name)

# reversed
## reverse sequence
list(reversed(range(10)))

# list comprehensions
list1 = ['a', 'b', 'ab', 'abc', 'abcd']
list2 = [x for x in list1 if len(x) > 2]
print(list2)

# dict comprehensions
{value:index for index, value in enumerate(list1)}