#####
# Markov chain
# https://bskyvision.com/573
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

# 99번 iteration에 대한 visualization
import matplotlib.pyplot as plt

result_a = np.zeros(99)
result_b = np.zeros(99)
for i in range(2,101) :
  # print(markov_pred(mat,initial,iteration=i))
  result_a[i-2], result_b[i-2] = markov_pred(mat,initial,i)

plt.plot(np.arange(99), result_a, result_b)


