import os

# List of video titles and their desired order
video_titles = [
    "Flow of Program - Flowcharts & Pseudocode",
    "Introduction to Java - Architecture & Installation",
    "First Java Program - Input/Output, Debugging and Datatypes",
    "Conditionals and Loops + Calculator Program",
    "Switch Statements + Nested Case in Java",
    "Functions / Methods in Java",
    "Introduction to Arrays and ArrayList in Java",
    "Linear Search Algorithm - Theory + Code + Questions",
    "Binary Search Algorithm - Theory + Code",
    "Binary Search Interview Questions - Google, Facebook, Amazon",
    "Binary Search in 2D Arrays",
    "Bubble Sort Algorithm - Theory + Code",
    "Selection Sort Algorithm - Theory + Code",
    "Insertion Sort Algorithm - Theory + Code",
    "Cycle Sort - Amazon, Google, Microsoft Interview Questions",
    "Strings and StringBuilder in Java",
    "Solve Any Pattern Question With This Trick!",
    "Introduction to Recursion - Learn In The Best Way",
    "Time and Space Complexity COMPLETE Tutorial - What is Big O?",
    "Bitwise Operators + Number Systems - Maths for DSA",
    "Maths for Data Structures & Algorithms",
    "Recursion - Level 1 Questions (Theory + Code + Tips)",
    "Recursion - Array Questions (Theory + Code + Tips)",
    "Recursion - Pattern Questions + Bubble Sort + Selection Sort",
    "Merge Sort Using Recursion (Theory + Complexity + Code)",
    "Quick Sort Using Recursion (Theory + Complexity + Code)",
    "Recursion Subset, Subsequence, String Questions",
    "Recursion - Permutations (Theory + Code + Tips)",
    "Recursion Google, Amazon Questions: Dice Throw & Letter Combinations of a Phone Number",
    "Backtracking Introduction + Maze Problems - Theory + Code + Tips",
    "N-Queens, N-Knights, Sudoku Solver (LeetCode) - Backtracking Questions",
    "OOP 1 | Introduction & Concepts - Classes, Objects, Constructors, Keywords",
    "OOP 2 | Packages, Static, Singleton Class, In-built Methods",
    "OOP 3 | Principles - Inheritance, Polymorphism, Encapsulation, Abstraction",
    "OOP 4 | Access Control, In-built Packages, Object Class",
    "OOP 5 | Abstract Classes, Interfaces, Annotations",
    "OOP 6 | Generics, Custom ArrayList, Lambda Expressions, Exception Handling, Object Cloning",
    "OOP 7 | Collections Framework, Vector Class, Enums in Java",
    "Linked List Tutorial - Singly + Doubly + Circular (Theory + Code + Implementation)",
    "Linked List Interview Questions - Google, Facebook, Amazon, Microsoft",
    "Stacks and Queues Complete Tutorial - Theory + Implementation + Types (Dynamic, Circular)",
    "Stacks and Queues Interview Questions - Google, Facebook, Amazon, Microsoft",
    "Tic Tac Toe Java Game in Under 15 Minutes",
    "Binary Trees Tutorial - Introduction + Traversals + Code | Binary Search Trees (BST)",
    "AVL Trees Tutorial | Self Balancing Binary Search Trees",
    "Segment Trees Tutorial | Range Queries | Interview Questions",
    "StringBuffer in Java | Data Formatting | Working With Large Data",
    "BigInteger & BigDecimal - Handling Large Numbers in Java",
    "File Handling in Java Complete Course",
    "Binary Tree Questions for Technical Interviews - Google, Facebook, Amazon, Microsoft",
    "Introduction to Heap Data Structure + Priority Queue + Heapsort Tutorial",
    "Introduction to HashMap & HashTable in Java",
    "Karp-Rabin String Matching Algorithm | Substring Search Pattern",
    "Count Sort Algorithm - Theory + Code",
    "Radix Sort Algorithm - Theory + Code",
    "Huffman Coding Greedy Algorithm | Text Compression",
    "Easily Solve Range Query Interview Problems with Square Root Decomposition/Mo's Algorithm",
    "Binary Tree from Preorder & Inorder Traversal - Advance Tree Questions",
    "Vertical Order Traversal of a Binary Tree - Google Interview Question",
    "Word Ladder - LeetCode Hard - Google Phone Screen Interview Question",
    "Two Sum IV - Google, Amazon, Facebook Interview Question",
    "Kth Smallest Element in a BST - Google, Amazon, Facebook Interview Question"
]

# Get the current directory
current_dir = "Z:\Other Videos\Educational\DSA"

# Counter for serial number
serial_number = 1

# Loop through video titles and rename files
for title in video_titles:
    # Find the matching video file
    for filename in os.listdir(current_dir):
        if filename.startswith(title):
            # Rename the file with serial number
            new_filename = f"{serial_number:03d} - {title}.mp4"
            os.rename(os.path.join(current_dir, filename),
                      os.path.join(current_dir, new_filename))
            serial_number += 1
            break

print("Videos renamed successfully!")
