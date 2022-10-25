import math
from sympy import diff,symbols
import numpy as np

x = symbols("x")

def sum_squared(n):
    odd = np.arange(1,2*n+1,2)
    odd_sq = np.square(odd)
    odd_sq_sum = np.sum(odd_sq)
    return(odd_sq_sum)

print(sum_squared(20))

def bisection(f,x0,x1):
    if f(x0)*f(x1) > 0:
        return None
    
    for i in range(20):
        xr = (x0+x1)/2
        
        if f(x0)*f(xr) < 0:
            x1 = xr
            
        if f(x1)*f(xr) < 0:
            x0 = xr
        elif xr ==0:
            return(xr)
    return(xr)

f = lambda x: math.sin(x)*((math.e**x)**0.1)
print(bisection(f, 1, 4.1))


f = lambda x: x**2+5*x-8
df= f(x).diff(x)

def newton_rapson(f,x0,e):
    for i in range(10):
        
        x1 = x0-(f(x0)/df.subs({x:x0}))
        
        if abs(x1-x0) < e:
            return round(x1,4)
        print(f"x0: {round(x0,2)}, x1: {round(x1,2)}")
        x0 = x1
            
root = newton_rapson(f, 0, 0.005)
print(root)


def mod_secant(f,x0,e):
   
    for i in range(5):
        delta = 0.005
        x1 = x0+delta*x0
        
        dx = -f(x0)/(f(x0)-f(x1))*(x0-x1)
        
        xr = x0-(dx*f(x0))/(f(x0+dx)-f(x0))
            
        if abs(xr-x0) < e:
            return xr,i
        x0 = xr
        
f = lambda x: np.exp(-x)-x

            
root = mod_secant(f, 6, 0.005)
print(root)


f = lambda x: x**2+4*x-12

def secant(f,x0,x1):
    if f(x0)*f(x1) > 0:
        return None
    
    for i in range(10):
        xr = x0 - f(x0)*(x1-x0)/(f(x1)-f(x0))
        
        if f(x0)*f(xr) < 0:
            x1 = xr
            
        if f(x1)*f(xr) < 0:
            x0 = xr
            
        elif f(xr) == 0:
            return xr
        
    return(xr)

root = secant(f,-7,1)
print(root)



################ Poly Root Finding ###############


def Muller(f,xr,h,e):
    x2 = xr
    x0 = x2-h*xr
    x1 = x2+h*xr

    for i in range(10):
        h0 = x1-x0
        h1 = x2-x1
        d0 = (f(x1)-f(x0))/h0
        d1 = (f(x2)-f(x1))/h1

        a = (d1-d0)/(h1-h0)
        b = a*h1 + d1
        c = f(x2)

        rad = np.sqrt(b**2 - 4*a*c)

        if abs(b+rad) > abs(b-rad):
            den = b+rad
        else:
            den = b-rad

        dxr = -2*c/den
        xr = x2 + dxr

        if abs(dxr) < e*xr:
            return(xr)

        x0 = x1
        x1 = x2
        x2 = xr
    return(xr)

f = lambda x: x**3-13*x-12
print(Muller(f,5,0.5,0.002))



        




print(eval("0"))

f = lambda x: eval("x*0")
x = np.array([1,2,3,4])
print(f(x))