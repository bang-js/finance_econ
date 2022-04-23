#####
# Markov chain
# https://bskyvision.com/573
#####

###
# SIMPLE EXAMPLE (2by2)
# Pr(x(t+1)=x(0)|x(t)=x(1))을 matrix화
###
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

# 99번 iteration에 대한 visualization : unconditional prob. 계산
import matplotlib.pyplot as plt

result_a = np.zeros(99)
result_b = np.zeros(99)
for i in range(2,101) :
  # print(markov_pred(mat,initial,iteration=i))
  result_a[i-2], result_b[i-2] = markov_pred(mat,initial,i)

plt.plot(np.arange(99), result_a, result_b)

###
# general case (n by n) 
###
import numpy as np
import sys

n = int(input("matrix dimension :")) # 행렬 차원 설정
mat = []
for i in range(n) :
    my_list = list(map(float, input("{}번 입력:".format(n-1)).split())) # 반환값을 &nbsp; 기준으로 각각을 쪼개서 list로 저장, 헷갈리지 않도록 n-1번 입력하라고 명시
    if 1-sum(my_list) < 0 : # n-1개의 합이 1을 넘어버리면 오류로 간주하고 실행중단
        print("error")
        sys.exit(0) # 실행중단
    my_list.append(1-sum(my_list)) # 마지막 확률값은 1-sum(.)이므로 자동으로 계산한 뒤 마지막 원소로 추가
    mat.append(my_list) # list를 행렬(리스트)의 각 원소로 저장
mat = np.array(mat) 
print(mat)

# 반복횟수
iter = int(input("iteration :"))
# n개의 초기값 입력
initial = np.array(
    list(map(float, input("{}개의 초기값 :".format(n)).split()))
)

def markov_pred(mat,iter,initial):
    mat_temp = mat
    for i in range(iter-1):
        mat_temp = mat_temp.dot(mat)
    return initial.dot(mat_temp)

result = markov_pred(mat,iter,initial)
print(result)

##
# general case vasualization
##

import matplotlib.pyplot as plt
import pandas as pd

max_iter = int(input("iteration 수:"))
result = np.empty((0,n),int)
for i in range(2,max_iter) :
  temp = np.array([markov_pred(mat,initial,i)])
  result = np.append(result, temp, axis=0)

# df을 사용하여 중첩하여 그리기
df = pd.DataFrame(result)
print(df)

plt.figure(figsize=(10,5))
for a in range(n):
    plt.plot(np.arange(max_iter-2), df[a], "-", label=str(a))
plt.show()

# subplot을 이용하여 여러 그래프로 그리기
result = result.T
rows = int(np.ceil(n/5)) # ceil : 올림
cols = n if rows < 2 else 5  # 행이 1개면 열의 개수는 샘플의 개수, 그렇지 않으면 10개
fig, axs = plt.subplots(rows, cols, figsize=(15, 3), squeeze=False)
for i in range(rows) :
  for j in range(cols) :
    if i*5+j < n :
      axs[i,j].plot(result[i*5+j])
plt.show()

# symmetric markov
# rho = 2*pi-1 (rho : serial corr)
