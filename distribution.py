import math

#####
# POISSON DIST
#####

lambd = int(input("lambda값:"))

def poisson_pdf(x):
    poisson_pdf_value = math.exp((-1)*lambd) * pow(lambd,x) / math.factorial(x)
    return poisson_pdf_value

def poisson_cdf(x):
    poisson_cdf_value = 0
    for i in range(x+1) :
        poisson_cdf_value += math.exp((-1)*lambd) * pow(lambd,i) / math.factorial(i)
    return poisson_cdf_value

for i in range(10) :
    print("x={}".format(i), round(poisson_pdf(i),8))
    
print("cdf")
for i in range(10) :
    print("x={}".format(i), round(poisson_cdf(i),8))
