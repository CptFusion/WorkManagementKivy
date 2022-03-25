from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRoundFlatButton
from kivy.lang.builder import Builder
from kivy.uix.button import Button
import os
import sqlite3
from kivy.uix.popup import Popup


def create_new_contact(path):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        Customer_list_and_add(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)


def Customer_list_and_add(cursor):
    cursor.execute(
        '''
        CREATE TABLE Customers(
        ID INT PRIMARY KEY NOT NULL,
        NAME            TEXT NOT NULL,
        LOCATION        TEXT NOT NULL,
        AREA            TEXT NOT NULL,

        CUSTOMER_SINCE  TEXT NOT NULL,
        OBTAINED_BY     TEXT NOT NULL,
        ROYALTY_TO      TEXT NOT NULL,

        CONTACT         TEXT NOT NULL,
        ADDRESS         TEXT NOT NULL,
        CITY            TEXT NOT NULL,
        STATE           TEXT NOT NULL,

        PHONE           TEXT NOT NULL,
        EMAIL           TEXT NOT NULL,
        FAX             TEXT NOT NULL
        )'''
    )


class MessagePopup(Popup):
    pass


class MainWid(ScreenManager):

    ### this is the main Widget / App and the defenitions
    def __init__(self, **kwargs):
        super(MainWid, self).__init__()

        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH + "/my_database.db"
        self.MainWindow = MainWindow(self)
        self.Customer_List_Window = Customer_List_Window(self)
        self.LogInScreen = LogInScreen(self)
        ### This helps to clear out previous saved cust
        self.Create_Cus_Window = BoxLayout()

        ###This is for updating the cus cell blcok
        self.Update_cus_Cell_Block = BoxLayout()
        ###This is for the error pop up messages
        self.Popup = MessagePopup()

        #### These are the windows and the order in which they are called

        wid = Screen(name='loginscreen')
        wid.add_widget(self.LogInScreen)
        self.add_widget(wid)

        wid = Screen(name='start')
        wid.add_widget(self.MainWindow)
        self.add_widget(wid)

        wid = Screen(name='customer list')
        wid.add_widget(self.Customer_List_Window)
        self.add_widget(wid)

        wid = Screen(name='Create_Cus_Window')
        wid.add_widget(self.Create_Cus_Window)
        self.add_widget(wid)

        wid = Screen(name='Updatecusdata')
        wid.add_widget(self.Update_cus_Cell_Block)
        self.add_widget(wid)

        self.goto_start()

    ### This defines which screen the app starts with:
    def goto_start(self):
        self.current = 'loginscreen'

    def log_in_press(self):
        self.current = 'start'

    def cus_list(self):
        self.Customer_List_Window.check_memory()
        self.current = 'customer list'

    def goto_new_cus_data(self):
        self.Create_Cus_Window.clear_widgets()
        wid = Create_Cus_Window(self)
        self.Create_Cus_Window.add_widget(wid)
        self.current = 'Create_Cus_Window'

    def goto_updatecusdata(self, cus_data_id):
        self.Update_cus_Cell_Block.clear_widgets()
        wid = Update_cus_Cell_Block(self, cus_data_id)
        self.Update_cus_Cell_Block.add_widget(wid)
        self.current = 'Updatecusdata'


### This section is linked to the Main.Kv file and defines parameters of windows


class LogInScreen(Screen):
    def __init__(self, mainwid, **kwargs):
        super(LogInScreen, self).__init__()
        self.mainwid = mainwid
        self.current = 'LogInScreen'

    def log_in(self):
        self.mainwid.log_in_press()


class MainWindow(Screen):
    def __init__(self, mainwid, **kwargs):
        super(MainWindow, self).__init__()
        self.mainwid = mainwid
        self.current = 'Create_Cus_Window'

    def create_new_customer(self):
        create_new_contact(self.mainwid.DB_PATH)
        self.mainwid.cus_list()

    def Logout(self):
        self.mainwid.goto_start()


class Customer_List_Window(Screen):
    def __init__(self, mainwid, **kwargs):
        super(Customer_List_Window, self).__init__()
        self.mainwid = mainwid

    ### this checks and refreshes memory
    def check_memory(self):
        self.ids.cus_list_cont.clear_widgets()
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        cursor.execute('select ID, NAME, LOCATION, AREA, CUSTOMER_SINCE, OBTAINED_BY, ROYALTY_TO, CONTACT, ADDRESS, '
                       'CITY, STATE, PHONE, EMAIL, FAX from Customers')
        for i in cursor:
            wid = CusDataWid(self.mainwid)
            r1 = 'ID: ' + str(100000000 + i[0])[1:9] + '\n'
            r2 = i[1] + '\n'
            r3 = i[2] + ', ' + i[3] + '\n'
            r4 = i[4] + ', ' + i[5] + ', ' + i[6] + '\n'
            r5 = i[7] + '\n'
            r6 = i[8] + ', ' + i[9] + ', ' + i[10] + '\n'
            r7 = i[11] + ', ' + i[12] + ', ' + i[13] + '\n'

            wid.cus_data_id = str(i[0])
            wid.data = r1 + r2 + r3 + r4 + r5 + r6 + r7
            self.ids.cus_list_cont.add_widget(wid)

        wid = NewCusButton(self.mainwid)
        wid2 = BackButton(self.mainwid)
        self.ids.cus_list_cont.add_widget(wid)
        self.ids.cus_list_cont.add_widget(wid2)
        con.close()


