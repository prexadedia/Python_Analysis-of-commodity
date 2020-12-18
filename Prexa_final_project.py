'''
Program: analysis_of_commodity_final_project-prexa-00.py
Author: Prexa Dedhia
Description: Program for Analysis of Commodity Data
Revision:
01: Using Zip, ennumerate, join, map
02: Using Plotly
'''
#impoRT all the required packages
from datetime import datetime 
import csv 
import plotly.offline as py
import plotly.graph_objs as go

#defining the average function for calculation
def average(a):
    return sum(a)/len(a)

#printing title
print("="*26)
print("Analysis of Commodity Data")
print("="*26)

#importing CSV
with open('produce_csv.csv') as csvfile:
    reader = csv.reader(csvfile)
    data = [row for row in reader]

newData = [] #initialize new lists ,where we store records
for row in data: #traverse rows
    newRow = list() #create an empty to receive rows
    for item in row: #traverse the values in the old row
        if "$" in item: #test for price string and convert
            newRow.append(float(item.replace("$",""))) 
        elif "/" in item: #test for date and convert 
            newRow.append(datetime.strptime(item,'%m/%d/%Y'))
        else: #otherwise append item
            newRow.append(item)
    newData.append(newRow)   

locations = data.pop(0)[2:] #pop header for list of locations
rec = [] #initialize new lists ,where we store records 
for row in newData[1:]:
    newRow = row[:2]
    for loca,price in zip (locations,row[2:]): #used zip function to pair location and date
        rec.append(newRow+[loca,price]) #appendind it to list rec

#Creating a list by extracting unique commodity_list and indexing it
print("SELECT PRODUCT BY NUMBER ...") 
commodity_List=list({i[0] for i in rec})
commodity_List.sort()
for (i, c) in enumerate(commodity_List):
    print(f"<{i}> {c}")
user_prod = [int(i) for i in input("Enter product numbers separated by spaces: ").split()]
user_prod1 = [commodity_List[i] for i in user_prod]
print(f"selected poducts: {' '.join(map(str,user_prod1))} \n")

##Creating a list by extracting unique dates and indexing it
print("SELECT DATE RANGE BY NUMBER ...")
date_List=list({i[1] for i in rec})
date_List.sort()
for (i, d) in enumerate(date_List):
    print(f"<{i}> {datetime.strftime(d,'%Y-%m-%d')}")
print(f"Earliest available date is : {datetime.strftime(date_List[0],'%Y-%m-%d')}")
print(f"Latest available date is : {datetime.strftime(date_List[-1],'%Y-%m-%d')}")
user_date = [int(i) for i in input("Enter start/end date numbers separated by a space: ").split()]  
user_date1 = [datetime.strftime(date_List[i],'%Y-%m-%d') for i in user_date]
print(f"Dates from  {''.join(map(str,user_date1[0]))} to {''.join(map(str,user_date1[1]))}")
start_Date =  datetime.strptime(user_date1[0],'%Y-%m-%d')
end_Date = datetime.strptime(user_date1[1],'%Y-%m-%d')

#Creating a list by extracting unique Locations and indexing it
print("SELECT LOCATIONS BY NUMBER ...")
locations.sort()
for (i, L) in enumerate(locations):
    print(f"<{i}> {L}")
user_Location = [int(i) for i in input(f"Enter location numbers separated by spaces: ").split()]
user_Location1 = [locations[i] for i in user_Location]
print(f"Selected locations: {' '.join(map(str,user_Location1))}")

#creating list of all the user selected options
user_selection = list(filter(lambda i:i[0] in user_prod1 and (start_Date<=i[1]<=end_Date) and i[2] in user_Location1,rec ))
print(f"{len(user_selection)} records have been selected.")

#creating dictionary of user_selection
data_Store = {}
for i in user_Location1:
    data_Store[i]={}
    for k in user_prod1:
        data_Store[i].update({k:[]})
        data_Store[i][k]=[x[3] for x in user_selection if x[2]==i and x[0]==k]

#Calculating the average of prices of user selected options 
data_Plot = {}
for q in data_Store:
    data_Plot.update({q:{}})
    for p in data_Store[q]:
       data_Plot[q].update({p:average(data_Store[q][p])}) 

#Traversing the dictionary and creating list of plotly traces        
trace_Bar=[]
for loca in user_Location1:
    price_Listing = [data_Plot[loca][prod] for prod in user_prod1]
    trace_Bar.append(go.Bar(x=user_prod1, y=price_Listing, name=loca))
layout=go.Layout(
        barmode='group'
        )
#updating figure layout
fig= go.Figure(data = trace_Bar, layout=layout)
fig.update_layout(
        title=f"Product prices from {user_date1[0]} through {user_date1[1]}",
        xaxis_title="Product",
        yaxis_title="Average Price"
        )
#plot the figure to the html file
fig.update_layout(yaxis_tickformat = '$.2f')
py.plot(fig, filename='Produce_Bar_Graph_Analysis.html')
fig.show()
