# Unique Binary Search Trees Design
## Introduction
The unique binary search trees system calculates the number of structurally unique binary search trees that can be formed with n nodes, where each node has a unique value from 1 to n.

## Algorithm
The system will use dynamic programming to calculate the number of unique BST's. The algorithm will be based on the concept of combinatorics and the properties of BST's.

## Data Structures
1. An array to store the number of unique BST's for each value of n from 1 to n.

## Components
1. A function to calculate the number of unique BST's for a given n.
2. A function to initialize the array and calculate the base cases.

## Example Use Cases
1. Input: n = 3, Output: 5
2. Input: n = 1, Output: 1

## Pseudocode
```
function uniqueBSTs(n):
  initialize array dp of size n+1
  dp[0] = 1
  dp[1] = 1
  for i from 2 to n:
    dp[i] = 0
    for j from 1 to i:
      dp[i] += dp[j-1] * dp[i-j]
  return dp[n]
```