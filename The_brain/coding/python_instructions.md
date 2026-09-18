# Python Code Instructions (Alpaca)

Total: 300 examples


## Q1: Create a function to calculate the sum of a sequence of integers.

**Input:**
```
[1, 2, 3, 4, 5]
```

**Answer:**
# Python code
def sum_sequence(sequence):
  sum = 0
  for num in sequence:
    sum += num
  return sum

---

## Q2: Generate a Python code for crawling a website for a specific type of data.

**Input:**
```
website: www.example.com 
data to crawl: phone numbers
```

**Answer:**
import requests
import re

def crawl_website_for_phone_numbers(website):
    response = requests.get(website)
    phone_numbers = re.findall('\d{3}-\d{3}-\d{4}', response.text)
    return phone_numbers
    
if __name__ == '__main__':
    print(crawl_website_for_phone_numbers('www.example.com'))

---

## Q3: Create a Python list comprehension to get the squared values of a list [1, 2, 3, 5, 8, 13].

**Answer:**
[x*x for x in [1, 2, 3, 5, 8, 13]]

---

## Q4: Generate a python script to perform this action.

**Input:**
```
Given a string, remove all the consecutive duplicates from the string.

Input: "AAABBCCCD"
```

**Answer:**
def remove_duplicates(string): 
    result = "" 
    prev = '' 

    for char in string:
        if char != prev: 
            result += char
            prev = char
    return result

result = remove_duplicates("AAABBCCCD")
print(result)

---

## Q5: Write a python script to generates random numbers between 0 and 9 that are divisible by 3.

**Answer:**
def generate_random_divisible_number():
    import random
    while True:
        # Generate a random number
        process = random.randint(0, 9)
        # Check if the number is divisible by 3
        if process % 3 == 0:
            # If it is divisible, return it
            return process

---

## Q6: Write a Python code to get the third largest element in a given row.

**Input:**
```
[12, 13, 13, 45, 22, 99]
```

**Answer:**
def third_largest(lst):
    if len(lst) < 3:
        return
    distinct = []
    for i in lst:
        if i not in distinct:
            distinct.append(i)
    distinct.sort(reverse=True)
    return distinct[2]

---

## Q7: Generate a REST API with Python and Flask that allows users to create, read, update, and delete records from a database.

**Input:**
```
Not applicable
```

**Answer:**
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Record(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 name = db.Column(db.String(120), unique=True)

db.create_all()

@app.route('/records', methods=['GET'])
def get_records():
 records = Record.query.all()
 return {'records':[record.name for record in records]}

@app.route('/records', methods=['POST'])
def create_record():
 record = Record(name=request.json['name'])
 db.session.add(record)
 db.session.commit()
 return {'id': record.id}

@app.route('/records/int:id', methods=['PUT'])
def update_record(id):
 record = Record.query.get(id)
 record.name = request.json['name']
 db.session.commit()
 ret

---

## Q8: Create a Python function that takes in a string and a list of words and returns true if the string contains all the word

**Input:**
```
'This is a test', ['test', 'this', 'is']
```

**Answer:**
def contains_words(input_string, words):
 for word in words:
 if word not in input_string:
 return False
 return True

print(contains_words('This is a test', ['test', 'this', 'is'])) # True

---

## Q9: What should this Python program do?

**Input:**
```
def is_palindrome(s):
    '''Write your code here.'''
```

**Answer:**
def is_palindrome(s):
    '''This function returns True if the string s is a palindrome and False if it isn't.''' 
    return s == s[::-1]  # Checks if s is the same as its reverse.

---

## Q10: Create a Python program to sort and print out the elements of an array of integers.

**Input:**
```
[17, 41, 5, 22, 54, 6, 29, 3, 13]
```

**Answer:**
arr = [17, 41, 5, 22, 54, 6, 29, 3, 13]

arr.sort()

print(arr)

# Output: [3, 5, 6, 13, 17, 22, 29, 41, 54]

---

## Q11: Generate a Python program that adds two then doubles the result.

**Answer:**
def double_add(num1, num2): 
    return (num1 + num2) * 2

---

## Q12: Write a python program to extract the non-vowel words in a sentence.

**Input:**
```
This machine learning project is challenging.
```

**Answer:**
def extract_words(sentence):
    non_vowel_words = []
    words = sentence.split()
    vowels = ['a','e','i','o','u','A','E','I','O','U']
    for word in words:
        if not any(char in vowels for char in word):
            non_vowel_words.append(word) 
    return non_vowel_words

---

## Q13: Write a Python program to calculate the average of a list of positive integers and output the result.

**Input:**
```
List of positive integers: [1, 5, 6, 7, 8]
```

**Answer:**
list_of_positive_integers = [1, 5, 6, 7, 8]
total = sum(list_of_positive_integers)

avg = total/len(list_of_positive_integers)

print("The average of the list of positive integers is {}".format(avg))

---

## Q14: Develop a function in Python that prints out the Pascal's triangle for a given number of rows.

**Answer:**
def pascal_triangle(n): 
    trow = [1] 
    y = [0] 
    for x in range(max(n, 0)): 
        print(trow) 
        trow=[l+r for l,r in zip(trow + y, y + trow)] 
    return n>=1

pascal_triangle(5)

---

## Q15: Implement a decision-making algorithm for a rock-paper-scissors game using Python.

**Answer:**
# Rock, paper, scissors game!

def play_game(player1, player2):
    #  Define the winning rules
    rules = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    if player1 == player2:
        return 'It is a draw!'
    elif rules[player1] == player2:
        return 'Player 1 wins!'
    elif rules[player2] == player1:
        return 'Player 2 wins!'

# Get user input
player1 = input('Player 1, make a choice: rock, paper, or scissors? ').lower()
player2 = input('Player 2, make a choice: rock, paper, or scissors? ').lower()

# Start the game and get the result
result = play_game(player1, player2)
print(result)

---

## Q16: Collate a machine learning model in Python that distinguishes between cats and dogs.

**Input:**
```
A dataset of 800 images of cats and dogs
```

**Answer:**
import numpy as np
import keras
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator

# Create the neural network model
model = Sequential()

# Input layer
model.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Hidden layers
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.3))
model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.3))
model.add(Conv2D(64, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.3))

# Output layer
model.add(Flatten())
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 1, activation = 'sig

---

## Q17: Write a Python program to find all the numbers divisible by a certain number within a certain range.

**Input:**
```
int m=36, int n=74, int divisor=6
```

**Answer:**
def find_numbers_divisible_by(m, n, divisor):
    divisible_numbers = []
    for i in range(m, n+1):
        if i % divisor == 0:
            divisible_numbers.append(i)
    return divisible_numbers

---

## Q18: Implement a Python function that will take two strings and return true if the first string contains the second.

**Input:**
```
query = "catering"
word = "cat"
```

**Answer:**
def check_contains(query, word): 
    if query.find(word) != -1:
        return True
    return False

result = check_contains(query, word)

---

## Q19: Write an algorithm in Python 3 that calculates the factorial of a number.

**Input:**
```
Not applicable
```

**Answer:**
def factorial(n):
 if n == 0:
  return 1
 else:
  return n * factorial(n-1)

---

## Q20: Develop a Python function to predict the class labels of a given set of data.

**Input:**
```
The dataset contains 4 features: Length, Width, Height and Weight.
```

**Answer:**
# Load the dataset
import pandas as pd
csv_url = 'http://test.test/test.csv'
df = pd.read_csv(csv_url)

# Split the dataset into features and label
X = df.iloc[:, 0:4].values
y = df.iloc[:, 4].values

# Import the ML model
from sklearn.tree import DecisionTreeClassifier

# Create and fit the model
model = DecisionTreeClassifier()
model.fit(X, y)

# Predict the label
def predict(data):
    predicted_label = model.predict([data])
    return predicted_label

---

## Q21: Develop a Python program to generate random passwords that consist of 8 characters.

**Input:**
```
Not applicable
```

**Answer:**
import string
import random

def generate_password():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))

password = generate_password()
print(password)

---

## Q22: Generate a list using a while loop in Python and appends the current number to the list.

**Answer:**
my_list = []

num = 0

while num < 10:
    my_list.append(num)
    num += 1

print(my_list)

---

## Q23: Write a Python program to query Twitter to get the most recent tweets from a user.

**Input:**
```
username: @elonmusk
```

**Answer:**
import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")
# Create API object
api = tweepy.API(auth)

# Get the most recent tweets from the given user
tweets = api.user_timeline(screen_name="@elonmusk")

for tweet in tweets:
 print(tweet.text)

---

## Q24: Create a Python neural network model that takes in a given trajectory of stock prices and predicts the stock price for t

**Input:**
```
[10, 10.4, 10.5, 10.6, 10.7, 10.9, 11]
```

**Answer:**
import numpy as np
import tensorflow as tf

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(7, )),
        tf.keras.layers.Dense(1)
    ])

    model.compile(loss='mean_squared_error', 
                  optimizer='adam',
                  metrics=['accuracy'])

    return model
    
if __name__ == "__main__":
    model = create_model()

    input_data = np.array([[10, 10.4, 10.5, 10.6, 10.7, 10.9, 11]])
    predictions = model.predict(input_data)

    print(f"Predicted stock price for the next day is: {predictions[0][0]}")

---

## Q25: Create a way to encrypt a message using a key in Python.

**Input:**
```
message = "Hello world!"
key = "secret"
```

**Answer:**
import hashlib

def encrypt(message, key):
    encrypted_msg = ""
    for char in message:
        encrypted_msg += chr(ord(char) + ord(key[0]))
    return encrypted_msg

encrypted_msg = encrypt(message, key)
print(encrypted_msg)

---

## Q26: Create a function in Python that takes two parameters and prints out the larger of them.

**Input:**
```
parameter_1 = 7
parameter_2 = 9
```

**Answer:**
def printMax(parameter_1, parameter_2):
    if parameter_1 > parameter_2:
        print(parameter_1)
    else:
      print(parameter_2)

---

## Q27: Rewrite the following Python code by introducing list comprehensions.

**Input:**
```
even_numbers = []
for i in range(1,21):
    if i % 2 == 0:
        even_numbers.append(i)
```

**Answer:**
even_numbers = [i for i in range(1, 21) if i % 2 == 0]

---

## Q28: Develop an algorithm in Python to print Fibonacci series up to a given number.

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
      
n = int(input("Enter a number: "))
print(fibonacci(n))

---

## Q29: Make the following code snippet into a function in Python3 capable of solving Any Sudoku puzzle

**Input:**
```
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]
```

**Answer:**
def solve_sudoku(board): 
  
    # Utility function to find vacant cells 
    # Returns a boolean     
    def find_vacant_cell(board, l): 
        for row in range(9): 
            for col in range(9): 
                if board[row][col] == 0: 
                    l[0] = row 
                    l[1] = col 
                    return True
        return False
  
    # Utility function to check if a number  
    # is not currently placed in a particular  
    # row, column and block 
    def is_safe(board, row, col, num): 
  
        # Check if 'num' is not already placed  
        # in current row, current column  
        # and current 3x3 box 
        for i in range(9): 
  
            # Check the rows
            if(board[row][i] == num): 
                return False
  
            # 

---

## Q30: Write a function in Python to calculate the sum of the digits in a given number.

**Answer:**
def sum_digits(num):
    total = 0
    while num > 0:
        digit = num % 10
        total += digit
        num = num // 10
    return total

---

## Q31: Take the list of people below and create a Python dictionary with the names as keys and the ages as values.

**Input:**
```
John (20), Jane (40), Alex (18), Peter (45)
```

**Answer:**
people_dict = {'John': 20, 'Jane': 40, 'Alex': 18, 'Peter': 45}

---

## Q32: Develop a Python program to clearly understand the concept of recursion.

**Answer:**
# This program is to understand recursion in Python.

# Define a recursive function to calculate the factorial of a number
def factorial(n):
   if n == 1:
      return 1
   else:
      return n * factorial(n - 1)

# Calculate factorial of number 5
result = factorial(5)
print("Factorial of 5 is ", result) 

# Output: Factorial of 5 is 120

---

## Q33: Generate a random 6-digits number in Python.

**Answer:**
import random

number = random.randint(100000, 999999)
print(number)

---

## Q34: Create a sorting algorithm in Python to sort strings by their length.

**Input:**
```
["cat", "dog", "apple", "banana"]
```

**Answer:**
def sort_by_length(strings):
    for i in range(len(strings) - 1):
        for j in range(i + 1, len(strings)):
            if len(strings[i]) > len(strings[j]):
                strings[i], strings[j] = strings[j], strings[i]
    return strings

unsorted_list = ["cat", "dog", "apple", "banana"]

sorted_list = sort_by_length(unsorted_list)

print(sorted_list)

---

## Q35: Write a Python function to get the maximum and minimum values in a given list.

**Input:**
```
Not applicable
```

**Answer:**
def get_max_min(lst):
 min_value = lst[0]
 max_value = lst[0]
 
 for i in range(1, len(lst)):
  if lst[i] > max_value:
   max_value = lst[i]
  if lst[i] < min_value:
   min_value = lst[i]
 
 return (min_value, max_value)

---

## Q36: Create a for loop in Python to iterate over a list of numbers and print only the even numbers.

**Input:**
```
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

**Answer:**
for num in my_list:
    if num % 2 == 0:
        print(num)

---

## Q37: Can you suggest a pure python alternative to declaring a Float32 array with numbers from 0 to 10?

**Answer:**
myArray = [float(i) for i in range(0,11)]

---

## Q38: Construct a neural network model in Python to classify the MNIST data set correctly.

**Answer:**
import keras

# Input layer
input_layer = keras.layers.Input(shape=(784,))

# Hidden layer
hidden_layer = keras.layers.Dense(128, 
                activation='relu')(input_layer)

# Output layer
output_layer = keras.layers.Dense(10, 
                activation='softmax')(hidden_layer)

# Model
model = keras.Model(inputs=input_layer, outputs=output_layer)

# Compile model
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

---

## Q39: Create a machine learning classifier in Python for categorizing user input.

**Answer:**
from sklearn.naive_bayes import MultinomialNB 

# Assuming an input string is passed to the function as a parameter

def classify_string(input_string):

  # Feature extraction and transformation from string to numeric
  features = . . .

  # Create an instance of the classifier 
  model = MultinomialNB()

  # Train the classifier on the data
  model.fit(data, target)

  # Make a prediction based on the input
  prediction = model.predict([features])

  # Return the prediction
  return prediction

---

## Q40: Implement a algorithm in Python for sorting two large lists A and B. The algorithm should take the first element of list

**Input:**
```
A = [3, 6, 8, 10, 11]
B = [2, 5, 7, 12]
```

**Answer:**
def merge_sort(A, B):
 result = [] 
 i, j = 0, 0

# Compare elements and add lower one to result
while i < len(A) and j < len(B):
 if A[i] < B[j]:
 result.append(A[i])
 i += 1
 else:
 result.append(B[j])
 j += 1

# Add remaining elements
result += A[i:]
result += B[j:]

return result

#Test the algorithm
A = [3, 6, 8, 10, 11]
B = [2, 5, 7, 12]

print(merge_sort(A, B))
# Output: [2, 3, 5, 6, 7, 8, 10, 11, 12]

---

## Q41: Develop a program in Python for finding the longest common subsequence between two strings.

**Input:**
```
"ABCDF", "ABECD"
```

**Answer:**
def longest_common_subsequence(string1, string2):
    table = [[0]*(len(string2)+1) for _ in range(len(string1)+1)]

    for i, x in enumerate(string1):
        for j, y in enumerate(string2):
            if x == y:
                table[i+1][j+1] = table[i][j]+1
            else:
                table[i+1][j+1] = max(table[i+1][j], table[i][j+1])

    result = ""
    x, y = len(string1), len(string2)
    while x != 0 and y != 0:
        if table[x][y] == table[x-1][y]:
            x -= 1
        elif table[x][y] == table[x][y-1]:
            y -= 1
        else:
            result = string1[x-1] + result
            x -= 1
            y -= 1
    return result

result = longest_common_subsequence("ABCDF", "ABECD")
print(result)

---

## Q42: Convert a given Python program to a C# program.

**Input:**
```
def power(x, y):
    if y == 0:
        return 1
    else:
        return x * power(x, y - 1)
```

**Answer:**
public int Power(int x, int y)
{
    if (y == 0)
    {
        return 1;
    }
    else
    {
        return x * Power(x, y - 1);
    }
}

---

## Q43: Rewrite the following code in a different programming language.

**Input:**
```
// JavaScript code
let arr = [1, 2, 3, 4, 5];

