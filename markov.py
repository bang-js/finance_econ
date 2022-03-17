#####
# Markov chain
#####

# SIMPLE EXAMPLE (2by2)
import numpy as np

aa = float(input("P[A(t)->A(t+1)] :"))
# ab = float(input("P[A(t)->B(t+1)] :"))
ab = 1 - aa 
ba = float(input("P[B(t)->A(t+1)] :"))
# bb = float(input("P[B(t)->B(t+1)] :"))
bb = 1 - ba
iter = int(input("iteration :"))
a_0 = float(input("A(0) :"))
b_0 = float(input("B(0) :"))

mat = np.array([[aa,ab],[ba,bb]])
initial = np.array([a_0,b_0])

def markov_pred(mat,iter,initial):
    mat_temp = mat
    for i in range(iter-1):
        mat_temp = mat_temp.dot(mat)
    return initial.dot(mat_temp)

result = markov_pred(mat,iter,initial)
print(result)

# 추가할 요소 : iteration 횟수 1->100 로 갈 때 결과물 그래프로
# https://bskyvision.com/573
