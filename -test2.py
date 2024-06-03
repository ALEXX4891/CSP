import json
y = [1, 2, 3]
z = [[1, 2, 3], [1, 2, 3]]
x = []
x.append(y)
x.append(z)

json = json.dumps(x)
print(json)

#откроем нашу книгу и проверим содержимое
book = open("order.txt", 'r')
text = book.readlines()
print('text: ', text)
data = []
W = 0


for i in range(len(text)):
  if i == 0:
    W = int(text[i])
  if i > 0:
    str = text[i].split(' ')
    str[1] = int(str[1])
    str[0] = int(str[0])
    data.append(tuple(str))

print('data: ', data)
print('W: ', W)