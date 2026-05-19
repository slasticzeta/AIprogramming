def calc2(a, b):
    return a**b

a, b = input().split()
a, b = int(a), int(b)

result = calc2(a, b)
print(result)