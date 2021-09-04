import math
from itertools import chain, combinations
import numpy as np
from pyitlib import discrete_random_variable as drv
import pandas as pd
from sympy import *
from sympy import roots, solve_poly_system

#Weight Calculation_1
def wt1(val):
  sum = 0
  w=[]
  for i in range(3):
    w.append([0,0,0])
  for i in range(3):
    for j in range(3):
      if (i == j):
        w[i][j] = 0
      if (i != j):
        sum = 0
        for k in range(3):
          if  (k!=i and k!=j):
            sum = sum + val[k]
        avg = sum/3
        w[i][j] = avg
  return w

#Weight Calculation_2
def wt2(val):
  sum = 0
  w=[]
  for i in range(3):
    w.append([0,0,0])
  for i in range(3):
    for j in range(3):
      if (i == j):
        w[i][j] = 0
      if (i != j):
        sum = 0
        sum = math.log10(1/val[i])+math.log10(1/val[j])
        avg = sum/2
        w[i][j] = avg
  return w

#Weight Calculation_3
def wt3(val):
  sum = 0
  w=[]
  for i in range(3):
    w.append([0,0,0])
  for i in range(3):
    for j in range(3):
      if (i == j):
        w[i][j] = 0
      if (i != j):
        sum = 0
        sum = 1/val[i]+1/val[j]
        avg = sum/2
        w[i][j] = avg

  maximum = 0
  for i in range(len(w)):
    for j in range(len(w[0])):
      maximum = max(maximum, w[i][j])

  for i in range(len(w)):
    for j in range(len(w[0])):
      w[i][j] = w[i][j]/maximum
  return w

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def shapley_calculation(pred_mat, w, Y):
  shapley_value_list = []
  N = [1,2,3]
  total = 0
  for i in range(1, 4, 1):
    X_i = []
    for asdf in range(len(pred_mat)):
      X_i.append(pred_mat[asdf][i-1])
    X_i = np.asarray(X_i)
    M = []
    for j in range(len(N)):
      if(i != N[j]):
        M.append(N[j])
    classifier_list =list(powerset(M))
    for k in range(len(classifier_list)):
      st = str(classifier_list[k])
      classifier_subset = []
      for l in range(len(st)):
        if(st[l] == "1" or st[l] == "2" or st[l] == "3"):
          classifier_subset.append(int(st[l]))
      total = 0
      if(len(classifier_subset) == 1):
        a_1 = classifier_subset[0]
        X_1 = []
        for asdf in range(len(pred_mat)):
          X_1.append(pred_mat[asdf][a_1-1])
        X_1 = np.asarray(X_1)
        m_info_class = drv.information_mutual(X_i, Y)
        m_info_classif = drv.information_mutual(X_i, X_1)
        marginal_info = m_info_class - w[i-1][a_1-1]*m_info_classif
        total = total + (marginal_info*1/6)
      if(len(classifier_subset) == 2):
        a_1 = classifier_subset[0]
        a_2 = classifier_subset[1]
        X_1 = []
        X_2 = []
        for asdf in range(len(pred_mat)):
          X_1.append(pred_mat[asdf][a_1-1])
        X_1 = np.asarray(X_1)
        for asdf in range(len(pred_mat)):
          X_2.append(pred_mat[asdf][a_2-1])
        X_2 = np.asarray(X_2)
        m_info_class = drv.information_mutual(X_i, Y)
        m_info_classif_1 = drv.information_mutual(X_i, X_1)
        m_info_classif_2 = drv.information_mutual(X_i, X_2)
        m_info_classif = (w[i-1][a_1-1]*m_info_classif_1 + w[i-1][a_2-1]*m_info_classif_2)/2
        marginal_info_2 = m_info_class - m_info_classif
        total = total + (marginal_info_2*2/6)
    shapley_value = total 
    shapley_value_list.append(shapley_value)
  return shapley_value_list

def subset_list():
  N = [1,2,3]
  Subset_list = []
  total = 0
  for i in range(1, 4, 1):
    K =[]
    K.append(i)
    Subset_list.append(K)
  for i in range(1, 4, 1):
    for d in range(1,4,1):
      K = []
      if(d == i):
        break
      K.append(d)
      K.append(i)
      Subset_list.append(K)
  for i in range(1, 4, 1):
    for d in range(1,4,1):
      if(d == i):
        break
      for f in range(1,4,1):
        K = []
        if( f == d or f==i):
          break
        K.append(f)
        K.append(d)
        K.append(i)
        Subset_list.append(K)
  for i in range(1, 4, 1):
    for d in range(1,4,1):
      if(d == i):
        break
      for f in range(1,4,1):
        if( f == d or f==i):
          break
        for r in range(1,4,1):
          K = []
          if( r == d or r==i or r == f):
            break
          K.append(r)
          K.append(f)
          K.append(d)
          K.append(i)
          Subset_list.append(K)
  return Subset_list

def Cal_lambda_fuzzy(shapley_value_list, Subset_list):
  a1 = shapley_value_list[0]
  a2 = shapley_value_list[1]
  a3 = shapley_value_list[2]
  x = symbols('x')
  l = solve((a1*a2*a3)*x**3 + (a1*a2 + a2*a3 + a3*a1)*x**2 + (a1+a2+a3-1)*x, x)
  list_mu = []
  list_mu.append(shapley_value_list[0])
  list_mu.append(shapley_value_list[1])
  list_mu.append(shapley_value_list[2])
  for i in range(3, len(Subset_list)-1):
    K = Subset_list[i]
    if (len(K)==2):
      m1 = K[0]
      m2 = K[1]
      sv = shapley_value_list[m1-1] + shapley_value_list[m2-1] + l[2]*shapley_value_list[m1-1]*shapley_value_list[m2-1]
      list_mu.append(sv)
  list_mu.append(1)
  return list_mu

