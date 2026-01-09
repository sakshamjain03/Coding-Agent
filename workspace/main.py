#!/usr/bin/env python3
# Module docstring describing the application
"""
This module provides a function to calculate the number of unique binary search trees that can be formed with n nodes.
"""

import sys

def uniqueBSTs(n):
    """
    Calculate the number of unique binary search trees that can be formed with n nodes.

    Args:
    n (int): The number of nodes in the binary search tree.

    Returns:
    int: The number of unique binary search trees that can be formed with n nodes.
    """
    # Initialize an array to store the number of unique BST's for each value of n from 1 to n
    dp = [0] * (n + 1)
    
    # Base cases: there is only one way to form a BST with 0 or 1 nodes
    dp[0] = 1
    dp[1] = 1
    
    # Calculate the number of unique BST's for each value of n from 2 to n
    for i in range(2, n + 1):
        dp[i] = 0
        for j in range(1, i + 1):
            # The number of unique BST's with i nodes is the sum of the number of unique BST's with j-1 nodes and i-j nodes
            dp[i] += dp[j - 1] * dp[i - j]
    
    return dp[n]

def main():
    # Example use cases
    n = 3
    print("The number of unique binary search trees that can be formed with {} nodes is: {}".format(n, uniqueBSTs(n)))
    
    n = 1
    print("The number of unique binary search trees that can be formed with {} nodes is: {}".format(n, uniqueBSTs(n)))

if __name__ == "__main__":
    main()