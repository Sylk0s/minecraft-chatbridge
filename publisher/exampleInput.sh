#!/bin/bash
# exampleInput.sh

# Read a number from the input
read -p 'Enter a number: ' num

# Multiply the number by 5
ans1=$( expr $num \* 5 )

# Give the user the multiplied number
echo $ans1

# Ask the user whether they want to keep going
read -p 'Based on the previous output, would you like to continue? ' doContinue

if [ $doContinue == "yes" ]
then
    echo "Okay, moving on..."
    # [...] more code here [...]
else
    exit 0
fi