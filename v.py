def smart(f):
    def swap(a,b):
        if a<b:
            b,a=a,b
        return f(a,b)
    return swap

@smart
def division(a,b):
    return (a/b)

print(division(2,4))
