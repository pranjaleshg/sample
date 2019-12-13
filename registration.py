"""Banking System Registration Implementation."""

from base import Base

import os
import json
import pandas as pd


class BankingSystemRegistration(object):
    """Registration for Banking System."""

    def __init__(self):
        """Init class for Registration."""
        self.base = Base()

    @staticmethod
    def print_details(data):
        """Print all the account related details.

        :param data: Dataframe of account row
        """
        list_of_data = ['Account ID: ', 'Full Name: ', 'IFSC Code: ', 'Aadhaar Number: ', 'Address: ',
                        'Current Balance: ', 'Mobile Number: ', 'Debit Card Number: ', 'Debit Card Pin: ',
                        'Debit Card CVV: ', 'Credit Card Number: ', 'Credit Card Pin: ', 'Credit Card CVV: ']
        list_to_func = {'Account ID: ': "data['account_id'][0]", 'Full Name: ': "data['full_name'][0]",
                        'IFSC Code: ': "data['ifsc_code'][0]", 'Aadhaar Number: ': "data['aadhaar_number'][0]",
                        'Address: ': "data['address'][0]", 'Current Balance: ': "data['balance'][0]",
                        'Mobile Number: ': "data['mobile_number'][0]", 'Debit Card Number: ': "data['dc_number'][0]",
                        'Debit Card Pin: ': "data['dc_pin'][0]", 'Debit Card CVV: ': "data['dc_cvv'][0]",
                        'Credit Card Number: ': "data['cc_number'][0]", 'Credit Card Pin: ': "data['cc_pin'][0]",
                        'Credit Card CVV: ': "data['cc_cvv'][0]"}
        print('*' * 15)

        for indx, i in enumerate(list_of_data):
            print('{}{}'.format(list_of_data[indx], eval(list_to_func[list_of_data[indx]])))
        print('*' * 15)

        print('\nACCOUNT CREATED SUCCESSFULLY')
        print('\n*****NOTE DOWN THE ACCOUNT DETAILS.*****')

    def get_full_details(self):
        """Retrieve full details of applicant."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\t***REGISTRATION MENU***\n\n")
            print("\t1. ENTER DETAILS FOR REGISTRATION")
            print("\t2. EXIT")
            print("\n\tSelect Your Option (1-2)\n")
            ch = str(input())
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                print('\nEntering Details For Registration')
                if ch == '1':
                    full_name = self.base.full_name()
                    aadhaar_card = self.base.aadhaar()
                    address = input("\n\tEnter your address : ")
                    mobile_number = self.base.mobile_number()

                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('*' * 15)
                    print('\nACCOUNT DETAILS::')
                    print('\nYour full name:' + full_name)
                    print('\nYour Aadhaar Number:' + aadhaar_card)
                    print('\nYour Address:' + address)
                    print('\nYour Mobile Number:' + mobile_number)
                    print('*' * 15)

                    print('\nEnter 1 if to re-enter your details')
                    print('\nEnter 2 to continue')
                    verify = str(input())
                    if verify == '1':
                        continue
                    elif verify == '2':
                        balance = str(0)
                        ifsc_code = "ABCD1234567"
                        account_id = str(self.base.get_random_value(16))
                        dc_number = str(self.base.get_random_value(16))
                        dc_pin = str(self.base.get_random_value(4))
                        dc_cvv = str(self.base.get_random_value(3))
                        cc_number = str(self.base.get_random_value(16))
                        cc_pin = str(self.base.get_random_value(4))
                        cc_cvv = str(self.base.get_random_value(3))
                    else:
                        print('\nEnter a valid choice')
                        continue

                    load_data_dict = {'account_id': [account_id], 'full_name': [full_name], 'ifsc_code': [ifsc_code],
                                      'aadhaar_number': [aadhaar_card], 'address': [address], 'balance': [balance],
                                      'mobile_number': [mobile_number], 'dc_number': [dc_number], 'dc_pin': [dc_pin],
                                      'dc_cvv': [dc_cvv], 'cc_number': [cc_number], 'cc_pin': [cc_pin],
                                      'cc_cvv': [cc_cvv]}

                    self.print_details(load_data_dict)
                    input('\n Press Enter to Continue...')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    load_data_dict = json.dumps(load_data_dict)
                    client_data = json.loads(load_data_dict)
                    csv_file = self.base.csv_file
                    for line in csv_file:
                        if line:
                            headers = False
                        else:
                            headers = True

                    (pd.DataFrame.from_dict(data=client_data, orient='columns').
                     to_csv(csv_file, index=False, mode='a', header=headers))

                    break
                elif ch == '2':
                    print("\tThanks for using bank management system")
                    break
                else:
                    print("Invalid choice")
                os.system('cls' if os.name == 'nt' else 'clear')
            except NameError:
                print("Select Your Option (1-2)")
                ch = str(input("please use integer value \nEnter your choice : "))
            except SyntaxError:
                print("Please use 1 character \n Select Your Option (1-2)")
                ch = str(input("Enter your choice : "))
