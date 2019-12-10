import datetime
from extensions import db
from noise import noise, noise_seed, random_gaussian

reference_time = datetime.datetime(2019, 1, 1)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    cost_seed = db.Column(db.Integer, nullable=False)
    cost_min = db.Column(db.Integer, nullable=False)
    cost_range = db.Column(db.Integer, nullable=False)
    cost_offset = db.Column(db.Integer, nullable=False)

    def get_current_price(self):
        minutes = Item.get_minutes_since_reference(datetime.datetime.now())
        return self.get_price_at_minutes(minutes)

    def get_price_at(self, time):
        minutes = Item.get_minutes_since_reference(time)
        return self.get_price_at_minutes(minutes) 

    def get_price_at_minutes(self, minutes):
        noise_seed(self.cost_seed)
        cost = self.cost_min + self.cost_range * noise(self.cost_offset + minutes / 2000)
        return max(1, int(cost))

    @staticmethod
    def get_minutes_since_reference(time):
        delta_time = time - reference_time
        return int(delta_time.total_seconds() / 60)