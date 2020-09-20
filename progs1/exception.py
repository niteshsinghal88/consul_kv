KV = [
    {
    "name": "Nitesh",
    "last_name": None,
    "id": 21,
    "batch": 2020
},
    {
    "name": "perci",
    "last_name": None,
    "id": 21,
    "batch": 2020
}
    ]

try:
    print(KV.keys("name"))
except AttributeError as e:
    print('Attribute not found', e)
print('Program executed successfully')