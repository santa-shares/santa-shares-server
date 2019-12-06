import datetime
from extensions import db
from noise import noise, noise_seed, random_gaussian

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
        reference_time = datetime.datetime(2019, 1, 1)
        current_time = datetime.datetime.now()
        delta_time = current_time - reference_time
        time = int(delta_time.total_seconds() / 60)
        return self.get_price(time)

    def get_price(self, time):
        noise_seed(self.cost_seed)
        cost = self.cost_min + self.cost_range * noise(self.cost_offset + time / 2000)
        return max(1, int(cost))