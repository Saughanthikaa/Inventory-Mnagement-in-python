import mysql.connector
from datetime import date

mydb = mysql.connector.connect(host="localhost", user="root", password="hello123", database="inventory")
# print(mydb)
if (mydb):
    print('Connection Successful')
else:
    print('Connection Unsuccessful')
mycursor = mydb.cursor()

def customer():
    print('1.NEW CUSTOMER\n2.LOGIN\n3.GO BACK')
    ch1=int(input('ENTER YOUR CHOICE :'))
    if ch1==1:
        cust_id=int(input('ENTER NEW ID :'))
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("select cust_id from customers_details ")
        for i in mycursor:
            i=int(i[0])
            print(i)
            if i==cust_id:
                print('ID ALREADY EXISTS!...CREATE ACCOUNT WITH ANOTHER ID OR YOU MAY LOGIN WITH THIS ID!')
                customer()
        cust_name=input('ENTER YOUR NAME :')
        customer_1(cust_id,cust_name)
    elif ch1==2:
        cust_id=int(input('ENTER YOUR ID :'))
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("select cust_id from customers_details ")
        for i in mycursor:
            i = int(i[0])
            #print(i)
            if i == cust_id:
                print('LOGIN SUCCESSFUL! YOU CAN CONTINUE YOUR SHOPPING!')

                sqlselect="select cust_name from customers_details where cust_id=%s"
                data=(cust_id,)
                mycursor = mydb.cursor(buffered=True)
                mycursor.execute(sqlselect,data)
                for i in mycursor:
                    cust_name=str(i[0])
                customer_1(cust_id,cust_name)

        print('ID DOES NOT EXIST! CREATE NEW ID')
        customer()
    elif ch1==3:
        main()


def customer_1(cust_id,cust_name):
    print('1.PURCHASE FROM SHOP\n2.VIEW YOUR ORDERS\n3.GO BACK')
    ch = int(input('ENTER YOUR CHOISE :'))
    today = date.today()  # to calculate purchase date
    if ch == 1:
        mycursor = mydb.cursor()
        mycursor.execute("Select * from shop_details")    #
        for ddbb in mycursor:                             # display part of godown_details (erroorrrr if we call the function)
            print(ddbb)                                   #

        s_id = int(input('PRODUCT ID TO BUY :'))
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("select sp_id from shop_details")
        for i in mycursor:
            i = int(i[0])
            # print('i value is',i)
            # print('s_is is',s_id)
            if i == s_id:
                sqlstate = "select * from shop_details where sp_id=%s"
                data1 = (s_id,)  # Since you are using mysql module, cursor.execute requires a sql query and a tuple as parameters
                mycursor.execute(sqlstate, data1)
                for db in mycursor:
                    id = db[0]
                    name = db[1]
                    price = db[2]
                    quantity = db[3]
                    print('PRODUCT : ', name, '\t\tPRICE  :  ', price, '\t\tQUANTITY  : ', quantity)
                s_quantity = int(input('ENTER THE QUANTITY TO PURCHASE :'))

                if (quantity >= s_quantity):
                    sqlstate1 = "update shop_details set sp_quantity=sp_quantity-%s where sp_id=%s"
                    data2 = (s_quantity, s_id)
                    mycursor.execute(sqlstate1, data2)
                    mydb.commit()
                    print('SUCCESSFULLY PURCHASED !')
                    total_price=s_quantity*price
                    sql = "INSERT INTO customers_details(cust_id,cust_name,cp_id,cp_name,cp_price,cp_quantity,cp_total,cpurchase_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (cust_id,cust_name,id, name, price, s_quantity,total_price,today)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print('SUCCESSFULLY ADDED TO YOUR CART!')
                else:
                    print('INSUFFICIENT GOODS IN SHOP!')
                    main()
                main()
        print("INVALID PRODUCT ID!")
        main()
    elif ch == 2:
        mycursor = mydb.cursor()
        mycursor.execute("Select * from customers_details")
        for dbb1 in mycursor:
            print(dbb1)
        customer()
    elif ch == 3:
        customer()
    else:
        print('INVALID CHOICE...TRY AGAIN!')
        customer()


