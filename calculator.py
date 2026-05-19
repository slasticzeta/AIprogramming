def calc(a, b, c):
    if b == '+':
        return a + c
    elif b == '-':
        return a - c
    elif b == '*':
        return a * c
    elif b == '/':
        if c == 0:
            return "0으로 나눌 수 없습니다"
        return a / c
    else:
        return "지원하지 않는 연산자입니다"

a, b, c = input().split()
a, c = int(a), int(c)

result = calc(a, b, c)
print(result)