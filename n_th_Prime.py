######
# n번째 소수 찾기
######

n = int(input("order:"))

def nth_Prime(n) :
    if n == 1 :
        return 2
    else : 
        prime_list = [2]
        a = prime_list[-1]
        while len(prime_list) < n :
            a += 1
            m = 0
            for i in range(2,int(a**(0.5)+1)+1) :  # ROOT로 근사, 3의 경우 int(3**0.5+1)=2 라서 range(2,3)을 위해 +1
                if a%i == 0 :
                    break
                else :
                    m += 1
            if m == int(a**(0.5)+1)-1 :  
                prime_list.append(a)
        return prime_list[-1]

print(nth_Prime(n))
