
# Basic Condition
n = 0
while n < 2:
    n += 1
    print(f'Number: {n}')
    name = input('What is your name? ')
    print(f'Hello {name}')

# Using continue to jump based on condition
n = 0
while n < 4:
    n += 1
    if n == 2:
        print(f'Jumping {n}')
        continue
    print(f'Number: {n}')
    name = input('What is your name? ')
    print(f'Hello {name}')

# Stoping the code - break
n = 0
while n < 4:
    n += 1
    print(f'Number: {n}')
    name = input('What is your name? ')
    if name.lower() == 'andre':
        print(f'You are not welcome here!')
        break

# else
n = 0
while n < 2:
    n += 1
    print(f'Number: {n}')
    name = input('What is your name? ')
    print(f'Hello {name}')
else:
    print('Condição de parada!')