import random

def generate_password():
    
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
        'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    
    nr_letters = 2
    nr_symbols = 2
    nr_numbers = 5

    password = []

    while nr_letters > 0:
        pass_lett = random.choice(letters)
        password.append(pass_lett)
        nr_letters -= 1

    while nr_numbers > 0:
        pass_num = random.choice(numbers)
        password.append(pass_num)
        nr_numbers -= 1

    while nr_symbols > 0:
        pass_sym = random.choice(symbols)
        password.append(pass_sym)
        nr_symbols -= 1


    random.shuffle(password)
    return("".join(password))