"""Banking System Login Implementation."""

import json
import os
import time

import pandas as pd

from base import Base


class BankingSystemLogin(object):
    """Login for Banking System."""

    def __init__(self):
        """Init function for Login."""
        self.base = Base()
        os.system('cls' if os.name == 'nt' else 'clear')

    def authenticate_credentials(self):
        """Check for valid credentials."""
        retry = 0
        flag = 0
        csv_df = pd.read_csv(self.base.csv_file, usecols=['account_id', 'full_name'], header=0)
        while retry < 5:
            ch = input('\nEnter 0 to return to Main Page.\nOr ENTER To Continue\n')
            if ch == '0':
                return 0
            else:
                acc_id = int(input("\nEnter your account id:"))
                fname = str(input('\nEnter your full name as per the account:'))
                for key, value in csv_df.iterrows():
                    if value['account_id'] == acc_id and value['full_name'] == fname:
                        flag = 1
                        os.system('cls' if os.name == 'nt' else 'clear')
                if flag == 1:
                    self.login_page(acc_id)
                else:
                    print('\n Login Failed')


    def print_details(self, data):
        """Prints the details of the dataset.

        :param data: Dataframe of account row
        """
        row_num = data.index[0]

        list_of_data = ['Account ID: ', 'Full Name: ', 'IFSC Code: ', 'Aadhaar Number: ', 'Address: ',
                        'Current Balance: ', 'Mobile Number: ', 'Debit Card Number: ', 'Debit Card Pin: ',
                        'Debit Card CVV: ', 'Credit Card Number: ', 'Credit Card Pin: ', 'Credit Card CVV: ']
        list_to_func = {'Account ID: ': "str(data['account_id'][row_num])", 'Full Name: ': "data['full_name'][row_num]",
                        'IFSC Code: ': "data['ifsc_code'][row_num]",
                        'Aadhaar Number: ': "str(data['aadhaar_number'][row_num])",
                        'Address: ': "data['address'][row_num]", 'Current Balance: ': "str(data['balance'][row_num])",
                        'Mobile Number: ': "str(data['mobile_number'][row_num])",
                        'Debit Card Number: ': "str(data['dc_number'][row_num])",
                        'Debit Card Pin: ': "str(data['dc_pin'][row_num])",
                        'Debit Card CVV: ': "str(data['dc_cvv'][row_num])",
                        'Credit Card Number: ': "str(data['cc_number'][row_num])",
                        'Credit Card Pin: ': "str(data['cc_pin'][row_num])",
                        'Credit Card CVV: ': "str(data['cc_cvv'][row_num])"}
        print('\nThe Account Details are as follows:')

        for indx, i in enumerate(list_of_data):
            print('{}{}'.format(list_of_data[indx], eval(list_to_func[list_of_data[indx]])))

        print('*' * 15)

    def list_of_beneficiaries(self, row):
        """Lists the beneficiaries for the account id.

        :param row: Dataframe of account row
        """
        ben_df = pd.read_csv(self.base.ben_csv_file, na_filter=False)
        val = row['account_id'].values[0]
        ben_row_df = ben_df.loc[ben_df['account_id'] == int(val)]
        if ben_row_df.empty:
            print('\nNO BENEFICIARIES CURRENTLY PRESENT. GO BACK TO ADD THE SAME.')
        else:
            print('\nLIST OF BENEFICIARIES\n')
            output_df = pd.DataFrame(columns=['FULL NAME', 'ACCOUNT ID', 'IFSC CODE'])
            for key, value in ben_row_df.iterrows():
                output_df.loc[key, ['FULL NAME']] = value['ben_fname']
                output_df.loc[key, ['ACCOUNT ID']] = int(value['ben_acc_id'])
                output_df.loc[key, ['IFSC CODE']] = value['ben_ifsc_code']
            print(output_df.to_string(index=False))
        return 0

    def list_of_cards(self, row):
        """Display the list of cards associated with the account id.

        :param row: Dataframe of account row
        """
        print('\nDEBIT CARD INFO: ')
        print('CARD NUMBER: ' + row['dc_number'].values[0])
        print('CARD PIN: ' + row['dc_pin'].values[0])
        print('CARD CVV' + row['dc_pin'].values[0])

        print('\nCREDIT CARD INFO: ')
        print('CARD NUMBER: ' + row['cc_number'].values[0])
        print('CARD PIN: ' + row['cc_pin'].values[0])
        print('CARD CVV' + row['cc_pin'].values[0])
        print('*' * 15)
        return 0

    def add_beneficiary(self, row):
        """Function to add a beneficiary for an account.

        :param row: Dataframe of account row
        """
        print('\nADDING BENEFICIARY FOR ACCOUNT ID: ' + str(row['account_id'].values[0]))

        while True:
            flag = 0
            fname = self.base.full_name()
            print('ENTER ACCOUNT ID OF BENEFICIARY: ')
            ben_acc = str(input())
            if self.base.check_account(ben_acc):
                print('\nAccount ID Should Be 16 Digit.')
                flag = 1
                continue
            print('ENTER IFSC CODE OF BENEFICIARY: ')
            ben_ifsc = str(input())
            if self.base.check_ifsc(ben_ifsc):
                print('\nIFSC Code should consist of first 4 Characters and last 7 Digits')
                flag = 1
                continue
            if flag == 0:
                break
        add_ben = {
            'account_id': [str(row['account_id'].values[0])],
            'ben_acc_id': [ben_acc],
            'ben_ifsc_code': [ben_ifsc],
            'ben_fname': [fname]
        }
        load_ben_dict = json.dumps(add_ben)
        ben_data = json.loads(load_ben_dict)
        csv_file = self.base.ben_csv_file
        for line in csv_file:
            if line:
                headers = False
                break
            else:
                headers = True
                break
        (pd.DataFrame.from_dict(data=ben_data, orient='columns').
         to_csv(csv_file, index=False, mode='a', header=headers))
        return 0

    def card_info(self, card):
        """Function to update card pin.

        :param card: String value to depict whether it is Credit/Debit card
        """
        while True:
            print('\nEnter your New {} Card Pin'.format(card))
            pin = str(input())
            if not (pin.isdigit()):
                print('\nEnter Digits as your Pin')
            elif len(pin) != 4:
                print('\nEnter a 4 digit code')
            else:
                return pin

    def update_account_info(self, row):
        """Update account information for client.

        :param row: Dataframe of account row
        """
        while True:
            row_num = row.index[0]
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\nUPDATE YOUR ACCOUNT INFORMATION.')
            list_of_data = ['Full Name', 'Address', 'Aadhaar Number',
                            'Mobile Number', 'Debit Card Pin', 'Credit Card Pin']
            for indx, i in enumerate(list_of_data):
                print('{}. Update your {}'.format(indx + 1, i))
            print('\nEnter 0 to exit.')
            print('Enter your choice')

            data_to_func = {'Full Name': 'self.base.full_name()', 'Address': 'str(input("Enter your new Address"))',
                            'Aadhaar Number': 'self.base.aadhaar()', 'Mobile Number': 'self.base.mobile_number()',
                            'Debit Card Pin': 'self.card_info("Debit")', 'Credit Card Pin': 'self.card_info("Credit")'}
            list_of_df = {'1': 'full_name', '2': 'address', '3': 'aadhaar_number', '4': 'mobile_number', '5': 'dc_pin',
                          '6': 'cc_pin'}
            inp = str(input())
            if inp == '0':
                return row
            for indx, i in enumerate(list_of_data):
                if indx == (int(inp) - 1):
                    var = data_to_func[list_of_data[indx]]
                    df_col = list_of_df[inp]
                    row.at[row_num, df_col] = eval(var)
                    input('Values Updated. \nPress Enter to continue. ')
                    break

    def transfer_funds(self, row):
        """Transfer Funds from/to account.

        :param row: Dataframe of account row.
        """
        choice = input('\n1.ADD FUNDS TO YOUR ACCOUNT\n2.TRANSFER FUNDS TO ANOTHER ACCOUNT.')
        row_num = row.index[0]
        if choice == '1':
            add = int(input('\nEnter the amount to be added\n'))
            sum = add + int(row.at[row_num, 'balance'])
            row.at[row_num, 'balance'] = str(sum)
        elif choice == '2':
            while True:
                print('\nCurrent Balance: {}'.format(row.at[row_num, 'balance']))
                sub = int(input('\nEnter the amount to be transferred\n'))
                if sub > int(row.at[row_num, 'balance']):
                    print('Amount to be transferred is greater than your balance.')
                    input('Press Enter to retry')
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    final_val = int(row.at[row_num, 'balance']) - sub
                    row.at[row_num, 'balance'] = str(final_val)
                    break
        print('\nBalance has been updated.')
        return row

    def add_credit_card(self, row):
        """Transfer Funds from/to account.

        :param row: Dataframe of account row.
        """
        while True:
            row_num = row.index[0]
            ch = input('\nEnter 1.To change Credit Card Number\n2.To change Credit Card CVV')
            if ch == '1':
                row.at[row_num, 'cc_number'] = self.base.get_random_value(16)
            elif ch == '2':
                row.at[row_num, 'cc_cvv'] = self.base.get_random_value(3)
            else:
                print('\nEnter a valid option')
                input('\nPress Enter to try again')
                os.system('cls' if os.name == 'nt' else 'clear')
            print('\nNew Card Details: \n Card Number: {}\n Card CVV: {}'.format(row.at[row_num, 'cc_number'],
                                                                                 row.at[row_num, 'cc_cvv']))
            break
        return row

    def login_page(self, account_id):
        """Main page after successful login of client.

        :param account_id: Notifies the account id used for login.
        """
        print('*' * 15)
        print('Login Successful')
        print('*' * 15)
        home_screen_options = ["DISPLAY LIST OF BENEFICIARIES", "DISPLAY LIST OF CARDS", "ADD A BENEFICIARY",
                               "UPDATE ACCOUNT INFORMATION", "TRANSFER FUNDS", "REGISTER NEW CREDIT CARD", "EXIT"]
        option_to_func = {'DISPLAY LIST OF BENEFICIARIES': self.list_of_beneficiaries,
                          'DISPLAY LIST OF CARDS': self.list_of_cards,
                          'ADD A BENEFICIARY': self.add_beneficiary,
                          'UPDATE ACCOUNT INFORMATION': self.update_account_info,
                          'TRANSFER FUNDS': self.transfer_funds,
                          'REGISTER NEW CREDIT CARD': self.add_credit_card,
                          'EXIT': None}
        while True:
            csv_df = pd.read_csv(self.base.csv_file, dtype=str)
            row_df = csv_df.loc[csv_df['account_id'] == str(account_id)]
            self.print_details(row_df)
            for idx, i in enumerate(home_screen_options):
                print('CHOOSE {} TO {}'.format(idx + 1, i))
            opt = input('PLEASE ENTER SELECTION: ')
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                value = option_to_func[home_screen_options[int(opt) - 1]](row_df)
                input('\n PRESS ENTER TO CONTINUE...')
                os.system('cls' if os.name == 'nt' else 'clear')

                if not value.empty:
                    self.base.write_data(value, self.base.csv_file, self.base.csv_columns)
                    self.base.remove_duplicate(self.base.csv_file, self.base.csv_columns)
            except IndexError as e:
                print('NOT A VALID OPTION')
            except AttributeError:
                print('\nReturning to Menu')
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')

    def login_main(self):
        """Login page for client."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('***LOGIN MAIN PAGE***\n\n')
            print('1. ENTER DETAILS TO GO TO LOGIN PAGE')
            print('2. EXIT')
            ch = str(input())
            try:
                if ch == '1':
                    self.authenticate_credentials()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif ch == '2':
                    print('\tThank You for using bank management system.')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    print('Invalid choice.')

            except Exception:
                input('PRESS ENTER TO RETURN TO LOGIN PAGE')
