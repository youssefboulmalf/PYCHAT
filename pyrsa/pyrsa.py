from random import randint
import math


def random_prime_in_range(x, y):
    #checking for all posible prime numbers inbetween semi random range
    prime_number_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_number_list.append(n)


    return prime_number_list


def calculate_e(n,φ):
    print("Calculating possible e values...")
    r = list(range(2, φ))
    
    #caluculating estimated time.
    #TODO  calculate estimate with one timed loop for better accuracy
    print(f"Estimated time: {math.floor((6.499999999062311e-07 * (0.5 * φ * (φ + 1)))/60)+1} minutes")
    possibilities = []

    #checking for values that dont have common divisors with n or φ
    for value in r:
        divisors = []
        for i in range(2, min(n, value)+1):
            if n %i == value%i == 0:
                divisors.append(i)
        for i in range(2, min(φ, value)+1):
            if φ %i == value%i == 0:
                divisors.append(i)
        if not len(divisors)  > 0:
            possibilities.append(value)
    return possibilities[randint(0,len(possibilities)-1)]


def calculate_d(e,φ):
    l = []
    b=1
    while not len(l) >= 1:
        
        #checking for values that fit e*d(modφ)=1
        for i in range(1, b*1000):
            d = e * i
            if d % φ == 1:
                l.append(i)
        b+=1
    if len(l) > 1:
        r = randint(0, len(l)-1)
        return l[r]
    if len(l) == 1:
        return l[0]
    

def encrypt_message(public_key, message):

    stage = []
    for i in message:
        stage.append(ord(i))
    encrypted_message_list = []
    for index, i in enumerate(stage):
        # first int can't start with a "-"
        if index == 0:
            encrypted_message_list.append(f"{str((pow(i,public_key[0]))%public_key[1])}")
        else:
            encrypted_message_list.append(f"-{str((pow(i,public_key[0]))%public_key[1])}")
    
    end_message = "".join(encrypted_message_list)
    return end_message

def decrypt_message(private_key, message):
    value = message.split("-")
    stage = []
    for i in value:
            stage.append(int(i))
    decrypted_message_list = []
    for i in stage:
        decrypted_message_list.append(chr((pow(i,private_key[0]))%private_key[1]))
    end_message = "".join(decrypted_message_list)

    return end_message




def create_key():
    public_key=[]
    private_key=[]
    range = [1,randint(100, 250)]
    prime_numbers = random_prime_in_range(range[0],range[1])
    p = prime_numbers[randint(0,len(prime_numbers)-1)]
    q = prime_numbers[randint(0,len(prime_numbers)-1)]
    n = p*q
    φ = (p-1)*(q-1)
    e = calculate_e(n,φ)
    public_key.append(e)
    public_key.append(n)
    d = calculate_d(e,φ)
    private_key.append(d)
    private_key.append(n)
    keypair = [public_key, private_key]
    return keypair
