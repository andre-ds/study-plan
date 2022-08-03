
# Tuples
##  Creating tuples
tp = 1, 2, 3, 4 
print(tp)

tp = (1, 2, 3, 4) 
print(tp)

tp = ((1,2),(1, 2, 3, 4, 5)) 
print(tp)

## Converting list in tuple
lt = [1, 2, 3, 4, 5, 6]
tuple(lt)
tuple('object')

## Concating tuples
tp1 = (1, 2, 3, 4) 
tp2 = ('a', 'b', 'c') 

tp1 + tp2

## unpacking
tp = (1, 2, 3)
a, b, c = tp 
print(a)
print(b)
print(c)

## Advance unpacking
values = 1, 2, 3, 4, 5, 6
print(values)

a, b, *others = values
print(a)
print(b)
print(others)
'''
Obs: rest is convention.
'''

# List
lt = [1, 2, 3, 4, 5]
print(lt)

rg = range(10)
rg = list(rg)
print(rg)

## Adding
rg.append('add')
print(rg)

## Specifying the location
rg.insert(0, 'specific')
print(rg)

## Removing by index
rg.pop(0)
print(rg)

## Removing by element
rg.remove('add')
print(rg)

## Checking element in list
'add' not in rg
'add' in rg

## Concating
lt1 = [1,2]
lt2 = ['a','b']
lt3 = lt1 + lt2
print(lt3)

## Extending
lt = [1,2]
lt.extend([3, 4, 5, 6, 7])
print(lt)
lt.extend([1000])
print(lt)

## Ordering
lt = [10, 3, 78, 0]
lt.sort()
print(lt)

# dict
## sets of key and value
dict1 = {'a': 1000, 'b':2000, 'c':3000}
dict1['a']
dict1['b']

## check if contains key
'a' in dict1

## delete key and value
print(dict1)
dict1.pop('a')

## key and values are iterators
list(dict1.keys())
list(dict1.values())

## update
## update can be used to added elements
print(dict1)
dict1.update({'d':1850})

## update can be used to update elements
dict1.update({'b':20000})
print(dict1)

## get
dict1.get('b')

# set
## It is a collection of elements as keys of dictionaries.
set1 = {'a', 'b', 'c'}
set2 = {'a', 'd', 'e', 'f'}

set1 = set(['a', 'b', 'c'])
set2 = set(['a', 'd', 'e', 'f'])

# union
set1.union(set2)

# intersection
set1.intersection(set2)





