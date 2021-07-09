queue = set()
queue.add((1,2))
queue.add((2,3))
queue.add((3,4))
queue.remove((1,2))
x = {"apple":2,"pears":1,"banana":5,"peach":1}
a = {word: rank for word, rank in sorted(x.items(), key=lambda item: item[1])}
b = [word for word in a.keys()]
s = {(1,1),(2,2),(3,3),(4,4),(5,5)}

l = 3
w = [(l,num) for num in range(10)]
print(w)
