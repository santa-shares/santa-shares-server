from extensions import db
from app import app
from models import Item
from noise import random_gaussian
import random

with app.app_context():
    db.drop_all()
    db.create_all()

    with open("gifts.csv", "r") as file:
        lines = file.readlines()
    
    for line in lines:
        item = Item(name=line.strip())
        item.amount = random.randint(1, 10)
        item.cost_min = int(random.random() * 50_00)
        item.cost_range = int(random_gaussian(50, 50_00))
        item.cost_seed = int(random.randint(0, 1000_00))
        item.cost_offset = int(random.random() * 1000_00)
        db.session.add(item)
    db.session.commit()