arr.forEach(item => {
 console.log(item * 2);
});
```

**Answer:**
# Python code
arr = [1, 2, 3, 4, 5]

for item in arr:
 print(item * 2)

---

## Q44: Create a TicTacToe game in Python.

**Answer:**
class TicTacToe:

def __init__(self):
    self.board = [['_' for _ in range(3)] 
                   for _ in range(3)]
    self.turn = 'x'
    
def display(self):
    for row in self.board:
        print(' '.join(row))

def check_win(self):
    board = self.board

    # check if the player with the current turn has a row of three
    for row in self.board:
        if row.count(self.turn) == 3:
            return True
        
    # check if the player with the current turn has a column of three
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[2][col] == self.turn:
            return True
        
    # check for the two diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == self.turn:
    

---

## Q45: Create a Python program to store the strings "Hello" and "World" and print them in the same line.

**Answer:**
string1 = "Hello"
string2 = "World"

print(string1 + " " + string2)

---

## Q46: Use the inputs provided, write Python code to check if two integers are equal.

**Input:**
```
First Integer: 10
Second Integer: 10
```

**Answer:**
if int(10) == int(10):
    print("The two integers are equal")
else:
    print("The two integers are not equal")

---

## Q47: Create a Python program for analyzing the sentiment of given text. The program should categorize the text into positive,

**Input:**
```
Not applicable
```

**Answer:**
import nltk
from nltk.tokenize import sent_tokenize
from nltk.classify import NaiveBayesClassifier

def analyze_sentiment(text):
    sents = sent_tokenize(text)
    neg = 0
    pos = 0
    for sentence in sents:
        sentiment_analysis = NaiveBayesClassifier.classify(sentence)
        if sentiment_analysis == 'neg':
            neg += 1
        if sentiment_analysis == 'pos':
            pos += 1
    
    if neg > pos:
        sentiment = 'negative'
    elif pos > neg:
        sentiment = 'positive'
    else:
        sentiment = 'neutral'
    
    return sentiment

# End analyze sentiment definition

---

## Q48: Create a Python program to calculate the average of five numbers entered by a user.

**Answer:**
nums = []
for i in range(5):
    nums.append(int(input("Please enter number: ")))

#Calculate average
average = sum(nums) / len(nums)

#Print average
print("The average is ", average)

---

## Q49: Write a Python program to generate a Markov chain given a text input.

**Input:**
```
Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, `and what is the use of a book,' thought Alice `without pictures or conversation?'
```

**Answer:**
import random

def generateMarkov(text):
  words = text.split(' ')
  markovChain = {}

  for i in range(len(words) - 2):
    current = words[i]
    next = words[i + 1]
    if current in markovChain:
      if next in markovChain[current]:
        markovChain[current][next] += 1
      else:
        markovChain[current][next] = 1
    else:
      markovChain[current] = {next: 1}

  generatedText = ""
  current = random.choice(list(markovChain))
  generatedText += current

  for i in range(100):
    choices = markovChain[current]
    choices = [
      key for key, value in choices.items()
      for i in range(value)
    ]
    try:
      current = random.choice(choices)
      generatedText += " " + current
    except:
      break

  return generatedText

text = 'Alice was beginning to get very t

---

## Q50: Write a Python program to determine if a number provided by the user is prime or not.

**Input:**
```
17
```

**Answer:**
# Ask the user for a number
num = int(input('Enter a number: '))

# Set initial values
is_prime = True

# Check for prime
for i in range(2, num):
 if num % i == 0:
 is_prime = False
 break

# Output result
if is_prime:
 print(f'{num} is a prime number.')
else:
 print(f'{num} is not a prime number.')

---

## Q51: Write a Python program to calculate the difference between the lowest and highest value for an array of integers.

**Input:**
```
[12, 24, 3, 8, -1]
```

**Answer:**
def diffHighestLowest(arr):
    lowest = min(arr)
    highest = max(arr)
    return highest - lowest

arr = [12, 24, 3, 8, -1]
difference = diffHighestLowest(arr)
print(difference)  # 25

---

## Q52: Rewrite the following code snippet to find prime numbers using Python.

**Input:**
```
Not applicable
```

**Answer:**
def is_prime(num):
    # Iterate from 2 to the square root of the number
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Iterate from 2 to n
for n in range(2, n+1):
    # Check if the number is prime
    if is_prime(n):
        print(n)

---

## Q53: Write a Python program to create a dictionary where the keys are numbers between 1 and 15 (both included) and the values

**Answer:**
d = {}

for i in range(1, 16):
    d[i] = i**2

print(d)

---

## Q54: Write a Python program to calculate the sum of all even numbers less than or equal to n.

**Answer:**
def sum_of_even_numbers(n):
 result = 0
 for i in range(2, n+1, 2):
 result += i
 return result

---

## Q55: Create a Python script to calculate the Fibonacci numbers up to a given number.

**Answer:**
def Fibonacci(n): 
	if n==0: 
		return 0
	if n==1: 
		return 1
	else: 
		return Fibonacci(n-1)+Fibonacci(n-2)

---

## Q56: Write a Python program to calculate the total cost of a shopping cart. The program should consider the item prices, quan

**Input:**
```
[ 
 {"name": "widget", "price": 10, "quantity": 5 },
 {"name": "thingy", "price": 7, "quantity": 3 },
 {"name": "doodad", "price": 5, "quantity": 2 },
]
Shipping cost: 7.50
Tax rate: 9.5%
```

**Answer:**
items = [
 {"name": "widget", "price": 10, "quantity": 5 },
 {"name": "thingy", "price": 7, "quantity": 3 },
 {"name": "doodad", "price": 5, "quantity": 2 },
]

taxRate = 0.095
shippingCost = 7.50

totalCost = 0

for item in items:
 totalCost += item['price'] * item['quantity']

totalCost += totalCost * taxRate
totalCost += shippingCost

print('Total cost:', totalCost)

---

## Q57: In Python, create a function to find the maximum value within a nested dictionary.

**Input:**
```
sample_dict = {
    "key1": {
        "value1": 10,
        "value2": 20
    },
    "key2": {
        "value3": 40
    },
}
```

**Answer:**
def findMaxValue(dict):
    max_val = None
    for key, value in dict.items():
        if isinstance(value, dict):
            max_val = max(findMaxValue(value), max_val)
        else:
            max_val = max(value, max_val)
    return max_val

print(findMaxValue(sample_dict))

---

## Q58: Write a function in Python that returns an object of the following time and date: Sunday March 7 5:30 PM.

**Answer:**
from datetime import datetime

def get_date_time():
    dt = datetime(year=2021, month=3, day=7, hour=17, minute=30)
    return dt

date_time = get_date_time()
print(date_time) # will output 2021-03-07 17:30:00

---

## Q59: Generate a Python program to perform matrix multiplication on two given matrices.

**Answer:**
def matrix_multiplication(A, B):  
    rows_A = len(A)  
    cols_A = len(A[0])  
    rows_B = len(B)  
    cols_B = len(B[0])  
    result = [[0 for i in range(cols_B)] for j in range(rows_A)]  
    for i in range(rows_A): 
        for j in range(cols_B): 
            for k in range(cols_A): 
                result[i][j] += A[i][k] * B[k][j] 
    return result

---

## Q60: Write a Python script to read an array from the user and then determine the mean and median of the array.

**Input:**
```
arr = [10, 15, 20, 25, 30, 35]
```

**Answer:**
def mean_median(arr): 
      arr_sum = 0 
      for i in range(len(arr)): 
            arr_sum += arr[i] 
      
      mean = arr_sum/len(arr) 
    
      arr = sorted(arr) 
      if len(arr) % 2 != 0: 
            median = arr[floor(len(arr)/2)] 
      else: 
            median = (arr[len(arr)//2] + arr[len(arr)//2 - 1]) / 2
      
      return mean, median

mean, median = mean_median(arr) 
print("Mean =", mean) 
print("Median =", median)

---

## Q61: Create an algorithm in Python to check whether an array has even or odd number of elements.

**Input:**
```
[1, 2, 3, 4]
```

**Answer:**
def is_array_even(arr): 
  if len(arr)%2 == 0:
    return True
  else:
    return False

---

## Q62: Implement a Python function to calculate the Gini coefficient of a given dataset.

**Input:**
```
[2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,21]
```

**Answer:**
def gini(x):
    """Calculate Gini Coefficient of a given dataset."""
    # calculate the frequency of each item in x
    x_value_counts = x.value_counts().sort_index() 

    # calculate the cumulative sum of x_value_counts
    x_cum_sum = x_value_counts.cumsum()

    # calculate the Lorenz values
    n = len(x)
    lorenz = x_cum_sum / n
    lorenz = np.insert(lorenz, 0, 0) # add 0 to the beginning of array

    # calculate the Gini Coefficient
    width = lorenz[:-1] - lorenz[1:]
    gini_coef = (1 / n) * sum(width * (lorenz[1:] + lorenz[:-1]))

    return gini_coef

if __name__ == '__main__':
    x = np.array([2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,21])
    gini_coef = gini(x)
    print(gini_coef) # should print 0.605

---

## Q63: Generate a neural network model with TensorFlow and Python for classifying hand-written digits from the MNIST dataset.

**Input:**
```
Not applicable
```

**Answer:**
import tensorflow as tf

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data", one_hot=True)

# Parameters
learning_rate = 0.001
training_epochs = 15
batch_size = 100
display_step = 1

# Network Parameters
n_hidden_1 = 256 # 1st layer number of neurons
n_hidden_2 = 256 # 2nd layer number of neurons
n_input = 784 # MNIST data input (img shape: 28*28)
n_classes = 10 # MNIST total classes (0-9 digits)

# tf Graph input
X = tf.placeholder("float", [None, n_input])
Y = tf.placeholder("float", [None, n_classes])

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_

---

## Q64: Write a function to generate a prime number sequence using Python.

**Answer:**
def generate_prime_numbers(n): 
        primes = [True for i in range(n+ 1)] 
        p = 2
        while (p * p <= n): 
            if (primes[p] == True): 
                for i in range(p * p, n + 1, p): 
                    primes[i] = False
            p += 1
        primes[0] = False
        primes[1] = False
        for p in range(n + 1): 
            if primes[p]: 
                print(p)

---

## Q65: Write a Python program that removes duplicates from a list.

**Input:**
```
Input List: [1, 2, 3, 4, 3, 2, 1]
```

**Answer:**
def remove_duplicates(my_list):
 return list(dict.fromkeys(my_list))

my_list = [1, 2, 3, 4, 3, 2, 1]

print(remove_duplicates(my_list)) # output [1, 2, 3, 4]

---

## Q66: Generate a Python script to sort the given list of words.

**Input:**
```
['bubble', 'selection', 'quicksort', 'insertion']
```

**Answer:**
# function to sort the given list of words
def sort_words(words):
    # sort the list of words in alphabetical order
    words.sort()

    # print the sorted list of words
    print(words)

# driver code
words = ['bubble', 'selection', 'quicksort', 'insertion']
sort_words(words)

# output
['bubble', 'insertion', 'quicksort', 'selection']

---

## Q67: Generate a function for calculating the average of a list of numbers in Python.

**Input:**
```
Not applicable
```

**Answer:**
def avg_list(lst):
 sum = 0
 count = 0
 for i in lst:
  sum += i
  count += 1
 avg = sum / count
 return avg

---

## Q68: Generate a Python program that compares two binary trees to check if they are similar.

**Answer:**
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def are_similar(root1, root2):
    if root1 is None and root2 is None:
        return True
    if (root1 and root2) is None or (root1 or root2) is None:
        return False
    if root1.val != root2.val:
        return False
    else:
        return are_similar(root1.left, root2.left) and are_similar(root1.right, root2.right)

---

## Q69: Create a program for solving a quadratic equation in Python.

**Input:**
```
Equation: x2 + 3x - 4 = 0
```

**Answer:**
import math
  
def solveQuadratic(a, b, c): 
    discriminant = (b**2) - (4*a*c);
    
    # If discriminant is negative there are no real roots.
    if (discriminant < 0): 
        return {
            "status": false,
            "roots": []
        }
    # If discriminant is zero, there is only one real roots.
    elif (discriminant == 0):
        x = -b/(2*a)
        return {
            "status": true,
            "roots": [x]
        }
    # Otherwise there are 2 real roots 
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2*a); 
        x2 = (-b - math.sqrt(discriminant)) / (2*a); 
        return {
            "status": true,
            "roots": [x1, x2]
        }

a = 1
b = 3
c = -4

print(solveQuadratic(a, b, c)) #{'status': True, 'roots': [-4.0, 1.0]}

---

## Q70: Construct a Python code for adding two matrices.

**Answer:**
def add_matrix(matrix1, matrix2):
    if len(matrix1) != len(matrix2):
        return 'Matrices not compatible'
    if len(matrix1[0]) != len(matrix2[0]):
        return 'Matrices not compatible'
    
    rows = len(matrix1)
    cols = len(matrix1[0])
    result = [[sum(row) for row in zip(*size)] for size in zip(matrix1, matrix2)]
    
    return result

---

## Q71: Generate a Python program which takes a string as input and prints all of its substrings in order from longest to shorte

**Answer:**
def substring_in_order(string): 
    result = [] 
    n = len(string) 
    for l in range(n, 0, -1): 
        for i in range(n-l + 1): 
            result.append(string[i:i+l]) 
    return result 

string = input("Enter the string: ") 
print ("All substrings in order from longest to shortest:") 
print (substring_in_order(string))

---

## Q72: Generate a Python function which takes an array and a value and returns the index at which this value is present in the 

**Input:**
```
arr = [2, 5, 9, 15], x = 5
```

**Answer:**
def find_index(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

print(find_index(arr, x))

---

## Q73: Develop a Python program to find the common elements in two lists.

**Input:**
```
List 1: [3, 9, 15, 21, 27]
List 2: [21, 7, 13, 29, 31]
```

**Answer:**
common_elements = [] 
  
# using loop 
for i in [3, 9, 15, 21, 27]:  
    for j in [21, 7, 13, 29, 31]:  
        if i == j: 
            common_elements.append(i) 
  
# printing common elements 
print(common_elements) 
# Output: [21]

---

## Q74: Create a Python program that takes in two strings and returns an integer indicating the number of common substrings betw

**Input:**
```
s1 = "abcd", s2 = "bae"
```

**Answer:**
def num_common_substrings(s1, s2):
    count = 0
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                count += 1
    return count

result = num_common_substrings("abcd", "bae")
print(result)

---

## Q75: Generate a Python program to convert a string to its lowercase version.

**Answer:**
def str_to_lower(string):
    new_string = ""

    for char in string:
        new_string += char.lower()

    return new_string

---

## Q76: Can you generate a function in Python that shuffles a given list?

**Answer:**
import random

def shuffle_list(list): 
    # Initialize the random number generator
    random.seed()

    # Shuffle the list
    random.shuffle(list) 

    # Return the list
    return list

---

## Q77: Write a Python function to validate an a list of emails. The function should return a boolean indicating whether a given

**Input:**
```
mail_list = ["example.user@gmail.com", "bad@example"]
```

**Answer:**
def validate_mail_list(mail_list):
    for mail in mail_list:
        if not re.match("[^@]+@[^@]+\.[^@]+", mail):
            return False
    return True

---

## Q78: Create a Python script that will perform several simple math operations. The script should accept two integers as inputs

**Input:**
```
int1 = 10
int2 = 5
```

**Answer:**
int1 = 10
int2 = 5

addition = int1 + int2
print('Addition:', addition)

subtraction = int1 - int2
print('Subtraction:', subtraction)

multiplication = int1 * int2
print('Multiplication:', multiplication)

division = int1 / int2
print('Division:', division)

modulo = int1 % int2
print('Modulo:', modulo)

---

## Q79: Create a Python program to perform sentiment analysis on product reviews. The program should use natural language proces

**Input:**
```
Not applicable
```

**Answer:**
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# Read in the data
data = pd.read_csv('reviews.csv')

# Tokenise the texts
data['tokenised'] = data['review'].apply(word_tokenize)

# Remove stopwords
stop_words = set(stopwords.words('english'))
data['filtered'] = data['tokenised'].apply(lambda x: [val for val in x if val not in stop_words])

# Normalize words
wordnet_lemmatizer = WordNetLemmatizer()
data['normalised'] = data['filtered'].

---

## Q80: Write a python program to clean up a list of emails and put them into a new list.

**Input:**
```
The original list of emails:
['bob@example.com', 'alice+bob@cafe.com', 'bob@gmail.com.uk', 'bob+alice@example']
```

**Answer:**
original_list = ['bob@example.com', 'alice+bob@cafe.com', 'bob@gmail.com.uk', 'bob+alice@example']

clean_list = []

for email in original_list:
 email_without_plus = email.split('+')[0]
 email_without_dot_uk = email_without_plus.split('.uk')[0]
 clean_list.append(email_without_dot_uk)

print(clean_list) # prints ['bob@example.com', 'alice@cafe.com', 'bob@gmail.com', 'bob@example']

---

## Q81: Generate sample data for a web application using Python's faker library. The output should contain three columns of data

**Input:**
```
Not applicable
```

**Answer:**
from faker import Faker

fake = Faker()
for _ in range(10):
 print(fake.name(), fake.email(), fake.random_int(min=18, max=60))

---

## Q82: Create a Python algorithm to classify positive and negative sentiment in tweets.

**Answer:**
def sentiment_analysis(tweets):
    # Initialize a list to store the result 
    results = [] 

    # Iterate through each tweet
    for tweet in tweets:
        # Clean the tweet 
        tweet = preprocessing(tweet)

        # Vectorize the tweet and obtain the prediction 
        tweet_vector = vectorize(tweet)
        prediction = predict_sentiment(tweet_vector)

        # Append the prediction to the result list
        if prediction == 1:
            results.append("Positive")
        elif preduction == 0:
            results.append("Negative")

    return results

---

## Q83: Parse the given URL and print out the protocol, domain name, and path using Python.

**Input:**
```
https://www.example.com/path/to/file
```

**Answer:**
import urllib.parse

url = 'https://www.example.com/path/to/file'
parsed_url = urllib.parse.urlparse(url)

# Get the protocol
protocol = parsed_url.scheme

# Get the domain name
domain_name = parsed_url.netloc

# Get the path
path = parsed_url.path

# Print the results
print('Protocol:', protocol)
print('Domain name:', domain_name)
print('Path:', path)

# Output:
# Protocol: https
# Domain name: www.example.com
# Path: /path/to/file

---

## Q84: Write a recursive Python function to generate Fibonacci numbers.

**Answer:**
def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
 
print(fibonacci(10))

---

## Q85: Create a Kubernetes pod setup that publishes a tweet every 5 minutes.

**Input:**
```
Not applicable
```

**Answer:**
apiVersion: v1
kind: Pod
metadata:
  name: tweet-publisher
spec:
  containers:
    - name: tweet-publisher
      image: <INSERT_PUBLIC_PULLABLE_IMAGE_PATH_HERE>
      command:
        - sh
        - -c
        - 'crontab -lcrontab && while true; do python publish-tweet.py && crontab -l | { cat; echo "*/5 * * * * python publish-tweet.py"; } | crontab -; sleep 31622400; done'
      volumeMounts:
        - mountPath: /crontab/crontab
          subPath: crontab
          name: cronmount
  volumes:
    - name: cronmount
      configMap:
        name: tweet-cron
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: tweet-cron
data:
  crontab: "* * * * * python publish-tweet.py"

---

## Q86: Write a code to generate a two-dimensional array with zeros shapes in Python

**Input:**
```
Row = 3, Column = 3
```

**Answer:**
"""
Write a code to generate a two-dimensional array with zeros shapes in Python
"""

def generate_zeros_array(row,col):
    return [[0] * col for _ in range(row)]

# Example
row = 3
col = 3

array = generate_zeros_array(row, col)
print(array)
# Output: [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

---

## Q87: Write a Python code to create a dictionary which contains a data structrue in the form of [x:x^2] where x is the key and

**Input:**
```
numbers = [1, 2, 3, 4, 5]
```

**Answer:**
numbers = [1, 2, 3, 4, 5] 

dict_numbers = {num: num**2 for num in numbers}
print(dict_numbers)

---

## Q88: Create a Python script to print the numbers from 1 to 50, but for multiples of 3 print "Fizz" instead of the number, for

**Input:**
```
Not applicable
```

**Answer:**
for i in range(1, 51):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

---

## Q89: Create a Python program to calculate the square root of a user-defined positive number.

**Input:**
```
n = 100
```

**Answer:**
import math

n = 100

#Calculate the square root of a number
square_root = math.sqrt(n)

print(f'Square root of {n} is {square_root}')

---

## Q90: Create a Python class called Rectangle to represent a two-dimensional rectangle with a length and width.

**Answer:**
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

---

## Q91: Create a data visualization dashboard in Python using Matplotlib.

**Answer:**
import matplotlib
import matplotlib.pyplot as plt

# Generate the data for the dashboard
x = [1,2,3,4,5]
y = [10,25,30,50,80]

# Create the figure and set the size
fig = plt.figure(figsize=(10,6))

# Configure the plot
plt.plot(x, y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)
plt.title("My Data Visualization Dashboard")
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Show the plot
plt.show()

---

## Q92: Edit the following python code to prompt the user to enter the value of radius to calculate the area of a circle.

**Answer:**
# Calculate area of a circle

Pi = 3.14

# Get radius from user
radius = float(input("Please enter the radius of the circle: "))

# Calculate the circle area
area = Pi*radius**2

# Print the area
print("The area of the circle is:", area)

---

## Q93: Create a Python algorithm to identify the longest word in a sentence.

**Input:**
```
“The rain in Spain stays mainly in the plain.”
```

**Answer:**
def find_longest_word(sentence):
    words = sentence.split()
    # initialise longest_word variable with 0
    longest_word = 0
    for word in words:
        if len(word) > longest_word:
            longest_word = len(word)
            longest_word_str = word
    return longest_word_str

---

## Q94: Write a Python script that can convert degrees Fahrenheit to degrees Celsius.

**Answer:**
def FahrenheitToCelsius(temp_fahrenheit):
    temp_celsius = (temp_fahrenheit - 32) * 5/9
    return temp_celsius

---

## Q95: Generate a Python function that checks if a given number is an Armstrong number.

**Answer:**
def is_armstrong_number(num):   
    n = len(str(num)) 
    # initialize sum  
    temp = num  
    sum_of_digits = 0
  
    # find sum of nth power of individual digits  
    while temp > 0:  
        digit = temp % 10  
        sum_of_digits += digit ** n  
        temp //= 10  
  
    # if num is equal to sum_of_digits then the number is an Armstrong number  
    if num == sum_of_digits:  
        return True 
  
    else: 
        return False

---

## Q96: Write a code in Python to print the following pattern:

**Answer:**
for i in range(5):
    for j in range(i+1):
        print("*", end="")
    print("")

for i in range(5, 0, -1):
    for j in range(i):
        print("*", end="")
    print("")

---

## Q97: Program a web scraper in Python to extract the latest stock prices from specific websites.

**Input:**
```
["AAPL stocks", "MSFT stocks", "FB stocks", "GOOG stocks"]
```

**Answer:**
import requests
from bs4 import BeautifulSoup

# input
stocks = ["AAPL stocks", "MSFT stocks", "FB stocks", "GOOG stocks"]

# process
def get_stock_price(stock):
    url = f"https://finance.yahoo.com/quote/{stock}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    return price

# output
for stock in stocks:
    price = get_stock_price(stock)
    print(f'The price of {stock} is {price}.')

---

## Q98: The code provides Python wrappers around TensorFlow ops for decoding LibSVM input to tensors. To use it, call the `decod

