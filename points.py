import csv, sys, json
from datetime import datetime
from collections import defaultdict


# Verifies that the arguments passed are valid
# returns 1 on success, 0 on failure
def verify_args(args):
    # Test that user provided enough arguments
    if int(len(args)) > 3:
        print("Error: Too many arguments were provided.")
        return 0
    
    # Test that user provided a numerical value for points
    if (args[1].isnumeric() == False):
        print("Error: Points provided were not numerical.")
        return 0
    return 1
    

# Reads in a csv file and outputs a list where each element is a dict representing one row of the file read & the amounts of points spent
# i.e. [{'payer': 'DANNON', 'points': '1000', 'timestamp': '2020-11-02T14:00:00Z', 'spent': 0}, 
#       {'payer': 'UNILEVER', 'points': '200', 'timestamp': '2020-10-31T11:00:00Z', 'spent': 0}]
def load_csv(csvfile):
    try:
        with open(csvfile) as csv_file:
            csv_reader = csv.DictReader(csv_file)
             # Success 
            csvList = list(csv_reader)

            [d.update({'spent':0}) for d in csvList]
            return csvList
    except FileNotFoundError:
        print("Error: The file you provided was not found.")
        exit



# Changes the dates stored into datetime format for easier handling
def formatDates(data):

    # Iterate through each row of data
    for i in range(len(data)):

        # Convert to datetime format (and remove the Z from end of timestamp)
        data[i]['timestamp'] = datetime.fromisoformat(data[i]['timestamp'][:-1])
        

# Sorts our data from oldest to most recent timestamp
def sortTimestamp(data):
    data.sort(key = lambda x:x['timestamp'])


# Find the payer(s) that points should be spent from and spends the points.
# Oldest points first and payer cannot go negative.
def redeemPoints(numPoints, data):
    
    # Sort data from oldest to newest
    sortTimestamp(data)
    numPoints = int(numPoints)
    i = 0
    
    # Redeem points
    while(i < len(data)):

        # Check if payer has a negative transaction
        if int(data[i]['points']) < 0:  
            numPoints = numPoints + abs(int(data[i]['points']))
            data[i]['points'] = 0
            i = i + 1
            continue

        # Check if we've spent all the points
        if(int(numPoints) <= 0):
            break

        # Payer can cover all the points
        if int(data[i]['points']) >= int(numPoints):
            data[i]['spent'] = numPoints
            data[i]['points'] = int(data[i]['points']) - numPoints
            numPoints = 0

        # Payer can cover some of the points
        elif int(data[i]['points']) > 0:
            numPoints = numPoints - int(data[i]['points'] )
            data[i]['spent'] = data[i]['points']
            data[i]['points'] = 0

        # Increment index
        i = i + 1
       

# Prints out the results which show how much each payer paid.
def printPayers(data):

    # Sum all transactions
    c = defaultdict(int)
    for d in data:
        c[d['payer']] += int(d['points'])

    # Print formatting
    print(json.dumps(dict(c), indent=4))
    


# Run the program
if(verify_args(sys.argv) == 1):
    data = load_csv(sys.argv[2])
    formatDates(data)
    redeemPoints(sys.argv[1], data)
    printPayers(data)
    
