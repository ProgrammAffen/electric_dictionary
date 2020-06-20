'''
客户显示界面
'''
from client_bll import *
class ManagerView:
    def __init__(self):
        self.manager = ClientController()
    def get_name(self):
        name = self.sign_in()
        return name
    def usr_register(self):
        while True:
            name = input('Please enter name')
            password = input('Please enter password')
            res = self.manager.register(name,password)
            if res == False:
                print('User name already exists')
                continue
            else:
                print('Register succeeded !')
                return True
    def sign_in(self):
        while True:
            name = input('Please enter name')
            password = input('Please enter password')
            res = self.manager.log_in(name,password)
            if res == True:
                print('Log in secceeded')
                return name
            else:
                print('User name or password is wrong')
                continue
    def sign_out(self):
        self.manager.log_out()
    def look_up_word(self):
        name = self.get_name()
        word = input('please enter the word you want to look up')
        word1 = self.manager.find_word(name,word)
        if word1 == False:
            print('The word is not included')
        else:
            print(word1)
    def look_up_history(self):
        name = self.get_name()
        res = self.manager.get_history(name)
        if res == False:
            print('Unknown Error')
            return
        else:
            tuple1 = eval(res)
            print('the checking up history of',name,":\n")
            for item in tuple1:
                print(item[0],item[1],sep = '\t',end = '\n')
    def print_1_class_menu(self):
        print('**************************')
        print('1) Register               ')
        print('2) Log in                 ')
        print('q) Log out                ')
        print('**************************')
    def print_2_class_menu(self):
        print('**************************')
        print('1) Look up word           ')
        print('2) Acquire history        ')
        print('b) Back to log in         ')
        print('**************************')
    def main1(self):
        while True:
            self.print_1_class_menu()
            choice = input('Please enter your choice')
            if choice == '1':
                res = self.usr_register()
                if res == True:
                    ch1 = input('enter T to get to dictionary,enter B to go to main menu')
                    if ch1 == 'T':
                        self.main2()
                    elif ch1 == 'B':
                        break
                    else:
                        continue
            elif choice == '2':
                self.sign_in()
                self.main2()

            elif choice == 'q':
                self.sign_out()
    def main2(self):
            while True:
                self.print_2_class_menu()
                ch = input('please enter your choice')
                if ch == '1':
                    while True:
                        try:
                            self.look_up_word()
                        except KeyboardInterrupt:
                            print('Quit dictionary')
                            return
                elif ch == '2':
                    self.look_up_history()
                elif ch == 'b':
                    return