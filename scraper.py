import requests
import json
import time

max_pizza_value = -1 
pizza_combination = []

def get_pizza_size(pizza_name):
    if(pizza_name == "10SCREEN"):
        return 10
    elif(pizza_name == "12SCREEN"):
        return 12
    elif(pizza_name == "14SCREEN"):
        return 14
    elif(pizza_name == "16SCREEN"):
        return 16

def send_request(toppings, i, weight, portion, size):
    #time.sleep(0.01)
    payload = r'''{"Order":{"Address":{"Street":"561 Princess Street","City":"Kingston","Region":"ON","PostalCode":"K7L1C8","Coordinates":{"latitude":44.23588,"longitude":-76.49839,"altitude":0,"altitudeReference":-1}},"Coupons":[],"CustomerID":"","Email":"","Extension":"","FirstName":"","LastName":"","LanguageCode":"en","OrderChannel":"OLO","OrderID":"nxUlkJlW8CSlEZRsbVjB","OrderMethod":"Web","OrderTaker":null,"Payments":[],"Phone":"","PhonePrefix":"","Products":[{"Code":"''' + size  + '''","Qty":1,"ID":1,"isNew":false,"Options":{''' 
    for j in range(0, i):
        if j == 0:
          payload +=r'''"''' + toppings[j % 13]  + '''":{"''' + portion  + '''":"''' + weight  + '''"}'''
        if j > 0:
          payload +=r''',"''' + toppings[j % 13]  + '''":{"''' + portion  + '''":"''' + weight  + '''"}'''

    payload+=r''' }}],"ServiceMethod":"Carryout","SourceOrganizationURI":"order.dominos.com","StoreID":"10310","Tags":{},"Version":"1.0","NoCombine":true,"Partners":{},"OrderInfoCollection":[]}}'''

    #print("PAYLOAD: " + payload)

    r = requests.post('https://order.dominos.ca/power/price-order', data=payload)
    result = r.json()
    if("Amounts" in r.text):
        price = result["Order"]["Amounts"]["Customer"]
        pizza_size = get_pizza_size(size)
        pizza_value = (pizza_size * 10 * i) / price
        print("Toppings: " +str(i)+ "; weight: "+ weight  +"; portion: " + portion  + "; size: " + str(pizza_size) + "; Pizza Value: " + str(pizza_value))
        global max_pizza_value
        if (pizza_value > max_pizza_value):
            max_pizza_value = pizza_value
            combination = [i, weight, portion, size]

toppings = ["C", "X", "Q", "K", "Z", "Rp", "Sp", "J", "T", "O", "N", "G", "V"]
cheese_weights = ["0",  "0.5", "1", "1.5", "2", "3"]
weights = ["0.5", "1", "1.5"]
portions = ["1/1", "1/2", "2/2"]
sizes = ["10SCREEN", "12SCREEN", "14SCREEN", "16SCREEN"]

toppings_count = len(toppings)


for portion in portions:
    for size in sizes:
        for weight in weights:
            for i in range(1, toppings_count-1):
                send_request(toppings, i, weight, portion, size)

print("Best pizza value: " + max_pizza_value)
print("Deal: ")
print("Toppings: " + combination[0])
print("Weight: " + combination[1])
print("Portion: " + combination[2])
print("Size: " + combination[3])
