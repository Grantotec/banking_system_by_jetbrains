import sqlite3
from random import randint


class Account:
    id: int
    number: str
    pin: str
    balance: int

    COUNT_ID = 0

    def __init__(self):
        Account.COUNT_ID += 1
        self.id = Account.COUNT_ID
        self.balance = 0
        while True:
            rand_number = '400000' + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
            rand_number += luhn_algorithm(rand_number)
            if check_number(rand_number):
                continue
            else:
                self.number = rand_number
                self.pin = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
                break
        columns = [self.id, self.number, self.pin, self.balance]
        conn_init = sqlite3.connect("card.s3db")
        cur_init = conn_init.cursor()
        cur_init.execute("INSERT INTO card VALUES (?, ?, ?, ?)", columns)
        conn_init.commit()
        cur_init.close()

        print('\n'
              'Your card has been created\n'
              'Your card number:\n'
              '{}\n'
              'Your card PIN:\n'
              '{}\n'.format(self.number, self.pin)
              )


def log_in_menu(card):
    while True:
        var = input('1. Balance\n'
                    '2. Add income\n'
                    '3. Do transfer\n'
                    '4. Close account\n'
                    '5. Log out\n'
                    '0. Exit\n'
                    )
        if var == '1':
            cur_b = conn.cursor()
            cur_b.execute(f"SELECT balance FROM card WHERE number = {card}")
            past_b = cur_b.fetchall()[0][0]
            print(f"\nBalance: {past_b}\n")
        elif var == '2':
            how = input('\nEnter income:\n')
            cur_add = conn.cursor()
            cur_add.execute(f"SELECT balance FROM card WHERE number = {card}")
            balance = cur_add.fetchall()[0][0] + int(how)
            cur_add.close()
            cur_add = conn.cursor()
            cur_add.execute(f"""UPDATE card 
                            SET balance = {balance} 
                            WHERE number = {card}""")
            conn.commit()
            cur_add.close()
            print("Income was added!\n")
        elif var == '3':
            print("Transfer")
            enter_card = input("Enter card number:\n")
            cur_check_card = conn.cursor()
            cur_check_card.execute(f"SELECT number FROM card WHERE number = {enter_card}")
            number = [x[0] for x in cur_check_card.fetchall()]
            if enter_card == card:
                print("You can't transfer money to the same account!\n")
                continue
            if not luhn_algorithm_checking(enter_card[:-1], enter_card[-1]):
                print("Probably you made a mistake in the card number. Please try again!")
                continue
            if enter_card not in number:
                print("Such a card does not exist.\n")
                continue
            cur_check_card.close()
            money = int(input("Enter how much money you want to transfer:\n"))
            cur_check_card = conn.cursor()
            cur_check_card.execute(f"SELECT balance FROM card WHERE number = {card}")
            if cur_check_card.fetchall()[0][0] < money:
                print("Not enough money!\n")
                continue
            do_transfer(card, enter_card, money)
            print("Success!\n")
        elif var == '4':
            cur_del = conn.cursor()
            cur_del.execute(f"DELETE FROM card WHERE number = {card}")
            conn.commit()
            cur_del.close()
            print('\nThe account has been closed!\n')
            break
        elif var == '5':
            print('\nYou have successfully logged out!\n')
            break
        elif var == '0':
            print("Bye!")
            exit()


def do_transfer(card, enter_card, money):
    cur_do = conn.cursor()
    cur_do.execute(f"SELECT balance FROM card WHERE number = {card}")
    b_one = cur_do.fetchall()[0][0]
    cur_do.execute(f"SELECT balance FROM card WHERE number = {enter_card}")
    b_two = cur_do.fetchall()[0][0]
    cur_do.close()
    cur_do = conn.cursor()
    cur_do.execute(f"UPDATE card SET balance = {b_one - money} WHERE number = {card}")
    conn.commit()
    cur_do.close()
    cur_do = conn.cursor()
    cur_do.execute(f"UPDATE card SET balance = {b_two + money} WHERE number = {enter_card}")
    conn.commit()
    cur_do.close()


def log_in_check(card, pin):
    conn_login = sqlite3.connect("card.s3db")
    cur_login = conn_login.cursor()
    cur_login.execute(f"SELECT number FROM card WHERE number = {card}")
    numbers = [x[0] for x in cur_login.fetchall()]
    cur_login.execute(f"SELECT pin FROM card WHERE number = {card}")
    if card in numbers:
        pins = cur_login.fetchall()[0][0]
        if pin == pins:
            return True
        else:
            print('\nWrong card number or PIN!\n')
            return False
    else:
        print('\nWrong card number or PIN!\n')
        return False


def main():
    choice = input(
        '1. Create an account\n'
        '2. Log into account\n'
        '0. Exit\n'
    )
    if choice == '1':
        Account()
    elif choice == '2':
        card_number = input('\nEnter your card number:\n')
        card_pin = input('Enter your PIN:\n')
        if log_in_check(card_number, card_pin):
            print("\nYou have successfully logged in!\n")
            log_in_menu(card_number)
        else:
            print("\nWrong card number or PIN!\n")
    elif choice == '0':
        exit()


def luhn_algorithm_checking(number, letter):
    check_sum = 0
    k = 0
    for x in number:
        plus = int(x)
        if k % 2 == 0:
            plus *= 2
            if plus > 9:
                plus -= 9
            check_sum += plus
        else:
            check_sum += plus
        k += 1

    if check_sum % 10 == 0:
        return letter == '0'
    else:
        return letter == str(10 - check_sum % 10)


def luhn_algorithm(number):
    check_sum = 0
    k = 0
    for x in number:
        plus = int(x)
        if k % 2 == 0:
            plus *= 2
            if plus > 9:
                plus -= 9
            check_sum += plus
        else:
            check_sum += plus
        k += 1

    if check_sum % 10 == 0:
        return '0'
    else:
        return str(10 - check_sum % 10)


def check_number(number):
    cur_for_check = conn.cursor()
    cur_for_check.execute("""SELECT number FROM card""")
    all_cards = cur_for_check.fetchall()
    conn.commit()
    cur_for_check.close()
    if number in all_cards:
        return True
    return False


if __name__ == "__main__":
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS card ( 
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );""")
    conn.commit()
    cur.close()
    while True:
        main()
