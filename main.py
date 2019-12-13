"""Main File For Banking System."""

from login import BankingSystemLogin
from registration import BankingSystemRegistration

if __name__ == '__main__':
    register = BankingSystemRegistration()
    login_user = BankingSystemLogin()
    retry = 0
    while True:
        while retry < 3:
            print('\nMAIN MENU')
            print('\n1. LOGIN FOR EXISTING USER')
            print('\n2. REGISTER A NEW USER')
            print('\n9. EXIT')
            input_val = input('Enter your choice\n')

            if input_val == '1':
                login_user.login_main()
            elif input_val == '2':
                register.get_full_details()
            elif input_val == '9':
                print('Exiting out of Banking System.')
                exit(0)
            else:
                print('\nThis value is not defined. Choose between 1, 2 or 9.\n')
                retry += 1
        print('\nNumber of retries exceeded.')
        exit(0)
