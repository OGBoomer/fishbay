from specs.models import Pattern


data_list = 'solid, striped, plaid'


for data in data_list:
    code = '&Pattern=' + data
    Pattern.objects.create(name=data, code=code)
    print(f'{data} added')

print("all done")
