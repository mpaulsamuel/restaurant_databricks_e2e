import random
import os
import time
import csv
import json
import pandas as pd
from datetime import datetime,timedelta


script_dir = os.path.dirname(os.path.abspath(__file__))
cust_df = pd.read_csv(os.path.join(script_dir,'data','customers.csv'))
menu_item_df = pd.read_csv(os.path.join(script_dir,'data','menu_items.csv'))
restra_df = pd.read_csv(os.path.join(script_dir,'data','restaurants.csv'))

restra_id_list = restra_df['restaurant_id'].tolist()
cust_id_list = cust_df['customer_id'].tolist()

menu_items_per_restra = menu_item_df.groupby('restaurant_id')\
    .apply(lambda x : x.to_dict(orient='records'),include_groups=False).to_dict()

order_types = ["dine-in","takeaway","delivery"]
payment_methods = ["cash","card","wallet"]
order_status = ["delivered","completed"]

def generate_history_order(order_date : datetime):
    restaurant_id = random.choice(restra_id_list)
    customer_id = random.choice(cust_id_list)
    items = []
    total_amt = 0.0

    menu_items =  menu_items_per_restra[restaurant_id]
    num_items = random.randint(1,min(5,len(menu_items)))
    selected_items = random.sample(menu_items,num_items)

    for item in selected_items:
        quantity = random.randint(1,3)
        subtotal = item["price"] * quantity
        total_amt = total_amt + subtotal

        items.append({
            "item_id" : item["item_id"],
            "name" : item["name"],
            "category" : item["category"],
            "quantity" : quantity,
            "unit_price" : item["price"],
            "subtotal" : round(subtotal,2)
        })
    
    order_id = f"ORD-{order_date.strftime('%Y%m%d')}-{random.randint(100000,999999)}"

    return{
        "order_id" : order_id,
        "timestamp" : order_date.isoformat(),
        "restaurant_id" : restaurant_id,
        "customer_id" : customer_id,
        "order_type" : random.choice(order_types),
        "items" : json.dumps(items),
        "total_amount" : total_amt,
        "payment_method" : random.choice(payment_methods),
        "order_status" : random.choice(order_status),
        "created_at" : order_date.isoformat()
    }

def generate_history_orders(num_orders : int,months_back : int) -> list[dict]:
    enddate = datetime.now()
    startdate = enddate - timedelta(days=months_back * 30)
    orders = []
    #print(f"Generating {num_orders} orders from {startdate} to {enddate}")
    for i in range(num_orders):
        days_offset = random.randint(0,(enddate-startdate).days)
        order_date = startdate + timedelta(days=days_offset)
        order_date = order_date.replace(
            hour=random.randint(10,22),
            minute=random.randint(0,59),
            second=random.randint(0,59)
        )
        order = generate_history_order(order_date=order_date)
        orders.append(order)

        # if (i+1) % 1000 == 0:
        #     print(f"generated {(i+1)} orders")
        
    return orders

def delete_files(loc : str,word : str) -> str:
    try:
        for x in os.listdir(path=loc):
            if x.startswith(word):
                file_path = os.path.join(loc,x)
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"error deleting the files in the path: {e.strerror}")
        print(f"old {word} file removed")
    except FileNotFoundError:
        print(f"Error: Directory not found at {loc}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

if __name__ == '__main__':

    # deletes old csv files
    delete_files(loc=os.path.abspath(path='.')+r'\data',word='hist')
    time.sleep(3)

    # write history data
    field_names = [x for x,y in generate_history_orders(num_orders=8000,months_back=6)[0].items()]
    with open(
        file=os.path.join(script_dir,'data','history_orders.csv'),
        mode='w',
        encoding='utf-8',
        newline=''
    ) as csvfile:
        writer = csv.DictWriter(f=csvfile,fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rowdicts=generate_history_orders(num_orders=8000,months_back=6))
    print("history_orders csv data file is created")