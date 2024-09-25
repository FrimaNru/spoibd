print("Hello World")

def get_math_text(a, b, c): 
    d = (b ** 2) - 4 * a * c
    if (d < 0):
        return None 
    else:
        x1 = ((b * (-1)) + d ** 0.5) / 2 * a
        x2 = ((b * (-1)) - d ** 0.5) / 2 * a
        return [x1, x2]
    
a = input("Введите коэффициент a")
b = input("Введите коэффициент b")
c = input("Введите коэффициент c")

solution = get_math_text(a,b,c)

print(solution)
