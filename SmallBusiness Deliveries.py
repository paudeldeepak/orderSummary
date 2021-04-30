#----------------------------------------------------
# A python program that will take delivery service orders placed for all the
# stores each week, and summarize the information into an easy to read table that tells the store owners
# how many drivers they will be neede, total delivery cost and delivery cost/ total purchases. The program will also summarize the order information 
# based on the order of a specific address and creat a invoice file for that address
# Author: Deepak Paudel
# References: 
#----------------------------------------------------

def main():

    deliveryZones = getDeliveryZones()
    orderDetails = getOrders()
    productNameID, productCodePrice = getProducts()
    addressOrderDetails = getAddressDetails(orderDetails)
    totalRevenue = getTotalRevenue(productCodePrice,orderDetails)
    deliverySummary = getDeliverySummary(deliveryZones,addressOrderDetails)
    
    closeProgram = False

    # ask the user for menu options until they choose to close the program
    while not closeProgram:
        userChoice = menuSelection()
        # based on the user choice call the required function
        if userChoice == 1:
            printDeliverySummary(deliverySummary,totalRevenue)
            print()
        elif userChoice == 2:
            address = getAddress(addressOrderDetails)
            if address != None:
                addressSummary = getAddressSummary(address, productNameID, productCodePrice,addressOrderDetails)
                creatInvoice(address,addressSummary)
                print()
                printInvoive()
        else:
            print("Thank you for using the Small Business Delivery Program! Goodbye.")
            closeProgram = True # turn off the program loop


def creatInvoice(address,addressSummary):
    """ 
    This funtion will creat a invoice summary for specific address
    that includes the month and day of purchase, name of item purchased and total price of item purchased
    Parameter: 
    address: a string of the adress that we will be printing and invoicing the summary for 
    addressSummary: a list of list that contains date item price per specific address 
    Return: n/a
    """

    # initialize a file to write to
    createFile = open('invoice.txt', 'w')

    itemPrice = [] # empty list to store each item price total

    # sort list of list based on the index 1(date)
    addressSummary.sort(key = lambda x: x[1]) 

    # format the address order summary in a readable manner and add it to the invoice file 
    if len(address) > 30:
        print("Delivery for:%32s*" %(address[:29]), file= createFile)
    else: 
        print("Delivery for:%32s" %(address), file= createFile)
    print("=============================================",file= createFile)
    print("Date    Item                        Price",file= createFile )
    print("------  --------------------------  ---------",file= createFile)
    for summery in addressSummary:
        itemPrice.append(float((summery[4]))) # keep track of each item price to sum later
        if len(summery[3]) > 20:
            print("%s  %03d x %-18s*  $  %6.2f   " % (summery[1],int(summery[2]), (summery[3])[:19],float((summery[4]))), end = "",file= createFile)
            print("",file= createFile)
        else:
            print("%s  %03d x %-20s  $  %6.2f     " % (summery[1],int(summery[2]), (summery[3]),float((summery[4]))), end = "",file= createFile)
            print("",file= createFile)
    print("%45s" % ("---------"),file= createFile)
    # add all the item prices
    totalPrice = sum(itemPrice)
    print("%37s%8.2f" % ("$", totalPrice),file= createFile)
    createFile.close()

def printInvoive():
    """ 
    This funtion will print the invoice.txt file created 
    Parameter: n/a
    Return: n/a
    """
    # open the file to read
    inFile = open('invoice.txt', 'r')
    print(inFile.read()) # print each line
    inFile.close()

def  getAddressSummary(address, productNameID, productCodePrice,addressOrderDetails):
    """ 
    This funtion will  create a summary for a specific address 
    that includes the month and day of purchase, name of item purchased and total price of item purchased
    Parameter: 
    address:  a string of the adress that we will be creating the summary for
    productNameID: a dictionary with Key = product ID  and Value: product name
    productCodePrice: a dictionary with Key = product ID and  Value: product price
    addressOrderDetails: a dictionary with Key = address and Value: list of list with order details based on the address
    Return: a list of list that contains date, amount and name of product ordred and total price per specific address
    """
    # list to match month with corresponding number value
    letterMonths = ['JAN ', 'FEB ', 'MAR ', 'APR ', 'MAY ', 'JUN ', 'JUL ','AUG ', 'SEP ', 'OCT ','NOV ', 'DEC ']
    numberMonths = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] 
    
    addressSummary = [] # empty list to store list that contain address summary details

    # go through each order deatil per address
    for detial in addressOrderDetails.get(address):
        orderDetail = [] # inialize a list to store desired info
        orderDate = detial[0]
        productID = detial[1]
        productQuality = detial[2]

        # convert each date from number to word format
        dateInfo = orderDate.split("-")
        month = dateInfo[1]
        letterMonth = letterMonths[numberMonths.index(month)] # match  the index of the number with letter
        orderDetail.append(month)
        orderDetail.append(letterMonth+dateInfo[2])

        # convert each product code into product name 
        orderDetail.append(productQuality)
        productName = productNameID.get(productID)
        orderDetail.append(productName)

        # get total price of each product purchased
        productPrice = productCodePrice.get(productID)
        totalProductPrice = (int(productPrice)*int(productQuality))*0.01
        orderDetail.append(totalProductPrice)
        addressSummary.append(orderDetail) # add each order detail to creat a list of all the orders
    
    return addressSummary


