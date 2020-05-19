import re
from random import randint

def create_email(email_list, new_name, new_surname):
    new_name = new_name.lower()
    new_surname = new_surname.lower()
    test =  []
    for i in email_list:
        if new_name in i and new_surname in i:
            test.append(i)
    if len(test) > 0:    
        test_email = test[-1]
        test_char = re.split("@", test_email , 1)[0][-1]
        new_email = ""
        if not(test_char.isdigit()):
            new_email = "%s.%s%s@email.com"%(new_name, new_surname, 1)
        else:
            email_number = re.findall("\d+", test_email)[0]
            new_email = "%s.%s%s@email.com"%(new_name, new_surname, str(int(email_number) + 1))
    else:
        new_email = "%s.%s@email.com"%(new_name, new_surname)
            
    return new_email

#Definiranje potrebnih funkcija za tablicu kartica
def pick_card_type():
	random_number = randint(0,1)
	card = ""
	if(random_number == 0):
		card = "Visa"
	else:
		card = "MasterCard"
	return card

def generate_card_number(card_number_list):
	random_number = randint(1000000000000000, 9999999999999999)
	while str(random_number) in card_number_list:
		random_number = randint(1000000000000000, 9999999999999999)
		
	return str(random_number)
    
#Definiranje potrebnih funkcija za tablicu vozac
def pick_random_car(auto_primary_key_list):
    random_number = randint(0, len(auto_primary_key_list) - 1)
    return auto_primary_key_list[random_number]

def pick_random_user(korisnik_primary_key_list):
    random_number = randint(0, len(korisnik_primary_key_list) - 1)
    return korisnik_primary_key_list[random_number]