def class_0_pred(class_0,list_mu, Subset_list):
  fa_cl0 = []
  for sample in range(len(class_0)):
    min_cl0 = min(class_0[sample])
    ar1 = []
    val1 = []
    ar2 = []
    val2 = []
    ar3 = []
    val3 = []
    ar4 = []
    val4 = []
    db = 0
    for i in range(len(class_0[sample])):
      if (class_0[sample][i] == min_cl0 and db == 0):
        temp = i
        db = db + 1
        v1 = class_0[sample][temp]
      else :
        ar1.append(i+1)
        val1.append(class_0[sample][i])
    for j in range(len(Subset_list)):
      if (ar1 == Subset_list[j]):
        f2 = list_mu[j]

    min_cl0 = min(val1)
    db = 0
    for i in range(len(val1)):
      if (val1[i] == min_cl0 and db == 0):
        temp = i
        db =  db + 1
        v2 = val1[temp]
      else :
        ar2.append(ar1[i])
        val2.append(class_0[sample][ar1[i]-1])
    for j in range(len(Subset_list)):
      if (ar2 == Subset_list[j]):
        f3 = list_mu[j]
  
    min_cl0 = min(val2)
    db = 0
    for i in range(len(val2)):
      if (val2[i] == min_cl0 and db == 0):
        temp = i
        db =  db + 1
        v3 = val2[temp]
      else :
        ar3.append(ar2[i])
        val3.append(class_0[sample][ar2[i]-1])
    fuzzy_estimate_cl0 = v1*1 + (v2-v1)*f2 + (v3-v2)*f3
    fa_cl0.append(fuzzy_estimate_cl0)
  return fa_cl0

def class_1_pred(class_1,list_mu, Subset_list):
  fa_cl1 = []
  for sample in range(len(class_1)):
    min_cl1 = min(class_1[sample])
    ar1 = []
    val1 = []
    ar2 = []
    val2 = []
    ar3 = []
    val3 = []
    ar4 = []
    val4 = []
    db = 0
    for i in range(len(class_1[sample])):
      if (class_1[sample][i] == min_cl1 and db == 0):
        temp = i
        db = db + 1
        v1 = class_1[sample][temp]
      else :
        ar1.append(i+1)
        val1.append(class_1[sample][i])
    for j in range(len(Subset_list)):
      if (ar1 == Subset_list[j]):
        f2 = list_mu[j]

    min_cl0 = min(val1)
    db = 0
    for i in range(len(val1)):
      if (val1[i] == min_cl0 and db == 0):
        temp = i
        db =  db + 1
        v2 = val1[temp]
      else :
        ar2.append(ar1[i])
        val2.append(class_1[sample][ar1[i]-1])
    for j in range(len(Subset_list)):
      if (ar2 == Subset_list[j]):
        f3 = list_mu[j]
  
    min_cl0 = min(val2)
    db = 0
    for i in range(len(val2)):
      if (val2[i] == min_cl0 and db == 0):
        temp = i
        db =  db + 1
        v3 = val2[temp]
      else :
        ar3.append(ar2[i])
        val3.append(class_1[sample][ar2[i]-1])
    fuzzy_estimate_cl1 = v1*1 + (v2-v1)*f2 + (v3-v2)*f3
    fa_cl1.append(fuzzy_estimate_cl1)
  return fa_cl1

def class_2_pred(class_2,list_mu, Subset_list):
  fa_cl2 = []
  for sample in range(len(class_2)):
    min_cl2 = min(class_2[sample])
    ar1 = []
    val1 = []
    ar2 = []
    val2 = []
    ar3 = []
    val3 = []
    ar4 = []
    val4 = []
    db = 0
    for i in range(len(class_2[sample])):
      if (class_2[sample][i] == min_cl2 and db == 0):
        temp = i
        db = db + 1
        v1 = class_2[sample][temp]
      else :
        ar1.append(i+1)
        val1.append(class_2[sample][i])
    for j in range(len(Subset_list)):
      if (ar1 == Subset_list[j]):
        f2 = list_mu[j]

    min_cl0 = min(val1)
    db = 0
    for i in range(len(val1)):
      if (val1[i] == min_cl0 and db == 0):
        temp = i
        db =  db + 1
        v2 = val1[temp]
      else :
        ar2.append(ar1[i])
        val2.append(class_2[sample][ar1[i]-1])
    for j in range(len(Subset_list)):
      if (ar2 == Subset_list[j]):
        f3 = list_mu[j]
  
    min_cl0 = min(val2)
    db = 0
    for i in range(len(val2)):
      if (val2[i] == min_cl0 and db == 0):
        temp = i
        db =  db + 1
        v3 = val2[temp]
      else :
        ar3.append(ar2[i])
        val3.append(class_2[sample][ar2[i]-1])
    fuzzy_estimate_cl2 = v1*1 + (v2-v1)*f2 + (v3-v2)*f3
    fa_cl2.append(fuzzy_estimate_cl2)
  return fa_cl2

def cal_result(fa_cl0, fa_cl1, fa_cl2):
  result = []
  for i in range(len(fa_cl0)):
    maximum = max(fa_cl0[i] , fa_cl1[i] , fa_cl2[i])
    if(maximum == fa_cl0[i]):
      result.append(0)
    if(maximum == fa_cl1[i]):
      result.append(1)
    if(maximum == fa_cl2[i]):
      result.append(2)
  return result

def majority_aggregation(result1, result2, result3):
  result = []
  for i in range(len(result1)):
    if (result1[i]==result2[i] or result1[i]==result3[i]):
      result.append(result1[i])
    elif (result2[i]==result3[i]):
      result.append(result2[i])
    else:
      result.append(result3[i])
  return result
