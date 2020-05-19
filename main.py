import mysql.connector

from random import randint
import re

from functions import create_email, pick_card_type, generate_card_number, pick_random_user, pick_random_car
from random_data_gen import names, surnames

#Stvaranje konekcije sa mysql bazom podataka
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password123",
    database = "databasename"
    )

mycursor = mydb.cursor()

print("Za prekid programa 0.\nZa ubacivanje podataka u tablicu 'korisnik' unesite 1.\nZa ubacivanje podataka u tablicu 'kartica' unesite 2.\nZa unos podataka u tablicu 'vozac' unesite 3\n")
unos = 1000
while(unos != 0):
    unos = int(input("Unesite odgovarajući broj: "))
    print("---------------------------------------")
    if unos == 1:
        broj_redaka_korisnik = int(input("Unesite broj redaka: "))
        #Upit koji uzima sve ntorke iz tablice korisnik
        mycursor.execute("SELECT * FROM korisnik")

        korisnik_list = mycursor.fetchall()

        #Spremanje primarnog ključa od posljednjeg korisnika (korisnikID)
        last_korisnikID = korisnik_list[-1][0]

        #print(last_korisnikID)

        new_list = korisnik_list

        #Email lista
        email_list = []
        for item in new_list:
            email_list.append(item[-1])

        #Generiranje korisnika
        for i in range(last_korisnikID + 1, last_korisnikID + broj_redaka_korisnik + 1):
            new_name = names[randint(0,49)]
            new_surname = surnames[randint(0,49)]
            new_email = create_email(email_list, new_name, new_surname)
            email_list.append(new_email)
            new_list.append((i,new_name,new_surname, new_email))

        #Generiranje sql izraza
        sql_txt = ""
        for i in new_list[last_korisnikID:]:
            sql_txt += "(%s, '%s', '%s', '%s'),"%(i[0], i[1], i[2], i[3])
        print("Ubačeni su sljedeći podaci: ")
        print(sql_txt[:-1])

        #Ubacivanje podataka u bazu (tablica korisnik)
        sql = "INSERT INTO korisnik (korisnikID, ime, prezime, email) VALUES %s"%(sql_txt[:-1])

        mycursor.execute(sql)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        print("---------------------------------------")
        
    elif unos == 2:
        #Pretraga korisnika koji nemaju karticu
        mycursor.execute("SELECT ko.korisnikID FROM korisnik ko WHERE NOT EXISTS (SELECT 1 FROM kartica ka WHERE ko.korisnikID = ka.korisnikID)")

        korisnik_list = mycursor.fetchall()

        for i in korisnik_list:
            print(i[0])
            
        #Dohvat zadnjeg primarnog ključa iz tablice kartica
        mycursor.execute("SELECT * FROM kartica ORDER BY karticaID DESC LIMIT 1")
        last_card_ID= mycursor.fetchall()[0][0]

        #print(last_card_ID)
            
        #Dohvat brojeva kartice
        mycursor.execute("SELECT broj FROM kartica")
        card_number_list_tuples= mycursor.fetchall()
        card_number_list = [i[0 ]for i in card_number_list_tuples]
        #print(card_number_list)
        print("-----------------------------------------------------------")

        #Dodavanje kartice korisnicima koji nisu imali karticu
        payment_cards = ['Visa', 'MasterCard']
        test = []

        sql_txt = ""
        counter = last_card_ID + 1
        for i in korisnik_list:
            random_number = randint(0, 1)
            if(random_number == 0):
                random_card_number = generate_card_number(card_number_list)
                sql_txt += "(%s, '%s', '%s', %s),"%(counter,random_card_number, pick_card_type(), i[0])
                card_number_list.append(random_card_number)
                counter += 1
            else:
                random_card_number1 = generate_card_number(card_number_list)
                random_card_number2 = generate_card_number(card_number_list)
                sql_txt += "(%s, '%s', '%s', %s),"%(counter,random_card_number1, "Visa", i[0])
                sql_txt += "(%s, '%s', '%s', %s),"%(counter + 1,random_card_number2, "MasterCard", i[0])
                counter += 2


        print(sql_txt)
        print("-----------------------------------------------------------")

        #Ubacivanje podataka u tablicu kartica
        if(len(sql_txt) == 0):
            print("Svi korisnici imaju jednu ili više kartica!")
        else:
            sql = "INSERT INTO kartica (karticaID, broj, vrsta_kartice, korisnikID) VALUES %s"%(sql_txt[:-1])
            mycursor.execute(sql)

            mydb.commit()
            print("Ubacivanje podataka uspješno!")
            
        print("---------------------------------------")
        
    elif unos == 3:
        #Dohvaćanje zadnjeg primarnog ključa iz tablice vozac
        mycursor.execute("SELECT * FROM vozac ORDER BY vozacID DESC LIMIT 1")

        vozac_last_ID = mycursor.fetchall()[0][0]

        #print(vozac_last_ID)

        #Dohvaćanje primarnih ključeva iz tablice auto
        mycursor.execute("SELECT autoID FROM auto")

        auto_primary_key_list = [i[0] for i in mycursor.fetchall()]
        #print(auto_primary_key_list)

        #Dohvaćanje primarnih ključeva iz tablice korisnik
        mycursor.execute("SELECT korisnikID FROM korisnik")

        korisnik_primary_key_list = [i[0] for i in mycursor.fetchall()]
        #print(korisnik_primary_key_list)

        #Generiranje ntorki

        broj_redaka = int(input("Koliko redaka za unijeti? "))

        sql_txt = ""

        for i in range(vozac_last_ID + 1, vozac_last_ID + broj_redaka + 1):
            sql_txt += "(%s, %s, %s),"%(i, pick_random_car(auto_primary_key_list), pick_random_user(korisnik_primary_key_list))
            
        #print(sql_txt[:-1])

        #Ubacivanje podataka u tablicu vozac
        sql = "INSERT INTO vozac (vozacID, autoID, korisnikID) VALUES %s"%(sql_txt[:-1])
        mycursor.execute(sql)

        mydb.commit()

        print(sql_txt[:-1])
        print(mycursor.rowcount, "record inserted.")


