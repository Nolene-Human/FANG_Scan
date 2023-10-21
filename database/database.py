import sqlite3

#conn = sqlite3.connect('client.db')
conn2=sqlite3.connect('clients.db')

#create cursor
c= conn2.cursor()


#create a database
c.execute("""
   CREATE TABLE clients (
        email text,
          key text,
         otp interger)
""")


# #insert to database
# c.execute("""
# INSERT INTO clients VALUES("NAME","cherry grape honeydew elderberry apple",123456)
#          """)

# c.execute("""
# INSERT INTO clients VALUES("NAME2","cherry2 grape2 honeydew2 elderberry2 apple2",654321)
#         """)

#call from database
# c.execute("SELECT*FROM clients WHERE email='NAME'")
# #print(c.fetchall())

# clients=c.fetchall()

# for aclient in clients:
#      print(aclient)

# #update database
# c.execute("""
#     UPDATE clients SET email='BOB' WHERE email='NAME'
# """)
# conn2.commit()


# c.execute("SELECT*FROM clients")
# print(c.fetchall())

#delete record
c.execute('DELETE from clients WHERE email="NAME2"')


#commit our command
conn2.commit()

c.execute("SELECT*FROM clients")
print(c.fetchall())


c.execute('SELECT * FROM clients ORDER BY "name"')

#close connection
conn2.close()