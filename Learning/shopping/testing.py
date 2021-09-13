import csv
with open('c:\\Users\\patri\\OneDrive\\Desktop\\CS50_AI\\Learning\\shopping\\testing.csv','r') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        money,desk = row[::2]
        print("Money",money)
        print("Desk",desk)
        
x = {"Jan":0,"Feb":1,"Mar":2,"Apr":3,"May":4,"Jun":5,"Jul":6,"Aug":7,"Sep":8,"Oct":9,"Nov":10,"Dec":11}
b = "Feb"
if b in x.keys():
    print(x[b])