def printDeliverySummary(deliverySummary,totalRevenue):
    """ 
    This funtion will print information on delivery zone, deliveries, drivers,
    total drivers needed, total delivery cost and delivery cost/purchases
    Parameter: 
    deliverySummary: a list of list that contains delivery zone, number of deliveries per delivery zone 
    totalRevenue: a int value that contains the total revenue from all the Purchases in dollars
    and number of drivers delivery zone
    Return: n/a
    """

    totalDrivers = 0
    totalDeliveries = 0
    border = "+---------------+------------+-----------+"

    # sort a list of list in alphabetical order based on the 0 index (zone)
    deliverySummary.sort(key = lambda x: x[0]) 

    # iterate to get total values of drivers and deliveries
    for zoneSummary in deliverySummary:
           totalDrivers += zoneSummary[2]
           totalDeliveries += zoneSummary[1]

    totalDeliveryCost = totalDeliveries*12
    costPercentage =  (totalDeliveryCost/totalRevenue)*100

    # display the delivery summary in a readable manner
    print(border+"\n"+"| Delivery Zone | Deliveries |  Drivers  |"+"\n"+border)
    for summery in deliverySummary:
        print("| %-14s|     %-7i|     %-6i|" % (summery[0],summery[1], summery[2]), end = "")
        print() # creat a new line
    print(border)
    print("| %-10s %17i |" % ("Total drivers needed",totalDrivers))
    print("| %-10s          $%8.2f |" % ("Total delivery cost",totalDeliveryCost))
    print("| %-10s %13.1f%s |" % ("Delivery cost/purchases",costPercentage,"%"))
    print("+----------------------------------------+")