**Answer:**
"""Python wrappers around TensorFlow ops.

This file is MACHINE GENERATED! Do not edit.
Original C++ source file: libsvm_ops.cc
"""

import collections as _collections
import six as _six

from tensorflow.python import pywrap_tensorflow as _pywrap_tensorflow
from tensorflow.python.eager import context as _context
from tensorflow.python.eager import core as _core
from tensorflow.python.eager import execute as _execute
from tensorflow.python.framework import dtypes as _dtypes
from tensorflow.python.framework import errors as _errors
from tensorflow.python.framework import tensor_shape as _tensor_shape

from tensorflow.core.framework import op_def_pb2 as _op_def_pb2
# Needed to trigger the call to _set_call_cpp_shape_fn.
from tensorflow.python.framework import common_shapes as _common_shapes
f

---

## Q99: Write a Python program to compute the sum of the values of a given dictionary

**Input:**
```
dictionary = {'A':5, 'B':6, 'C':10}
```

**Answer:**
def dict_sum(dict):
    sum = 0
    for key, value in dict.items():
        sum += value
    return sum

---

## Q100: Create a REST API in Python that can be used to delete an item from a list.

**Input:**
```
Not applicable
```

**Answer:**
from flask import Flask, request
import json

app = Flask(__name__)
items = ["Apple", "Banana", "Orange"]

@app.route('/items', methods=["GET"])
def get_items():
 return json.dumps(items)

@app.route('/items/<item>', methods=["DELETE"])
def delete_item(item):
 if item in items:
  items.remove(item)
  message = "Item successfully deleted."
 else:
  message = "Item not found."
 return json.dumps({"message": message})

---

## Q101: Read a given list of strings and create a new list of all strings that are longer than 5 characters long.

**Input:**
```
['Python', 'is', 'Fun']
```

**Answer:**
def filter_long_strings(string_list):
 long_strings = []
 for string in string_list:
 if len(string) > 5:
 long_strings.append(string)
 return long_strings

string_list = ['Python', 'is', 'Fun']

long_strings = filter_long_strings(string_list)
print(long_strings)

---

## Q102: Craft an algorithm in Python to move all zeroes in a list to the end of the list.

**Input:**
```
[3, 0, 1, 0, 5, 0, 2]
```

**Answer:**
def move_zeroes(lst):
    # Count the number of non-zero elements
    num_non_zeroes = 0
    for num in lst:
        if num != 0:
            num_non_zeroes += 1
  
    # Initialize the new list
    new_lst = []
  
    # Move all non-zeroes to the beginning of the new list
    for i in range(num_non_zeroes):
        new_lst.append(lst[i])
  
    # Append 0's to the end
    for _ in range(len(lst)-num_non_zeroes):
        new_lst.append(0)
  
    # Return the new list
    return new_lst

lst = [3, 0, 1, 0, 5, 0, 2]
result = move_zeroes(lst)
print(result)

---

## Q103: Create a Python program to implement the Fibonacci sequence.

**Answer:**
def fibonacci_seq(n): 
    if n==0: 
        return 0
    elif n==1: 
        return 1
    else: 
        return fibonacci_seq(n-1)+fibonacci_seq(n-2)

---

## Q104: Write a function in Python to print out an array backwards.

**Answer:**
def print_reverse_array(arr):
 for i in range(len(arr)-1, -1, -1): 
  print(arr[i])

---

## Q105: Create a Python program to find the possible prime numbers from one to one hundred by using the Sieve of Eratosthenes al

**Answer:**
def sieve_eratosthenes(n): 
    prime_list = [True] * (n+1) 
    prime_list[0] = False
    prime_list[1] = False
    primes = [] 
      
    for i in range(2, n+1): 
        if prime_list[i] == True: 
            primes.append(i) 
            for j in range(i*i, n+1, i): 
                prime_list[j] = False
    return primes 
  
n = 100
print("The Prime numbers from 1 to 100 are:")
print(sieve_eratosthenes(n))

---

## Q106: Create a Python function named "Transpile" that takes in four arguments: "src_dir", "dst_dir", "model_filename", and "pa

**Answer:**
import os
import sys
import argparse
import paddle.fluid as fluid


def Transpile(src_dir, dst_dir, model_filename, params_filename):
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)

    inference_scope = fluid.core.Scope()
    with fluid.scope_guard(inference_scope):
        print "Loading inference_program from ", src_dir
        [inference_program, feed_target_names,
         fetch_targets] = fluid.io.load_inference_model(src_dir, exe, model_filename, params_filename)

        inference_transpiler_program = inference_program.clone()
        # NOTE: Applying the inference transpiler will change the inference_transpiler_program.
        t = fluid.InferenceTranspiler()
        # Under the with statement, inference_scope is the global scope.
        t.transpile(inference_transp

---

## Q107: Create a Python function called add_marks which takes two parameters: marks(a list) and mark(an integer). The function s

**Input:**
```
marks = [87, 56, 99, 54]
mark = 4
```

**Answer:**
def add_marks(marks, mark):
 return [m + mark for m in marks]

---

## Q108: Design a positive feedback loop for the following python program.

**Input:**
```
for i in range(10):
    print("hello")
```

**Answer:**
for i in range(10):
    print("hello")
    i += 1
    if i == 10:
        print("You've got it!")

---

## Q109: Implement a function that prints out the numbers from 1 to 50 in python

**Answer:**
def print_numbers():
    for i in range(1, 51):
        print(i)

print_numbers()

---

## Q110: Write a Python program to send an automated email. The program should take a list of emails as input, iterate over the l

**Input:**
```
recipient_emails = ["email1@example.com","email2@example.com"]
```

**Answer:**
import smtplib

sender_email = 'example@gmail.com'
password = 'example_password'

for email in recipient_emails:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)

        subject = 'Automated Email from Program'
        message = 'Message body'
 
        server.sendmail(sender_email, email, 'Subject: ' + subject + '\n\n' + message)
        server.quit()
        print('Email sent successfully.')

---

## Q111: Create a Python class which represents a 3D Vector

**Answer:**
class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

---

## Q112: Given two strings, write a Python program to find the total number of common characters present in both strings

**Answer:**
def num_common_chars(str1, str2):
    common = 0
    for c in str1:
        if c in str2:
            common += 1
    return common

---

## Q113: Modify the following Python code to handle errors.

**Input:**
```
def read_data_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data
```

**Answer:**
def read_data_from_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("The file specified does not exist.")
    except json.decoder.JSONDecodeError:
        print("The file specified is not in a valid JSON format.")

---

## Q114: Analyze a given Python code and write a function that checks if a given number is prime.

**Input:**
```
def primeCheck(num):
```

**Answer:**
def primeCheck(num):
 if num > 1:
 for i in range(2, num):
  if (num % i) == 0:
   return False
 else:
  return False
 return True

---

## Q115: Create a python program to filter out all the even numbers from a given list.

**Input:**
```
[3, 4, 5, 6, 7]
```

**Answer:**
def filter_even_numbers(numbers):
    even_numbers = []
    for i in numbers:
        if i % 2 == 0:
            even_numbers.append(i)
    return even_numbers
    
    
filtered = filter_even_numbers([3, 4, 5, 6, 7])
print(filtered)

---

## Q116: Implement a function in Python that takes a Huffman tree and drop all its leaf nodes.

**Input:**
```
(1)
      /      \
    (2)      (3)
    / \      / \
  (4) (5)  (6) (7)
```

**Answer:**
def dropLeafNodes(head): 
    
    # If node is not None and doesn't have any children 
    if head and not head.left and not head.right: 
        return None
  
    # Don't change anything if head is None 
    if not head: 
        return None
  
    # Recursively call dropLeafNodes on left and right subtrees
    head.left = dropLeafNodes(head.left) 
    head.right = dropLeafNodes(head.right) 
  
    # Return head of the modified tree
    return head

---

## Q117: Create a web crawler in Python that starts from a website and looks for other links in the page then scrapes the page co

**Input:**
```
Not applicable
```

**Answer:**
import requests
from bs4 import BeautifulSoup
import re

def crawl(url):
 visited = set()
 queue = [url] 
 
 while queue:
 curr = queue.pop(0)
 visited.add(curr) 
 response = requests.get(curr)
 
 if response.ok:
 soup = BeautifulSoup(response.text, 'html.parser')

# scrape the page here 

# find all the links
 links = soup.find_all('a', href=re.compile('^http')) 
 
 for link in links:
 if link['href'] not in visited:
 queue.append(link['href'])

---

## Q118: Write a Python program to calculate the maximum, minimum and mean number of elements in a given string.

**Answer:**
def get_stats_for_string(string):
    num_elements = len(string)
    max_element = max(string)
    min_element = min(string)
    mean_element = sum(string) / num_elements
    return (max_element, min_element, mean_element)

string = "abcdef"
stats_for_string = get_stats_for_string(string)
print("Max: {0}, Min: {1}, Mean: {2}".format(*stats_for_string))

---

## Q119: Write a Python program to calculate the compound interest.

**Input:**
```
investment_amount = 1000, time = 5, rate_of_interest = 5
```

