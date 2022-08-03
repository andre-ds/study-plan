
# Printing text
print('My text is "fucking" cool.')
print("My text is 'fucking' cool.")
print("My text is \'fucking\' cool.")

# Escaping
print("My text is \"fucking\" cool.")
print("My text is \nfucking cool.")

# Execute all text
print(r"My text is \nfucking cool.")

# Formating text I
name = 'André'
print(f'My name is {name}')

pi = 3.14159265359
print(f'The pi is {pi:.2f}')

# Formating text II
print('My name is {}, the pi is {:.2f}'.format(name, pi))
print('My name is {0}, the pi is {1:.2f}'.format(name, pi))
print('My name is {n}, the pi is {pi:.2f}'.format(n=name, pi=pi))

# Others
str = 'string'
print(f'{str:s}')

digit = 3
print(f'{pi:d}')

# then numbers left
num = 786
print(f'{num:0>10}')

# then numbers right
num = 786
print(f'{num:0<10}')

# then numbers in center
num = 786
print(f'{num:0^10}')

# add - to have 10 characters
str = 'string'
print(f'{str:-^10}') # center
print(f'{str:-<10}') # right
print(f'{str:->10}') # left