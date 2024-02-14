import sqlite3
s=sqlite3.connect('attendance_marking.db')
x=s.cursor()

l2=list(x.execute('select * from attendance'))
f=open('login_logouttime.txt','w')
for i in l2:
    f.write(i[2])
    f.write('\n')
f.close()
f=open('login_logouttime.txt','r')
list_of_login=f.readlines()
print('login_time:',list_of_login[0])
for i in range (1,len(list_of_login)+1):
    try:
        if i%2==0:
            print('login_time:',list_of_login[i])
        else:
            print('logout_time:',list_of_login[i])
    except:
        pass