# CodeAlpaca Mixed Languages

Total: 300 examples


## Q1: Create an array of length 5 which contains all even numbers between 1 and 10.

**Answer:**
arr = [2, 4, 6, 8, 10]

---

## Q2: Formulate an equation to calculate the height of a triangle given the angle, side lengths and opposite side length.

**Answer:**
Height of triangle = opposite side length * sin (angle) / side length

---

## Q3: Write a replace method for a string class which replaces the given string with a given set of characters.

**Input:**
```
string = "Hello World!"
replace_with = "Greetings!"
```

**Answer:**
def replace(self, replace_with):
    new_string = ""
    for char in self:
        if char == " ":
            new_string += replace_with
        else:
            new_string += char
    return new_string

---

## Q4: Create an array of length 15 containing numbers divisible by 3 up to 45.

**Answer:**
arr = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]

---

## Q5: Write a function to find the number of distinct states in a given matrix.

**Input:**
```
matrix = [[1, 0, 0],
          [1, 0, 1],
          [1, 1, 1]]
```

**Answer:**
def find_num_distinct_states(matrix):
    states = set()
    for row in matrix:
        state = "".join([str(x) for x in row])
        states.add(state)
    return len(states)

---

## Q6: Create a nested loop to print every combination of numbers between 0-9

**Answer:**
for i in range(10):
    for j in range(10):
        print(i, j)

---

## Q7: Write a function to find the maximum difference between two numbers in a given array.

**Input:**
```
arr = [5, 3, 17, 11, 9]
```

**Answer:**
def max_difference(arr):
    max_diff = 0
    for i in range(len(arr)-1):
        diff = arr[i+1] - arr[i]
        if diff > max_diff:
            max_diff = diff
    return max_diff

---

## Q8: Write a function to generate the nth Fibonacci number.

**Input:**
```
< noinput >
```

**Answer:**
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-2) + fib(n-1)

---

## Q9: Write a class to represent a 2D point with x and y coordinates.

**Answer:**
class Point:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
   
    def __str__(self): 
        return "({0},{1})".format(self.x, self.y)

---

## Q10: Write code that removes spaces from a given string.

**Input:**
```
string = " A B C D "
```

**Answer:**
def remove_spaces(string): 
    return "".join(string.split())

---

## Q11: Write a function that checks if a give number is even or odd.

**Answer:**
def is_even(n):
    if n%2 == 0:
        return True  
    else:
        return False

---

## Q12: Write code to create a list of all prime numbers between 2 and 100.

**Answer:**
def find_primes(n): 
    prime_list = [2] 
    for number in range(2, n + 1): 
        is_prime = True
        for k in range(2, number): 
            if number % k == 0: 
                is_prime = False 
        if is_prime: 
            prime_list.append(number) 
    return prime_list

---

## Q13: Edit the following code to print out all even numbers from 1 to 10.

**Input:**
```
for i in range(1,11):
    print(i)
```

**Answer:**
for i in range(1,11):
    if i % 2 == 0:
        print(i)

---

## Q14: Write code to find the sum of all numbers between 1 and 10.

**Answer:**
sum = 0
for i in range(1,11):
    sum += i
print(sum)

---

## Q15: Create a function to calculate the area of a given circle.

**Answer:**
def area_circle(radius):
    return 3.14 * (radius**2)

---

## Q16: Follow the comments in the code to complete the program which prints a conversion table from Fahrenheit to Celsius.

**Input:**
```
# This program prints a conversion table from Fahrenheit to Celsius

# Print a heading for the table
# TODO

# Print the column headings
# TODO

# Calculate and print the table body
# TODO
```

**Answer:**
# This program prints a conversion table from Fahrenheit to Celsius

# Print a heading for the table
print("Fahrenheit to Celsius Conversion Table")

# Print the column headings
print("Fahrenheit \t Celsius")

# Calculate and print the table body
for fahr in range(-50 , 121):
  celsius = (fahr - 32) * 5 / 9
  print("%3d \t\t %.2f" % (fahr, celsius))

---

## Q17: Develop a classification algorithm in Python to predict whether a bird is a hawk or a falcon.

**Answer:**
import pandas as pd
import numpy as np

# Define features
features = ["wing_shape", "size", "tails_length", "color_pattern"] 

# Load the data
data = pd.read_csv("birds.csv")

# Preprocess the data to generate feature vectors
X = np.array(data[features]) 

# Make a target vector 
y = np.array(data["species"]) 

# Divide the data into training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a classification model
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Generate evaluation metrics
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test

---

## Q18: Create a function in Java for computing the factorial of a positive integer number.

**Answer:**
public static long factorial(int n) {
    if (n == 0) {
        return 1;
    }
    long result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

---

## Q19: Create a C++ program for randomly shuffling an array of integers.

**Answer:**
#include <iostream>
#include <algorithm>
#include <random>

void shuffleArray(int array[], int size) {
	std::random_device rd;
	std::mt19937 g(rd()); 
	std::shuffle(array, array+size, g); 
}

int main() 
{ 
	int array[] = {1, 2, 3, 4, 5, 6, 7, 8}; 
	int size = sizeof(array) / sizeof(array[0]); 

    // Print original array
    std::cout << "Original array: ";
    for (int i : array)
        std::cout << i << " ";
    std::cout << "\n";

    // Shuffle array
	shuffleArray(array, size); 

    // Print shuffled array
    std::cout << "Shuffled array: ";
    for (int i : array)
        std::cout << i << " ";
    std::cout << "\n";

	return 0; 
}

---

## Q20: Use the function to debug the given program and prevent the segmentation fault.

**Input:**
```
#include <stdio.h>

int main() {
    int array[] = {1, 2, 3, 4, 5};
    int n = 5;
    int i;
    // TODO
    for (i = 0; i <= n; i++) {
        printf("%d\n", array[i]);
    }
    return 0;
}
```

**Answer:**
#include <stdio.h>

int main() {
    int array[] = {1, 2, 3, 4, 5};
    int n = 5;
    int i;
    // Limit loop size to the length of the array
    for (i = 0; i < n; i++) {
        printf("%d\n", array[i]);
    }
    return 0;
}

---

## Q21: Replace the placeholder with a for loop for iterating over the numbers from 1 to n and printing them.

**Input:**
```
for i in range(n):
    # TODO
```

**Answer:**
for i in range(1, n+1):
    print(i)

---

## Q22: Use try-except statements to detect and handle exceptions in the code.

**Input:**
```
for i in range(n):
    x = 1/i
```

**Answer:**
try:
    for i in range(n):
        x = 1/i
except ZeroDivisionError:
    print("Zero division error encountered!")

---

## Q23: Re-write the code segment as a list comprehension.

**Input:**
```
numbers = []
for i in range(10):
    if i % 2 == 0:
        numbers.append(i)
```

**Answer:**
numbers = [i for i in range(10) if i % 2 == 0]

---

## Q24: Remove the boilerplate code from the program for printing 10 random numbers.

**Input:**
```
import random

# Generate 10 random numbers
for i in range(10):
    # TODO
```

**Answer:**
import random

# Generate 10 random numbers
for i in range(10):
    print(random.randrange(1, 101))

---

## Q25: Modify the code to perform the mathematical expression “x to the power of y”.

**Input:**
```
# Calculate x to the power of y
# TODO
```

**Answer:**
# Calculate x to the power of y
x_pow_y = x**y

---

## Q26: Create a dictionary for counting the occurrence of each letter in the given string.

**Input:**
```
string = "hello world"
#TODO
```

**Answer:**
string = "hello world"
letter_counts = {}

for letter in string:
    if letter in letter_counts:
       letter_counts[letter] += 1
    else:
        letter_counts[letter] = 1

print(letter_counts)

---

## Q27: Follow the comments to complete the code that finds the maximum value in an array.

**Input:**
```
# Find the maximum value in an array
arr = [4, 5, 2, 8, 7]
# TODO
```

**Answer:**
# Find the maximum value in an array
arr = [4, 5, 2, 8, 7]

max_value = arr[0]
for i in range(1, len(arr)):
    if arr[i] > max_value:
        max_value = arr[i]

print(max_value)

---

## Q28: Write a function in HTML for creating a table of n rows and m columns.

**Answer:**
<table>
  <tbody>
    <% for (let i = 0; i < n; i++) { %>
      <tr>
        <% for (let j = 0; j < m; j++) { %>
          <td>Cell Content</td>
        <% } %>
      </tr>
    <% } %>
  </tbody>
</table>

---

## Q29: Create a CSS script that centers the login form on the webpage.

**Answer:**
.login-form {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

---

## Q30: Create a Java program that prints out the sum of the numbers in the array.

**Input:**
```
int[] numbers = {1, 2, 3 , 4, 5};
```

**Answer:**
public class SumOfArray {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3 , 4, 5};
        int sum = 0;
        for(int i=0; i < numbers.length;i++) {
            sum = sum + numbers[i];
        }
        System.out.println("The sum of numbers in the given array is: " + sum);
    }
}

---

## Q31: Write a SQL query to calculate the total number of orders in the "orders" table.

**Answer:**
SELECT COUNT(*) AS "Total Number of Orders" 
FROM orders;

---

## Q32: Write a Python function to convert a given string to lowercase.

**Input:**
```
string = "FOO"
```

**Answer:**
def to_lowercase(string):
    return string.lower()

string = "FOO"
print(to_lowercase(string))

---

## Q33: Create a C program that prints out the Fibonacci sequence.

**Answer:**
#include <stdio.h>

int main()
{
    int i, num, first=0, second=1, next;
    printf("Enter the number of elements: ");
    scanf("%d", &num);
    printf("Fibonacci Series: ");
    for (i = 0; i < num; i++)
    {
        if (i <= 1)
            next = i;
        else
        {
            next = first + second;
            first = second;
            second = next;
        }
        printf("%d ", next);
    }
    return 0;
}

---

## Q34: Write a function in JavaScript to count the number of vowels in a given string.

**Input:**
```
const string = "abcdefg"
```

**Answer:**
function countVowels(string) {
    let vowelCount = 0;
    const vowels = ["a","e","i","o","u"];
  
    for (let i = 0; i < string.length; i++) {
      if (vowels.includes(string[i])) {
        vowelCount++;
      }
    }
  
    return vowelCount;
}

const string = "abcdefg";
console.log(countVowels(string));

---

## Q35: Create a JSX code that renders a "Hello, World!" message in the browser.

**Answer:**
import React from "react";

function App() {
  return (
    <div>
      <h1>Hello, World!</h1>
    </div>
  );
}

export default App;

---

## Q36: Write an SQL query to calculate the average order price for each product category in the "orders" table.

**Answer:**
SELECT category, AVG(price) as "Average Order Price"
FROM orders
GROUP BY category;

---

## Q37: Create a Java program that prints out the contents of a given two-dimensional array.

**Input:**
```
int[][] arr = {{1,2},{3,4},{5,6}}
```

**Answer:**
public class TwoDArray {

    public static void main(String[] args) {
        int[][] arr = {{1,2},{3,4},{5,6}};

        for(int i=0;i<arr.length;i++){
            for(int j=0;j<arr[i].length;j++){
                System.out.print(arr[i][j]+" ");
            }
            System.out.println();
        }
    }
}

---

## Q38: Create a C++ program that sorts a given array in descending order.

**Input:**
```
int array[] = {6, 3, 8, 12, 9, 4};
```

**Answer:**
#include<iostream>
using namespace std;
 
int main()
{
    int array[] = {6, 3, 8, 12, 9, 4};
    int arraySize = sizeof(array)/sizeof(array[0]);
 
    //ascending order sorting
    for(int i = 0; i < arraySize; i++)
    {
        // find the position of smallest element
        int small = i;
        for(int j = i+1; j < arraySize; j++)
        {
            if(array[j] > array[small])
                small = j;
        }
 
        // swap the position of smallest element
        int temp = array[i];
        array[i] = array[small];
        array[small] = temp;
    }
 
    // print the sorted array
    cout << "Sorted array : ";
    for(int i = 0; i < arraySize; i++)
        cout << array[i] << " ";
 
    return 0;
}

---

## Q39: Edit the Python code so that it prints out the total number of elements in the list.

**Input:**
```
list = [1, 2, 3, 4, 5]
```

