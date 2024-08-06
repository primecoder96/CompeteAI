from django.db import models

# Create your models here.
class DirectRating():
    def __init__(self,org_name,cust_rating,market_share):
        self.org_name = org_name
        self.cust_rating=cust_rating
        self.market_share=market_share


class InDirectRating():
    def __init__(self, org_name, cust_rating,market_share):
        self.org_name = org_name
        self.cust_rating = cust_rating
        self.market_share = market_share


