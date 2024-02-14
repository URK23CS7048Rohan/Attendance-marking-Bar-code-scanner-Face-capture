import sqlite3
c=sqlite3.connect('scans.db')
x=c.cursor()


l1=list(x.execute('select * from scans'))
for i in l1:
    print(i[2])