**Answer:**
def compoundInterest(investment_amount, rate_of_interest, time):
    compound_interest = investment_amount * (pow((1 + rate_of_interest / 100), time))
    return compound_interest

ci = compoundInterest(1000, 5, 5)
print(ci)

---

## Q120: Create a command-line application in Python that stores customer data and allows customer to query by customer name

**Answer:**
import sys 
  
def print_customer_data(name): 
    # Code for searching customer data by customer name and 
    # printing results 
    ...

# Main function for the customer search application
if __name__=="__main__": 
    # Get command line arguments 
    args = sys.argv 
    
    if len(args) == 2: 
        name = args[1]
        print_customer_data(name) 
    else: 
        print("Invalid arguments, please specify a customer name.")

---

## Q121: Develop a program in Python to calculate the Fibonacci sequence.

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

# Driver Code 
print(fibonacci(9))

---

## Q122: Generate a python program that takes two sets of integers as input and outputs the intersection of those sets.

**Input:**
```
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
```

**Answer:**
def intersection(set1, set2): 
   return set1 & set2

result = intersection(set1, set2) 
print(result)

---

## Q123: Design an algorithm in Python to find the smallest number in a given list.

**Input:**
```
[4, 5, 6, 7, 8]
```

**Answer:**
def smallestNumber(nums):
    smallest = nums[0]
    for i in range(1, len(nums)):
        if nums[i] < smallest:
            smallest = nums[i]
    return smallest

nums = [4, 5, 6, 7, 8]
smallestNum = smallestNumber(nums)
print('The smallest number is', smallestNum)

---

## Q124: Generate a python program for printing a Pascal triangle.

**Input:**
```
Number of rows= 5
```

**Answer:**
def PascalTriangle(n) : 
      
    # An auxiliary array to store 
    # generated pscal triangle values 
    arr = [0 for i in range(n)] 
      
    # Iterate through every line and 
    # print integer(s) in it 
    for line in range(0, n) : 
          
        # Every line has number of  
        # integers equal to line  
        # number 
        for i in range (0, line + 1) : 
              
            # First and last values  
            # in every row are 1 
            if (i == 0 or i == line) : 
                arr[i] = 1
                  
            # Other values are sum of  
            # values just above and  
            # left of above 
            else : 
                arr[i] = arr[i] + arr[i - 1]  
              
        # Printing array in 
        # mantainence o

---

## Q125: Create a python script that filters out all negative numbers from the given matrix

**Input:**
```
[[-1, 2, -3], [-4, 5, 6], [-7, 8, 9]]
```

**Answer:**
import numpy as np

def filter_out_negative(matrix):
  # Convert matrix to numpy array
  matrix = np.array(matrix)
  # Find all negative numbers and set them to 0
  matrix[matrix < 0] = 0
  return matrix

result = filter_out_negative([[-1, 2, -3], [-4, 5, 6], [-7, 8, 9]])
print(result)

---

## Q126: Create a basic REST API using Python and Flask to list all the countries in the world.

**Input:**
```
Not applicable
```

**Answer:**
import flask
from flask import Flask, request, jsonify
import json

app = Flask(name)

@app.route('/countries', methods=['GET'])
def get_countries():
with open('data.json', 'r') as f:
 countries = json.load(f)
 return jsonify(countries)

if name == 'main':
 app.run()

---

## Q127: Create a web scraper in Python that can extract hotel reviews from TripAdvisor.

**Input:**
```
Not applicable
```

**Answer:**
import requests
from bs4 import BeautifulSoup

# Define the URL and the headers
url = '<url>'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

# Make a request and get HTML in response
response = requests.get(url, headers=headers)

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all reviews
reviews = soup.find_all('div', {'class': 'review-container'})

# Go through every review and extract the data
for review in reviews:
    # Get the title
    title = review.find('span', {'class': 'noQuotes'}).text

    # Get the text
    text = review.find('p', {'class': 'partial_entry'}).text

    # Print for demo
    print(title)
    print(text)
    print('-' * 50)

---

## Q128: Develop a machine learning model in Python to identify the author of a given article.

**Answer:**
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# load data
samples = [
  "sample 1 from AuthorA",
  "sample 2 from AuthorA",
  "sample 1 from AuthorB",
  "sample 2 from AuthorB"
]
labels = [
  "AuthorA",
  "AuthorA",
  "AuthorB",
  "AuthorB"
]

# build the model
model = Pipeline([
  ('tfidf', TfidfVectorizer()),
  ('clf', GaussianNB())
])

# train the model
X_train, X_test, y_train, y_test = train_test_split(samples, labels, test_size=0.3)
model.fit(X_train, y_train)

# evalulate the model
score = model.score(X_test, y_test)
print(f'model score: {score}')

---

## Q129: Write a Python program to divide a given list of numbers into two equal parts such that the difference between the sum o

**Input:**
```
[2, 3, 4, 5, 6, 7]
```

**Answer:**
def divide_in_two_equal_parts(lst):
    target = sum(lst) // 2
    part1 = []
    part2 = []
    left_sum = 0
    right_sum = 0
    
    for num in lst:
        if left_sum <= right_sum:
            left_sum += num
            part1.append(num)
        else:
            right_sum += num
            part2.append(num)
         
    return part1, part2

part1, part2 = divide_in_two_equal_parts([2, 3, 4, 5, 6, 7])

print("Part 1:", part1)
print("Part 2:", part2)

---

## Q130: Develop an algorithm to detect and fix Python syntax errors in a given code snippet.

**Input:**
```
def test ():
    x = 5
    y = 3 
    z
```

**Answer:**
def test():
    x = 5
    y = 3
    try:
        z
    except NameError:
        print("NameError: Name 'z' is not defined")

---

## Q131: Design a data structure in Python to store integer values.

**Answer:**
class IntList:
    def __init__(self):
        self.values = []
   
    def add_value(self, value):
        self.values.append(value)
    
    def find_min(self):
        return min(self.values)

---

## Q132: Create an algorithm in Python for a linear search. The algorithm should take in an array and a value to search for, and 

**Input:**
```
Array: [5, 3, 7, 2]
Search value: 7
```

**Answer:**
def linearSearch(arr, value):
  for i in range(len(arr)):
    if arr[i] == value:
      return i  # value found, return index
  return -1  # value not found

arr = [5, 3, 7, 2]
searchValue = 7

result = linearSearch(arr, searchValue)

if result == -1:
  print("Element not found")
else:
  print("Element present at index", result)

---

## Q133: Given a list of strings, write a Python function to remove all the whitespaces from each string.

**Input:**
```
['Hello  World  ', 'Hi  there', 'Good  Morning']
```

**Answer:**
def remove_whitespace(word_list):
    return [word.strip() for word in word_list]

stripped_list = remove_whitespace(['Hello  World  ', 'Hi  there', 'Good  Morning'])
print(stripped_list)

---

## Q134: Design a Python program to randomize a list of given integers using an optimized Fisher-Yates algorithm.

**Answer:**
def randomized_list(num_list):
    for i in range(len(num_list)-1,0,-1):
        j = random.randint(0,i)
        num_list[i],num_list[j] = num_list[j],num_list[i]
    return num_list

---

## Q135: Create a system in Python for generating natural language responses.

**Input:**
```
A sample utterance "What time is it?"
```

**Answer:**
from tensorflow.keras.layers import Input, Dense, Embedding, GRU
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model

# Create inputs
inputs1 = Input(shape=(20,))
x1 = Embedding(1000, 64)(inputs1)
x1 = GRU(128)(x1)

# Create outputs
y1 = Dense(1000, activation='softmax')(x1)

# Create model
model = Model(inputs=[inputs1], outputs=[y1])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit([inputs], [outputs],  epochs=10, batch_size=32)

# Generate the response to the sample utterance
query = "What time is it?"
prediction = model.predict(query)

print(prediction)

---

## Q136: Create a web scraper using Python that collects the title and content from the homepage of a given website.

**Input:**
```
https://www.example.com as the target website.
```

**Answer:**
import requests
import bs4

url = 'https://www.example.com'
r = requests.get(url)
html = bs4.BeautifulSoup(r.text,"html.parser")

# Find title
title = html.find('title')
print(title.text)

# Find content
content = html.find('div', {'class': 'content'})
print(content.text)

---

## Q137: Generate a Python script that finds the total surface area of a cuboid, given its three dimensions.

**Input:**
```
2, 3, 4
```

**Answer:**
def find_total_surfacearea(length, breadth, height):
   return (2*(length*breadth + breadth*height + height*length))

print(find_total_surfacearea(2, 3, 4))

Output: 52

---

## Q138: Generate a Python program to clean a string of HTML tags.

**Input:**
```
Example Input: "<p>This is a <b>test</b> string</p>".
```

**Answer:**
import re

# Clean a string of HTML tags 
def clean_html_tags(str):
    clean_str = re.sub("<.*?>", "", str)
    return clean_str

html_string = "<p>This is a <b>test</b> string</p>"

clean_str = clean_html_tags(html_string)

print(clean_str) #This is a test string

---

## Q139: Generate a Python function that takes an integer array as input and returns the number of unique elements in the array.

**Input:**
```
[1, 2, 3, 2, 1, 4, 7, 8, 9, 8]
```

**Answer:**
def num_unique_elements(arr):
    unique_arr = set(arr)
    return len(unique_arr)

print(num_unique_elements([1, 2, 3, 2, 1, 4, 7, 8, 9, 8]))

---

## Q140: Create a Python program to scrape an online news website to get the headlines.

**Answer:**
import requests
from bs4 import BeautifulSoup 

# url of the website you want to scrape 
url = "https://www.news.com/" 

# get the response in the form of html
r = requests.get(url) 

# create a beautifulsoup object to parse contents 
soup = BeautifulSoup(r.content, 'html5lib') 

# find headlines from the parsed page  
headlines = soup.find_all('h2') 

# Print the headlines 
for headline in headlines: 
    print(headline.text)

---

## Q141: Edit the given Python program to print 'Happy Holidays' 10 times.

**Input:**
```
for i in range(10):
    print('Hello World')
```

**Answer:**
for i in range(10):
    print('Happy Holidays')

---

## Q142: Combine 2 strings and reverse the result in Python.

**Input:**
```
words = "Hello "
words2 = "world!"
```

**Answer:**
words = "Hello "
words2 = "world!"

combined = words + words2
result = combined[::-1]

print(result)

---

## Q143: Create a class to represent a bank account in Python.

**Answer:**
class BankAccount:
    
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False
        
    def get_balance(self):
        return self.balance

---

## Q144: Optimize the following Python code to sort a set of numbers (set = [2, 6, 3, 8, 4]) in O(n) time complexity.

**Input:**
```
unsorted_list = [2, 6, 3, 8, 4]
```

**Answer:**
def sort_list(unsorted_list):
    sorted_list = []
    while unsorted_list:
        min_elem = min(unsorted_list)
        unsorted_list.remove(min_elem)
        sorted_list.append(min_elem)
    return sorted_list

---

## Q145: Design a Python program to perform linear regression for predicting the numbers in a given dataset.

**Input:**
```
X = [1,2,3,4,5]
Y = [3,5,7,9,13]
```

**Answer:**
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([1,2,3,4,5]).reshape(-1,1)
Y = np.array([3,5,7,9,13])

model = LinearRegression()
model.fit(X, Y)

# Predicts the value of y
print(model.predict([[7]]))

---

## Q146: Create a Python object that contains two attributes, "Name" and "Age".

**Answer:**
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("John", 25)

---

## Q147: Write a function in Python that takes a list of objects and returns a list of those objects sorted by one of their attri

**Input:**
```
[{"name": "Alice", "age": 20}, {"name": "Bob", "age": 21}]
```

**Answer:**
def sort_by_attr(objects, attr):
 return sorted(objects, key=lambda item: item[attr])
 
sort_by_attr([{"name": "Alice", "age": 20}, {"name": "Bob", "age": 21}], "age")

---

## Q148: Write a Python program to generate an HTML table displaying information about the top 10 bestselling books in a specific

**Input:**
```
Table name: Books
Table columns: id (int), title (string), author (string), genre (string), sales (int)
```

**Answer:**
import sqlite3

# connect to the database
conn = sqlite3.connect('books.db')
c = conn.cursor()

# retrieve the data
c.execute('''SELECT title, author, genre, sales
FROM Books
WHERE genre='Fantasy'
ORDER BY sales DESC
LIMIT 10''')

# save the results
results = c.fetchall()

# generate the HTML code
html = '<table>'
html += '<tr><th>Title</th><th>Author</th><th>Genre</th><th>Sales</th></tr>'

for result in results:
 title = result[0]
 author = result[1]
 genre = result[2]
 sales = result[3]

 html += f'<tr><td>{title}</td><td>{author}</td><td>{genre}</td><td>{sales}</td></tr>'

html += '</table>'

# display the results
print(html)

---

## Q149: Create a Python script to filter out all the vowels from a string.

**Answer:**
def filter_vowels(string):
     vowels = ('a', 'e', 'i', 'o', 'u')
     return ''.join(c for c in string if c not in vowels)

---

## Q150: In Python, write a script to sort the list items in descending order.

**Input:**
```
list_items = [3, 7, 5, 8, 10]
```

**Answer:**
list_items = [3, 7, 5, 8, 10]

list_items.sort(reverse=True)

print(list_items) # Output: [10, 8, 7, 5, 3]

---

## Q151: Create a Python function that takes in a text string and returns a dictionary of words and the number of times each word

**Input:**
```
A quick brown fox jumps over the lazy dog
```

**Answer:**
def words_count(text):
 words_dict = {}
 for word in text.split(' '):
 if word in words_dict:
 words_dict[word] += 1
 else:
 words_dict[word] = 1
 return words_dict

words_dict = words_count("A quick brown fox jumps over the lazy dog")
print(words_dict)

---

## Q152: Create an object-oriented structure to solve a maze by using python.

**Answer:**
import collections

class Maze:
    def __init__(self, n, m):
        self._n, self._m = n, m
        self._grid = [[None] * m for _ in range(n)]

    def solve_maze(self):
        result, found = [], False
        start, end = (0, 0), (self._n-1, self._m-1)

        for i in range(self._n):
            for j in range(self._m):
                if self._grid[i][j] == 1:
                    value = 0
                    self._find_omega(i, j, value, result, start, end,
                                     found)
                    return result

    def _find_omega(self, i, j, value,
                    result, start, end, found):
        rowNbr, colNbr = [-1, 0, 0, 1], [0, -1, 1, 0]

        if (i, j) == end:
            found = True
            result.append(value)
            return

   

---

## Q153: Compose a piece of code to print the length of a given string.

**Input:**
```
"Python"
```

**Answer:**
string = "Python"
print("Length of the given string is:", len(string))

---

## Q154: Compose a Python program to calculate the maximum possible revenue from the items with given weights and values.

**Input:**
```
weights = [2, 1, 3], values = [4, 2, 3]
```

**Answer:**
"""
Calculate the maximum possible revenue from the items with given weights and values
"""

# given  weights and values 
weights = [2, 1, 3] 
values = [4, 2, 3] 

# number of items 
n = len(weights) 
  
# function to calculate the maximum revenue 
def knapsack(weights, values, n): 
  
    # total capacity of knapsack 
    W = 5
  
    # matrix to store solution matrix 
    K = [[0 for x in range(W+1)] for x in range(n+1)] 
  
    # build the solution matrix in bottom up manner 
    for i in range(n+1): 
        for w in range(W+1): 
            if i==0 or w==0: 
                K[i][w] = 0
            elif weights[i-1] <= w: 
                K[i][w] = max(values[i-1] + K[i-1][w-weights[i-1]],  K[i-1][w]) 
            else: 
                K[i][w] = K[i-1][w] 
  
    return K[n][W] 
  
pr

---

## Q155: Write a Python program to read in a tweet and remove all punctuation, special characters and stopwords.

**Input:**
```
"I'm so excited to be going to the #MuseumTour! #BigDay #travel"
```

**Answer:**
import re
import string
from nltk.corpus import stopwords

tweet = "I'm so excited to be going to the #MuseumTour! #BigDay #travel"
tweet_clean = re.sub(r'[^\w\s]','',tweet) #remove punctuation
tokens = tweet_clean.split() #split string into individual words 
stop_words = set(stopwords.words("english")) #get list of stopwords
filtered_tokens = [w for w in tokens if not w in stop_words] #remove stopwords
print(filtered_tokens)

---

## Q156: Implement a web scraper in Python to extract the top ten trending YouTube videos.

