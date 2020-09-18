import json
import sqlite3
import random
import time

conn = sqlite3.connect('quizdb.sqlite')
cur = conn.cursor()


cur.executescript('''
DROP TABLE IF EXISTS country;

CREATE TABLE country(
        SNo        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Name       TEXT UNIQUE,
        Capital    TEXT UNIQUE,
        Continent  TEXT
);

''')

json_data=json.loads(open("country-capitals.json").read())

print("\n Please wait while the database for QUIZ is being prepared....")
for entry in json_data:
    cur.execute('''INSERT OR IGNORE INTO country(Name,Capital,Continent)
                    VALUES( ?, ?, ? )''',
                (entry["CountryName"],entry["CapitalName"],entry["ContinentName"]))

    conn.commit()

print("\n Database for quiz prepared.\n\nWelcome to the QUIZ!!!\n")
n=int(input("Enter the number of question sets you want to answer:  "))
print("\n The max marks you can get is: ",2*n)
print("\n The quiz will contain {} question sets of country capital name and continent name".format(n))
print("\n For each correct capital you will be awarded 1.5 and for each correct continent you will be awarded 0.5 marks")
print("\n \"Enter the correct option A, B, C, D in any case for response\" \n")
print("\n Press Enter key to start\n____________________________________\n")
input()
marks=0.0
qnum=1
for i in range(n):
    x=random.randrange(1,240)
    #print("\n",x,"\n")
    cur.execute('SELECT Name, Capital, Continent FROM country WHERE SNo = ?',(x,))
    s1=cur.fetchone()
    while s1 is not None:
        data1=s1
        s1=cur.fetchone()
    


    if(x<4):
        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x+1,))
        s2=cur.fetchone()
        while s2 is not None:
            data2=s2
            s2=cur.fetchone()

    
        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x+2,))
        s3=cur.fetchone()
        while s3 is not None:
            data3=s3
            s3=cur.fetchone()

        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x+3,))
        s4=cur.fetchone()
        while s4 is not None:
            data4=s4
            s4=cur.fetchone()
            


    elif(x>237):
        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x-1,))
        s2=cur.fetchone()
        while s2 is not None:
            data2=s2
            s2=cur.fetchone()

        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x-2,))
        s3=cur.fetchone()
        while s3 is not None:
            data3=s3
            s3=cur.fetchone()

        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x-3,))
        s4=cur.fetchone()
        while s4 is not None:
            data4=s4
            s4=cur.fetchone()

    else:
        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x-2,))
        s2=cur.fetchone()
        while s2 is not None:
            data2=s2
            s2=cur.fetchone()

        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x-1,))
        s3=cur.fetchone()
        while s3 is not None:
            data3=s3
            s3=cur.fetchone()

        cur.execute('SELECT Capital, Continent FROM country WHERE SNo = ?',(x+1,))
        s4=cur.fetchone()
        while s4 is not None:
            data4=s4
            s4=cur.fetchone()

    caps=list()
    conts=list()
    optcap=dict()
    optcon=dict()

    continentlist=["Asia","Africa","Antarctica","North America","South America","Europe","Australia"]
    
    caps.append(data1[1])
    caps.append(data2[0])
    caps.append(data3[0])
    caps.append(data4[0])

    #conts.append(data1[2])
    #conts.append(data2[1])
    #conts.append(data3[1])
    #conts.append(data4[1])

    conts.append(data1[2])
    for r in continentlist:
        if(len(conts)>=4):
            break
        if(r not in conts):
            conts.append(r)
    #print(conts,"\n\n")
    

    random.shuffle(caps)
    random.shuffle(conts)

    optcap["A"]=caps[0]
    optcap["B"]=caps[1]
    optcap["C"]=caps[2]
    optcap["D"]=caps[3]
    key_list_caps=list(optcap.keys())
    value_list_caps=list(optcap.values())

    optcon["A"]=conts[0]
    optcon["B"]=conts[1]
    optcon["C"]=conts[2]
    optcon["D"]=conts[3]
    key_list_conts=list(optcon.keys())
    value_list_conts=list(optcon.values())
    

    for e in caps:
        if(data1[1] == e):
            anscap=e
        

    for g in conts:
        if(data1[2] == g):
            anscont=g

    #print(anscap,anscont)
    
    print("\n{}.a) Enter the capital of country {}:\n  (A){} (B){} (C){} (D){}"
              .format(qnum,data1[0],optcap["A"],optcap["B"],optcap["C"],optcap["D"]))

    usercap=str(input("  \nResponse: "))
    if(optcap[usercap.upper()] == anscap):
        print("Correct")
        marks=marks+1.5
    else:
        print("Wrong")
        print("\n Correct answer is {}".format(key_list_caps[value_list_caps.index(anscap)]))

    print("\n{}.b) Enter the continent of country {}:\n  (A){} (B){} (C){} (D){}"
              .format(qnum,data1[0],optcon["A"],optcon["B"],optcon["C"],optcon["D"]))
    
    usercon=str(input("  Response: "))

        
    if(optcon[usercon.upper()] == anscont):
        print("Correct")
        marks=marks+0.5
    else:
        print("Wrong")
        print("\n Correct answer is {}".format(key_list_conts[value_list_conts.index(anscont)]))

    qnum=qnum+1
    if(qnum<=n):
        print("\n Wait for 2 second for next question\n\n\n")
        time.sleep(2)
    
print("\n\nQUIZ COMPLETED!\n Your score is {}".format(marks))
