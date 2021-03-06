#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 13:16:54 2020

@author: pfm
"""
import numpy as np


def Dlp(A, B, p=2):
    cost = np.sum(np.power(np.abs(A - B), p))
    return np.power(cost, 1 / p)


def twed(A, timeSA, B, timeSB, nu, _lambda):
    # [distance, DP] = TWED( A, timeSA, B, timeSB, lambda, nu )
    # Compute Time Warp Edit Distance (TWED) for given time series A and B
    #
    # A      := Time series A (e.g. [ 10 2 30 4])
    # timeSA := Time stamp of time series A (e.g. 1:4)
    # B      := Time series B
    # timeSB := Time stamp of time series B
    # lambda := Penalty for deletion operation
    # nu     := Elasticity parameter - nu >=0 needed for distance measure
    # Reference :
    #    Marteau, P.; F. (2009). "Time Warp Edit Distance with Stiffness Adjustment for Time Series Matching".
    #    IEEE Transactions on Pattern Analysis and Machine Intelligence. 31 (2): 306–318. arXiv:cs/0703033
    #    http://people.irisa.fr/Pierre-Francois.Marteau/

    # Check if input arguments
    if len(A) != len(timeSA):
        print("The length of A is not equal length of timeSA")
        return None, None

    if len(B) != len(timeSB):
        print("The length of B is not equal length of timeSB")
        return None, None

    if nu < 0:
        print("nu is negative")
        return None, None

    # Add padding
    A = np.array([0] + list(A))
    timeSA = np.array([0] + list(timeSA))
    B = np.array([0] + list(B))
    timeSB = np.array([0] + list(timeSB))

    n = len(A)
    m = len(B)
    # Dynamical programming
    DP = np.zeros((n, m))

    # Initialize DP Matrix and set first row and column to infinity
    DP[0, :] = np.inf
    DP[:, 0] = np.inf
    DP[0, 0] = 0

    # Compute minimal cost
    for i in range(1, n):
        for j in range(1, m):
            # Calculate and save cost of various operations
            C = np.ones((3, 1)) * np.inf
            # Deletion in A
            C[0] = (
                DP[i - 1, j]
                + Dlp(A[i - 1], A[i])
                + nu * (timeSA[i] - timeSA[i - 1])
                + _lambda
            )
            # Deletion in B
            C[1] = (
                DP[i, j - 1]
                + Dlp(B[j - 1], B[j])
                + nu * (timeSB[j] - timeSB[j - 1])
                + _lambda
            )
            # Keep data points in both time series
            C[2] = (
                DP[i - 1, j - 1]
                + Dlp(A[i], B[j])
                + Dlp(A[i - 1], B[j - 1])
                + nu * (abs(timeSA[i] - timeSB[j]) + abs(timeSA[i - 1] - timeSB[j - 1]))
            )
            # Choose the operation with the minimal cost and update DP Matrix
            DP[i, j] = np.min(C)
    distance = DP[n - 1, m - 1]
    return distance, DP

def backtracking(DP):
    # [ best_path ] = BACKTRACKING ( DP )
    # Compute the most cost efficient path
    # DP := DP matrix of the TWED function

    x = np.shape(DP)
    i = x[0] - 1
    j = x[1] - 1

    # The indices of the paths are save in opposite direction
    # path = np.ones((i + j, 2 )) * np.inf;
    best_path = []

    steps = 0
    while i != 0 or j != 0:
        best_path.append((i - 1, j - 1))

        C = np.ones((3, 1)) * np.inf

        # Keep data points in both time series
        C[0] = DP[i - 1, j - 1]
        # Deletion in A
        C[1] = DP[i - 1, j]
        # Deletion in B
        C[2] = DP[i, j - 1]

        # Find the index for the lowest cost
        idx = np.argmin(C)

        if idx == 0:
            # Keep data points in both time series
            i = i - 1
            j = j - 1
        elif idx == 1:
            # Deletion in A
            i = i - 1
            j = j
        else:
            # Deletion in B
            i = i
            j = j - 1
        steps = steps + 1

    best_path.append((i - 1, j - 1))

    best_path.reverse()
    return best_path[1:]

# Simple test
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    A=np.array([[0],[0],[1],[1],[2],[3],[5],[2],[0],[1],[-0.1]])
    tA=list(i for i in range(len(A)))
    B=np.array([[0],[1],[2],[2.5],[3],[3.5],[4],[4.5],[5.5],[2],[0],[0],[.25],[.05],[0]])
    tB=list(i for i in range(len(B)))
    C=np.array([[4],[4],[3],[3],[3],[3],[2],[5],[2],[.5],[.5],[.5]])
    tC=list(i for i in range(len(C)))
    nu=.1
    _lambda=.2
    print("twed(A,B,nu,lambda)=", twed(A,tA,B,tB,nu,_lambda)[0])
    print("twed(A,C,nu,lambda)=", twed(A,tA,C,tC,nu,_lambda)[0])
    print("twed(B,C,nu,lambda)=", twed(B,tB,C,tC,nu,_lambda)[0])
        
    plt.plot(A, label='A')
    plt.plot(B, label='B')
    plt.plot(C, label='C')
    plt.legend()
    plt.show()