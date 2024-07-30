pointed_cats = []

cats = {'cc': '1',
        'ss': '2',
        'tt': ['3', '4']}
servs = ['11', '22']
for cat in cats:
    pointed_cat = {
        'name': cat,
    }
    for serv in servs:
        pointed_serv = {
            'name': serv,
            'price': serv
        }
        pointed_cat['services'] = pointed_serv
    pointed_cats.append(pointed_cat)

for i in pointed_cats:

    print(i['services']['name'])