**Answer:**
import requests
from bs4 import BeautifulSoup

# make a request to get the page content
page = requests.get("https://www.youtube.com/feed/trending")

# parse the page content
soup = BeautifulSoup(page.content, 'html.parser')

# extract the list of trending videos
trending_videos = soup.find_all(class_='expanded-shelf-content-item-wrapper')

# print the top ten trending videos
for video in trending_videos[:10]:
    print(video.find(class_='yt-uix-tile-link').get('title'))

---

## Q157: Make a code in Python to find the mode of the given set of values.

**Input:**
```
1, 2, 3, 2, 4, 2
```

**Answer:**
def find_mode(list):
  max_count = 0
  mode = list[0]
  count = {}
  for item in list:
    if (item in count):
      count[item] += 1
    else:
      count[item] = 1
    if (count[item] > max_count):
      max_count = count[item]
      mode = item
  return mode

---

## Q158: Create a web API with Python and Flask to give the current date and time.

**Input:**
```
Not applicable
```

**Answer:**
from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/datetime')
def get_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    app.run()

---

## Q159: Create a Python function that takes a list containing fruit names and returns the most common fruit name.

**Input:**
```
['Apple', 'Orange', 'Apple', 'Pineapple', 'Grape', 'Apple']
```

**Answer:**
def most_common_fruit(fruit_list):
 
    # Dictionary to get count of each fruit
    freq_dict = {}
 
    # Count frequency of each fruit
    for fruit in fruit_list:
        if fruit in freq_dict:
            freq_dict[fruit] += 1
        else:
            freq_dict[fruit] = 1
 
    # Get maximum frequency 
    max_freq = 0
    for freq in freq_dict.values():
        if freq > max_freq:
            max_freq = freq
 
    # Get the most common fruit
    most_common_fruit = None
    for fruit, freq in freq_dict.items():
        if freq == max_freq:
            most_common_fruit = fruit
            break
 
    return most_common_fruit

---

## Q160: Write a Python program to take in a list of phrases and generate a string with the each phrase followed by its length.

**Input:**
```
phrases = ["A bird in the hand", "is worth two in the bush"]
```

**Answer:**
result = "A bird in the hand (17)is worth two in the bush (25)"
 
code:
input_phrases = ["A bird in the hand", "is worth two in the bush"]
 
result = ""
for phrase in input_phrases:
 result += phrase + ' (' + str(len(phrase)) + ')'
 
print(result)

---

## Q161: Write a simple Python function that takes a list of integers and returns the sum of all elements divisible by 3.

**Input:**
```
li = [4, 6, 17, 24, 5, 9]
```

**Answer:**
def divisibleBy3(li):
 total = 0
 for num in li:
  if num % 3 == 0:
   total += num
 return total
# Output: 24

---

## Q162: Create a program in Python that takes a number from the user and prints all the divisors of the number.

**Answer:**
divisors = []

num = int(input('Enter a number: '))
 
for i in range(1, num + 1):
    if num % i == 0:
        divisors.append(i)

print('The divisors of',num ,'are:')
print(*divisors, sep=', ')

---

## Q163: Write a Python program to generate an HTML page containing a table with some employee data.

**Input:**
```
Employee Data:
Name: John Doe
Job Title: Senior Developer
Department: IT
Salary: $120,000

Name: Jane Doe
Job Title: Manager
Department: Finance
Salary: $95,000

Name: Tim Smith
Job Title: Junior Developer
Department: IT
Salary: $55,000
```

**Answer:**
<html>
  <head>
    <title>Employee Data</title>
  </head>
  <body>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Job Title</th>
          <th>Department</th>
          <th>Salary</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>John Doe</td>
          <td>Senior Developer</td>
          <td>IT</td>
          <td>$120,000</td>
        </tr>
        <tr>
          <td>Jane Doe</td>
          <td>Manager</td>
          <td>Finance</td>
          <td>$95,000</td>
        </tr>
        <tr>
          <td>Tim Smith</td>
          <td>Junior Developer</td>
          <td>IT</td>
          <td>$55,000</td>
        </tr>
      </tbody>
    </table>
  </body>
</html>

---

## Q164: Create a Python function to select all rows from a table where the 'status' is 'approved'

**Answer:**
def select_approved_rows():
   sql = "SELECT * FROM table WHERE status = 'approved'"
   cur.execute(sql)
   return cur.fetchall()

---

## Q165: Create a Python program to generate random passwords of length 8 characters, containing at least one lowercase letter, o

**Answer:**
from random import choice
import string

def generate_password():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    password = ''.join(choice(chars) for i in range(8))
    if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password):
        return password
    else: 
        return generate_password()

if __name__ == '__main__':
    print(generate_password())

---

## Q166: Generate a solution to translate a text from English to French using Python.

**Answer:**
# install the module 
# in command prompt
pip install googletrans

# import module
from googletrans import Translator

# create an object
translator = Translator()

# define text
text = "Hello, this is a sample text to translate."

# call the function and pass the text
translation = translator.translate(text, dest='fr') 

# print the translation 
print(translation.text)

---

## Q167: Create a function to generate a unique 6 digit number.

**Answer:**
# Python program to generate 
# a unique 6 digit number 
import random 
def generate_number(): 
      
    # Choose a random number 
    # between 10000 and 99999 
    random_number = random.randint(10000, 99999) 
  
    # Return the random number 
    return random_number 
  
# Driver Code 
if __name__ == "__main__": 
    print(generate_number())

---

## Q168: Write a Python program to generate 10 random numbers and put them in a list.

**Answer:**
import random

random_list = []
for i in range(10):
 number = random.randint(1, 100)
 random_list.append(number)

---

## Q169: Write a Python program to replace all occurrences of a given string with an alternate string.

**Input:**
```
"Hello World!", "World", "Python"
```

**Answer:**
def replace_string(input_string, target_string, replacement_string):
    return input_string.replace(target_string, replacement_string)

print(replace_string("Hello World!", "World", "Python"))

---

## Q170: Generate a Python class for an online store item that includes fields for ID, name, price, and description.

**Input:**
```
Not applicable
```

**Answer:**
class StoreItem:
    def __init__(self, item_id, name, price, description):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.description = description

    def __str__(self):
        return f'{self.name}, ${self.price}'

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }

---

## Q171: Create a virtual assistant using Python and Dialogflow to answer a basic set of questions.

**Input:**
```
Not applicable
```

**Answer:**
import dialogflow_v2 as dialogflow
import requests

project_id = 'project-id'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(project_id, 'session-id')

while True:
 text = input('User: ')
 text_input = dialogflow.types.TextInput(text=text, language_code='en-US')
 query_input = dialogflow.types.QueryInput(text=text_input)
 response = session_client.detect_intent(session=session, query_input=query_input)

 print('Assistant:', response.query_result.fulfillment_text)

---

## Q172: Create an algorithm in Python to solve "Tower of Hanoi" game of a 4 disk problem.

**Answer:**
def solveTowerOfHanoi(num_disks, start_rod = 'A', end_rod = 'C', aux_rod = 'B'): 
    if num_disks == 1: 
        print("Move disk 1 from rod", start_rod, "to rod", end_rod) 
        return
    solveTowerOfHanoi(num_disks - 1, start_rod, aux_rod, end_rod) 
    print("Move disk", num_disks, "from rod", start_rod, "to rod", end_rod) 
    solveTowerOfHanoi(num_disks - 1, aux_rod, end_rod, start_rod) 
  
  
# Driver code 
num_disks = 4
solveTowerOfHanoi(num_disks)

---

## Q173: Generate an api response in Python for the provided data.

**Input:**
```
Data = {
"name" : "John",
"age" : 28
}
```

**Answer:**
response = {
  "status": 200,
  "data": {"name": "John","age":28},
  "message": "Success"
}

---

## Q174: Create a webscraper using Python’s Selenium that retrieves data from an online store.

**Input:**
```
Not applicable
```

**Answer:**
from selenium import webdriver

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.maximize_window()

# navigate to the application home page
driver.get("https://www.example.com/")

# get the search textbox
search_field = driver.find_element_by_name("q")
search_field.clear()

# enter search keyword and submit
search_field.send_keys("shoes")
search_field.submit()

# get the list of elements which are displayed after the search
# currently on result page using find_elements_by_class_name
product_list = driver.find_elements_by_class_name("product")

# iterate through each element and print the text that is
# name of the product
for product in product_list:
    print(product.text)

# close the browser window
driver.quit()

---

## Q175: Develop a web scraper with Python BeautifulSoup to scrape data from an online web store.

**Input:**
```
Not applicable
```

**Answer:**
import requests
from bs4 import BeautifulSoup
 
# Make a GET request to fetch the raw HTML content
html_content = requests.get('http://web-store.com').text
 
# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
 
# Get the product data
products = soup.find_all('div', attrs={"itemprop": "product"})
for product in products:
    name = product.find("span", attrs={"itemprop": "name"}).text
    price = product.find("span", attrs={"itemprop": "price"}).text
    description = product.find("span", attrs={"itemprop": "description"}).text
    print(name, price, description)

---

## Q176: Implement a basic algorithm in Python to calculate the nth Fibonacci number.

**Input:**
```
6
```

**Answer:**
def fibonacci(n):
 if n == 0:
 return 0
 elif n == 1:
 return 1
 else:
 return fibonacci(n - 1) + fibonacci(n - 2)
 
print(fibonacci(6)) // 8

---

## Q177: Create a Python class that receives two strings and has methods for comparing the strings and returning whether they are

**Input:**
```
Not applicable
```

**Answer:**
class StringComparator:

def __init__(self, string1, string2):
 self.string1 = string1
 self.string2 = string2

def is_equal(self):
 return self.string1 == self.string2

def is_different(self):
 return self.string1 != self.string2

def is_similar(self, threshold=0.5):
 distance = edit_distance(self.string1, self.string2)
 max_length = max(len(self.string1), len(self.string2))

 return distance / max_length < threshold

---

## Q178: Generate a program in Python to evaluate the accuracy of a machine-learning model.

**Input:**
```
from sklearn.svm import SVC
clf = SVC(kernel='poly', degree=2, gamma=0.05)
```

**Answer:**
import numpy as np
from sklearn.metrics import accuracy_score

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Calculating the accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy: " + str(accuracy))

---

## Q179: Write a Python program to replace all occurrences of a character in a string with the provided replacement character.

**Input:**
```
str = "Hello World!"

replacement = ‘X'
```

**Answer:**
def replace_all_occurrences(str, char, replacement):
  return str.replace(char, replacement)

print(replace_all_occurrences("Hello World!", 'l', 'X'))

---

## Q180: Create a python program to find the largest prime factor of a number.

**Input:**
```
Number: 331
```

**Answer:**
import math

def largest_prime_factor(n):

# Separate the list of larger factors of the number into prime and composite numbers 
    factors = []
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            factors.append(int(n/i))
# Find the largest prime factor in the list
    prime_factors = []
    for potential_factor in factors:
        is_prime = True
        for j in range(2,int(math.sqrt(potential_factor))+1):
            if potential_factor % j == 0 and potential_factor != j: 
                is_prime = False
        if is_prime:
            prime_factors.append(potential_factor)

# Return the largest prime factor
    return max(prime_factors)

print(largest_prime_factor(331))

---

## Q181: Write a Python program to check if an element exists within a given list of integers.

**Answer:**
def element_exists(elem, list_int):
  return elem in list_int

---

## Q182: Create a Python program that takes a sentence and converts it to Morse code.

**Input:**
```
Not applicable
```

**Answer:**
MORSE_CODE = {
 'A': '.-', 'B': '-...',
 'C': '-.-.', 'D': '-..',
 'E': '.', 'F': '..-.',
 'G': '--.', 'H': '....',
 'I': '..', 'J': '.---',
 'K': '-.-', 'L': '.-..',
 'M': '--', 'N': '-.',
 'O': '---', 'P': '.--.',
 'Q': '--.-', 'R': '.-.',
 'S': '...', 'T': '-',
 'U': '..-', 'V': '...-',
 'W': '.--', 'X': '-..-',
 'Y': '-.--', 'Z': '--..',
 '0': '-----', '1': '.----',
 '2': '..---', '3': '...--',
 '4': '....-', '5': '.....',
 '6': '-....', '7': '--...',
 '8': '---..', '9': '----.',
 ' ': ' ', '.': '.-.-.-',
 ',': '--..--', '?': '..--..',
 '/': '-..-.', '-': '-....-',
 '(': '-.--.-', ')': '-.--.-'
}

def encode(message):
 code = ''
 for letter in message:
  code += MORSE_CODE[letter.upper()] + ' '
 
 return code

print(encode("Hello world"))
# Output: .... . .-.. .-.. ---  .-- --- .-. .-.

---

## Q183: Generate a python program to sort a list of numbers

**Input:**
```
array = [4, 2, 6, 7, 1]
```

**Answer:**
def sort_list(array): 
    n = len(array) 
  
    for i in range(n): 
  
        min_idx = i 
        for j in range(i+1, n): 
            if array[min_idx] > array[j]: 
                min_idx = j 
        array[i], array[min_idx] = array[min_idx], array[i]

if __name__ == "__main__":
    array = [4, 2, 6, 7, 1]
    sort_list(array)
    print(array)

---

## Q184: Create a program in Python to remove all the occurrences of an item from a list.

**Input:**
```
List: [1, 2, 3, 4, 2, 5, 2]
Item to Remove: 2
```

**Answer:**
def removeItem(list, item):
    # loop through the list
    for i in list:
        # check if the element is the item to remove
        if i == item:
            # remove the item
            list.remove(i)
    # return the list
    return list

#example
list = [1, 2, 3, 4, 2, 5, 2]
result = removeItem(list, 2)

print(result)
# Output: [1, 3, 4, 5]

---

## Q185: Could you build a web scraper in Python that collects all the links from a website?

**Answer:**
# Python program to scrape a webpage
import requests as req 
from bs4 import BeautifulSoup 
  
URL = "http://www.example.com/"
  
# GET request 
r = req.get(URL) 
  
# parse the downloaded homepage and grab all text
soup = BeautifulSoup(r.text, "html.parser") 
  
# find and print all links 
links = soup.find_all('a') 
for link in links: 
    print(link.get('href'))

---

## Q186: Generate a Python program to delete a given key from a dictionary.

**Input:**
```
dictionary = {'foo': 1, 'bar': 2, 'baz': 3}
key = 'baz'
```

**Answer:**
dictionary = {'foo': 1, 'bar': 2, 'baz': 3}
key = 'baz'

def delete_key(dic, k):
  if k in dic:
    del dic[k]

delete_key(dictionary, key)

print(dictionary)

---

## Q187: Analyze the following Python function to detect any potential errors.

**Input:**
```
def expand_list(list):
    for item in list:
        list *= 2
```

**Answer:**
The function is attempting to modify the list while iterating over it. This can lead to unexpected behavior and should be avoided. To fix the code, the list should be copied before the iteration takes place: 

def expand_list(list):
    list_copy = list[:]   # make a copy of the list
    for item in list_copy:
        list *= 2

---

## Q188: Generate a Python program to reverse the order of words in a sentence but keep the order of the characters in each word 

**Answer:**
def reverse_words(string):
  words = string.split(" ")
  reversed_words = []
  for word in words:
    reversed_words.insert(0, word)
  return ' '.join(reversed_words)

string = 'This is a sentence.'
reverse_words = reverse_words(string)
print(reverse_words)

---

## Q189: Port a Java code snippet to Python 3.

**Input:**
```
public class Foo {
  public int foo( int a, int b ) {
    return a + b;
  }
}
```

**Answer:**
def foo(a, b):
 return a + b

---

## Q190: Generate a Python program that takes a list of strings as input and prints the strings in alphabetical order.

**Input:**
```
['cat', 'dog', 'apple', 'banana']
```

**Answer:**
strings = ['cat', 'dog', 'apple', 'banana']

strings.sort()

for string in strings:
    print(string)

---

## Q191: Build a Python program that extracts all email addresses from a given string.

**Input:**
```
"This is an example with two emails: john@example.com, and jane@example.com"
```

**Answer:**
import re

def find_emails(text):
    regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    emails = re.findall(regex, text)
    return emails

emails = find_emails("This is an example with two emails: john@example.com, and jane@example.com")
print(emails)

---

## Q192: Create a Python code to generate a random string of length 8 made of uppercase letters and numbers.

**Answer:**
import string
import random

