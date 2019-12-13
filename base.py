"""Base class for Banking System."""
import random
import pandas as pd
import re


class Base(object):
    """Implements base functionality."""

    csv_file = '/home/pranjalesh/PycharmProjects/banking_system/database/account_info.csv'
    ben_csv_file = '/home/pranjalesh/PycharmProjects/banking_system/database/beneficiary.csv'
    csv_columns = ['account_id', 'full_name', 'ifsc_code', 'aadhaar_number', 'address', 'balance', 'mobile_number',
                   'dc_number', 'dc_pin', 'dc_cvv', 'cc_number', 'cc_pin', 'cc_cvv']

    def __init__(self):
        """Init method."""
        pass

    def get_random_value(self, power):
        """Returns a random 16 digit integer"""
        return random.randrange(1*pow(10, power-1), 1*pow(10, power))

    @staticmethod
    def full_name():
        """Get the correct full_name from user.
            :return: String, full_name
        """
        while True:
            full_name = str(input("\tEnter Full Name : ")).strip()
            if bool(re.findall(r'[0-9]+', full_name)):
                print("\nFull Name Should Not Consist of Digits.\n")
                continue
            else:
                return full_name

    def aadhaar(self):
        """Get the correct aadhaar number from user.
            :return: String, aadhaar number
        """
        while True:
            aadhaar_card = str(input("\tEnter your Aadhaar Card number : "))
            try:
                if len(aadhaar_card) != 16 and int(aadhaar_card):
                    print("\nPlease Enter 16 digit Aadhaar card number.\n")
                    continue
                else:
                    break
            except ValueError:
                print("\nPlease Enter 16 digit Aadhaar card number.\n")
                continue
        return aadhaar_card

    def mobile_number(self):
        """Get the correct mobile number from user.
            :return: String, full_name"""
        while True:
            mob_number = str(input("\tEnter your 10 digit mobile number : "))
            try:
                if len(mob_number) == 10 and int(mob_number):
                    break
                else:
                    print("\nPlease Enter your 10 digit mobile number (should be digit)\n")
                    continue
            except ValueError as e:
                print("\nPlease Enter your 10 digit mobile number (should be digit)\n")
                continue
        return mob_number

    def check_account(self, acc):
        """Checks if account_id is a 16 digit number.

        :param acc: Account id entered by the user.
        """
        if not acc.isdigit() and len(acc) != 16:
            return True
        else:
            return False

    def check_ifsc(self, ifsc):
        """Checks if account_id is a 16 digit number.

        :param ifsc: Account id entered by the user.
        """
        if bool(re.findall(r'[a-z]', (ifsc[:4]).lower())) and ifsc[4:].isdigit() and len(ifsc) == 11:
            return False
        else:
            return True

    def write_data(self, data_frame, filename, column_name):
        """Append the data in filename.

        :params data_frame: data frame, row to be written.
        :params filename: file name to write.
        :params columnname: column name of file.
        """
        with open(filename, 'a') as f:
            data_frame.to_csv(f, header=False, index=False, columns=column_name)

    def remove_duplicate(self, filename, column_name):
        """Remove Duplicates From dataframe.

        :param filename: csv Filename in which duplicates are searched.
        :param column_name: Name of columns present in filename.
        """
        account_df = pd.read_csv(filename, dtype=str, header=0)
        clean_account_df = account_df.drop_duplicates(subset='account_id', keep="last")
        clean_account_df.to_csv(filename, header=True, index=False, columns=column_name)
