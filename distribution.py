import math

###
# POISSON DIST
###

lambd = int(input("lambda값:"))

def poisson_pdf(x):
    poisson_pdf_value = math.exp((-1)*lambd) * pow(lambd,x) / math.factorial(x)
    return poisson_pdf_value

for i in range(10) :
    print("x={}".format(i), round(poisson_pdf(i),8))