def getDeliverySummary(deliveryZones,addressOrderDetails):
    """ 
    This function will get the delivery zones, 
    the total number of deliveries per delivery zones and 
    the total number of delivery drivers needed per delivery zones
    Parameter: 
    deliveryZones: dictionary with Key = delivery zones and Value = list containing postal codes in the delivery zones
    productNameID: dictionary with Key = product ID and Value: product name
    productCodePrice: dictionary with Key = product ID and Value: product price
    addressOrderDetails: a dictionary with Key = address and Value: list of list with order details based on the address
    Return: 
    zoneDeliverySummary: a list of list that contains delivery zone, number of deliveries per delivery zone 
    and number of drivers delivery zone
    """
    
    zoneDeliverySummary = [] # empty list to hold each zone delivery summary

    # get zone and postalcodes 
    for zone , postalcodes in deliveryZones.items():
        totalDeliveries = 0
        deliverySummary = []

        # match address to delivery zone 
        for address in addressOrderDetails.keys():
            for postalcode in postalcodes:
                if postalcode in address:
                    totalDeliveries +=1

        # get total drivers needed 
        # add driver per 10 package
        if totalDeliveries%10 != 0:
            totalDrivers = (totalDeliveries//10) +1
        else:
            totalDrivers = totalDeliveries//10

        # add Delivery if the zone has delivers needed to be made
        if totalDeliveries > 0:
            deliverySummary.append(zone)
            deliverySummary.append(totalDeliveries)
            deliverySummary.append(totalDrivers)
            zoneDeliverySummary.append(deliverySummary)

    return zoneDeliverySummary


def getTotalRevenue(productCodePrice,orderDetails):
    """ 
    This function will add the total revenue from all the purchase made
    Parameter: 
    productCodePrice: dictionary with Key = product and id Value = price 
    orderDetails: list with details of all the order made 
    Return: 
    totalRevenue: int with dollar amount of total revenue from all the purchase made
    """

    totalRevenue = 0

    # iterate to get info from each order
    for index in range(len(orderDetails)):
        # convert product code to price
        productcode = orderDetails[index][2]
        amountOrdered = orderDetails[index][3]
        productPrice = productCodePrice.get(productcode)
        # add the total from each order
        totalRevenue += int(amountOrdered)*int(productPrice)
    
    return totalRevenue*0.01 # convert to dollars
        
def menuSelection():
    """ 
    This function will prompt the user to select valid program menu options 
    Parameter: 
    N/A
    Return: 
    userChoice: The valid int menu number selected by the user
    """
    
    welcomeMessage = "Welcome to the Small Business Delivery Program"
    messageBorder = "*"* len(welcomeMessage)

    print(messageBorder)
    print(welcomeMessage)
    print(messageBorder)

    print("What would you like to do?\n"+
    "1. Display DELIVERY SUMMARY TABLE for this week\n"+
    "2. Display and save DELIVERY ORDER for specific address\n"+
    "3.Quit")
    
    inValid = True
    # loop until the user choice is valid
    while inValid:
        # getting user input
        userChoice = input()
        if userChoice.isdigit():
            userChoice = int(userChoice)
            if 1 <= userChoice <= 3:
                inValid = False # setting boolean flag
                return int(userChoice)
        else:
            print("Sorry, invalid entry. Please enter a choice from 1 to 3.")

def getAddress(addressOrderDetails):
    """ 
    This function will prompt the user to input a address to print order summer for 
    Parameter: 
    addressOrderDetails: a dictionary with Key = address  Value: list of list with order details based on the address
    Return: 
    address: a string that is a valid address that is in the order details
    """
    # get user input 
    address = input("Address: ")
    
    # check if the input address has made a order
    if address in addressOrderDetails.keys():
        return address
    else: 
        print("Invalid address.")

def getAddressDetails(orderDetails): 
    """
    This function will itteriate throught a list of list of orders details and 
    get order inforomtion based on the order address
    Parameter: 
    orderDetails: a list of list containing customers order details
    Return: 
    addressDetails: a dictionary with Key = Address and 
    Value: list of list with order details based on the address
     """

    addressDetails = {} # empty dictionary to store order details based on address

    # iterate to intialize a dictionary with one instance of a address
    for order in orderDetails:
        address = order[0]
        addressDetails[address] = []
    # add the other order details to one instance of a address
    for order in orderDetails:
        if order[0] in addressDetails.keys():
            addressDetails[order[0]].append(order[1:])

    return addressDetails

def getProducts(): 
     """
    This function will open the products.txt file 
    and extra the data that is in the file
    Parameter: 
    N/A
    Return: 
    productNameID: a dictionary with Key = product ID and Value: product name
    productCodePrice: a dictionary with Key = product ID  and Value: product price
     """

     productNameID = {} # empty dictionary to store product id and name 
     productCodePrice = {} # empty dictionary to store product id and price 

     inFile = open('products.txt', 'r')
    # iterate to get each line
     for line in inFile:
         line = line.strip() # remove '\n'
         (productID, productName, productPrice) = line.split(";") # seperate the 3 different values in the file 
         # add corresponding info to the dictionaries
         productNameID[productID] = productName  
         productCodePrice[productID] = productPrice  
     inFile.close()
    
     return productNameID, productCodePrice 

def getOrders():
    """
    This function will open the orders.txt file 
    and extra the data that is in the file
    Parameter: 
    N/A
    Return: 
    orderDetails = List of list that contains all the order data
    """

    orderDetails = [] # initalize a empty list to hold order details

    inFile = open('orders.txt', 'r')
    # iterate to get each line
    for line in inFile:
        line = line.strip() # remove '\n' 
        line = line.split("%")
        fileContent = []
        # isolating for the data that we only need 
        for contentIndex in range(len(line)): 
            if contentIndex == 0 or contentIndex == 3 or contentIndex == 4: 
                fileContent.append(line[contentIndex])
            # organizing the data so details are after the address
            elif contentIndex == 2:
                fileContent.insert(0,line[contentIndex])
        orderDetails.append(fileContent)
    inFile.close()

    return orderDetails

def getDeliveryZones():
    """
    This function will open the order.txt file 
    and extra the data that is in the file
    Parameter: 
    N/A
    Return: 
    deliveryZones = a dictionary with Key = Delivery Zones and 
    Value = List containing postal codes in the Delivery Zones
    """

    deliveryZones = {} # empty dictionary to hold the zones and postal code 

    inFile = open('zones.txt', 'r')
    # iterate to get each line
    for line in inFile:
        line = line.strip() # remove '\n' 
        (zone, postalCodes) = line.split("#") # seperate zones from the postal code
        deliveryZones[zone] = postalCodes.split(",")  # add zone and postal code to dictionary
    inFile.close()

    return deliveryZones

main()