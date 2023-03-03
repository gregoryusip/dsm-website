from flask import Flask, render_template
import pandas as pd # reading all required header files
import numpy as np
import random
import operator
import math
# import matplotlib.pyplot as plt

# df = 0.59	0.80	0.73	0.61	0.49	0.9	0.8	1.0	0.7	1.0	0.8	0.7	0.6	0.8	1.0	0.8
					
# Number of Clusters
k = 5
# Maximum number of iterations
MAX_ITER = 100
# Fuzzy parameter
m = 1.7 #Select a value greater than 1 else it will be knn

n = 1

# params = 16

def initializeMembershipMatrix(): # initializing the membership matrix
    membership_mat = []
    for i in range(n):
        random_num_list = [random.random() for i in range(k)]
        summation = sum(random_num_list)
        temp_list = [x/summation for x in random_num_list]
        
        flag = temp_list.index(max(temp_list))
        for j in range(0,len(temp_list)):
            if(j == flag):
                temp_list[j] = 1
            else:
                temp_list[j] = 0
        
        membership_mat.append(temp_list)
    return membership_mat

df_center = pd.read_csv("Dataset/center.csv")
cluster_centers = df_center.values.tolist()

def updateMembershipValue(membership_mat, cluster_centers, result): # Updating the membership value
    p = float(2/(m-1))
    for i in range(n):
        x = result[i]
        distances = [np.linalg.norm(np.array(list(map(operator.sub, x, cluster_centers[j])))) for j in range(k)]
        for j in range(k):
            den = sum([math.pow(float(distances[j]/distances[c]), p) for c in range(k)])
            membership_mat[i][j] = float(1/den)       
    return membership_mat

def getClusters(membership_mat): # getting the clusters
    cluster_labels = list()
    for i in range(n):
        max_val, idx = max((val, idx) for (idx, val) in enumerate(membership_mat[i]))
        cluster_labels.append(idx)
    return cluster_labels

def fuzzyCMeansClustering(result): #Third iteration Random vectors from data
    
    # Membership Matrix
    membership_mat = initializeMembershipMatrix()
    curr = 0
    percentage = []
    while curr < MAX_ITER:
        membership_mat = updateMembershipValue(membership_mat, cluster_centers, result)
        cluster_labels = getClusters(membership_mat)
        curr += 1
    percentage = np.array(membership_mat)
    return cluster_labels, cluster_centers, percentage
