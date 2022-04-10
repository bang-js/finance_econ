import math

#####
# Binomial dist
#####

n = int(input("n(총횟수)값:"))
p = float(input("p(성공확률)값:"))

def bin_pdf(n,p,x):
    bin_pdf_value = (math.factorial(n)/(math.factorial(x)*math.factorial(n-x)))*pow(p,x)*pow(1-p,n-x)
    return bin_pdf_value

def bin_cdf(n,p,x):
    bin_cdf_value = 0
    for i in range(x+1) :
        bin_cdf_value += (math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))*pow(p,i)*pow(1-p,n-i)
    return bin_cdf_value

print("cdf")
i=0
while bin_cdf(n,p,i) <= 0.999 :
    print("x={}".format(i), round(bin_cdf(n,p,i),8))
    i += 1
# cdf가 0.999를 넘지않는 최대 x를 i로 고정
print("pdf")
for j in range(i) :
    print("x={}".format(j), round(bin_pdf(n,p,j),8))

#####
# hypergeometric dist : K, M, n
#####

print("hypergeometric dist")
n = int(input("n(선택횟수)값:"))
k = int(input("k(대상(불량) 수)값:"))
m = int(input("m(전체표본 수)값:"))

def combination(a,b):
    return (math.factorial(a))/(math.factorial(b)*math.factorial(a-b))

def hg_pdf(n,k,m,x):
    hg_pdf_value = (combination(k,x)*combination(m-k,n-x))/combination(m,n)
    return hg_pdf_value

def hg_cdf(n,k,m,x):
    hg_cdf_value = 0
    for i in range(x+1) :
        hg_cdf_value += (combination(k,i)*combination(m-k,n-i))/combination(m,n)
    return hg_cdf_value

print("cdf")
i=0
while hg_cdf(n,k,m,i) <= 0.999 :
    print("x={}".format(i), round(hg_cdf(n,k,m,i),8))
    i += 1
# cdf가 0.999를 넘지않는 최대 x를 i로 고정
print("pdf")
for j in range(i) :
    print("x={}".format(j), round(hg_pdf(n,k,m,j),8))

#####
# POISSON DIST
#####

lambd = int(input("lambda값:"))

def poisson_pdf(lambd, x):
    poisson_pdf_value = math.exp((-1)*lambd) * pow(lambd,x) / math.factorial(x)
    return poisson_pdf_value

def poisson_cdf(lambd, x):
    poisson_cdf_value = 0
    for i in range(x+1) :
        poisson_cdf_value += math.exp((-1)*lambd) * pow(lambd,i) / math.factorial(i)
    return poisson_cdf_value

print("cdf")
i=0
while poisson_cdf(lambd,i) <= 0.999 :
    print("x={}".format(i), round(poisson_cdf(lambd, i),8))
    i += 1
# cdf가 0.999를 넘지않는 최대 x를 i로 고정
print("pdf")
for j in range(i) :
    print("x={}".format(j), round(poisson_pdf(lambd,j),8))

# v(단위당 평균횟수), t(총 단위), z(시행횟수) 가 주어질 때 포아송 분포 계산
# t동안(에서) z번 이상 발생할 확률 : P[Z(t) >= z] = SIGMA_(x=z)^(inf)[(exp(-vt)*(vt)^(-x))/x!] 
#                                                = 1 - SIGMA_(x=0)^(z-1)[(exp(-vt)*(vt)^(-x))/x!]
# 이상, 이하, 초과, 미만은 SIGMA의 시작/끝값을 적절히 조정해야함
# t동안(에서) z번 발생할 확률 : P[Z(t) = z] = [(exp(-vt)*(vt)^(-z))/z!] 


v = float(input("단위당 평균횟수(v):"))
t = float(input("총 단위(t):"))
z = int(input("시행횟수(z):"))
q_range = input("z 기준 more(초과)/less(미만)/notless(이상)/notmore(이하)/point 중 택일:")

def poisson_v2_under(v1,t1,z1): # under : 미만
    prob = 0
    for i in range(z1) : # z1을 포함X
        prob += (math.exp(-v1*t1))*(pow(v1*t1,i))/(math.factorial(i))
    return prob

def poisson_v2_point(v2,t2,z2):
    prob = (math.exp(-v2*t2))*(pow(v2*t2,z2))/(math.factorial(z2))
    return prob

if q_range == 'notless' :
    a = poisson_v2_under(v,t,z)
    print("prob:", 1-a)
elif q_range == 'point' :
    b = poisson_v2_point(v,t,z)
    print("prob:", b)
elif q_range == 'less' :
    print("prob:", poisson_v2_under(v,t,z))
elif q_range == 'notmore' : # P[Z <= z] = P[Z < z] + P[Z = z] => under + point
    print("prob:", poisson_v2_under(v,t,z) + poisson_v2_point(v,t,z) )
elif q_range == 'more' : # P[Z > z] = 1- P[Z < z] - P[Z = z] => 1 - under - point
    print("prob:", 1 - poisson_v2_under(v,t,z) - poisson_v2_point(v,t,z) )
else : 
    print("올바른 범위 작성 요망")
