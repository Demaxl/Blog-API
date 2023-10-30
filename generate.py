from api.models import *
import json

with open("MOCK_DATA.json", "r") as file:
    data = json.load(file)

for row in data:
    Article.objects.create(**row)