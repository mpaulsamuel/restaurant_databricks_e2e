import random
import os
import csv
import time
from datetime import datetime,timedelta
import json
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
hist_orders_df = pd.read_csv(filepath_or_buffer=os.path.join(script_dir,'data','history_orders.csv'))

REVIEW_TEMPLATES = {
    5: [
        "Absolutely amazing {dishes}! The {highlight} was cooked to perfection. Fresh ingredients and authentic flavors. Highly recommend!",
        "Outstanding experience! The {dishes} exceeded all expectations. {highlight} was the star of the meal. Will definitely order again!",
        "Best Indian food in UAE! {dishes} were incredible. {highlight} had the perfect balance of spices. Five stars!",
        "Exceptional quality! Ordered {dishes} and everything was delicious. The {highlight} melted in my mouth. Perfect!",
        "Wow! Just wow! {dishes} were all fantastic. {highlight} was particularly memorable. Can't wait to order again!",
        "Hands down the best {highlight} I've ever had! {dishes} were all prepared beautifully. Fresh and flavorful!",
        "Incredible meal! {dishes} arrived hot and fresh. The {highlight} was absolutely divine. Highly satisfied!",
        "Perfect in every way! {dishes} were all excellent. {highlight} stood out with its rich, authentic taste.",
    ],
    4: [
        "Really good {dishes}! The {highlight} was delicious. Slight delay in delivery but food quality made up for it.",
        "Great food overall. {dishes} were tasty, especially the {highlight}. Would order again!",
        "Enjoyed the {dishes}! {highlight} was very good. Portion sizes were generous. Recommend!",
        "Solid experience. {dishes} were well-prepared. {highlight} had great flavor. Minor issues with packaging.",
        "Very satisfied! {dishes} were fresh and flavorful. {highlight} was the standout dish.",
        "Good quality food. {dishes} were nicely done. {highlight} could have been slightly spicier but still good!",
        "Pleasant meal! {dishes} arrived warm. {highlight} was tasty though not exceptional. Would order again.",
    ],
    3: [
        "Decent food but nothing special. {dishes} were okay. {highlight} lacked the punch I expected.",
        "Average experience. {dishes} were fine but {highlight} was a bit bland. Room for improvement.",
        "Mixed feelings. {dishes} were acceptable. {highlight} was decent but portion was small for the price.",
        "It was okay. {dishes} arrived lukewarm. {highlight} tasted fine but could be better.",
        "Not bad, not great. {dishes} were edible. {highlight} needed more seasoning.",
        "Mediocre. {dishes} were fine but forgettable. {highlight} didn't stand out.",
    ],
    2: [
        "Disappointed with {dishes}. {highlight} was cold when it arrived. Not worth the money.",
        "Below expectations. {dishes} were underwhelming. {highlight} was overcooked and dry.",
        "Not good. {dishes} arrived late and cold. {highlight} had barely any flavor. Poor quality.",
        "Unsatisfactory. {dishes} were not fresh. {highlight} tasted reheated. Won't order again.",
        "Poor experience. {dishes} were disappointing. {highlight} was burnt on the edges. Very unhappy.",
        "Expected better. {dishes} were subpar. {highlight} was too oily and greasy. Stomach upset followed.",
    ],
    1: [
        "Terrible experience! {dishes} were all inedible. {highlight} was completely burnt. Waste of money!",
        "Absolutely horrible! {dishes} arrived ice cold after 2 hour delay. {highlight} was spoiled. Disgusting!",
        "Worst food ever! {dishes} were all wrong. {highlight} made me sick. Never ordering again!",
        "Disaster! {dishes} were all stale. {highlight} had a weird smell. Completely unacceptable!",
        "Appalling quality! {dishes} were swimming in oil. {highlight} was raw inside. Health hazard!",
        "Shocking! {dishes} bore no resemblance to the menu description. {highlight} was inedible. Refund demanded!",
    ]
}

def extract_items_from_order(items_json : list[dict]) -> list:
    items = json.loads(items_json)
    return [item["name"] for item in items]

def format_dishes(dish_list : list) -> str:
    if len(dish_list) == 1:
        return dish_list[0]
    elif len(dish_list) == 2:
        return f"{dish_list[0] and dish_list[1]}"
    else:
        return f"{', '.join(dish_list[:-1])} and {dish_list[-1]}"


def generate_review_text(rating : int,dish_list : list) -> str:
    template = random.choice(REVIEW_TEMPLATES[rating])
    dishes_formatted = format_dishes(dish_list=dish_list)
    highlight = random.choice(seq=dish_list)
    review = template.format(dishes=dishes_formatted,highlight=highlight)
    return review


def generate_customer_reviews(review_perc : float) -> list[dict]:
    reviews = []
    ratings_weights = {
        5:0.50,
        4:0.25,
        3:0.12,
        2:0.08,
        1:0.05
    }

    ratings_pool = []
    for rating,weight in ratings_weights.items():
        ratings_pool.extend([rating] * int(weight * 100))
    
    for index,row in hist_orders_df.iterrows():
        if random.random() > review_perc:
            continue

        dishes = extract_items_from_order(items_json=row["items"])

        rating = random.choice(seq=ratings_pool)

        review_text = generate_review_text(rating=rating,dish_list=dishes)

        # review date: 1-7 after order
        order_date = datetime.fromisoformat(row["timestamp"])
        review_ts = order_date + timedelta(days=random.randint(1,7))

        review_id = f"REV-{len(reviews) + 1:06d}"

        review = {
            "review_id" : review_id,
            "order_id" : row["order_id"],
            "customer_id" : row["customer_id"],
            "restaurant_id" : row["restaurant_id"],
            "review_text" : review_text,
            "rating" : rating,
            "review_timestamp" : review_ts.isoformat()
        }

        reviews.append(review)
        return reviews

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

if __name__ == "__main__":
    # delete old review file
    delete_files(loc=os.path.abspath(path='.')+r'\data',word='reviews')
    time.sleep(3)

    # create review file
    field_names = [x for x,y in generate_customer_reviews(review_perc=0.35)[0].items()]
    with open(
        file=os.path.join(script_dir,'data','reviews.csv'),
        mode='w',
        encoding='utf-8',
        newline=''
    ) as csvfile:
        writer = csv.DictWriter(f=csvfile,fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rowdicts=generate_customer_reviews(review_perc=0.35))