**Answer:**
list = [1, 2, 3, 4, 5]
print("Total number of elements in the list: ", len(list))

---

## Q40: Create a Swift code that show the number of days in the given month.

**Input:**
```
int month = 5
```

**Answer:**
let month = 5
let daysEndingInth = [3, 0, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3]
let daysInMonth = daysEndingInth[month - 1] 
print("The number of days in the month of \(month) is \(daysInMonth).")

---

## Q41: Write a HTML code that create a form for user to fill out their current address.

**Answer:**
<form action="">
    <label for="street">Street</label>
    <input type="text" name="street" id="street">
    <label for="city">City</label>
    <input type="text" name="city" id="city">
    <label for="state">State</label>
    <input type="text" name="state" id="state">
    <label for="zip">Zip Code</label>
    <input type="text" name="zip" id="zip"> 
    <input type="submit" value="Submit">
</form>

---

## Q42: Write a SQL query to find the total number of orders placed between two given dates.

**Input:**
```
start_date = '2020-01-01'
end_date = '2020-02-01'
```

**Answer:**
SELECT COUNT(*)
FROM orders
WHERE order_date BETWEEN '2020-01-01' AND '2020-02-01';

---

## Q43: Create a Ruby code that prints out the median of a given array of numbers.

**Input:**
```
nums = [1, 7, 3, 6]
```

**Answer:**
nums = [1, 7, 3, 6]
sorted_nums = nums.sort

# Calculation of median 
if sorted_nums.length % 2 == 0
  mid_index = sorted_nums.length/2
  median = (sorted_nums[mid_index] + sorted_nums[mid_index - 1])/2.to_f
else
  mid_index = sorted_nums.length/2
  median = sorted_nums[mid_index]
end

puts median

---

## Q44: Create a PHP code to check if an array contains a given item.

**Input:**
```
$input_array = array(1,2,3,4,5);
$item_to_check = 3;
```

**Answer:**
<?php
$input_array = array(1,2,3,4,5);
$item_to_check = 3;

if(in_array($item_to_check, $input_array)) {
  echo "Array contains the given item.";
} else {
  echo "Array doesn't contain the given item.";
}
?>

---

## Q45: Edit the code to create a try-except block to handle the exception.

**Input:**
```
a = 5
b = 0

ans = a/b
```

**Answer:**
try:
    a = 5
    b = 0

    ans = a/b
except ZeroDivisionError:
    print("Cannot divide by zero.")

---

## Q46: Write a script using Bash that replaces all vowels with a number.

**Answer:**
#!/bin/bash

string="Hello World!"
vowels=("a" "e" "i" "o" "u" "A" "E" "I" "O" "U")

for i in "${vowels[@]}"
do
    string="${string//$i/0}"
done

echo $string #H0ll0 W0rld!

---

## Q47: Change the variable `x` to the data type desired.

**Input:**
```
x = 'Hello World!'
```

**Answer:**
x = "Hello World!"

---

## Q48: Create a function that takes an array as an argument and returns the sum of all the elements in the array.

**Input:**
```
arr = [1, 2, 3, 4, 5]
```

**Answer:**
def arraySum(arr):
    total = 0
    for num in arr:
        total += num
    return total

---

## Q49: Sort the array in ascending order.

**Input:**
```
arr = [3, 2, 1, 5, 4]
```

**Answer:**
arr.sort() # [1, 2, 3, 4, 5]

---

## Q50: Generate a random integer between 4 and 8 (inclusively).

**Answer:**
import random
x = random.randint(4, 8)

---

## Q51: Write a list comprehension to square each number in the list.

**Input:**
```
arr = [1, 2, 3, 4, 5]
```

**Answer:**
arr = [x**2 for x in arr] # [1, 4, 9, 16, 25]

---

## Q52: Write a function that takes a string and reverses the words.

**Input:**
```
text = "Hello World!"
```

**Answer:**
def reverseWords(text):
    return ' '.join(text.split()[::-1])

reverseWords(text) # "World! Hello"

---

## Q53: Write a SQL query to return the sum of all salaries.

**Answer:**
SELECT SUM(salary)
FROM employees;

---

## Q54: Create a function that takes in two numbers as arguments and returns the product of the two.

**Answer:**
def multiply(x, y):
    return x*y

---

## Q55: Sum up the numbers in the array in Javascript.

**Input:**
```
arr = [1,2,3,4,5]
```

**Answer:**
let sum = arr.reduce((total, num) => total + num);
console.log(sum); // 15

---

## Q56: Using the given function, create a loop that counts from 0 to 9.

**Input:**
```
function printNum(num){
  console.log(num)
}
```

**Answer:**
for (let i = 0; i < 10; i++){
    printNum(i);
}

---

## Q57: Create a JSON object with three key-value pairs.

**Answer:**
{
  "firstName": "John",
  "lastName": "Doe",
  "age": 30
}

---

## Q58: Count the number of characters in the string.

**Input:**
```
text = "Hello World!"
```

**Answer:**
len(text) # 12

---

## Q59: Generate a random number between 0 and 1 (inclusively).

**Answer:**
Math.random(); // a random number between 0 and 1 (inclusively)

---

## Q60: Compose a function named average_list which takes a list of numbers as its argument and computes the average.

**Answer:**
def average_list(nums):
    return sum(nums)/len(nums)

---

## Q61: Generate a snippet of code to extract all the URLs from the given string.

**Input:**
```
This string contains some urls such as https://www.google.com and https://www.facebook.com.
```

**Answer:**
import re

string = "This string contains some urls such as https://www.google.com and https://www.facebook.com."

urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 

print(urls)

---

## Q62: Write a code to convert a given spredsheet in csv format to json format.

**Answer:**
import csv
import json

def csv_to_json():
    # Path of csv file
    file_csv = 'mycsvfile.csv'
    
    # Path of json file
    file_json = 'myjsonfile.json'
    
    with open(file_csv, 'r') as input_file:
        reader = csv.DictReader(input_file)
        data = list(reader)
    
    with open(file_json, 'w') as output_file:
        json.dump(data, output_file)

csv_to_json()

---

## Q63: Create a list comprehension to generate a list of multiples of 3 from 0 to 23.

**Answer:**
list_of_multiples_of_3 = [x*3 for x in range(8)]

---

## Q64: Design a program to find the longest element in the given list.

**Input:**
```
[10, 100, 200, 500, 400]
```

**Answer:**
def longest_element(list):
  max_length = 0
  max_length_item = None

  for item in list:
    if len(item) > max_length:
      max_length = len(item)
      max_length_item = item

  return max_length_item

list = [10, 100, 200, 500, 400]
longest_element(list) # 500

---

## Q65: Write a function to print all prime numbers between two given numbers.

**Answer:**
def print_prime_numbers_in_range(start, end):
  # start = starting number
  # end = ending number

  for num in range(start, end+1):
    # Prime numbers are greater than 1
    if num > 1:
      for i in range(2, num):
        if (num % i) == 0:
          break
      else:
        print(num)
---

11. Instruction: Generate a snippet of code to reverse given string
11. Input:
<noinput>
11. Output:
def reverse_string(input_string):
  string_length = len(input_string)
  reversed_string = ""
  
  for i in range(string_length-1,-1,-1):
    reversed_string += input_string[i]
  
  return reversed_string

---

## Q66: Describe the basic syntax of a Java function?

**Answer:**
A Java function consists of a function name, return type, parameters (arguments), and body. The syntax of a Java function is as follows: 
public <return type> <function name>(<list of parameters>) { 
    // function body 
    <statements> 
}

---

## Q67: How to reverse a list in C++?

**Answer:**
You can reverse a list in C++ using the std::reverse algorithm. To reverse the list, pass the list as the first parameter and the beginning and end of the list as the second and third parameter, respectively. Alternatively, you can also reverse the list using a for loop and the operator [] to access each element of the list.

---

## Q68: Write a SQL query to update a value x in a column y in a table z.

**Input:**
```
x = 5, y = 'amount' and z = 'payments'.
```

**Answer:**
UPDATE payments 
SET amount = 5 
WHERE payments.amount IS NOT NULL;

---

## Q69: Write an algorithm in Python to determine if a number is even or odd.

**Answer:**
def is_even(num): 
    if num % 2 == 0: 
        return True 
    else: 
        return False

---

## Q70: What is the purpose of a constructor in a class in Java?

**Answer:**
The purpose of a constructor in a class in Java is to initialize an object of that class. A constructor is a special kind of method that is used to create an object of its associated class. When an object of the class is created, the constructor is used to set the initial state of the object.

---

## Q71: Write a JavaScript code to get the current browser URL.

**Answer:**
var currentURL = window.location.href;
console.log(currentURL);

---

## Q72: Rewrite the following C++ code using only pointer references instead of array subscripts:

**Input:**
```
int arr[3] = {1,2,3};
int sum = 0;
for (int i = 0; i < 3; i++) 
{
    sum += arr[i];
}
```

**Answer:**
int arr[3] = {1,2,3};
int sum = 0;
int* ptr = arr;
for (int i = 0; i < 3; i++) 
{
    sum += *(ptr+i); 
}

---

## Q73: Write a MySQL query to print the column names of a table named 'employees'.

**Answer:**
SELECT column_name FROM information_schema.columns WHERE table_name = 'employees';

---

## Q74: Generate a regular expression to match a valid email address.

**Answer:**
/^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/

---

## Q75: How to delete a particular row in an SQLite database table?

**Answer:**
To delete a particular row in an SQLite database table, you can use the DELETE statement with a WHERE clause to specify the row to be deleted. For example: DELETE FROM table_name WHERE condition;

---

## Q76: Is it possible to set a breakpoint that is not associated with any source code line in a GDB program?

**Answer:**
Yes, it is possible to set a breakpoint that is not associated with any source code line in a GDB program. For example, you can set a breakpoint on a function or a memory address. You can do this by using the break command with '*' prefix followed by the address of the breakpoint.

---

## Q77: Write a C++ code to find the average of an array of integers.

**Answer:**
#include <iostream>

int calculateAverage(int array[], int n){
    int sum = 0; 
    for (int i=0; i<n; i++){
        sum += array[i]; 
    } 
    int average = sum/n;
    return average;
}

---

## Q78: How can we encrypt a string in Python?

**Answer:**
We can encrypt a string in Python using the cryptography module. The cryptography module provides high level cryptographic primitives using the Fernet cipher. The Fernet cipher uses AES-128 in CBC mode and PKCS7 padding to encrypt the string.

---

## Q79: What is the purpose of declaring a function as static in C++?

**Answer:**
The purpose of declaring a function as static in C++ is to restrict its visibility to only the translation unit in which it is declared. A static function can only be called from within the same translation unit and thus, it cannot be accessed from outside of that translation unit.

---

## Q80: How to print the elements of a two-dimensional array in C?

**Answer:**
We can use nested loops to print the elements of a two-dimensional array in C. The outer loop iterates over the rows, while the inner loop iterates over the columns. For example, the following code snippet prints the elements of a two-dimensional array: 
 
