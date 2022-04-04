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


# v(단위당 평균횟수), t(총 단위), z(시행횟수) 가 주어질 때 포아송 분포 계산
# t동안(에서) z번 이상 발생할 확률 : P[Z(t) >= z] = SIGMA_(x=z)^(inf)[(exp(-vt)*(vt)^(-x))/x!] 
#                                                = 1 - SIGMA_(x=0)^(z-1)[(exp(-vt)*(vt)^(-x))/x!]
# 이상, 이하, 초과, 미만은 SIGMA의 시작/끝값을 적절히 조정해야함
# t동안(에서) z번 발생할 확률 : P[Z(t) = z] = [(exp(-vt)*(vt)^(-z))/z!] 

v = float(input("단위당 평균횟수(v):"))
t = float(input("총 단위(t):"))
z = int(input("시행횟수(z):"))
q_range = input("z 기준 more/less/over/under/point 중 택일:")

def poisson_v2_under(v1,t1,z1):
    prob = 0
    for i in range(z1) :
        prob += (math.exp(-v1*t1))*(pow(v1*t1,i))/(math.factorial(i))
    return prob

def poisson_v2_point(v2,t2,z2):
    prob = (math.exp(-v2*t2))*(pow(v2*t2,z2))/(math.factorial(z2))
    return prob

if q_range == 'more' :
    a = poisson_v2_under(v,t,z)
    print("prob:", 1-a)
elif q_range == 'point' :
    b = poisson_v2_point(v,t,z)
    print("prob:", b)
elif q_range == 'under' :
    print("prob:", poisson_v2_under(v,t,z))
elif q_range == 'less' : # P[Z <= z] = P[Z < z] + P[Z = z] => under + point
    print("prob:", poisson_v2_under(v,t,z) + poisson_v2_point(v,t,z) )
elif q_range == 'over' : # P[Z > z] = 1- P[Z < z] - P[Z = z] => 1 - under - point
    print("prob:", 1 - poisson_v2_under(v,t,z) - poisson_v2_point(v,t,z) )
else : 
    print("올바른 범위 작성 요망")
