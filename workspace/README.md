# Unique Binary Search Trees
## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Function Reference](#function-reference)
- [Examples](#examples)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Overview
The unique binary search trees problem is a classic problem in computer science that involves calculating the number of unique binary search trees that can be formed with n nodes.

## Features
* Calculates the number of unique binary search trees that can be formed with n nodes
* Uses dynamic programming to optimize performance
* Handles edge cases properly

## Requirements
* Python 3.x

## Installation
To install the unique binary search trees package, simply clone the repository and run the following command:
```bash
git clone https://github.com/username/unique-binary-search-trees.git
```

## Usage
To use the unique binary search trees package, simply import the `uniqueBSTs` function and call it with the desired value of n:
```python
from main import uniqueBSTs
n = 3
print(uniqueBSTs(n))
```

## Code Structure
The code is structured into a single module called `main.py` that contains the `uniqueBSTs` function.

## Function Reference
### uniqueBSTs(n)
Calculates the number of unique binary search trees that can be formed with n nodes.

* Parameters: `n` (int) - the number of nodes in the binary search tree
* Returns: `int` - the number of unique binary search trees that can be formed with n nodes

## Examples
* Calculate the number of unique binary search trees that can be formed with 3 nodes:
```python
from main import uniqueBSTs
n = 3
print(uniqueBSTs(n))  # Output: 5
```
* Calculate the number of unique binary search trees that can be formed with 1 node:
```python
from main import uniqueBSTs
n = 1
print(uniqueBSTs(n))  # Output: 1
```

## Testing
To test the unique binary search trees package, simply run the following command:
```bash
python -m unittest test_main.py
```

## Troubleshooting
If you encounter any issues while using the unique binary search trees package, please refer to the troubleshooting section below.

### Common Issues
* If you encounter a `TypeError` while calling the `uniqueBSTs` function, make sure that you are passing an integer value for `n`.
* If you encounter a `ValueError` while calling the `uniqueBSTs` function, make sure that you are passing a positive integer value for `n`.

## Performance Considerations
The unique binary search trees package uses dynamic programming to optimize performance. However, for large values of `n`, the package may take a significant amount of time to calculate the result.

## Contributing
If you would like to contribute to the unique binary search trees package, please fork the repository and submit a pull request with your changes.

## License
The unique binary search trees package is licensed under the MIT License.

## Acknowledgments
The unique binary search trees package was developed by [Your Name].