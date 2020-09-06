sql = ''
with open('text/main.txt', 'r') as f:
    sql += f.readlines()

with open('text/main.txt', 'w') as f:
    f.writelines(sql[1:])
print(sql)