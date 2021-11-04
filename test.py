import random
from sqlite3.dbapi2 import Connection
import database




# ---------------------------------------Functions

def luhm_check(card_num):

    # Converting to list
    card_num = list(map(int, card_num))

    # Drop the last digit
    last = card_num.pop()

    # Multiply odd digits by 2
    card_num = [card_num[element] * 2 if element % 2 == 0 else card_num[element] for element in range(len(card_num))]

    # Substract 9 from numbers over 9
    card_num = [element - 9 if element > 9 else element for element in card_num ]

    # Last check if sum divisible by 10
    all_numbers_sum = sum(card_num) + last

    return all_numbers_sum % 10 == 0

def create_card():

    valid = False

    while not valid:

        temp = str(random.randint(1, 999999999)).zfill(9)
        card = f"400000{temp}3"

        if(luhm_check(card)):
            valid = True

    return card

def create_pin():
    pin_num = random.randint(1, 9999)
    pin_num = str(pin_num).zfill(4)
    return pin_num

# --------------------------------Global Variables---------------------------------------

temp_acc = None

# ----------------------------------- Main Loop ---------------------------------------
def menu():
    connection = database.connect()
    database.create_tables(connection)
    
    
    while True:

        choice = int(input(("""1. Create an account\n2. Log into account\n0. Exit\n>""")))

        if choice == 1:

            card_num = create_card()
            card_pin = create_pin()
            
            print(f"Your card has been created\nYour card number: \n{card_num}")
            print(f"Your card PIN: \n{card_pin}\n")

            

            database.add_data(connection, card_num, card_pin)

        elif choice == 2:
            user_card = input("Enter your card number: \n")
            user_pin = input("Enter your PIN: \n")
            try:
                result = database.println(connection, user_card, user_pin)
                
                res = list(result[0])
                temp_acc = res
            except :
                
                print("Wrong card number or PIN!\n")
                continue
            if res[1] == user_card and res[2] == user_pin:
                print("You have successfully logged in!\n")

                while True:

                    choice2 = int(input("""1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n>"""))

                    if choice2 == 1:
                        
                        
                        print(temp_acc[3])
                    
                    elif choice2 == 2:
                        income = input("Enter income: \n")
                        
                        temp_acc[3] += int(income)
                        database.insert_money(connection, income, temp_acc[1], temp_acc[2])
                        
                        print("Income was added!\n")


                    elif choice2 == 3:
                        transfer = input("""Transfer\nEnter card number: \n""")
                        if transfer == temp_acc[1]:
                            print("You can't transfer money to the same account!")
                            continue
                        

                        if (luhm_check(transfer)):
                            
                            tr = database.transac(connection, transfer)

                            if tr != None:

                                cost = input("Enter how much money you want to transfer: \n")
                                if temp_acc[3] < int(cost):
                                    print("Not enough money!")
                                
                                
                                
                                else:
                                    temp_acc[3] -= int(cost)
                                    database.sender(connection, cost, temp_acc[1], temp_acc[2])
                                    
                                    database.reciever(connection, cost, transfer)
                                    


                                    print("Success")    



                            else:
                                
                                print("Such a card does not exist!")

                        else:
                            print("Probably you made a mistake in the card number. Please try again!")   

                        
                        
                        


                    elif choice2 == 4:
                        acc = temp_acc[1]
                        database.delete_row(connection, acc)
                        print("The account has beeb closed!")
                        break

                    elif choice2 == 5:
                        print("You have succesfully logged out!\n")
                        break

                    elif choice2 == 0:
                        print("Bye!\n")
                        exit()
                    else:
                        print("Wrong action, try again")
            
                    
            

        # elif choice == 6:
        #     cards = database.get_all_info(connection)
        
        #     for card in cards:
        #         print(card)
        else:
            exit()
menu()
    
          