def shopkeeper():
    print('1.PURCHASE\n2.DISPLAY\n3.GO BACK')
    ch=int(input('ENTER YOUR CHOISE :'))

    if ch==1:
        mycursor = mydb.cursor()
        mycursor.execute("Select * from godown_details")     #
        for dbb in mycursor:                                 #display part of godown_details (erroorrrr if we call the function)
            print(dbb)                                       #

        s_id = int(input('PRODUCT ID TO BUY :'))
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("select gp_id from godown_details")
        for i in mycursor:
            i = int(i[0])
            #print('i value is',i)
            #print('s_is is',s_id)
            if i==s_id:
                sqlstate = "select * from godown_details where gp_id=%s"
                data1 = (s_id,)  # Since you are using mysql module, cursor.execute requires a sql query and a tuple as parameters
                mycursor.execute(sqlstate, data1)
                for db in mycursor:
                    id = db[0]
                    name = db[1]
                    price = db[2]
                    quantity = db[3]
                    print('PRODUCT : ',name,'\t\tPRICE  :  ',price,'\t\tQUANTITY  : ',quantity)
                s_quantity=int(input('ENTER THE QUANTITY TO PURCHASE :'))

                if (quantity>=s_quantity):
                    sqlstate1="update godown_details set gp_quantity=gp_quantity-%s where gp_id=%s"
                    data2=(s_quantity,s_id)
                    mycursor.execute(sqlstate1,data2)
                    mydb.commit()
                    print('SUCCESSFULLY PURCHASED !')

                    mycursor.execute("Select sp_id from shop_details")
                    for x in mycursor:
                        x=int(x[0])
                        if id==x:
                            #print(s_quantity)
                            sql1="Update shop_details set sp_quantity=sp_quantity+%s where sp_id=%s"
                            data3=(s_quantity,x)
                            mycursor.execute(sql1,data3)
                            mydb.commit()
                            print('SUCCESSFULLY UPDATED TO SHOP')
                            main()
                    sql = "INSERT INTO shop_details(sp_id,sp_name,sp_price,sp_quantity) VALUES (%s,%s,%s,%s)"
                    val = (id,name,price,s_quantity)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print('SUCCESSFULLY ADDED TO SHOP')
                else:
                    print('INSUFFICIENT GOODS IN GODOWN!')
                    main()
                main()
        print("INVALID PRODUCT ID!")
        main()
    elif ch==2:
        mycursor = mydb.cursor()
        mycursor.execute("Select * from shop_details")
        for dbb1 in mycursor:
            print(dbb1)
        main()
    elif ch==3:
        main()
    else:
        print('INVALID CHOICE...TRY AGAIN!')
        shopkeeper()

def g_display():
    mycursor.execute("Select * from godown_details")
    for dbb in mycursor:
        print(dbb)
    main()

def g_add():
    print('\n')
    g_p_id = int(input('PRODUCT ID :'))
    #if g_p_id==0:
     #   print('INVALID PRODUCT ID..TRY AGAIN!!')
      #  g_add()
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("select gp_id from godown_details")
    for y in mycursor:
        y=int(y[0])
        if g_p_id==y:
            print('PRODUCT WITH THIS ID ALREADY EXISTS!')
            sqlstate5 = "select * from godown_details where gp_id=%s"
            data4 = (g_p_id,)    # Since you are using mysql module, cursor.execute requires a sql query and a tuple as parameters
            mycursor.execute(sqlstate5, data4)
            for db1 in mycursor:
                print(db1)
            print('DO YOU WANT TO\n1.UPDATE QUANTITY\n2.GO BACK\n')
            ch1=int(input('ENTER YOUR CHOICE :'))
            if ch1==1:
                quant=int(input('QUANTITY TO BE ADDED :'))
                sqlstate6="update godown_details set gp_quantity=gp_quantity+%s where gp_id=%s"
                data6=(quant,g_p_id)
                mycursor.execute(sqlstate6,data6)
                mydb.commit()
                print('SUCCESSFULLY UPDATED THE QUANTITY!')
                main()
            elif ch==2:
                godown()
            else:
                print('INVALID CHOICE!')
                main()

    g_p_name = input('PRODUCT NAME :' )
    g_p_price = int(input('PRODUCT PRICE :'))
    g_p_quantity = int(input('QUANTITY :'))
    mycursor = mydb.cursor()
    sqlform = "Insert into godown_details(gp_id,gp_name,gp_price,gp_quantity) values(%s,%s,%s,%s)"
    data = (g_p_id, g_p_name, g_p_price, g_p_quantity)
    mycursor.execute(sqlform, data)
    mydb.commit()
    main()

def godown():
    print('1.ADD\n2.DISPLAY\n3.GO BACK\nENTER YOUR CHOICE :')
    ginp=int(input())
    if ginp==1:
        print('ADD OPTION IN GODOWN')
        g_add()
    elif ginp==2:
        print('DISPLAY OPTION IN GODOWN')
        g_display()
    elif ginp==3:
        print('GO BACK STATEMENT IS BEING EXECUTED.....')
        main()

def main():
    print('\n')
    print('1.CUSTOMER\n2.SHOPKEPPER\n3.Godown\n4.EXIT\nENTER YOUR CHOICE:')
    inp=input()
    inp=int(inp)
    if inp==1:
        print('customer option')
        customer()
    elif inp == 2:
        print('YOU HAVE CHOOSEN OPTION 2 --> SHOPKEEPER')
        shopkeeper()
    elif inp==3:
        print('YOU HAVE CHOOSEN OPTION 3 --> GODOWN')
        godown()
    elif inp==4:
        print('EXIT STATEMENT...')
        exit()
    else:
        print('Wrong choice')
        main()



if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
