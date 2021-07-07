queue = set()
queue.add((1,2))
queue.add((2,3))
queue.add((3,4))
queue.remove((1,2))
x = {"apple":2,"pears":1,"banana":5,"peach":1}
a = {word: rank for word, rank in sorted(x.items(), key=lambda item: item[1])}
b = [word for word in a.keys()]
print(a)
print(b)