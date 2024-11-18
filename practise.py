import mysql.connector
import pandas as pd
mydb=mysql.connector.connect(host="localhost",user="root",password="mumbaikar@1099",database="cms_db")#connecting database using object 
c=mydb.cursor() #Connect module has cursor class, created another object(c) in class.

# to retrieve data from customers table
c.execute("select * from customers")# all the data from customers table stored in 'C'object.
mydata=c.fetchall()#using fetchall function to add data in mydata variable.
mycolumns=c.column_names # A tuple used to return column_names
df=pd.DataFrame(data=mydata,columns=mycolumns) #Saving all the data in df variable to create 2 dimentional data,1)column labels 2) All data
print("Centralized Customer Database:")
print(df)
print()

# to retrieve data from interactionstable
c.execute("select * from interactions")# all the data from interactions table stored in 'C'object.
mydata=c.fetchall()#using fetchall function to add data in mydata variable.
mycolumns=c.column_names # A tuple used to return column_names
df=pd.DataFrame(data=mydata,columns=mycolumns) #Saving all the data in df variable to create 2 dimentional data,1)column labels 2) All data
print("\nInteraction Tracking:")
print(df)
print()


# to retrieve data from projects
c.execute("select * from projects")# all the data from projects table stored in 'C'object.
mydata=c.fetchall()#using fetchall function to add data in mydata variable.
mycolumns=c.column_names # A tuple used to return column_names
df=pd.DataFrame(data=mydata,columns=mycolumns) #Saving all the data in df variable to create 2 dimentional data,1)column labels 2) All data
print("\nProjects Status:")
print(df)
print()

# to retrieve data from reports
c.execute("select * from reports")# all the data from reports table stored in 'C'object.
mydata=c.fetchall()#using fetchall function to add data in mydata variable.
mycolumns=c.column_names # A tuple used to return column_names
df=pd.DataFrame(data=mydata,columns=mycolumns) #Saving all the data in df variable to create 2 dimentional data,1)column labels 2) All data
print("\nReporting and Analytics:")
print(df)
print()

# to retrieve data from supporttickets
c.execute("select * from supporttickets")# all the data from supporttickets table stored in 'C'object.
mydata=c.fetchall()#using fetchall function to add data in mydata variable.
mycolumns=c.column_names # A tuple used to return column_names
df=pd.DataFrame(data=mydata,columns=mycolumns) #Saving all the data in df variable to create 2 dimentional data,1)column labels 2) All data
print("\nSupport Ticketing System:")
print(df)
print()

# to retrieve data from users
c.execute("select * from users")# all the data from users table stored in 'C'object.
mydata=c.fetchall()#using fetchall function to add data in mydata variable.
mycolumns=c.column_names # A tuple used to return column_names
df=pd.DataFrame(data=mydata,columns=mycolumns) #Saving all the data in df variable to create 2 dimentional data,1)column labels 2) All data
print("\nUsers:")
print(df)
print()