length = 8
chars = string.ascii_uppercase + string.digits
password = ''.join(random.choice(chars) for i in range(length))

print (password)

---

## Q193: This code calculates the percent of transcripts mapping to rRNA. To use it, you need to supply two inputs: an HTseq_coun

**Answer:**
#!/usr/bin/python

# Malwina Prater, mn367@cam.ac.uk,  2017, Copyright
# Centre for Trophoblast Research, University of Cambridge
#
# Script version: v01.
#
# Script to calculate the percent of transcripts mapping to rRNA
#
#  INPUTS :
# 1. HTseq_counts file
# 2. Original reference transcriptome alignned to
#
#  USAGE :    
#  For producing table(s) with rRNA and MT counts for each sample use commands like that:
#
#    ./rRNA_MT_count.py --gtf /Users/malwina/Documents/CTR-Data/genomes/Mus_musculus/mm10/Mus_musculus.GRCm38.84.gtf --htseq C17_3_S20_Aligned.out.srt.bam_htseq_combined_counts.txt
#


# import modules: 
import os,sys
from optparse import OptionParser
import re

# parse in the user options:

parser = OptionParser(usage="%prog [-x Excel [-i imagefile] [-s squares]",
              

---

## Q194: Modify the following Python code to raise an exception if the input value is not an integer

**Input:**
```
def square_root(x):
    return x**0.5
```

**Answer:**
def square_root(x):
    if not isinstance(x, int):
        raise TypeError('Input must be an integer')
    return x**0.5

---

## Q195: Create a program in Python that extracts titles of all YouTube videos from a URL.

**Input:**
```
https://www.youtube.com/user/Thexvid/videos
```

**Answer:**
import requests
import re

url = "https://www.youtube.com/user/Thexvid/videos"

r = requests.get(url)
titles = re.findall('<a href="/watch\?v=([^"]+)">(.+?)<\/a>',r.content.decode('utf-8'))

for title in titles:
 print(title[1])

---

## Q196: Write Python code to list the contents of a directory.

**Answer:**
# get the list of contents
import os
directory_contents = os.listdir()

# print the contents
for content in directory_contents:
    print(content)

---

## Q197: Create an AI-powered Python script to optimize any given code.

**Input:**
```
Example code:
function getResult(a, b, c) {
 return a + b + c;
}
```

**Answer:**
# Import the required libraries
from dataclasses import dataclass

@dataclass
class Params:
 a: int
 b: int
 c: int

def get_result(params: Params) -> int:
 """Returns the sum of the three given numbers"""
 return params.a + params.b + params.c

# Optimize the code
def optimize(fn, params):
 best_score = 0
 best_params = None
 for a in range(params.a - 10, params.a + 10):
 for b in range(params.b - 10, params.b + 10):
 for c in range(params.c - 10, params.c + 10):
 score = fn(Params(a, b , c))
 if score > best_score:
 best_score = score
 best_params = {
 'a': a,
 'b': b,
 'c': c
 }
 return best_params

if __name__ == '__main__':
 # Initialize the parameters
 params = Params(a=1, b=2, c=3)
 # Get the optimized params
 best_params = optimize(get_result, params)
 # Print the optimized result


---

## Q198: Create a Python function that takes two strings and returns true if the first string is a subsequence of the second.

**Input:**
```
String 1: abc
String 2: qaxbcy
```

**Answer:**
def is_subsequence(str1, str2):
    i = 0
    j = 0

    while(i < len(str1) and j < len(str2)):
        if str1[i] == str2[j]:
            i += 1
        j += 1

    return i == len(str1)

---

## Q199: Create a neural network class in Python to model a linear regression function.

**Answer:**
import numpy as np
class LinearRegressionModel:
    def __init__(self, input_dim, output_dim):
        ''' Initialises the weights and bias of the linear regression model
        Arguments:
            input_dim {int} -- Number of input features
            output_dim {int} -- Number of outputs
        '''
        self.weights = np.zeros((input_dim, output_dim))
        self.bias = np.zeros((1, output_dim))

    def forward(self, x):
        ''' Calculates the forward pass of the linear regression model
        Arguments:
            x {numpy array} -- Input data of size (N, input_dim)
        Returns:
            out {numpy array} -- Output of the linear regression model of size (N, output_dim)
        '''
        out = np.dot(x, self.weights) + self.bias
        return out

---

## Q200: Develop a ML model in Python for predicting the winning team of football matches. Use data from the past 5 years of the 

**Input:**
```
Not applicable
```

**Answer:**
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

# Load data
data = pd.read_csv('data.csv')

# Select features
features = data[['home_team_goals', 'away_team_goals', 'home_team_possession', 'away_team_possession',
                 'home_team_shots', 'away_team_shots', 'home_team_yellow_cards', 'away_team_yellow_cards',
                 'home_team_red_cards', 'away_team_red_cards']]

# Select target
target = data['winner']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the model
gbm = GradientBoostingClassifier()
gbm.fit(X_train, y_train)

# Make predictions
y_pred = gbm.predict(X_test)



---

## Q201: Create a program in Python that evaluates a postfix expression. The input to the program should be a string with the pos

**Input:**
```
"2 3 + 4 5 * *"
```

**Answer:**
def evaluate(expression): 
  
    # split expression into list  
    expression = expression.split() 
  
    # stack to store integer values. 
    stack = []  
  
    # do for every element of expression. 
    for element in expression: 
  
        # If element is an operand push 
        # into stack it's a number only 
        if element.isdigit(): 
            stack.append(element) 
  
        # if element is an operator, 
        # pop two elements from stack 
        # perform respective operations 
        else:  
            val1 = stack.pop() 
            val2 = stack.pop() 
            stack.append(str(eval(val2 + element + val1))) 
  
    # return the value  
    return (int(stack[0])) 
  
# Driver Code  
expression = "2 3 + 4 5 * *"
  
print(evaluate(expression)) 

Output: 46

---

## Q202: Write a Python script to identify the words that contain more than one vowel in a given sentence.

**Input:**
```
Sentence: The quick brown fox jumped over the lazy dog.
```

**Answer:**
import re

sentence = "The quick brown fox jumped over the lazy dog."
pattern = r"\b(\w*[aeiou]\w*){2,}\b"

match = re.findall(pattern, sentence)
print(match)

# Output: ['quick', 'brown', 'jumped', 'over', 'lazy']

---

## Q203: This code provides a Python API for KB SRU. To use it, you can create an instance of the "sru" class and call its "searc

**Answer:**
#! /usr/bin/env python
"""
Python API for KB SRU
"""

import sys
import urllib
import requests
from lxml import etree

SRU_BASEURL = 'http://jsru.kb.nl/sru/sru'
SRU_BASEURL += '?version=1.2&maximumRecords=%i'
SRU_BASEURL += '&operation=searchRetrieve'
SRU_BASEURL += '&startRecord=%i'
SRU_BASEURL += '&recordSchema=%s'
SRU_BASEURL += '&x-collection=%s&query=%s'

SETS = {'ANP': {'collection': 'ANP',
                'description_en': 'Radio Bulletins ANP Press Agency',
                'description_nl': 'ANP Radiobulletins Digitaal',
                'metadataPrefix': 'didl',
                'recordschema': 'dcx',
                'setname': 'anp',
                'time_period': [1937, 1989]},
        'DPO': {'collection': 'DPO_boekdeel',
                'description_en': 'Early Dutch Books Onlin

---

## Q204: Using numpy, create a Python code which would return an array with the running total of numbers in a given list.

**Answer:**
import numpy as np

def runningTotal(arr):
    return np.cumsum(arr)

---

## Q205: Construct a neural network in Python that can perform basic regression.

**Input:**
```
Not applicable
```

**Answer:**
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
 
# Load the data
data = pd.read_csv('data.csv')
 
# Split the data into features and labels
X = data.drop(['label'], axis=1).values
y = data['label'].values
 
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
# Create the neural network
model = Sequential()
model.add(Dense(12, input_dim=X.shape[1], kernel_initializer='normal', activation='relu'))
model.add(Dense(12, kernel_initializer='normal', activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))
 
# Compile the model
model.compile(loss='mean_squared_error', optimizer='adam')
 


---

## Q206: Generate a program in Python to take in two strings as input, and output a list of all thewords in both strings.

**Input:**
```
String 1: I want to make a difference
String 2: The journey to success is long
```

**Answer:**
def string_to_list(s1, s2):
    s1_list = s1.split()
    s2_list = s2.split()
    output_list = s1_list + s2_list
    return output_list

words = string_to_list("I want to make a difference", "The journey to success is long")
print(words)

---

## Q207: Create a web scraper using Python that retrieves the 10 most recent articles from a news website.

**Input:**
```
Not applicable
```

**Answer:**
import requests 
from bs4 import BeautifulSoup 
  
# URL to scrap 
URL = 'http://example.com/news'
  
# get the source code 
html_content = requests.get(URL).text 
  
# parse the html content 
soup = BeautifulSoup(html_content, "lxml") 
  
# get all the articles  
articles = soup.find_all('article') 
  
# print the first 10 articles 
for article in articles[:10]: 
    print(article.text)

---

## Q208: Create a Python program to convert HTML to plain text without using any libraries.

**Answer:**
def html_to_text(html_string):
    output = ''
    in_tag = False
    for char in html_string:
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        elif in_tag == False:
            output += char
    return output

---

## Q209: Write a python program to convert the given temperature from Celsius to Fahrenheit.

**Input:**
```
0°C
```

**Answer:**
"""
Convert the given temperature from Celsius to Fahrenheit
"""

def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

if __name__ == '__main__':
    celsius = 0
    print(celsius_to_fahrenheit(celsius))

---

## Q210: Create a lambda expression in Python to filter a list of integer greater than 50.

**Input:**
```
[45, 12, 52, 89, 33, 99]
```

**Answer:**
list1 = [45, 12, 52, 89, 33, 99]
filtered_list = list(filter(lambda x: x > 50, list1))

print(filtered_list)

---

## Q211: Create a Python program to evaluate and compare the performance of two different heuristics algorithms.

**Answer:**
import time
import heuristics_algorithm1
import heuristics_algorithm2

#input data for algorithms
data1 = ...
data2 = ...

#Evaluate and compare the performance of two different heuristics algorithms
start = time.time()
result1 = heuristics_algorithm1.run(data1)
end = time.time()
time1 = end - start

start = time.time()
result2 = heuristics_algorithm2.run(data2)
end = time.time()
time2 = end - start

if time1 < time2:
    print("Algorithm 1 is faster than algorithm 2")
elif time2 < time1:
    print("Algorithm 2 is faster than algorithm 1")
else:
    print("Both algorithms have the same performance time")

---

## Q212: Generate a function in Python that takes in a dictionary (string → integer) and returns the sum of all values in the dic

**Input:**
```
my_dict = {
   "a": 5,
   "b": 10,
   "c": 15
}
```

**Answer:**
def compute_dict_sum(input_dict):
    result = 0
    for val in input_dict.values():
        result += val
    return result

print(compute_dict_sum(my_dict))

---

## Q213: Write a Python script that filters a list of integers and returns only even numbers.

**Input:**
```
list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

**Answer:**
def filter_even_numbers(lst):
    # Filter out even numbers from the given list 
    even_numbers = [num for num in lst if num % 2 == 0]
    return even_numbers

list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = filter_even_numbers(list)
print(result)

---

## Q214: Generate a Python program that takes a sentence as input and prints out only the verbs.

**Input:**
```
The cat jumped over the moon.
```

**Answer:**
import nltk

def extract_verbs(sentence):
    tokens = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(tokens)
    verbs = [word for word, pos in tags if pos.startswith('V')]
    return verbs

sentence = "The cat jumped over the moon."
verbs = extract_verbs(sentence)
print(verbs)

---

## Q215: Create an AI-based system in Python for predicting stock market movements.

**Input:**
```
Not applicable
```

**Answer:**
#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#import data
data = pd.read_csv('data.csv') 

#split data into train and test data
X_train=data.iloc[:, 0] #Choosing the independent variable 
y_train=data.iloc[:, 1]  #Choosing the dependent variable
X_test=data.iloc[:, 0] #Choosing the independent variable 
y_test=data.iloc[:, 1]  #Choosing the dependent variable

#Build a deep learning model
#import necessary libraries
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

#create a model and add layers
model = Sequential()
model.add(Dense(64, input_shape=(1,), activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.ad

---

## Q216: Develop an API in Python that fetches data from an SQL database and presents the data in the form of a JSON.

**Input:**
```
None
```

**Answer:**
import json 
import sqlite3
from flask import Flask, request, jsonify 

app = Flask(__name__) 
  
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d 
  
@app.route('/', methods=['GET'])
def index(): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = dict_factory
    cur = connection.cursor() 
    all_users = cur.execute('SELECT * FROM users;').fetchall() 
    return jsonify(all_users) 
  
if __name__ == '__main__': 
    app.run(debug = True)

---

## Q217: Generate a Python dictionary that contains the count of the characters in a given string.

**Input:**
```
"Hello World"
```

**Answer:**
def count_chars(string):
    count_dict = {}

    for char in string:
        if char in count_dict:
            count_dict[char] += 1
        else:
            count_dict[char] = 1

    return count_dict

print(count_chars("Hello World"))

# Output: {'H': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'W': 1, 'r': 1, 'd': 1}

---

## Q218: Write a Python program to store and querying user data.

**Input:**
```
user_data = {
    "Name": "John",
    "Age": 25,
    "City": "New York"
    
}
```

**Answer:**
import json

user_data = {"Name": "John", "Age": 25, "City": "New York"}

def store_user_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f)

def get_user_data():
    with open('user_data.json') as f:
        return json.load(f)

# store data in JSON file
store_user_data(user_data)

# get data
data = get_user_data()
print(data)

---

## Q219: You are required to write a Python program to optimize an equation.

**Input:**
```
x + x + y + y + y
```

**Answer:**
def optimize_equation(equation):
    variables = []
    for term in equation.split('+'):
        var, count = term.strip().split(' ')
        variables.append((var, int(count)))

    new_equation = ""
    for var, count in variables:
        new_equation += (var + '^' + str(count)) + ' + '
    return new_equation[:-3]

equation = 'x + x + y + y + y'

print(optimize_equation(equation))

---

## Q220: Generate Python code that takes a list of strings and generates a list of lists of words from the strings. The returned 

**Input:**
```
["Hello world", "This is a test"]
```

**Answer:**
def get_word_lists(strings):
    word_lists = []
    for string in strings:
        words = string.split(" ")
        word_list = []
        for i in range(len(words)):
            word_list.append(words[i:])
        word_lists.append(word_list)
    return word_lists

word_lists = get_word_lists(["Hello world", "This is a test"])
print(word_lists) # prints "[["Hello", "world"], ["This", "is", "a", "test"]]"

---

## Q221: Create a web scraper that extracts specific data from a given website.

**Answer:**
The web scraper should utilize the Python package BeautifulSoup to parse webpages and extract the required data. BeautifulSoup will allow us to find HTML elements on the webpage using tags and attributes. Once the data is found, it can be converted into the desired format and stored.

For example, to extract the URL from a list of webpages, the following code snippet can be used:

import requests
from bs4 import BeautifulSoup

# Get the web page
webpage = requests.get("<url_of_webpage>")

# Parse the web page
soup = BeautifulSoup(webpage.content, 'html.parser')

# Find all 'a' tags
links = soup.find_all('a')

# Extract the URLs in the 'href' attribute
for link in links:
    print(link.get('href'))

---

## Q222: Construct a script in Bash that can install a given software.

**Input:**
```
Python 3.8.5
```

**Answer:**
#!/bin/bash

# Download latest version of Python
curl -O https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz

# Extract the tgz file
tar -xzf Python-3.8.5.tgz

# Move into the Python directory
cd Python-3.8.5

# Run the configure script
./configure

# Compile and install
make
make install

---

## Q223: Write a function in Python that takes a list of integers and returns a new list containing only odd numbers.

**Input:**
```
[3, 8, 6, 10, 17]
```

**Answer:**
def odd_numbers_list(numbers):
    return [num for num in numbers if num % 2 != 0]

---

## Q224: Create a Python script that adds two numbers together and prints the result.

**Answer:**
def add(a, b):
    sum = a + b
    print(sum)

add(5,7)

---

## Q225: Design an algorithm in Python to find the most common elements in an array of integers.

**Input:**
```
[3, 4, 1, 2, 5, 3, 3]
```

**Answer:**
def most_common(nums):
    # Create a dictionary to store the counts
    counts = {}

    # Iterate over the elements
    for num in nums:
        # If the element is not present in the dictionary, add it
        if num not in counts:
            counts[num] = 0

        # Update the count
        counts[num] += 1

    # Get the maximum count
    max_count = max(counts.values())

    # Return the elements that have maximum count
    return [num for num, count in counts.items() if count == max_count]

---

## Q226: Write a Python program to find the maximum element in the given array [1, 10, 50, 3, 8].

**Input:**
```
Not applicable
```

**Answer:**
array = [1, 10, 50, 3, 8]

# Get the maximum element
max_element = max(array)

print(max_element) # Output: 50

---

## Q227: Create a Python script to analyze the sentiment of a text.

**Answer:**
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

def sentiment_analyzer(text):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Create stemmer object
    stemmer = SnowballStemmer('english')

    # Stem each token
    stemmed_words = [stemmer.stem(word) for word in tokens]

    # Remove punctuation
    clean_words = [word for word in stemmed_words if re.match('[a-zA-Z-]+$', word)]

    # Remove stopwords
    meaningful_words = [word for word in clean_words if not word in stopwords.words('english')]

    # Create a SentimentIntensityAnalyzer object
    sid = SentimentIntensityAnalyzer()

    # Get the polarity score of the text
    po

---

## Q228: Create a Python script that takes a list of email addresses as input and prints a filtered list of email addresses that 

**Input:**
```
list = ["john@gmail.com", "sarah@yahoo.com", "bob@microsoft.com", "sophie@gmail.com"]
```

**Answer:**
filtered_list = [email for email in list if email.endswith("@gmail.com")]

print(filtered_list)
# Output: ["john@gmail.com", "sophie@gmail.com"]

---

## Q229: Generate a Python function to execute a valid insertion sort on a given list of integers.

**Answer:**
def insertion_sort(arr):
 for i in range(1, len(arr)):
 key = arr[i]
 j = i -1
 while j >= 0 and key < arr[j] :
    arr[j + 1] = arr[j]
    j = j - 1
 arr[j + 1] = key

return arr

---

## Q230: Generate a program to sort a list of numbers using Insertion Sort algorithm in Python.

**Answer:**
def insertionSort(arr):
	for i in range(1, len(arr)):
		current = arr[i]
		j =i-1
		while j>=0 and arr[j]>current:
			arr[j+1] = arr[j]
			j-=1
		arr[j+1] = current
	return arr

if __name__ == '__main__':
	arr = [2, 4, 7, 3, 8, 6, 1]
	print(insertionSort(arr))

---

## Q231: Create an Python function that takes a string containing a numerical expression and returns the result.

**Answer:**
def eval_expr(expr):
   return eval(expr)

---

## Q232: Given a json-formatted string, create a python program to parse it into a dict.

**Input:**
```
data = '{"name": "John","age": 30,"address": {"city": "New York","state": "NY"}}'
```

**Answer:**
import json

data = '{"name": "John","age": 30,"address": {"city": "New York","state": "NY"}}'

data_dict = json.loads(data)

---

## Q233: Create a Python program to compress a given string by replacing all repeating characters with a single instance and its 

**Input:**
```
String: aabbbbbbcccc
```

**Answer:**
def compress(s): 
    # Initialize results 
    output = "" 
  
    # Initialize count 
    count = 1
  
    # Traverse the string 
    for i in range(len(s)): 
          
        # If the current character is same 
        # as next one, increment its count 
        if (i+1 < len(s) and s[i] == s[i+1]): 
            count += 1
          
        else: 
            # Append the count and character 
            outputo + = str(count) + s[i] 
          
            # Reset the  count  
            count = 1
          
    # Append the last obtained characters 
    # and their count 
    output += str(count) + s[i] 
  
    return output

s = "aabbbbbbcccc"
print(compress(s))
# Output: 2a6b4c

---

## Q234: Create a basic CRUD API for the BlogPost model with Python/Flask. The API should include endpoints for creating a post, 

**Input:**
```
Not applicable
```

**Answer:**
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///test.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200))
  content = db.Column(db.Text)

  def __repr__(self):
    return '<BlogPost %r>' % self.title

@app.route('/post', methods=['POST'])
def create_post():
  data = request.get_json()
  post = BlogPost(title=data['title'], content=data['content'])
  db.session.add(post)
  db.session.commit()
  return jsonify(post.id)

@app.route('/posts', methods=['GET'])
def get_posts():
  posts = BlogPost.query.all()
  return jsonify([post.serialize() for post in posts])

@app.route('/post/<id>', methods=['GET'])
def

---

## Q235: Write a Python program that calculates the distance between two points on a two-dimensional plane.

**Input:**
```
Point1 (x1: 3, y1: 4); Point2 (x2: -9, y2: -2)
```

**Answer:**
#include <iostream>
#include <math.h>

int main() 
{ 
    int x1 = 3; 
    int y1 = 4; 

    int x2 = -9; 
    int y2 = -2;

    float distance = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2)); 

    std::cout << "Distance between the two points is: " << distance << std::endl; 

    return 0; 
}

---

## Q236: Create an AI-based chatbot in Python that can answer simple queries about a product or service.

**Input:**
```
Not applicable
```

**Answer:**
import random

# The answers to the queries
answers = {
    'What is XYZ?': 'XYZ is a company that provides XYZ services.',
    'What does XYZ do?': 'XYZ helps customers find solutions to their problems.',
    'Where is XYZ located?': 'XYZ is located in ABC city.',
    'What are the benefits of using XYZ?': 'XYZ provides a quick and easy way to find solutions to your problems.'
}

# Generate a response
def generate_response(question):
    if question in answers:
        return answers[question]
    else:
        return random.choice(['I am not sure I understand.', 'Can you give me more information?', 'Can I help you with something else?'])

# Start the conversation
question = input('Welcome to XYZ. How can I help you? ')
response = generate_response(question)

while response != 'Goodbye':


---

## Q237: Generate a python program to read the contents from a given URL

**Answer:**
import requests

def read_url(url):
  r = requests.get(url)
  if r.status_code == 200:
    return r.text
  else:
    return None

---

## Q238: Code a function in Python that takes a list of integers (denoted by `lst`) and returns a list of booleans where each ele

**Input:**
```
lst = [7, 8, 12, 19, 22, 23]
```

**Answer:**
def is_prime(n):
 # check if n is divisible by any of the numbers
 # between 2 and n-1
 for i in range(2, n):
 if n % i== 0:
 return False

 return True 

def check_lst(lst):
 # generate a list of booleans 
 # where each element corresponds to the corresponding
 # element of lst
 result_lst = []
 for i in range(len(lst)):
 if is_prime(lst[i]):
 result_lst.append(True)
 else:
 result_lst.append(False)

 return result_lst

lst = [7, 8, 12, 19, 22, 23]
print(check_lst(lst))

# Output: 
# [True, False, False, True, False, True]

---

## Q239: Generate a program in Python to output the top 3 numbers from an array of integers

**Input:**
```
[7, 13, 5, 8, 50, 11, 64, 48]
```

**Answer:**
def top_three(numbers):
    sorted_numbers = sorted(numbers, reverse=True)
    return sorted_numbers[:3]

print(top_three([7, 13, 5, 8, 50, 11, 64, 48]))

---

## Q240: Using Python, build a dictionary containing the numbers from 1 to n as the key and the square of each number as the valu

**Input:**
```
n = 10
```

**Answer:**
my_dict = {}

for i in range(1,n+1):
 my_dict[i] = i**2

print(my_dict)

---

## Q241: Edit the following Python program to make a correct API request and parse the response.

**Input:**
```
import requests

url = 'https://api.example.com/users'

response = requests.get(url)

print(response.json())
```

**Answer:**
import requests

url = 'https://api.example.com/users'

headers = {
 'Authorization': 'Bearer YOUR_API_TOKEN',
 'Content-Type': 'application/json',
}

response = requests.get(url, headers=headers).json()

for user in response['data']:
 print(user)

---

## Q242: Create a Python program that takes in text input from the user and searches a given list of strings to find any matches.

**Input:**
```
strings = ["First","Second","Third"]
```

**Answer:**
import re 
  
# input string 
strings = ["First","Second","Third"]

# Get the string 
inp_str = input("Please enter your string :") 

# Initialize the flag 
found = False
  
# Search the string 
for i in strings: 
    if re.search(i, inp_str):
        found = True

# Print result 
if found == True: 
    print("String matches") 
else: 
    print("String doesn't matches")

---

## Q243: Generate a program in Python to convert all characters of a string in lowercase.

**Input:**
```
String = "HELLO"
```

**Answer:**
def to_lower(string):
    return string.lower()

---

## Q244: Edit the following Python program to use a dictionary instead of a list.

**Input:**
```
items = [1, 2, 3, 4]

for item in items:
 print(item)
```

**Answer:**
items = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}

for key, value in items.items():
 print(value)

---

## Q245: Construct a prime number sieve in Python which returns a list of all primes up to a given number.

**Input:**
```
n = 10
```

**Answer:**
def primeSieve(n): 
    prime_list = [True for i in range(n+1)] 
    p = 2
    while (p * p <= n): 
        if (prime_list[p] == True): 
            for i in range(p * 2, n+1, p): 
                prime_list[i] = False
        p += 1
    primes=[] 
    for p in range(2, n): 
        if prime_list[p]: 
            primes.append(p) 
    return primes

print(primeSieve(10))  # [2, 3, 5, 7]

---

## Q246: Write a python code to print all prime numbers between 1 and a given number n.

**Answer:**
# Function to generate prime numbers between 1 and a given number n 
def generate_prime_numbers(n): 
  
    # Array for checking if a number is prime or not
    prime_list = [True for i in range(n + 1)] 
    p = 2
    while (p * p <= n): 
          
        # If prime_list[p] is not changed, then it is a prime 
        if (prime_list[p] == True): 
              
            # Update all multiples of p 
            for i in range(p * 2, n + 1, p): 
                prime_list[i] = False
        p += 1
  
    # Collecting prime numbers 
    for p in range(2, n): 
        if prime_list[p]: 
            print(p)

---

## Q247: Find the optimal solution to solve a knapsack problem using dynamic programming.

**Input:**
```
Given Items (with values and weights): [(60, 10), (100, 20), (120, 30)] 
Capacity of Knapsack: 50
```

**Answer:**
// A Naive recursive Python 
// program for 0-1 Knapsack problem 
 
# Returns the maximum value  
# that can be put in a knapsack of  
# capacity W 
def knapSack(W, wt, val, n): 
  
    # Base Case 
    if n == 0 or W == 0 : 
        return 0
  
    # If weight of the nth item is more 
    # than Knapsack capacity W, then 
    # this item cannot be included in the optimal solution 
    if (wt[n-1] > W): 
        return knapSack(W, wt, val, n-1) 
  
    # return the maximum of two cases: 
    # (1) nth item included 
    # (2) not included 
    else: 
        return max(val[n-1] + knapSack(W-wt[n-1], wt, val, n-1), 
                    knapSack(W, wt, val, n-1)) 
  
# end of function knapSack

---

## Q248: Using Python, create a function that calculates the objective function of a linear equation.

**Input:**
```
ax + by = c

a = 3, b = 5, c = 7
```

**Answer:**
def linear_eq(a, b, c):
    return a*x + b*y - c

# For example:
result = linear_eq(3, 5, 7)
print(result)

---

## Q249: Implement an insertion sort algorithm in Python.

**Answer:**
def insertion_sort(list):
    for i in range(1,len(list)):
        key = list[i]
        j = i - 1
        while j>=0 and key < list[j]:
            list[j+1] = list[j]
            j-=1
        list[j+1] = key
    return list

---

## Q250: Write a python program to generate a random password given a set of letters, numbers, and characters.

**Input:**
```
No input
```

**Answer:**
import random 
  
  
# All the possible characters 
# that could go into the password 
string = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
  
# Using the choice function of the 
# random module choose any 
# character randomly from the set of characters 
password =  "".join(random.sample(string, 8)) 
print(password)

---

## Q251: Develop a Python module to generate random numbers.

**Answer:**
import random

def generate_random_numbers(length, min_value, max_value):
    return [random.uniform(min_value, max_value) for _ in range(length)]

---

## Q252: How do we use recursion to solve a given problem in Python?

**Answer:**
Recursion is a powerful technique for solving problems. It involves defining a problem in terms of itself. A recursion problem is solved by breaking it down into smaller problems, until the problem is small enough to be solved directly. The result from a smaller problem can then be combined with the result from the larger problem, until the original problem is solved. In Python, a recursive function is one that calls itself.

---

## Q253: Create an application using Python and Flask to submit form data and store it in a database.

**Input:**
```
Form elements: Name, Email, Phone
```

**Answer:**
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
 return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
 name = request.form.get('name')
 email = request.form.get('email')
 phone = request.form.get('phone')
 
 conn = sqlite3.connect('data.db')
 cur = conn.cursor()
 
 cur.execute("INSERT INTO data (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
 conn.commit()
 
 return redirect('/')
	
if __name__ == '__main__':
 app.run(debug=True)

---

## Q254: Optimize a Python program that processes a 2d array and stores the transpose output in a new array.

**Input:**
```
Not applicable
```

**Answer:**
def transpose(A):
 n = len(A)
 m = len(A[0])

 B = [[0 for x in range(n)] for x in range(m)]

 for i in range(n):
 for j in range(m):
 B[j][i] = A[i][j]

 return B

---

## Q255: Generate a Python script that takes any number of integer arguments and returns their sum.

**Input:**
```
3 5 7
```

**Answer:**
def sum_ints(*args):
    total = 0
    for num in args:
        total += num
    
    return total

print(sum_ints(3, 5, 7))

---

## Q256: Create a function in Python which takes a list as input and returns the sum of the items in the list.

**Answer:**
def sum_list(input_list):
  sum = 0
  for i in input_list:
    sum += i
  return sum

---

## Q257: Create a Selenium script in Python to automate the login process in a given website.

**Input:**
```
Target website: www.example.com
```

**Answer:**
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Initialize web driver
driver = webdriver.Chrome()

# Navigate to the target web page
driver.get('http://www.example.com')

# Locate username field
username = driver.find_element_by_name('username')

# Enter username
username.send_keys('username')

# Locate password field
password = driver.find_element_by_name('password')

# Enter password
password.send_keys('password')

# Locate submit button
submit_button = driver.find_element_by_name('submit')

# Click submit button
submit_button.click()

# Wait for login process to complete
time.sleep(5)

# Login successful
print('Login successful!')

driver.close()

---

## Q258: Create an AI model in Python to classify emails from the Enron Spam Dataset as either spam or non-spam.

**Input:**
```
Not applicable
```

**Answer:**
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import precision_score

# Load the dataset
df = pd.read_csv("spam.csv", encoding='iso-8859-1')
# Load label and data
X = df['EmailText']
y = df['Label']

# Split data into train-test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Create bag of words model
count_vectorizer = CountVectorizer()
X_train_counts = count_vectorizer.fit_transform(X_train)

# Train the model
clf = svm.SVC(kernel='linear')
clf.fit(X_train_counts, y_train)

# Test the model
X_test_counts = count_vectorizer.transform(X_test)
predictions = clf.predict(X_test_counts)
score = precision_score(y_t

---

## Q259: Re-write the following SQL query in Python.

**Input:**
```
SELECT * FROM Movies WHERE category = 'horror';
```

**Answer:**
import sqlite3

conn = sqlite3.connect('movies.db') 
cursor = conn.cursor()

cursor.execute("SELECT * FROM Movies WHERE category = 'horror'")

result = cursor.fetchall()
for row in result:
    print(row)

conn.close()

---

## Q260: Take two matrices, A and B, and produce a matrix C where each element is the product of the corresponding elements of A 

**Input:**
```
A = [[3, 4], 
     [1, 2]]
B = [[7, 5],
     [0, 1]]
```

**Answer:**
# Python
def matrixMultiplication(A, B):
    if len(A[0]) != len(B):
        return "Matrix multiplication not possible"

    C = [[0 for i in range(len(A[0]))] for j in range(len(B[0]))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]

    return C

A = [[3, 4], 
     [1, 2]]
B = [[7, 5],
     [0, 1]]
C = matrixMultiplication(A, B)

print(C) # Output = [[21, 17], [0, 2]]

---

## Q261: Come up with a correct approach to optimize the following python program.

**Input:**
```
numbers = [1, 2, 3, 4, 5, 6]

for x in numbers:
    print(x)
```

**Answer:**
numbers = [1, 2, 3, 4, 5, 6]

print(*numbers, sep='\n')

---

## Q262: Design a program in Python to detect the vowel in a given string.

**Input:**
```
Hello World
```

**Answer:**
def vowelCheck(inputString): 
    vowels = ['a','e','i','o','u','A','E','I','O','U'] 
    for x in inputString: 
        if x in vowels: 
            return x

---

## Q263: Convert a given SQL statement into a Python Pandas DataFrame.

**Input:**
```
SELECT * FROM book;
```

**Answer:**
import pandas as pd

df = pd.read_sql_query("SELECT * FROM book;", conn)

---

## Q264: Using the data provided, generate a histogram in Python.

**Input:**
```
data = [3, 5, 7, 2, 8, 10, 11, 65, 72, 81, 99, 100, 150]
```

**Answer:**
import matplotlib.pyplot as plt

data = [3, 5, 7, 2, 8, 10, 11, 65, 72, 81, 99, 100, 150]

# plotting the histogram 
plt.hist(data, bins = [0, 20, 40, 60, 80, 100, 120, 140, 160], edgecolor = 'black') 
  
# x-axis label 
plt.xlabel('Range of values') 
# y-axis label 
plt.ylabel('Number of Occurrences') 
# plot title 
plt.title('Histogram of data') 
  
# function to show the plot 
plt.show()

---

## Q265: Create a Python script to populate an array with random numbers from 1-100.

**Answer:**
import random

def populateArray(array_length):
 array = []
 for i in range(array_length):
 array.append(random.randint(1, 100))
 return array

---

## Q266: Create an natural language processing application in Python that extracts the top 10 most frequent words from a given te

**Input:**
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
```

**Answer:**
from collections import Counter

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

# Split the text into individual words
words = text.split()

# Create a counter object
counter = Counter(words)

# Get the top 10 most frequent words
top_words = counter.most_common(10)

print(top_words)

# Output: [('dolor', 1), ('Lorem', 1), ('ipsum', 1), ('amet', 1), ('consectetur', 1), ('adipiscing', 1), ('elit,', 1), ('sed', 1), ('do', 1), ('eiusmod', 1)]

---

## Q267: Given an array of strings, write a Python function to remove all duplicates and return the resulting array.

**Input:**
```
Example array: ['a', 'b', 'a', 'c', 'c', 'd']
```

**Answer:**
def removeDuplicates(arr):
 result = [] 
  
 # traverse for all elements 
 for i in arr: 
  
  # check if exists in result 
  if i not in result: 
   result.append(i) 
  
 # return result 
 return result

---

## Q268: Generate a Python script to find the longest common substring in two strings.

**Input:**
```
"Helwallomst", "Welcome"
```

**Answer:**
def longest_common_substring(str1, str2):
    match = 0
    substr = ""
    for i in range(len(str1)):
        for j in range(len(str2)):
            l = 0
            while (i + l < len(str1) and j + l < len(str2) and str1[i + l] == str2[j + l]):
                l += 1
            if l > match:
                substr = str1[i:i + l]
                match = l
    return substr

result = longest_common_substring("Helwallomst", "Welcome")
print(result)

---

## Q269: Write a function in Python to search for a character in a given string.

**Input:**
```
String: “Hello”
Character: ‘l’
```

**Answer:**
def serach_char(input_str, char):
  for char in input_str:
    if char == input_char:
      return True
  return False

---

## Q270: Write a python program to parse an XML document and return a list of tag objects.

**Input:**
```
<xml>
  <root>
    <child1 id="1">
      <subchild1 value="a">
      </subchild1>
      <subchild2 value="b">
      </subchild2>
    </child1>
    <child2 id="2">
      <subchild3 value="c">
      </subchild3>
      <subchild4 value="d">
      </subchild4>
    </child2>
  </root>
</xml>
```

**Answer:**
def parse_xml(text):
    tag_objects = []

    root = ET.fromstring(text)
    for child in root:
        tag = Tag(child.attrib["id"])
        for subchild in child:
            tag.add_value(subchild.attrib["value"])
        tag_objects.append(tag)

    return tag_objects

class Tag:
    def __init__(self, tag_id):
        self.tag_id = tag_id
        self.values = []
    
    def add_value(self, value):
        self.values.append(value)

---

## Q271: Based on a given input, create a function in Python to generate a random string of length 6.

**Answer:**
import random
import string

def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

random_string(6)

---

## Q272: Create a Python program to average the elements of a 2-dimensional array.

**Input:**
```
a = [[3,2,6],
     [8,5,9],
     [4,7,1]]
```

**Answer:**
def averageMatrix(matrix):
 sum = 0
 for row in matrix:
  for e in row:
   sum += e

 return sum / (len(matrix) * len(matrix[0]))

a = [[3,2,6],
     [8,5,9],
     [4,7,1]]

print(averageMatrix(a)) # 4.77

---

## Q273: Generate a code in Python to convert a number into binary format.

**Answer:**
"""
Generate a code in Python to convert a number into binary format
"""
def convert_to_binary(num):
    # check if the number is 0, if so return 0
    if num == 0:
        return 0
    
    # initialize an empty binary string
    binary = ''
    
    # loop through the number and get the remainder 
    # which is the bits of the binary
    while num != 0:
        remainder = num % 2
        binary = str(remainder) + binary
        num = num // 2
    
    return binary

# test the function 
print(convert_to_binary(10)) # 1010

---

## Q274: Generate a python program that takes an integer and then prints out the factorial of it?

**Input:**
```
7
```

**Answer:**
def factorial(num):
    if num <= 1:
        return 1
    else:
        return num * factorial(num - 1) 

n = int(input("Enter a number: "))  
print("Factorial of",n,"is",factorial(n))

---

## Q275: Write a Python program to convert a positive integer to negative or vice versa using bitwise NOT operator.

**Answer:**
def convert_to_negative(x): 
    return ~x + 1 
  
def convert_to_positive(x): 
    return ~(x-1)

---

## Q276: Build a simple blockchain system in Python.

**Input:**
```
Not applicable
```

**Answer:**
import hashlib
import json

# Define the Block class
class Block:
 def __init__(self, index, timestamp, data, previous_hash):
 self.index = index
 self.timestamp = timestamp
 self.data = data
 self.previous_hash = previous_hash
 self.hash = self.hash_block()

 # Create the hash of the block contents
 def hash_block(self):
 sha = hashlib.sha256()
 sha.update((str(self.index) + 
 str(self.timestamp) + 
 str(self.data) + 
 str(self.previous_hash)).encode('utf-8'))
 return sha.hexdigest()

# Create the blockchain
def create_blockchain():
 blockchain = [create_genesis_block()]
 previous_block = blockchain[0]

 # Add blocks for each item in the list of transactions
 for i in range(1, len(blockchain_transactions)):
 block_to_add = next_block(previous_block, blockchain_transactions[i])
 blockchain

---

## Q277: Write a Python script to find the GCD of two numbers.

**Input:**
```
1000, 500
```

**Answer:**
def findGCD(a, b): 
   if (b == 0): 
       return a
   return findGCD(b, a % b)
    
a = 1000
b = 500
print("GCD of number is: ", findGCD(a, b))

---

## Q278: Create a program in Python to find the number of occurrences of an element x in a list y.

**Input:**
```
[3, 5, 2, 7, 4, 3, 2], x = 2
```

**Answer:**
def count_x(x, y):
    count = 0
    for i in y:
        if i == x:
            count += 1
    return count

---

## Q279: Write a Python program to convert ratings in a list of strings to a float.

**Input:**
```
['4.5', '3.0', '2.5', '4.0']
```

**Answer:**
def str_to_float(ratings):
    return [float(x) for x in ratings]

---

## Q280: Create a Python program that encrypts a message using a Caesar cipher.

**Answer:**
def caesar_encrypt(message, shift):
    encrypted_message = ""
    for c in message:
        encrypted_c = ord(c) + shift
        if encrypted_c > 126:
            encrypted_c -= 94
        encrypted_message += chr(encrypted_c)
    return encrypted_message

---

## Q281: Write a Python program to find the largest three numbers in a list.

**Input:**
```
1, 6, 3, 8, 7, 4
```

**Answer:**
my_list = [1, 6, 3, 8, 7, 4]
largest_three = sorted(my_list)[-3:]
print(largest_three)

---

## Q282: Given two binary trees, check if the first tree is subtree of the second tree.

**Answer:**
# Python program to check if 
# a binary tree is subtree of another binary tree 
  
# A binary tree node 
class Node: 
      
    # Constructor to create a new node 
    def __init__(self, data): 
        self.data = data 
        self.left = None
        self.right = None
  
def isSubTree(T, S): 
    
    if S is None: 
        return True
  
    if T is None: 
        return False
  
    if areIdentical(T, S): 
        return True
  
    return isSubTree(T.left, S) or isSubTree(T.right, S) 
  
  
def areIdentical(T, S): 
      
    if T is None and S is None: 
        return True
  
    if T is None or S is None: 
        return False
  
    return (T.data == S.data and areIdentical(T.left, S.left)and
        areIdentical(T.right, S.right))

---

## Q283: Write a Python program to swap the values of two variables.

**Answer:**
x = 5
y = 10

# Swapping process 
x, y = y, x 

print("x:", x) 
print("y:", y)

---

## Q284: Optimize the following Python code to use built-in functions.

**Input:**
```
def removeDuplicates(array): 
    for i in range (len(array)): 
        for j in range (i + 1, len(array)): 
            if array[i] == array[j]: 
                array.pop(j)
```

**Answer:**
def removeDuplicates(array): 
    finalArray = []
    for element in array: 
        if element not in finalArray: 
            finalArray.append(element)
    return finalArray

---

## Q285: Create a program in Python that takes a list of words and an integer n and returns a list of words that appear at least 

**Input:**
```
words =['a', 'b', 'a', 'c', 'd', 'a', 'x', 'd', 'd']
n = 3
```

**Answer:**
from collections import Counter

def frequent_words(words, n):
    counts = Counter(words)
    return [word for word, count in counts.items() if count >= n]

result = frequent_words(words, n)

print(result) # prints ['a', 'd']

---

## Q286: Devise a Python program to determine whether a given number is even or odd.

**Answer:**
def even_or_odd(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"

---

## Q287: Compose a basic blockchain system in Python.

**Answer:**
import hashlib
import json

# We will use SHA256 as our hashing function
def sha256(data):
    hash_function = hashlib.sha256()
    hash_function.update(data.encode('utf-8'))
    return hash_function.hexdigest()

# Create a class for each block
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = sha256(f'{self.index}{self.timestamp}{self.data}{self.previous_hash}')

# Create a class for the blockchain
class Blockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, data):
        previous_hash = self.chain[-1].hash if len(self.chain) > 0 else None
        block = Block(len(self.chain), data['t

---

## Q288: Provide a Python code that uses the exponential smoothing algorithm to predict the next day's forecast temperature given

**Input:**
```
[21, 22, 20]
```

**Answer:**
"""
This code uses the exponential smoothing algorithm to predict the next day's forecasted temperature given the past three day's forecasted temperatures.
"""

def predict_temperature(temperature_list):
    alpha = 0.5 #Confidence value
    predicted_temperature = temperature_list[-1] # Initializing prediction
    for temperature in temperature_list[:-1]:
        predicted_temperature = alpha*temperature + (1-alpha)*predicted_temperature
    return predicted_temperature

if __name__ == '__main__':
    temperature_list = [21, 22, 20]
    print(predict_temperature(temperature_list))

---

## Q289: Write a function in Python to sort a dictionary according to its values, in descending order.

**Input:**
```
dictionary = {'apple': 2, 'banana': 3, 'mango': 1}
```

**Answer:**
def sortDictionary(dictionary):
  sorted_list = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
  sorted_dictionary = dict(sorted_list)
  return sorted_dictionary

sorted_dictionary = sortDictionary({'apple': 2, 'banana': 3, 'mango': 1})
print(sorted_dictionary)

---

## Q290: Create a function in Python to generate a multiplication table with numbers in a range given start and end parameters.

**Input:**
```
start = 5
end = 10
```

**Answer:**
def multiplication_table(start, end):
	for x in range(start, end + 1):
		for y in range(start, end + 1):
			print(x * y, end = "  ")
		print("\n")
		
multiplication_table(start, end)

---

## Q291: Write a python program to identify if a string s has matching parentheses

**Answer:**
def matching_paren(s):
    stack = []
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if len(stack) == 0:
                return False 
            stack.pop()
    
    if len(stack) == 0:
        return True
    else:
        return False

---

## Q292: Develop a function in Python to take as input two array of integers and swap their elements.

**Input:**
```
arr1 = [3, 5, 6, 9]
arr2 = [2, 4, 7, 8]
```

**Answer:**
def swap(arr1, arr2):
    assert len(arr1) == len(arr2)
    for i in range(len(arr1)):
        temp = arr1[i]
        arr1[i] = arr2[i]
        arr2[i] = temp

---

## Q293: Can you design a function in Python for reversing a list?

**Input:**
```
[1,2,3,4,5]
```

**Answer:**
def reverse_list(list): 
    return list[::-1]

---

## Q294: Create a Python script to build a dictionary from string to string of the given samples.

**Input:**
```
Samples:
apple->red
banana->yellow
cherry->red
```

**Answer:**
def build_dictionary(samples):
 dictionary = {}
 for sample in samples:
  key, value = sample.split("->")
  dictionary[key] = value
 return dictionary
 
samples = ["apple->red", "banana->yellow", "cherry->red"]
dictionary = build_dictionary(samples)

print(dictionary)

---

## Q295: Write a Python script to find the average of numbers stored in an array.

**Input:**
```
[10, 20, 30]
```

**Answer:**
def calculate_mean(numbers):
    total_sum = 0
    for num in numbers:
        total_sum += num
    mean = total_sum / len(numbers)
    return mean

print(calculate_mean([10, 20, 30]))

---

## Q296: Generate a Python program that takes two lists as input and returns a new list containing only the common elements.

**Input:**
```
[1, 2, 3, 4, 8], [2, 6, 8, 10]
```

**Answer:**
def common_elements(list1, list2): 
    common_list=[]
    for element in list1: 
        if element in list2: 
            common_list.append(element) 
    return common_list
  
list1 = [1, 2, 3, 4, 8] 
list2 = [2, 6, 8, 10]

common_list = common_elements(list1, list2) 

print(common_list)

---

## Q297: Create a loop in Python to print out all the odd numbers from 1 to 10.

**Answer:**
for i in range(1, 11):
    if i % 2 != 0:
        print(i)

---

## Q298: Create a machine learning model in Python that predecits customer lifetime value given a customer's past transactions.

**Input:**
```
Not applicable
```

**Answer:**
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

# Preprocessing
df = pd.read_csv('transactions.csv')
X = df.iloc[:,:-1].values
y = df.iloc[:,-1].values
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Model Training
model = RandomForestRegressor()
model.fit(X, y)

# Prediction
customer_input = np.array([[10,100,5,...]]) # provide data related to past transactions
trans_scaled = scaler.transform(customer_input)
predicted_LTV = model.predict(trans_scaled)[0]
print('Predicted customer lifetime value', predicted_LTV)

---

## Q299: Given a list of numbers and a target number, write a Python program to find a pair of numbers from the given list that a

**Input:**
```
Input List: [1, 2, 3, 4, 4, 5, 6]
Target: 8
```

**Answer:**
def find_pair(lst, target):
    for i in range(len(lst)):
        if (target - lst[i]) in lst[i+1:]:
            return [lst[i], target-lst[i]]

find_pair([1,2,3,4,4,5,6], 8)

---

## Q300: Develop a class in Python to perform various matrix operations like addition, subtraction, multiplication and transpose.

**Answer:**
class Matrix: 
    def __init__(self, m, n, lst): 
        self.m = m             
        self.n = n             
        self.mat = [] 
  
        c = 0
        for i in range(self.m): 
            a =[] 
            for j in range(self.n): 
                    a.append(lst[c]) 
                    c += 1
            self.mat.append(a) 
  
    def __str__(self): 
        output = ""
        for i in self.mat: 
            for j in i: 
                output += str(j) + " "
            output += '\n'
        return output 
  
    def add(self, mat2): 
        for i in range(self.m): 
            for j in range(self.n): 
                self.mat[i][j] += mat2.mat[i][j] 
  
    def sub(self, mat2): 
        for i in range(self.m): 
            for j in range(self.n): 
                self.m

---