int array[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
for (int i=0; i<3; i++)
{   
    for(int j=0; j<3; j++) 
    {
        printf("%d ", array[i][j]); 
    }
    printf("\n");
}

---

## Q81: Using the following code, clean up the bugs and make sure the output functions correctly.

**Input:**
```
def example_func(lst):
   for element in lst:
      if (type(element) == int):
         lst.append(element + 5)
   return lst
 
example_func([1, 2, "hello"])
```

**Answer:**
def example_func(lst):
   output_lst = []
   for element in lst:
      if (type(element) == int):
         output_lst.append(element + 5)
   return output_lst
 
example_func([1, 2, "hello"])

---

## Q82: Write a C++ function to generate a random integer between 0 and 10.

**Answer:**
#include <iostream> 
#include <cstdlib> 
#include <ctime> 
using namespace std; 

int randomIntGenerator() 
{ 
   // Setting the seed 
   srand(time(0)); 

   // Generating random integer 
   return (rand()%11); 
}

---

## Q83: Create a table to store customer information.

**Answer:**
CREATE TABLE customers (
   id int NOT NULL AUTO_INCREMENT,
   name varchar(100) NOT NULL,
   email varchar(100) NOT NULL,
   phone varchar(20) NOT NULL,
   address varchar(200) NOT NULL,
   PRIMARY KEY (id)
);

---

## Q84: Create a class in Java named Puppy that has two instance variables, age and name and two methods, bark and sleep.

**Answer:**
public class Puppy { 
   // Instance Variables 
   String name; 
   int age; 
  
   // Constructor 
   public Puppy(String name, int age){ 
      this.name = name; 
      this.age = age; 
   } 
  
   // Methods 
   public void bark(){ 
      System.out.println("Woof Woof!"); 
   } 
  
   public void sleep(){ 
      System.out.println("Zzzzzz..."); 
   } 
}

---

## Q85: Parse the string and return the number of unique alphabets in the string.

**Input:**
```
StringInput = "apple"
```

**Answer:**
int count = 0;
for (int i = 0; i < StringInput.length(); i++) {
  if ((StringInput.charAt(i) >= 'a' && StringInput.charAt(i) <= 'z') || (StringInput.charAt(i) >= 'A' && StringInput.charAt(i) <= 'Z')) {
   count++;
  }
}
System.out.println("Number of unique alphabets: " + count);

---

## Q86: Write a shell script to print the top 3  most frequently used commands.

**Answer:**
#!/bin/bash
# Store all commands used in the last hour in command_list.
history | tail -$(($(date +%H) * 60)) -n $(($(date +%M)+1)) | cut -d ' ' -f 5 > command_list
# Create frequency database and store them in frequency.dat
cat command_list | sort | uniq -c | sort -rn > frequency.dat
# Print top 3 commands
head -3 frequency.dat

---

## Q87: Read the JSON string below and convert it into a dictionary.

**Input:**
```
jsonString = '{"name": "John", "age": 30, "city": "New York"}'
```

**Answer:**
import json

jsonObject = json.loads(jsonString)
dictionary = dict(jsonObject)
print(dictionary)

---

## Q88: Implement a function that finds the maximum element in a given array.

**Input:**
```
arr = [45, 7, 0, 82, 23]
```

**Answer:**
def find_max_element(arr): 
    max_element = arr[0] 
    for index in range(1, len(arr)): 
        if arr[index] > max_element: 
            max_element = arr[index] 
    return max_element
  
arr = [45, 7, 0, 82, 23]
max_element = find_max_element(arr) 
print(max_element)

---

## Q89: Validate whether the string contains only alphabets or not.

**Input:**
```
myString = "abc123"
```

**Answer:**
def check_string_alphabets(myString):
    for character in myString:
        if (not character.isalpha()):
            return False
    return True

myString = "abc123"
if (check_string_alphabets(myString)):
    print("String contains only alphabets")
else:
    print("String contains numbers")

---

## Q90: Rewrite the following code using ternary operator.

**Input:**
```
num1 = 5
num2 = 10

if num1 < num2:
    print("num1 is smaller than num2")
else:
    print("num1 is greater than or equal to num2")
```

**Answer:**
num1 = 5
num2 = 10

print("num1 is smaller than num2") if (num1 < num2) else print("num1 is greater than or equal to num2")

---

## Q91: Write a script to check if a given number is a palindrome or not.

**Input:**
```
inputNumber = 121
```

**Answer:**
# Function to check whether the inputNumber is palindrome or not
def is_palindrome(inputNumber):

   # negative numbers are not palindrome
   if inputNumber < 0:
       return False

   # find the number of digits in the inputNumber
   div = 1
   while (inputNumber / div >= 10):
       div *= 10

   # check if the most significant and least significant digits match
   while (inputNumber != 0):
       # compare first and last digits
       firstdigit = inputNumber // div
       lastdigit =  inputNumber % 10
       if firstdigit != lastdigit:
           return False

       # remove the most and least significant digit of inputNumber
       inputNumber = (inputNumber % div) // 10

       # reduce div by a factor of 2,  since 2 digits
       # were removed
       div = div // 100
   return Tr

---

## Q92: Edit the following code to remove the bugs.

**Input:**
```
def reverse_string(user_string): 
  if len(user_string) == 0: 
    return "" 
  else: 
    return reverse_string(user_string[1:]) + user_string[0] 
    
print(reverse_string(“test”))
```

**Answer:**
def reverse_string(user_string): 
  reversed_string = ''
  if len(user_string) == 0: 
    return "" 
  else: 
    reversed_string = reverse_string(user_string[1:]) + user_string[0] 
    return reversed_string

user_string = 'test'
print(reverse_string(user_string))

---

## Q93: What is the output of the following code?

**Input:**
```
list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]

for x, y in zip(list1, list2):
    print(x * y)
```

**Answer:**
a
bb
ccc

---

## Q94: Write a function to remove all whitespace characters from a given string.

**Input:**
```
myString = "Hello   World    "
```

**Answer:**
def remove_whitespaces(myString):
    return ''.join(myString.split())

myString = "Hello   World    "
print(remove_whitespaces(myString))

---

## Q95: Edit the following code to add try catch block.

**Input:**
```
x = "5"
y = "2"
sum = int(x) + int(y)
print("Sum of x and y is", sum)
```

**Answer:**
x = "5"
y = "2"
try:
   sum = int(x) + int(y)
   print("Sum of x and y is", sum)
except:
   print("Error: Invalid input")

---

## Q96: Write a Python function that takes two lists of equal length and creates a dictionary of the elements in each list that 

**Input:**
```
list_one = [1, 2, 3, 4]
list_two = ["a", "b", "c", "d"]
```

**Answer:**
def list_dict(list_one, list_two):
    """Create a dictionary of elements in the two lists which have the same index."""
    assert len(list_one) == len(list_two), "lists must be same length"
    dict = {}
    for i in range(len(list_one)):
        dict[list_one[i]] = list_two[i]
    return dict

---

## Q97: Create a quick-sort algorithm in Python.

**Answer:**
def quick_sort(arr):
    """Sort a list of numbers in ascending order using the Quick-Sort algorithm"""
    if len(arr) == 0:
        return []

    pivot = arr[0]
    left_arr = [x for x in arr if x < pivot]
    right_arr = [x for x in arr if x > pivot]
    return quick_sort(left_arr) + [pivot] + quick_sort(right_arr)

---

## Q98: Develop an algorithm to find the value of n where n is the index of the Fibonacci sequence.

**Answer:**
def nth_fibonacci_number(n):
    """Find the value of n where n is the index of the Fibonacci Sequence.""" 
    if n < 2:
        return n 
    elif n == 2:
        return 1
    else:
        return nth_fibonacci_number(n-1) + nth_fibonacci_number(n-2)

---

## Q99: Create a program that finds all the prime numbers less than or equal to a given number.

**Answer:**
def find_primes(num):
    """Find all the prime numbers less than or equal to a given number."""
    primes = []
    for i in range(2, num + 1):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes

---

## Q100: Write a function that takes in a list of numbers and prints out the greatest number.

**Input:**
```
list = [8, 2, 14, 25]
```

**Answer:**
def find_greatest(list):
    """Print out the greatest number from a list of numbers."""
    greatest = list[0]
    for num in list:
        if num > greatest:
            greatest = num
    print('The greatest number is: ', greatest)

---

## Q101: Design an algorithm that takes a list of strings and returns the longest string.

**Input:**
```
list = ["cat", "dog", "lion", "bird"]
```

**Answer:**
def find_longest(list):
    """Return the longest string from a list of strings.""" 
    longest = list[0]
    for item in list:
        if len(item) > len(longest):
            longest = item
    return longest

---

## Q102: Write a function that takes in a matrix of numbers and reverses the order of the rows and columns.

**Input:**
```
matrix = [[1, 2, 3], 
          [4, 5, 6], 
          [7, 8, 9]
         ]
```

**Answer:**
def reverse_matrix(matrix):
    """Reverse the order of the rows and columns in a matrix of numbers."""
    reversed_matrix = [[0 for i in range(len(matrix[0]))] for j in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            reversed_matrix[j][i] = matrix[i][j]
    return reversed_matrix

---

## Q103: Design an algorithm that creates a random password of 8 characters.

**Answer:**
def generate_password():
    """Generate a random password of 8 characters."""
    import random
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    password = ''
    for i in range(8):
        password += random.SystemRandom().choice(chars)
    return password

---

## Q104: FOr a given list, create a program that prints out the standard deviation of the elements in the list.

**Input:**
```
list = [1, 4, 9, 16]
```

**Answer:**
def std_dev(list):
    """Print the standard deviation of elements in a given list."""
    numerator = 0
    mean = sum(list) / len(list)
    for num in list:
        numerator += (num - mean) ** 2
    sd = (numerator / (len(list) - 1)) ** 0.5
    return sd

---

## Q105: Create a program that can filter out words of a string that contain a specific character.

**Input:**
```
string = "This is a sentence"
character = 's'
```

**Answer:**
def filter_string(string, character):
    """Filter out words of a string that contain a specific character."""
    words = string.split(' ')
    filtered_words = []
    for word in words:
        if character not in word:
            filtered_words.append(word)
    return ' '.join(filtered_words)

---

## Q106: Create a program that can calculate the distance between two points in three-dimensional space.

**Input:**
```
point1 = (1, 5, 9)
point2 = (4, 2, 8)
```

**Answer:**
def dist_points_3d(point1, point2):
    """Calculate the distance between two points in three-dimensional space."""
    distance = ((point1[0] - point2[0]) ** 2 + 
                (point1[1] - point2[1]) ** 2 + 
                (point1[2] - point2[2]) ** 2) ** 0.5
    return distance

---

## Q107: Create a program that ciphers a given text using the caesar cipher.

**Input:**
```
text = "This is a secret message"
key = 3
```

**Answer:**
def caesar_cipher(text, key):
    """Cipher a given text using the Caesar Cipher."""
    ciphertext = ""
    for char in text: 
        if not char.isalpha():
            ciphertext += char
            continue
        offset = ord('a') if char.islower() else ord('A')
        new_char = (ord(char) - offset + key) % 26
        ciphertext += chr(offset + new_char)
    return ciphertext

---

## Q108: Find the second smallest element in an integer array of size n.

**Input:**
```
array = [4, 5, 8, 2, 9, 13]
```

**Answer:**
def second_smallest(array):

smallest = min(array)
second_smallest = float('inf')

for num in array:
    if num > smallest and num < second_smallest:
        second_smallest = num
        
return second_smallest

---

## Q109: Write a SQL query to find all the users in a database with age greater than 25.

**Answer:**
SELECT * FROM users WHERE age > 25

---

## Q110: Create a function to calculate the maximum of two numbers.

**Answer:**
def max_of_two(x, y):
    if x > y:
        return x
    else:
        return y

---

## Q111: Write a Python program to split a string on a given character separator.

**Input:**
```
mystring = "Hello, World!"
separator = ","
```

**Answer:**
def split(mystring, separator):
    return mystring.split(separator)

---

## Q112: Write a Python program to get the day of week from a given date and time.

**Input:**
```
from datetime import datetime
date = datetime(2020, 4, 20, 19, 15, 0)
```

**Answer:**
from datetime import datetime

def get_day_of_week(date):
    return date.strftime("%A")

---

## Q113: Write a Javascript function to determine if the given number is an even number or not.

**Answer:**
function isEven(num) {
return num % 2 === 0;
}

---

## Q114: Write a Python program to print out an ASCII art of a given word.

**Input:**
```
word = "happy"
```

**Answer:**
def draw_word(word):
    art = """
                 __
           _   /  \\
           \\_/\_/\_/
           /    |
           \___/
          \\\\_//
           \/ \/
            \/
        """
    for letter in word:
        art += "  " + letter
    print(art)

---

## Q115: Write a JavaScript function to validate a given URL.

**Answer:**
function isValidURL(url) {
    const regex = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/;
    return regex.test(url);
}

---

## Q116: Write a C# program to find the maximum and minimum of three numbers.

**Answer:**
public void Maximum_Minimum(int num1, int num2, int num3)
{
    int max = Math.Max(Math.Max(num1, num2),num3);
    int min =  Math.Min(Math.Min(num1,num2),num3);
    Console.WriteLine("Maximum Number is : " + max);
    Console.WriteLine("Minimum Number is : " + min);
}

---

## Q117: Write a Java program to reverse a given string.

**Answer:**
public class ReverseString
{ 

    public static void main(String[] args) 
    { 
        String input = "Hello"; 
        StringBuilder input1 = new StringBuilder(); 
  
        // append a string into StringBuilder input1 
        input1.append(input); 
  
        // reverse StringBuilder input1 
        input1 = input1.reverse(); 
  
        // print reversed String 
        System.out.println(input1); 
    } 
}

---

## Q118: Write an HTML template to display a greeting message. The message should include the name of the user who visits the web

**Input:**
```
username = "John"
```

**Answer:**
<html>
	<head>
		<title>Greeting Message</title>
	</head>
	<body>
		<h1>Hello, {{ username }}!</h1>
	</body>
</html>

---

## Q119: Write a Python program to concatenate all elements in a list into a string separated by a given separator.

**Input:**
```
input_list = ["Python", "is", "a", "programming", "language"]
separator = "-"
```

**Answer:**
def list_to_string(input_list, separator):
    return separator.join(input_list)

---

## Q120: Write a C program to find the sum of all digits of a given number

**Answer:**
#include <stdio.h>

int getSumOfDigits(int num) {
    // Initialize sum
    int sum = 0;

    // Find the sum of digits
    while(num > 0) {
        sum += num % 10;
        num /= 10;
    }

    return sum;
}

int main() {
    int num;
    scanf("%d", &num);

    printf("Sum of digits of %d is %d\n", num, getSumOfDigits(num));

    return 0;
}

---

## Q121: Write a Java program to generate random numbers

**Answer:**
import java.util.Random; 
  
public class GenerateRandom { 
  
    public static void main(String[] args) 
    { 
  
        Random rand = new Random(); 
  
        // Generate random integers in range 0 to 999 
        int x = rand.nextInt(1000); 
        System.out.println("Random Integers: " + x); 
  
        // Generate Random doubles 
        double y = rand.nextDouble(); 
        System.out.println("Random Doubles: " + y); 
  
        // Generate Random Boolean 
        boolean z = rand.nextBoolean(); 
        System.out.println("Random Boolean: " + z); 
    } 
}

---

## Q122: Rewrite the following Python code using a for-loop.

**Input:**
```
i = 0
while i <= 10:
    print(i)
    i += 1
```

**Answer:**
for i in range(11):
    print(i)

---

## Q123: Write a code to print the current date and time in ISO format.

**Answer:**
from datetime import datetime

date_time_obj = datetime.now()

print(date_time_obj.isoformat()) # prints "2020-07-29T15:10:01.584131"

---

## Q124: Create a new folder called 'data' within the current working directory.

**Answer:**
import os

# create 'data' folder in the current working directory
current_directory = os.getcwd()
new_directory = os.path.join(current_directory, 'data')
os.mkdir(new_directory)

---

## Q125: Write a code to sort the following array in increasing order.

**Input:**
```
[10, 2, 7, 8, 32, 4]
```

**Answer:**
# sorting array using insertion sort
arr = [10, 2, 7, 8, 32, 4] 

# traverse through all array elements 
for i in range(1, len(arr)):
    key = arr[i]

    # move elements of arr[0..i-1], that are greater than key,
    # to one position ahead of their current position
    j = i-1
    while j >= 0 and key < arr[j] : 
            arr[j + 1] = arr[j] 
            j -= 1
    arr[j + 1] = key
  
#print the sorted array
print(arr)

---

## Q126: Create a function in JavaScript that takes an array of integers and returns the largest number.

**Answer:**
function findMax(arr) {
    let max = arr[0];
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

---

## Q127: Create a regular expression to validate a URL string.

**Answer:**
# Regular expression to validate a URL string
^(http:\/\/|https:\/\/|ftp:\/\/)?(www\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\.)+[\w]{2,5}(\/\S*)?$

---

## Q128: Write a Python code to calculate the mean of a given array.

**Input:**
```
[1,2,3,4]
```

**Answer:**
# calculate the mean of given array
arr = [1,2,3,4]

def calc_mean(arr):
    sum = 0
    for num in arr:
        sum += num
    return sum / len(arr)

print(calc_mean(arr)) # prints 2.5

---

## Q129: Create a function in Java that takes a string and prints the reversed version.

**Answer:**
public static void reverseString(String str) { 
    StringBuilder sb = new StringBuilder(); 
  
    for (int i = str.length() - 1; i >= 0; i--) { 
        sb.append(str.charAt(i)); 
    } 
  
    System.out.print(sb.toString()); 
}

---

## Q130: Write a code to get the time difference between two date-time objects.

**Input:**
```
date1: 2019-05-11 21:00:00
date2: 2019-05-13 10:00:00
```

**Answer:**
from datetime import datetime

def time_difference(date1, date2):
    date1_obj = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    date2_obj = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')

    return (date2_obj - date1_obj).total_seconds() // 3600

print(time_difference('2019-05-11 21:00:00', '2019-05-13 10:00:00')) # prints 33.0

---

## Q131: Write a code to connect to a remote database.

**Input:**
```
username: john
password: john123
IP: 100.10.0.10
```

**Answer:**
import psycopg2

conn = psycopg2.connect(host="100.10.0.10", database="mydb", user="john", password="john123")

---

## Q132: Create an HTML form with a textbox, a submit button, and two radio buttons.

**Answer:**
<form>
  <input type="text" id="textbox">
  <input type="submit" value="Submit">
  <input type="radio" name="choice" value="yes">Yes
  <input type="radio" name="choice" value="no">No
</form>

---

## Q133: Write a code to access the nth element of a linked list.

**Answer:**
# defining the Node class
class Node: 
	def __init__(self, data): 
		self.data = data 
		self.next = None

def getNthElement(head, n): 
	current = head 
	count = 0

	# looping through the linked list
	while(current is not None): 
		if (count == n): 
			return current.data 
		count += 1
		current = current.next
	return -1

---

## Q134: Create a function in JavaScript to find the number of occurrences of a letter in a word.

**Input:**
```
word: hello
letter: l
```

**Answer:**
function findOccurrences(word, letter) {
    let count = 0;
    for (let i = 0; i < word.length; i++) {
        if (word.charAt(i) === letter) {
            count++;
        }
    }
    return count;
}

---

## Q135: Write a code to add two linked lists of different sizes.

**Input:**
```
list1 = [2->4->3]
list2 = [5->6->4->1]
```

**Answer:**
# adding two linked lists
class Node: 
	def __init__(self, data): 
		self.data = data 
		self.next = None

def addTwoLists(first, second):
    # defining current and prev variables
    prev = None
    carry = 0
    temp = None

    # looping until one list has all nodes added
    while(first is not None or second is not None): 
        Node = Node() 		# Node data

        Node.data = carry + (first.data if first else 0) + (second.data if second else 0) 
		
        # update carry
        if Node.data >= 10: 
            Node.data = Node.data % 10
            carry = 1
        else: 
            carry = 0
 
        temp = Node
        # Move first, second pointers ahead
        if first is not None: 
            first = first.next
        if second is not None: 
            second = second.n

---

## Q136: Create a function in Java to convert a list of strings to a 2D array.

**Input:**
```
list: ["aa", "bb", "cc"]
```

**Answer:**
public static String[][] convertTo2DArray(List<String> strings) {
    int n = strings.size();
    String[][] array = new String[n][1];
    for (int i = 0; i < n; i++) {
        array[i][0] = strings.get(i);
    }
    return array;
    
}

---

## Q137: Modify the code below to make it calculate the sum of all the numbers from 1 to n.

**Input:**
```
num = 5
sum = 0
for i in range(num):
  sum += i
```

**Answer:**
num = 5
sum = 0
for i in range(1, num+1):
  sum += i

---

## Q138: Create a program to generate a histogram using data from a set of numbers.

**Input:**
```
values = [3, 4, 2, 5, 8, 1, 2, 6]
```

**Answer:**
import matplotlib.pyplot as plt

values = [3, 4, 2, 5, 8, 1, 2, 6]

plt.hist(values, bins= 10, edgecolor='black', color='b')

plt.xlabel('Values')
plt.ylabel('Frequency')

plt.title('Histogram')

plt.show()

---

## Q139: Create a function to convert Celsius to Fahrenheit.

**Answer:**
def celsius_to_fahrenheit(c):
    f = c * (9/5) + 32
    return f

---

## Q140: Write a function to find the number of occurrences of an element in a list.

**Input:**
```
arr = [10, 20, 10, 40, 40, 40, 50]
```

**Answer:**
def count_occurrences(arr, element):
    count = 0
    for e in arr:
        if e == element:
            count += 1
    return count

print(count_occurrences(arr, 40)) # Outputs: 3

---

## Q141: Write a JavaScript code snippet to print the numbers from 1 to 10.

**Answer:**
for (let i = 1; i <= 10; i++) {
  console.log(i);
}

---

## Q142: Generate a dictionary of 10 key-value pairs, where the key is a string and the values are random numbers from 1 to 100.

**Answer:**
import random

d = dict()

keys = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

for key in keys:
    d[key] =  random.randint(1,100)

print(d)

---

## Q143: Create a JavaScript function which takes a string as a parameter and returns the most frequent character in the string.

**Input:**
```
'Hello World!'
```

**Answer:**
function mostFrequentChar(string) {
    let charMap = {};
    let maxCount = 0;
    let freqChar = '';
  
    for (let char of string) {
        if (charMap[char]) {
            charMap[char]++;
        } else {
            charMap[char] = 1;
        }
    }
  
    for (let char in charMap) {
        if (charMap[char] > maxCount) {
            maxCount = charMap[char];
            freqChar = char;
        }
    }
  
    return freqChar;
}

---

## Q144: Write a C# function which takes 2 strings as parameters and returns a new string which is a concatenation of the two par

**Input:**
```
'Hello', 'World!'
```

**Answer:**
string ConcatenateStrings(string str1, string str2)
{
   return str1 + str2;
}

---

## Q145: Create an HTML page where the main content area has a random background color when the page is loaded.

**Answer:**
<!DOCTYPE html>
<html>
   <head>
      <title>RandomBackground</title>
      <script>
         window.addEventListener("load",function(){
            var randomColor = "#"+((1<<24)*Math.random()|0).toString(16);
            document.querySelector("body").style.background = randomColor;
         });
      </script>
   </head>
   <body>
   </body>
</html>

---

## Q146: Create a Java program which takes an integer array as a parameter, sorts the array in ascending order, and returns the s

**Input:**
```
[3, 5, 9, 1, 6]
```

**Answer:**
public int[] SortIntegerArray(int[] nums)
{
    Arrays.sort(nums);
    return nums;
}

---

## Q147: Write an SQL query to select the number of employees in each department, sorted by the department name in ascending orde

**Answer:**
SELECT department, COUNT(employee_ID)
FROM employees
GROUP BY department
ORDER BY department ASC;

---

## Q148: Write a Python program to remove all instances of a given value from a given list.

**Input:**
```
[1, 2, 3, 2, 3, 4], 2
```

**Answer:**
def remove_value(nums, val):
    res = []
    for num in nums:
        if num != val:
            res.append(num)
    return res

---

## Q149: Create a Java program to take a given string and replace all occurrences of a given letter with another given letter

**Input:**
```
'bbac', 'b', 'a'
```

**Answer:**
public String ReplaceLetters(String str, char oldChar, char newChar) {
    return str.replace(oldChar, newChar);
}

---

## Q150: Write an SQL query to calculate the average salary of all employees in a table, rounded to the nearest integer.

**Answer:**
SELECT ROUND(AVG(salary))
FROM employees;

---

## Q151: Create a JavaScript function that takes a given sentence as a parameter and capitalizes the first letter of each word.

**Input:**
```
'hello world'
```

**Answer:**
function capitalizeSentence(str) {
    let words = str.split(' ');
    let res = [];
  
    for (let word of words) {
        res.push(word[0].toUpperCase() + word.slice(1));
    }
  
    return res.join(' ');
}

---

## Q152: Write a Python program to generate the first n Fibonacci numbers.

**Answer:**
def generate_fibonacci_numbers(n):
   if n==1:
       return [0]
   elif n==2:
       return [0,1]
   else:
       fib_list = [0,1]
       for i in range(2,n):
           fib_list.append(fib_list[i-1]+fib_list[i-2])
       return fib_list

---

## Q153: Create a C# program which takes two strings as parameters, and returns true if the two strings are anagrams of each othe

**Input:**
```
'listen', 'silent'
```

**Answer:**
bool AreAnagrams(string s1, string s2)
{
    if (s1.Length != s2.Length)
        return false;
 
    int[] a = new int[256];
    int n = s1.Length;
    for (int i = 0; i < n; i++)
    {
        int c1 = (int)s1[i];
        int c2 = (int)s2[i];
 
        a[c1]++;
        a[c2]--;
    }
 
    for (int i = 0; i < 256; i++)
    {
        if (a[i] != 0)
            return false;
    }
 
    return true;
}

---

## Q154: Write an SQL query to calculate the difference between the total salaries of male and female employees in a table.

**Answer:**
SELECT SUM(CASE WHEN gender = 'female' THEN salary ELSE 0 END) - SUM(CASE WHEN gender = 'male' THEN salary ELSE 0 END)
FROM employees;

---

## Q155: Create a JavaScript program which takes an array of integers as a parameter and reverses the array in-place.

**Input:**
```
[3, 5, 9, 1, 6]
```

**Answer:**
function reverseArrayInPlace(nums) {
    let left = 0;
    let right = nums.length - 1;
  
    while (left < right) {
        let temp = nums[left];
        nums[left] = nums[right];
        nums[right] = temp;
  
        left++;
        right--;
    }
    return nums;
}

---

## Q156: Explain what the following line of code does.

**Input:**
```
a %= b
```

**Answer:**
This line of code assigns the remainder of a divided by b to a, so that the resulting value of a is the remainder of a divided by b. For example, if a is 10 and b is 3, the value of a after executing this line of code would be 1 (the remainder of 10 divided by 3).

---

## Q157: Construct an if-else statement that returns ‘even’ if the given number is even and ‘odd’ if the given number is odd.

**Answer:**
if n % 2 == 0:
    return 'even'
else:
    return 'odd'

---

## Q158: Multiply two vectors of size 5 and return the output.

**Input:**
```
a = [1, 2, 3, 4, 5] 
b = [5, 4, 3, 2, 1]
```

**Answer:**
[5, 8, 9, 8, 5]

---

## Q159: Create a list comprehension that takes all the elements of list_one and creates a new list where all the elements are do

**Input:**
```
list_one = [1, 2, 3, 4, 5]
```

**Answer:**
[x*2 for x in list_one]

---

## Q160: You are given a matrix of m rows and n columns. Write a function that calculates the transpose of the given matrix.

**Input:**
```
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

**Answer:**
def transpose(matrix):
    m = len(matrix)
    n = len(matrix[0])

    transpose_matrix = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            transpose_matrix[j][i] = matrix[i][j]

    return transpose_matrix

---

## Q161: Given a list of numbers, print the difference between the largest and the smallest number.

**Input:**
```
list_of_numbers = [10, 7, 5, 12, 4]
```

**Answer:**
difference = max(list_of_numbers) - min(list_of_numbers)
print(difference)

---

## Q162: Create a for loop that goes through every element of list_of_words and prints ‘success’ if an element is equal to “examp

**Input:**
```
list_of_words = ["hello", "example", "world"]
```

**Answer:**
for word in list_of_words:
    if word == "example":
        print("success")
    else:
        print("failure")

---

## Q163: Create a function that takes in a list of temperatures and returns the average temperature

**Input:**
```
list_of_temperatures = [20, 24, 26, 18]
```

**Answer:**
def average_temperature(temperatures):
    num_items = len(temperatures)
    sum_items = 0
    for temperature in temperatures:
        sum_items += temperature
    return sum_items / num_items

---

## Q164: You are given a list of numbers. Create a function that returns a new list with duplicates removed

**Input:**
```
list_of_numbers = [3, 6, 5, 5, 7, 6, 3]
```

**Answer:**
def remove_duplicates(numbers):
    new_list = []
    for num in numbers:
        if num not in new_list:
            new_list.append(num)
    return new_list

---

## Q165: In a given string, create a function that returns the longest consecutive sequence of characters.

**Input:**
```
my_string = “abccdeefghj"
```

**Answer:**
def longest_consecutive(string):
    character_list = []
    max_length = 0
    max_sequence = ''
    for char in string:
        if char in character_list:
            continue
        else:
            character_list.append(char)
            current_length = 1
            for i in range(1, len(string)):
                if string[i-1] == char and string[i] == char:
                    current_length += 1
            if current_length>max_length:
                max_length = current_length
                max_sequence = char*max_length
    return max_sequence

---

## Q166: Create a function that takes in a string and counts the number of vowels in it

**Answer:**
def count_vowels(string):
    vowels = ["a", "e", "i", "o", "u"]
    count = 0
    for char in string:
        if char in vowels:
            count += 1
    return count

---

## Q167: Write a function that takes in a string and returns a list of all the words that have more than 5 characters

**Answer:**
def long_words(string):
    words = string.split()
    long_words_list = []
    for word in words:
        if len(word) > 5:
            long_words_list.append(word)
    return long_words_list

---

## Q168: Create a function that takes in a string and replaces all punctuation with a space

**Answer:**
import string

def replace_punctuation(string):
    for char in string:
        if char in string.punctuation:
            string = string.replace(char, " ")
    return string

---

## Q169: Create a function that takes in a list of numbers and returns true if the list contains at least one positive number

**Input:**
```
list_of_numbers = [-2, -5, 0, 3]
```

**Answer:**
def is_positive_number(numbers):
    for num in numbers:
        if num > 0:
            return True
    return False

---

## Q170: Write code in Java to generate the Fibonacci sequence up to N numbers.

**Input:**
```
N = 10
```

**Answer:**
public class Fibonacci { 
  
    public static void FibonacciN(int n) { 
        int i, f=0, s=1; 
  
        if (n == 1) 
            System.out.print(f+ " "); 
  
        else { 
            System.out.print(f+" "+s+" "); 
  
            for (i = 2; i < n; i++) { 
                int next = f + s; 
                System.out.print(next+" "); 
                f= s; 
                s = next; 
            } 
        } 
    } 
}

---

## Q171: Write an algorithm to find the largest element in an array.

**Input:**
```
[8, 11, 12, 5, 3]
```

**Answer:**
// Algorithm to find the largest element in an array

// Step 1: Create a variable 'max' and initialize it with value of the first element in the array
int max = arr[0];

// Step 2: Iterate through the array and compare each element with 'max'
for (int i = 1; i < arr.length; i++) {
    if (arr[i] > max) {
        max = arr[i];
    }
}

// Step 3: Return the value of 'max'
return max;

---

## Q172: Write code in Java to sort an array of integers in ascending order.

**Input:**
```
[5, 2, 8, 10, 4, 9]
```

**Answer:**
public static void sortAscending(int[] arr) {
    for(int i = 0; i < arr.length - 1; i++) {
        int min = i;
        for (int j = i + 1; j < arr.length; j++) {
            if (arr[j] < arr[min]) {
                min = j;
            }
        }
        int tmp = arr[i];
        arr[i] = arr[min];
        arr[min] = tmp;
    }
}

---

## Q173: Create a new button using HTML.

**Answer:**
<button>My Button</button>

---

## Q174: Write a SQL query to add a new column "age" in the employees table.

**Answer:**
ALTER TABLE Employees
ADD COLUMN age INT;

---

## Q175: Design a function in Python to delete duplicates from a list.

**Input:**
```
The list is: [2, 3, 2, 4, 5, 5, 6]
```

**Answer:**
def remove_duplicates(list): 
      
    unique_list = [] 
      
    for x in list: 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list 
  
list = [2, 3, 2, 4, 5, 5, 6] 
print ("Original List: ", list) 
print ("Unique List: ", remove_duplicates(list)) 

Output: 
Original List: [2, 3, 2, 4, 5, 5, 6]
Unique List: [2, 3, 4, 5, 6]

---

## Q176: Implement an algorithm to find the sum of all the elements in an array.

**Input:**
```
The array is: [3, 5, 8, 10, 4]
```

**Answer:**
// Algorithm to calculate the sum of all the elements in an array

// Step 1: Initialize a variable 'sum' and set it equal to 0
int sum = 0;

// Step 2: Iterate through the array and add each element to 'sum'
for (int i = 0; i < arr.length; i++) {
    sum += arr[i];
}

// Step 3: Return the value of sum
return sum;

---

## Q177: Write a MySQL query to display the name, job and salary of all employees.

**Answer:**
SELECT name, job, salary 
FROM employees;

---

## Q178: Find the sum of two numbers using C#.

**Input:**
```
The two numbers are: 123 and 456
```

**Answer:**
int  result = 123 + 456;
Console.WriteLine(result); //Output: 579

---

## Q179: Create a web page using HTML and CSS that displays a div with some text.

**Answer:**
<html>
   <head>
      <title>Div Example</title>
   </head>
   <body>
      <div>Hello, welcome to my website!</div>
   </body>
</html>

---

## Q180: Write a JavaScript function to capitalize the first letter of each word in a string.

**Input:**
```
String: "This is an example".
```

**Answer:**
function capitalizeFirstLetter(str) {
    return str.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}
capitalizeFirstLetter('This is an example');

---

## Q181: Write a Python program to loop through all the items in a given list.

**Input:**
```
List: [1, 2, 3, 4, 5, 6]
```

**Answer:**
my_list = [1, 2, 3, 4, 5, 6]
for item in my_list:
    print(item)

---

## Q182: Write a SQL query to select the name and address from a given table.

**Input:**
```
Table: Employee
```

**Answer:**
SELECT name, address FROM Employee

---

## Q183: Create a new CSS animation rule to rotate an object a full circle.

**Answer:**
@keyframes rotate {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

---

## Q184: Write a PL/SQL program to print out all numbers from 1 to 10.

**Answer:**
BEGIN
  FOR i IN 1..10 LOOP
    DBMS_OUTPUT.PUT_LINE(i);
  END LOOP;
END;

---

## Q185: Write a JavaScript code snippet to remove the last element from an array.

**Input:**
```
Array: [1, 2, 3, 4, 5]
```

**Answer:**
let array = [1, 2, 3, 4, 5];
array.pop(); // remove the last element
console.log(array); // [1, 2, 3, 4]

---

## Q186: Convert the following binary number to a decimal number.

**Input:**
```
Binary Number: 10011
```

**Answer:**
19 (10011 = 2^4 + 2^3 + 2^1 = 16 + 8 + 1 = 25)

---

## Q187: Write a Java program to calculate the sum of the two given integers.

**Input:**
```
Integers: 4 and 9
```

**Answer:**
public static int addIntegers(int a, int b) {
    int sum = a + b;
    return sum;
}

public static void main(String[] args) {
    int x = 4, y = 9;
    int sum = addIntegers(x, y);
    System.out.println("Sum is: "+sum);
}

---

## Q188: What is the largest prime factor of the number 885?

**Answer:**
The largest prime factor of 885 is 5.

---

## Q189: Create a function in Python which takes two parameters and returns their product.

**Answer:**
def product(a, b):
    return a*b

---

## Q190: Construct a for loop that prints out the numbers from 1 to 10

**Answer:**
for i in range(1, 11):
    print(i)

---

## Q191: Create an HTML form with three input fields: firstName, lastName and age.

**Answer:**
<form> 
    First Name:<br> 
    <input type="text" name="firstName"><br> 
    Last Name:<br> 
    <input type="text" name="lastName"><br> 
    Age:<br> 
    <input type="number" name="age"><br><br> 
    <input type="submit" value="Submit"> 
</form>

---

## Q192: Write a function in Java that takes two strings as parameters and returns true if the first string is a substring of the

**Answer:**
public boolean isSubstring(String s1, String s2) 
{ 
    int M = s1.length(); 
    int N = s2.length(); 
  
    for (int i = 0; i <= N - M; i++) { 
        int j; 
  
        for (j = 0; j < M; j++) 
            if (s2.charAt(i + j) != s1.charAt(j)) 
                break; 
  
        if (j == M) 
            return true; 
    } 
  
    return false; 
}

---

## Q193: Construct a while loop that increments a counter every time a number is divisible by 3.

**Answer:**
int count = 0; 
int i = 0; 
while(i < 100)
{
     if(i % 3 == 0)
          count++; 
     i++;
}

---

## Q194: Create a Regular Expression pattern to find words that contain the letters "a", "b", and "c".

**Answer:**
\b[abc]+\w*\b

---

## Q195: Create a class in Python to represent a Person.

**Answer:**
class Person:
    # Constructor 
    def __init__(self, name, age): 
         
        # instance attributes 
        self.name = name 
        self.age = age 
  
    # instance method 
    def greeting(self): 
        print("My name is", self.name) 
  
# construct an object 
person1 = Person("John", 36) 
  
# call a method of the object 
person1.greeting()

---

## Q196: Write a code to check whether the input string is a palindrome or not.

**Input:**
```
a man a plan a canal panama
```

**Answer:**
"""
Write a code to check whether the input string is a palindrome or not
"""

def check_palindrome(input_string):
    rev_str = input_string[::-1]
 
    # Checking if both string are equal or not
    if rev_str == input_string:
        return True
    return False
  
# main function
if __name__ == "__main__":
    str = "a man a plan a canal panama"
    if check_palindrome(str):
        print("String is Palindrome")
    else:
        print("String is not Palindrome")

---

## Q197: Write a code to remove the duplicates from a given list.

**Input:**
```
mylist = [1,2,3,1,2]
```

**Answer:**
"""
Write a code to remove the duplicates from a given list
"""

# List containing the elements
mylist = [1,2,3,1,2]

# Creating a new list with unique elements
unique_list = list(set(mylist))

# Printing the new list
print("New list with unique elements is {}".format(unique_list))

---

## Q198: Create a dictionary containing the key-value pair of a given string.

**Input:**
```
string = "test string"
```

**Answer:**
"""
Create a dictionary containing the key-value pair of a given string
"""

# Given string
string = "test string"

# Initialising an empty dictionary
my_dict = {}

# Looping through the given string
for char in string:
    # If the character is not already in dictionary
    if char not in my_dict:
        # Adding the character to the dictionary
        my_dict[char] = 1
    # If the character already exists in dictionary
    else:
        # Incrementing the frequency
        my_dict[char] += 1
        
# Printing the dictionary
print(my_dict)

---

## Q199: Write a code to generate a random number between 1 to 10.

**Answer:**
"""
Write a code to generate a random number between 1 to 10
"""

import random

# Generate random number between 1 to 10 
random_number = random.randint(1,10)

# Printing the random number
print(random_number)

---

## Q200: Write a code to create a 3 x 3 matrix containing all 0s.

**Answer:**
"""
Write a code to create a 3 x 3 matrix containing all 0s
"""

# Creating an empty 3 x 3 matrix
matrix = [[0 for x in range(3)] for y in range(3)] 
  
# Printing the matrix
print(matrix)

---

## Q201: Write a code to check whether two strings are anagrams or not.

**Input:**
```
first = "listen"
second = "silent"
```

**Answer:**
"""
Write a code to check whether two strings are anagrams or not
"""

# Strings to be checked
first = "listen"
second = "silent"

# Sorting the strings
first_sorted = "".join(sorted(first))
second_sorted = "".join(sorted(second))

# Checking if both sorted strings are equal or not
if first_sorted == second_sorted:
    print("Strings are Anagrams")
else:
    print("Strings are not Anagrams")

---

## Q202: Write a code to delete all the vowels from a given string.

**Input:**
```
string = "hello world"
```

**Answer:**
"""
Write a code to delete all the vowels from a given string
"""

# Given string
string = "hello world"

# Removing all the vowels from the string
no_vowels = "".join([letter for letter in string if letter not in "aeiouAEIOU"])

# Printing the new string
print("String without vowels is", no_vowels)

---

## Q203: Write a code to convert a given list of strings to uppercase.

**Input:**
```
mylist = ["hello","world"]
```

**Answer:**
"""
Write a code to convert a given list of strings to uppercase
"""

# List containing the strings
mylist = ["hello","world"]

# Converting the list of strings to uppercase
upper_list = [string.upper() for string in mylist]
 
# Printing the new list
print("List with strings in uppercase is", upper_list)

---

## Q204: Write a code to find the maximum in a given list of integers.

**Input:**
```
mylist = [1,2,3,4,5]
```

**Answer:**
"""
Write a code to find the maximum in a given list of integers
"""

# List containing the elements
mylist = [1,2,3,4,5]

# Finding the maximum element
max = mylist[0]

# Looping through each element to find if it is the maximum
for i in range(1,len(mylist)):
    # Comparing the element with the maximum
    if mylist[i] > max:
        max = mylist[i]

# Printing the maximum element
print("Maximum element of the list is", max)

---

## Q205: Write a code to generate the multiplication table of a given integer.

**Input:**
```
x = 5
```

**Answer:**
"""
Write a code to generate the multiplication table of a given integer
"""

# Number for which multiplication table will be generated
x = 5

# Generating the multiplication table
for i in range(1,11):
    # Printing each row of the table
    print("{} x {} = {}".format(x,i,x*i))

---

## Q206: Write a code to merge two given lists of equal size.

**Input:**
```
list1 = [1,2,3]
list2 = [4,5,6]
```

**Answer:**
"""
Write a code to merge two given lists of equal size
"""

# Given lists
list1 = [1,2,3]
list2 = [4,5,6]

# Initialising an empty list
merged_list = []

# Merging the lists
for i in range(len(list1)):
    merged_list.append(list1[i])
    merged_list.append(list2[i])

# Printing the merged list
print("Merged list is", merged_list)

---

## Q207: Write a code to compute the mean of an input list of numbers.

**Input:**
```
mylist = [1,2,3,4,5]
```

**Answer:**
"""
Write a code to compute the mean of an input list of numbers
"""

# List containing the elements
mylist = [1,2,3,4,5]

# Computing the sum and number of elements
sum = 0
num_elements = len(mylist)

# Looping through each element
for i in mylist:
    sum += i

# Computing the mean
mean = sum/num_elements

# Printing the mean
print("Mean of the list is", mean)

---

## Q208: Create a program to convert the input sentence to Pig Latin.

**Input:**
```
I am a computer programmer
```

**Answer:**
"""
Create a program to convert the input sentence to Pig Latin.
"""

def pig_latin(sentence):
    words = sentence.split()
    new_words = []
    for word in words:
        if word[0] in 'aeiou':
            new_words.append(word + 'ay')
        else:
            new_words.append(word[1:] + word[0] + 'ay')
    return ' '.join(new_words)

if __name__ == '__main__':
    print(pig_latin('I am a computer programmer'))

---

## Q209: Create a program to write an overwriting if-else logic for the following switch statement

**Input:**
```
switch(a) {
  case 1: 
    func1();
    break;
  case 2: 
    func2();
    break;
}
```

**Answer:**
"""
Create a program to write an overwriting if-else logic for the following switch statement
"""

def switch_to_if_else(a):
  if a == 1:
    func1()
  elif a == 2:
    func2()

if __name__ == '__main__':
    switch_to_if_else(a)

---

## Q210: Write a function that sorts the given list of numbers in descending order

**Input:**
```
[1, 2, 3, 5, 8, 10]
```

**Answer:**
"""
Write a function that sorts the given list of numbers in descending order
"""

def sort_list_descending(numbers):
    numbers.sort(reverse = True)
    return numbers

if __name__ == '__main__':
    print(sort_list_descending([1, 2, 3, 5, 8, 10]))

---

## Q211: Create a program to create a list of all the numbers from 1 to 10 which are divisible by 3

**Answer:**
"""
Create a program to create a list of all the numbers from 1 to 10 which are divisible by 3
"""

def divisible_by_three():
    divisible_by_three_list = []
    for i in range(1, 11):
        if i % 3 == 0:
            divisible_by_three_list.append(i)
    return divisible_by_three_list

if __name__ == '__main__':
    print(divisible_by_three())

---

## Q212: rewrite the following for-loop as a while-loop

**Input:**
```
for i in range(0, 5):
    print(i)
```

**Answer:**
"""
Rewrite the following for-loop as a while-loop
"""

i = 0
while i < 5:
    print(i)
    i += 1

---

## Q213: Create a program to compute the checksum of a given data packet

**Input:**
```
data_packet = [0xff, 0x0a, 0x1b, 0x3f]
```

**Answer:**
"""
Create a program to compute the checksum of a given data packet
"""

def compute_checksum(data_packet):
    checksum = 0
    for x in data_packet:
        checksum += x
    return checksum

if __name__ == '__main__':
    data_packet = [0xff, 0x0a, 0x1b, 0x3f]
    print(compute_checksum(data_packet))

---

## Q214: Create a program to parse a given string and return a dictionary with all the words and their frequency

**Input:**
```
"this is a practice string to learn the parsing of strings"
```

**Answer:**
"""
Create a program to parse a given string and return a dictionary with all the words and their frequency
"""

def parse_string(string):
    words = string.split()
    word_dict = {}
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    return word_dict

if __name__ == '__main__':
    print(parse_string("this is a practice string to learn the parsing of strings"))

---

## Q215: Create a program to classify whether the given number is even or odd

**Input:**
```
5
```

**Answer:**
"""
Create a program to classify whether the given number is even or odd
"""

def even_or_odd(number: int) -> str:
    if number % 2 == 0:
        return 'even'
    else:
        return 'odd'

if __name__ == '__main__':
    print(even_or_odd(5))

---

## Q216: Create a program to generate the sum of all the elements in a given list

**Input:**
```
[1, 2, 3, 4, 5]
```

**Answer:**
"""
Create a program to generate the sum of all the elements in a given list
"""

def sum_list(nums):
    total = 0
    for num in nums:
        total += num
    return total

if __name__ == '__main__':
    print(sum_list([1, 2, 3, 4, 5]))

---

## Q217: Create a program to find all the factors of a given number

**Input:**
```
24
```

**Answer:**
"""
Create a program to find all the factors of a given number 
"""

def find_factors(num):
    factors = []
    for i in range(1, num+1):
        if num % i == 0:
            factors.append(i)
    return factors

if __name__ == '__main__':
    print(find_factors(24))

---

## Q218: Create a program to check if a given string is a palindrome

**Input:**
```
"racecar"
```

**Answer:**
"""
Create a program to check if a given string is a palindrome
"""

def is_palindrome(string):
    n = len(string)
    for i in range(n // 2):
        if string[i] != string[n-i-1]:
            return False
    return True

if __name__ == '__main__':
    print(is_palindrome("racecar"))

---

## Q219: Create a program to generate all possible pairs of a given list of numbers

**Input:**
```
[1, 2, 3]
```

**Answer:**
"""
Create a program to generate all possible pairs of a given list of numbers
"""

def generate_pairs(nums):
    pairs = []
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            pairs.append((nums[i], nums[j]))
    return pairs

if __name__ == '__main__':
    print(generate_pairs([1, 2, 3]))

---

## Q220: Create a program that extracts a given pattern from a given string

**Input:**
```
text = "Hello world!", pattern = "l"
```

**Answer:**
"""
Create a program that extracts a given pattern from a given string
"""

def extract_pattern(text, pattern):
    result = []
    for i in range(len(text)):
        if text[i] == pattern:
            result.append(i)
    return result

if __name__ == '__main__':
    text = "Hello world!"
    pattern = "l"
    print(extract_pattern(text, pattern))

---

## Q221: Write a Python program to split special characters with a given string.

**Input:**
```
string = "Hello@#World"
```

**Answer:**
string = "Hello @# World"

---

## Q222: Create a regex to match the characters "CDE" in any order.

**Answer:**
regex = r"(C|D|E){3}"

---

## Q223: Convert the following string to a list of strings.

**Input:**
```
words = "How are you doing today"
```

**Answer:**
words = ["How", "are", "you", "doing", "today"]

---

## Q224: Generate a 5x5 array with all its elements equal to 1.

**Answer:**
arr = [[1,1,1,1,1],
       [1,1,1,1,1],
       [1,1,1,1,1],
       [1,1,1,1,1],
       [1,1,1,1,1]]

---

## Q225: Given a list of numbers, find the index of the greatest value.

**Input:**
```
lst = [3, 5, 6, 8, 9]
```

**Answer:**
index = 4

---

## Q226: Classify the following sentence as positive or negative sentiment.

**Input:**
```
This is the worst experience ever.
```

**Answer:**
Negative sentiment.

---

## Q227: Create a web page with a centered title and paragraph in HTML.

**Input:**
```
title = "My First Web Page"
paragraph = "This is my first web page. It is an amazing experience!"
```

**Answer:**
<!DOCTYPE html>
<html>
    <head>
        <title>My First Web Page</title>
    </head>
    <body>
        <div class="main">
            <h1 align="center">My First Web Page</h1>
            <p align="center">This is my first web page. It is an amazing experience!</p>
        </div>
    </body>
</html>

---

## Q228: Create a JavaScript function that finds the shortest word in a string.

**Input:**
```
sentence = "I'm so excited to begin this journey"
```

**Answer:**
function findShortestWord(sentence) { 
    let words = sentence.split(" "); 
    let shortestWord = words[0]; 
  
    for (let i = 0; i < words.length; i++) { 
        if (words[i].length < shortestWord.length) 
            shortestWord = words[i]; 
    } 
  
    return shortestWord; 
}

---

## Q229: Find the total number of elements in the following array.

**Input:**
```
my_array = [[1,2], 3, 4]
```

**Answer:**
Total number of elements = 4

---

## Q230: Write a SQL query to find the names of customers who have ordered products.

**Answer:**
SELECT c.name
FROM customers c, orders o
WHERE o.customer_id = c.id

---

## Q231: Classify the following sentence as a question or a statement.

**Input:**
```
Have you ever tried eating a brussel sprout?
```

**Answer:**
Question.

---

## Q232: Write a Python program that tests if a given number is divisible by 3.

**Input:**
```
num = 51
```

**Answer:**
if (num % 3 == 0):
    print("The number is divisible by 3")
else:
    print("The number is not divisible by 3")

---

## Q233: Edit the following code so it outputs the odd numbers between 1 and 50.

**Input:**
```
for i in range(1,51):
    print(i)
```

**Answer:**
for i in range(1,51):
    if i % 2 != 0:
        print(i)

---

## Q234: Write a function to compare two strings and return True if they are anagrams.

**Input:**
```
str1 = 'silent'
str2 = 'listen'
```

**Answer:**
def anagram(str1, str2): 

    # Get lenghts of both strings 
    n1 = len(str1) 
    n2 = len(str2) 
  
    # If lengths are not same, then strings   
    # are not anagrams 
    if n1 != n2:
        return False
    str1 = ''.join(sorted(str1))
    str2 = ''.join(sorted(str2))
    # Comparing sorted strings 
    for i in range(0, n1): 
        if str1[i] != str2[i]: 
            return False

    return True

print(anagram(str1, str2))

---

## Q235: Write a function that takes a list of integers as inputs and returns the sum of the square of all the even numbers.

**Input:**
```
lst = [2, 8, 9, 5, 3, 10]
```

**Answer:**
def sum_square_even(lst):
    result = 0
    for num in lst:
        if (num % 2 == 0):
            result += num ** 2
    return result

print(sum_square_even(lst))

---

## Q236: Using the input string, write a code to replace the "!" with a "?".

**Input:**
```
string = "Hello World!"
```

**Answer:**
string = "Hello World!"
string = string.replace("!", "?")
print(string)

---

## Q237: Write a code to take two string inputs and generate the output string containing alternate characters from each string.

**Input:**
```
str1 = 'abc'
str2 = '123'
```

**Answer:**
def alternate_char(str1, str2):
    # get the length of string
    n = len(str1)

    # initialize the output string
    output_str = ''

    # generate the output string
    for i in range(n):
        output_str += str1[i] + str2[i]
    
    return output_str

print(alternate_char(str1, str2))

---

## Q238: Given a list of strings, write a code to find the longest string.

**Input:**
```
lst = ['one', 'two', 'three', 'four', 'five']
```

**Answer:**
# initial max length
max_length = 0
# empty string to store the max length string
max_str = ''

# iterate through the list
for string in lst:
    # get the length
    length = len(string)
    # update the max length
    if length > max_length:
        # get the string
        max_str = string
        # update max length
        max_length = len(string)

print(max_str)

---

## Q239: Write a SQL query to get the total amount from orders table where status is "complete".

**Answer:**
SELECT SUM(amount)
FROM orders
WHERE status = 'completed';

---

## Q240: Write a function to get the mean of the given list of numbers.

**Input:**
```
lst = [1, 4, 5, 9, 3]
```

**Answer:**
def mean(lst):
    # calculate the sum
    total = 0
    for item in lst:
        total += item
    
    # calculate the mean
    mean = total / len(lst)
    return mean

print(mean(lst))

---

## Q241: Write a Django Model API to store status and published date for a blog post.

**Answer:**
from django.db import models

class BlogPost(models.Model):
    # post title
    title = models.CharField(max_length = 200)
    # post status (draft / published)
    status = models.CharField(max_length = 20)
    # post publish date
    published = models.DateTimeField(auto_now_add = True)

---

## Q242: Write a code to compare two lists and find the common elements.

**Input:**
```
list1 = [3, 6, 9, 12]
list2 = [2, 4, 5, 6, 8, 9]
```

**Answer:**
def find_common(list1, list2):
    # initial list to store common elements
    result = []

    # iterate through the list
    for num in list1:
        # check if the number is in list2
        if num in list2:
            # append the element
            result.append(num)

    return result
    
print(find_common(list1, list2))

---

## Q243: Write an algorithm to check if an array contains a given value

**Input:**
```
arr = [1, 7, 5, 8, 44]
value = 5
```

**Answer:**
def check_value(arr, value):
    for item in arr:
        if item == value:
            return True
    return False

---

## Q244: Write a Java program to print out the first n prime numbers

**Answer:**
public static void printPrimeNumbers(int n) 
    { 
        int num; 
        int count=0;
        for (int i = 2; i <= n;) 
        { 
            num=0; 
            for (int j = 2; j <= i / 2; j++)  
            { 
                if (i % j == 0) 
                { 
                    num++; 
                    break; 
                } 
            } 
            if (num == 0) 
            { 
                System.out.print(i+" "); 
                count++; 
            } 
            i++; 
        } 
    }

---

## Q245: Write a SQL query to find the names of all employees working at a given department

**Answer:**
SELECT e.name 
FROM employee e 
JOIN department d ON e.departmentid = d.id 
WHERE d.name = 'given department'

---

## Q246: Write a function to determine if two strings are anagrams of each other

**Answer:**
def are_anagrams(str1, str2):
    if len(str1) != len(str2):
        return False

    freq1 = {}
    freq2 = {}

    for char in str1:
        if char not in freq1:
            freq1[char] = 1
        else:
            freq1[char] += 1

    for char in str2:
        if char not in freq2:
            freq2[char] = 1
        else:
            freq2[char] += 1

    for key in freq1:
        if key not in freq2 or freq2[key] != freq1[key]:
            return False
    
    return True

---

## Q247: Write a JavaScript code to calculate the factorial of a number

**Answer:**
function factorial(n){
    if (n == 0){
        return 1;
    }
    else{
        return n * factorial(n - 1);
    }
}

---

## Q248: Write C++ code to find the maximum subarray sum

**Answer:**
int maxSubarraySum(int arr[], int n) { 
    int max_so_far = 0, max_ending_here = 0; 
  
    for (int i = 0; i < n; i++) { 
        max_ending_here = max_ending_here + arr[i]; 
        if (max_so_far < max_ending_here) 
            max_so_far = max_ending_here; 
  
        if (max_ending_here < 0) 
            max_ending_here = 0; 
    } 
    return max_so_far; 
}

---

## Q249: Write an algorithm to generate the Fibonacci series up to the nth term

**Answer:**
def fibonacci(n):  
    a = 0
    b = 1
    if n < 0: 
        print("Incorrect input") 
    elif n == 0: 
        return a 
    elif n == 1: 
        return b 
    else: 
        for i in range(2,n): 
            c = a + b 
            a = b 
            b = c 
        return b

---

## Q250: Connect to a MySQL database and select all rows from Customers where Phone is greater than 1000.

**Answer:**
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="",
  passwd="",
  database="mydatabase"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM customers WHERE phone > 1000")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

---

## Q251: Write a function that checks if a string is a palindrome or not.

**Input:**
```
string = "ana"
```

**Answer:**
def is_palindrome(string):
    rev = ''.join(reversed(string))
    if rev == string:
        return True
    else:
        return False

---

## Q252: Change the following array so that it orders in ascending order

**Input:**
```
array = [3, 7, 1, 8, 4]
```

**Answer:**
array.sort()

---

## Q253: Read a code and identify the data type of the variables a and b

**Input:**
```
a = 8
b = "Hello"
```

**Answer:**
A is an integer and B is a string.

---

## Q254: Write a simple calculator program.

**Answer:**
def calculator():
    number1 = int(input("Please enter first number: "))
    number2 = int(input("Please enter second number: "))
    print("Please choose operation -\n" \
          "1. Add\n" \
          "2. Subtract\n" \
          "3. Multiply\n" \
          "4. Divide\n") 

    choice = int(input("Enter your choice: "))
    if choice == 1:
        ans = number1 + number2
        print("Answer={}".format(ans))
    elif choice == 2:
        ans = number1 - number2
        print("Answer={}".format(ans))
    elif choice == 3:
        ans = number1 * number2
        print("Answer={}".format(ans))
    elif choice == 4:
        ans = number1 / number2
        print("Answer={}".format(ans))
    else:
        print("Invalid Choice")

---

## Q255: Parse the string "Hello[1]World[4]123[3]" into a list.

**Input:**
```
string = "Hello[1]World[4]123[3]"
```

**Answer:**
my_list = string.split('[')
my_list = [item.replace(']', '') for item in my_list]
my_list = [int(item) for item in my_list[1::2]]

---

## Q256: Read the following two JSON strings and merge them

**Input:**
```
json1 = {
    "name": "John",
    "age": 20
}

json2 = {
    "address": "123 Street"
}
```

**Answer:**
import json

json1 = json.loads(json1)
json2 = json.loads(json2)
merged_json = {**json1, **json2}

---

## Q257: Write a code to return the first 3 elements in a list.

**Input:**
```
mylist = [1,4,3,6,7,2,4]
```

**Answer:**
mylist[:3]

---

## Q258: Change the following array so that it only contains numbers divisible by 3

**Input:**
```
mylist = [2, 4, 5, 6, 7, 11, 12, 22]
```

**Answer:**
mylist = [x for x in mylist if x % 3 == 0]

---

## Q259: Write a function to remove duplicate items in a list.

**Input:**
```
mylist = [2, 3, 3, 4, 5, 6, 4, 7]
```

**Answer:**
def remove_duplicates(mylist):
    return set(mylist)

---

## Q260: Read a code and find all the function calls that are made.

**Input:**
```
print('Hello world!')
my_function()
my_function2(2, 3)
```

**Answer:**
The two function calls made are "my_function()" and "my_function2(2, 3)".

---

## Q261: Write a code to delete all items from a list with a value of 3.

**Input:**
```
mylist = [2, 3, 3, 4, 5, 6, 4, 7]
```

**Answer:**
mylist = [item for item in mylist if item != 3]

---

## Q262: Connect to a MongoDB database and select all documents from the collection ‘customers’.

**Answer:**
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

mydoc = mycol.find({})

for x in mydoc:
  print(x)

---

## Q263: Create a new array that contains only the even numbers from a given array.

**Input:**
```
arr = [1, 2, 3, 4, 5, 6, 7, 8]
```

**Answer:**
arr = [x for x in arr if x % 2 == 0]

---

## Q264: Find the number of times a letter appears in a string.

**Input:**
```
string = "Hello World"
letter = 'l'
```

**Answer:**
count = string.count(letter)

---

## Q265: Create a for loop to print the numbers from 1 to 100.

**Answer:**
for i in range(1, 101):
    print(i)

---

## Q266: Estimate the time complexity of the following algorithm.

**Input:**
```
for i in range(n):
    for j in range(n):
        print(i + j)
```

**Answer:**
O(n^2)

---

## Q267: Write a code snippet to return the item with the highest value in a given dictionary.

**Input:**
```
d = {'a':20, 'b':10, 'c':15}
```

**Answer:**
key = max(d, key = d.get) 
val = d[key]
return (key, val)

---

## Q268: For the following two arrays, create a code snippet to return the intersecting element.

**Input:**
```
arr1 = [1, 9, 4, 10]
arr2 = [2, 4, 7, 8]
```

**Answer:**
intersect_arr = [] 
for i in arr1:
    if i in arr2:
        intersect_arr.append(i)
return intersect_arr

---

## Q269: Using the numpy library, create a 3x3 Identity Matrix.

**Answer:**
iden_matrix = numpy.identity(3) 
print(iden_matrix)

---

## Q270: Create a Linked List Node with the data of type integer.

**Answer:**
class Node: 
  
  # Function to initializaee the node object 
  def __init__(self, data): 
    self.data = data # Assign data 
    self.next = None # Initialize next as null

---

## Q271: Generate a unique and random password for a user using python.

**Answer:**
import random 
characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=[ ]{}:'
password = random.choices(characters, k = 16) 
print("".join(password))

---

## Q272: Given a binary tree, write a code snippet to list all of its descendant leafs.

**Answer:**
def listDescendantLeaves(root):
    if not root: 
        return
    elif not root.left and not root.right: 
        print(root.val) 
    listDescendantLeaves(root.left) 
    listDescendantLeaves(root.right)

---

## Q273: Given a string, write a function to remove all the duplicate characters.

**Input:**
```
string = "apple"
```

**Answer:**
def remove_duplicates(string): 
    new_string = "" 
    for char in string:
        if char not in new_string:
            new_string += char 
    return new_string

---

## Q274: classify the following sentence using a sentiment analysis model.

**Input:**
```
The movie is awesome.
```

**Answer:**
"""
Classify the following sentence using a sentiment analysis model.
Sentence: The movie is awesome.
"""

from textblob import TextBlob

sentence = "The movie is awesome."

# convert the sentence to a TextBlob object
blob = TextBlob(sentence)

# get the sentiment
sentiment = blob.sentiment

if sentiment.polarity > 0:  # positive sentiment
    print("This sentence is classified as Positive.")
elif sentiment.polarity == 0:  # neutral sentiment
    print("This sentence is classified as Neutral.")
else:  # negative sentiment
    print("This sentence is classified as Negative.")

---

## Q275: convert all words in a sentence to camelCase

**Input:**
```
The quick brown fox jumps over the lazy dog
```

**Answer:**
"""
Convert all words in a sentence to camelCase

Input: The quick brown fox jumps over the lazy dog

Output: theQuickBrownFoxJumpsOverTheLazyDog
"""

def toCamelCase(sentence):
    words = sentence.split(" ")
    result = ""
    for index, word in enumerate(words):
        if index > 0:
            small_word = word.capitalize()
            result += small_word
        else:
            result += word
    return result

sentence = "The quick brown fox jumps over the lazy dog"
print(toCamelCase(sentence))

---

## Q276: Write a function to calculate the average score of a list of numbers.

**Answer:**
def get_average(numbers):
    """
    Calculate and return the average of a list of numbers
    :param numbers: the list of numbers
    :return: the average of the numbers
    """
    total = 0
    for number in numbers:
        total += number
    return total / len(numbers)

---

## Q277: Write a function to find the longest string in a list of strings.

**Answer:**
def find_longest_string(strings):
    """
    Find and return the longest string in a list of strings.
    :param strings: the list of strings
    :return: the longest string
    """
    longest = ""
    for string in strings:
        if len(string) > len(longest):
            longest = string
    return longest

---

## Q278: Implement a function to extract the last two words from a string of words

**Answer:**
def get_last_two_words(string):
    """
    Extract and return the last two words from a string of words
    :param string: the input string
    :return: the last two words
    """
    words = string.split(" ")
    return words[-2:]

---

## Q279: Write code to find the intersection of two sorted lists

**Input:**
```
list1 = [1, 3, 4, 6]
list2 = [1, 2, 5, 6]
```

**Answer:**
def find_intersection(list1, list2):
    """
    Find the intersection of two sorted lists
    :param list1: the first sorted list
    :param list2: the second sorted list
    :return: a list with elements found in both lists
    """
    intersection = []
    p1 = p2 = 0
    while p1 < len(list1) and p2 < len(list2):
        if list1[p1] == list2[p2]:
            intersection.append(list1[p1])
            p1 += 1
            p2 += 1
        elif list1[p1] < list2[p2]:
            p1 += 1
        else:
            p2 += 1
    return intersection

list1 = [1, 3, 4, 6]
list2 = [1, 2, 5, 6]
print(find_intersection(list1, list2))

---

## Q280: Write code to flatten a nested list

**Answer:**
def flatten_list(list):
    """
    Flatten a nested list
    :param list: the nested list to flatten
    :return: a flattened list
    """
    flattened_list = []
    for item in list:
        if isinstance(item, list):
            flattened_list.extend(flatten_list(item))
        else:
            flattened_list.append(item)
    return flattened_list

---

## Q281: Write code to remove all occurrences of a given element from a list

**Answer:**
def remove_element(list, element):
    """
    Remove all occurrences of a given element from a list
    :param list: the list
    :param element: the element to remove
    :return: the filtered list
    """
    filtered_list = [item for item in list if item != element]
    return filtered_list

---

## Q282: Generate pseudocode for a matrix multiplication algorithm.

**Answer:**
"""
Generate pseudocode for a matrix multiplication algorithm.
"""

# Create an NxN matrix result, initialized to 0
result = zeros(NxN)

# loop through matrix A and B
for i in range(N):
    for j in range(N):
        for k in range(N):
            # multiply the elements of A and B
            result[i][j] += A[i][k] * B[k][j]

# return the result matrix
return result

---

## Q283: Create a function to generate a random password of length n

**Answer:**
import random

def generate_password(n):
    """
    Create a function to generate a random password of length n
    :param n: the length of the password
    :return: a random password of length n
    """ 
    # create a character list of symbols, alphabets, and numbers
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-='
    # create a list of length n with random characters
    password = [random.choice(characters) for _ in range(n)] 
    # convert the list to a string
    password = ''.join(password)  
    # return the password
    return password

---

## Q284: Debug the following Python code

**Input:**
```
def f(x):
    if x > 0:
        return -1
    else:
        return 1
```

**Answer:**
"""
Debug the following Python code

def f(x):
    if x > 0:
        return -1
    else:
        return 1
"""

# incorrect indentation of the else statement
def f(x):
    if x > 0:
        return -1
    else:
        return 1   # correct indentation

---

## Q285: Generate a data structure that can efficiently store an array of words

**Answer:**
"""
Generate a data structure that can efficiently store an array of words
"""

# create a trie (a node with 26 references to other nodes)
class TrieNode:
    def __init__(self):
        self.children = dict()
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.end = True

# create an empty array
word_array = []

# create a new trie
trie = Trie()

# iterate over the array and insert the words into the trie
for word in word_array:
    trie.insert(word)

---

## Q286: Create a function to find the position of a substring in a string

**Answer:**
def find_substring(string, substring):
    """
    Find the position of a substring in a string
    :param string: the string
    :param substring: the substring to find
    :return: the position of the substring in the string
    """
    for i in range(len(string) - len(substring) + 1):
        if string[i:i+len(substring)] == substring:
            return i
    return -1  # substring not found

---

## Q287: Reorder a given array in specialized order

**Answer:**
def reorder_array(arr):
    """
    Reorder a given array in specialized order
    :param arr: the input array to reorder
    :return: the reordered array
    """
    # determine the size of the array
    n = len(arr)
    
    # create a new array to store the reordered results
    reordered = [0] * n
    
    # loop through the array 
    for i in range(n):
        # calculate the position of the current element
        pos = 2 * (arr[i] % (1 + n // 2))
        # find the first vacant position in the new array
        while reordered[pos] != 0:
            pos += 1
        # assign the current element to the vacant position
        reordered[pos] = arr[i]
    
    return reordered

---

## Q288: Write an HTML code to create a horizontal line.

**Answer:**
<hr>

---

## Q289: Design a function in Python that returns the median of an array of integers.

**Answer:**
def median(arr):
  sortedArr = sorted(arr)
  length = len(arr)
  if length % 2 == 0:
    return ((sortedArr[length//2-1] + sortedArr[length//2])/2)
  else:
    return sortedArr[length//2]

---

## Q290: Write a JavaScript code to valid a password based on the following rules:

**Answer:**
function validatePassword(password) {
  // Minimum 8 characters, one uppercase letter, one lowercase letter, one number, and one special character
  const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/;
  if (password.match(re)) {
    return true;
  }
  return false;
}

---

## Q291: Write a code to reverse the order of a data structure such as array, list, or stack.

**Input:**
```
list1 = [1, 3, 5, 7, 9]
```

**Answer:**
list1.reverse() # [9, 7, 5, 3, 1]

---

## Q292: Create a program in C++ that calculates the absolute difference between two numbers.

**Input:**
```
num1 = 50;
num2 = 40;
```

**Answer:**
#include <iostream>
using namespace std;

int main() 
{
  int num1 = 50;
  int num2 = 40;
  int absDiff = abs(num1 - num2);
  cout << "The absolute difference between two numbers is: " << absDiff;
  return 0;
}

---

## Q293: Design an HTML form with the following fields: first name, last name, age, phone number and address.

**Answer:**
<form> 
  <label> First Name: </label> 
  <input type="text" name="firstname" required> 
  <label> Last Name: </label> 
  <input type="text" name="lastname" required> 
  <label> Age: </label> 
  <input type="number" name="age" min="18" required> 
  <label> Phone Number: </label> 
  <input type="tel" name="phone" required> 
  <label> Address: </label> 
  <input type="text" name="address" required> 
  <input type="submit" value="Submit"> 
</form>

---

## Q294: Create a Ruby program to check if a number is even or odd.

**Answer:**
def is_even(number)
  number % 2 == 0
end

---

## Q295: Redesign the following Python program with functions.

**Input:**
```
my_list = [5, 10, 15, 20]
sum = 0
for number in my_list:
sum = sum + number
```

**Answer:**
def sum_of_list(my_list):
  sum = 0
  for number in my_list:
    sum = sum + number
  return sum

my_list = [5, 10, 15, 20]
result = sum_of_list(my_list)

---

## Q296: Create an HTML page displaying a table of 3 rows and 3 columns.

**Answer:**
<table>
  <tr>
    <td>Column 1</td>
    <td>Column 2</td>
    <td>Column 3</td>
  </tr>
  <tr>
    <td>Row 1</td>
    <td>Row 1</td>
    <td>Row 1</td>
  </tr>
  <tr>
    <td>Row 2</td>
    <td>Row 2</td>
    <td>Row 2</td>
  </tr>
  <tr>
    <td>Row 3</td>
    <td>Row 3</td>
    <td>Row 3</td>
  </tr>
</table>

---

## Q297: Debug the following JavaScript code which calculates the average of an array of integers:

**Input:**
```
arr = [2, 3, 4, 5]
sum = 0
for (i = 0; i < arr.length; i++) {
sum += arr[i]}
average = sum / arr.length
```

**Answer:**
arr = [2, 3, 4, 5]
sum = 0
for (i = 0; i < arr.length; i++) {
  sum += arr[i];
}
average = sum / arr.length;
console.log(average);

---

## Q298: Generate an random integer between 1 and 6.

**Answer:**
Math.floor(Math.random() * 6) + 1;

---

## Q299: Create a program that prints the first 10 Fibonacci numbers.

**Answer:**
"""
Print the first ten Fibonacci numbers
"""

def print_first_ten_fibonacci_numbers():
    """Print the first ten Fibonacci numbers."""

    n1, n2 = 0, 1
    num = 0
    while num < 10:
        print(n1)
        nth= n1 + n2
        n1 = n2
        n2 = nth
        num += 1
        
if __name__ == '__main__':
    print_first_ten_fibonacci_numbers()

---

## Q300: Calculate the sum of an array of integers

**Input:**
```
[3, 5, 7, 9]
```

**Answer:**
24

---