class Create_Cus_Window(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(Create_Cus_Window, self).__init__()
        self.mainwid = mainwid

    def insert_cus_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()

        d1 = self.ids.ti_id.text
        d2 = self.ids.ti_name.text
        d3 = self.ids.ti_location.text
        d4 = self.ids.ti_area.text

        d5 = self.ids.ti_cussince.text
        d6 = self.ids.ti_obtained.text
        d7 = self.ids.ti_royalty.text

        d8 = self.ids.ti_contact.text
        d9 = self.ids.ti_address.text
        d10 = self.ids.ti_city.text
        d11 = self.ids.ti_state.text

        d12 = self.ids.ti_phone.text
        d13 = self.ids.ti_email.text
        d14 = self.ids.ti_fax.text

        a1 = (d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14)
        # for the quiry underneath "customers comes from the table created on the top"
        s1 = 'INSERT INTO Customers(ID, NAME, LOCATION, AREA, CUSTOMER_SINCE, OBTAINED_BY, ROYALTY_TO, CONTACT, ' \
             'ADDRESS, CITY, STATE, PHONE, EMAIL, FAX)'
        # for text or things that dont have function put ""// numbers or functions dont have anything.
        s2 = 'VALUES(%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % a1

        try:
            cursor.execute(s1 + ' ' + s2)
            con.commit()
            con.close()
            self.mainwid.cus_list()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Inconpleate Fields"
            if '' in a1:
                message.text = 'Nessesary Fields Not FIlled'

            else:
                message.text = str(e)
            con.close()

    def Cancel_cus_data(self):
        self.mainwid.cus_list()


class Update_cus_Cell_Block(BoxLayout):
    def __init__(self, mainwid, cus_data_id, **kwargs):
        super(Update_cus_Cell_Block, self).__init__()
        self.mainwid = mainwid
        self.cus_data_id = cus_data_id
        self.check_memory()

    def check_memory(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'select NAME, LOCATION, AREA, CUSTOMER_SINCE, OBTAINED_BY, ROYALTY_TO, CONTACT, ADDRESS, CITY, STATE, ' \
            'PHONE, EMAIL, FAX from Customers where ID='
        cursor.execute(s + self.cus_data_id)
        for i in cursor:
            self.ids.ti_name.text = i[0]
            self.ids.ti_location.text = i[1]
            self.ids.ti_area.text = i[2]
            self.ids.ti_cussince.text = i[3]
            self.ids.ti_obtained.text = i[4]
            self.ids.ti_royalty.text = i[5]
            self.ids.ti_contact.text = i[6]
            self.ids.ti_address.text = i[7]
            self.ids.ti_city.text = i[8]
            self.ids.ti_state.text = i[9]
            self.ids.ti_phone.text = i[10]
            self.ids.ti_email.text = i[11]
            self.ids.ti_fax.text = i[12]
        con.close()

    def update_cus_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.ti_name.text
        d2 = self.ids.ti_location.text
        d3 = self.ids.ti_area.text

        d4 = self.ids.ti_cussince.text
        d5 = self.ids.ti_obtained.text
        d6 = self.ids.ti_royalty.text

        d7 = self.ids.ti_contact.text
        d8 = self.ids.ti_address.text
        d9 = self.ids.ti_city.text
        d10 = self.ids.ti_state.text

        d11 = self.ids.ti_phone.text
        d12 = self.ids.ti_email.text
        d13 = self.ids.ti_fax.text

        a1 = (d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13)
        s1 = 'UPDATE Customers SET'
        s2 = 'NAME="%s",  LOCATION="%s",  AREA="%s",  CUSTOMER_SINCE="%s",  OBTAINED_BY="%s",  ROYALTY_TO="%s",  ' \
             'CONTACT="%s",  ADDRESS="%s",  CITY="%s", STATE="%s", PHONE="%s", EMAIL="%s", FAX="%s" ' % a1
        s3 = 'WHERE ID=%s' % self.cus_data_id
        try:
            cursor.execute(s1 + ' ' + s2 + ' ' + s3)
            con.commit()
            con.close()
            self.mainwid.cus_list()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'One or more neccesary fields empty'
            else:
                message.text = str(e)
            con.close()

    def delete_cus(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'delete from Customers where ID=' + self.cus_data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.mainwid.cus_list()

    def back_to_cusDB(self):
        self.mainwid.cus_list()


# This is the Widget that appears when cus is creaeted
class CusDataWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(CusDataWid, self).__init__()
        self.mainwid = mainwid

    def update_data(self, cus_data_id):
        self.mainwid.goto_updatecusdata(cus_data_id)


class NewCusButton(Button):
    def __init__(self, mainwid, **kwargs):
        super(NewCusButton, self).__init__()
        self.mainwid = mainwid

    #### This creates the new buttons*?

    def create_new_customerB(self):
        self.mainwid.goto_new_cus_data()


class BackButton(Button):
    def __init__(self, mainwid, **kwargs):
        super(BackButton, self).__init__()
        self.mainwid = mainwid


class MainApp(MDApp):
    title = 'Fusion Window Cleaning'

    def build(self):
        return MainWid()


if __name__ == '__main__':
    MainApp().run()
