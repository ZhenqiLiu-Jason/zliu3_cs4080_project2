Here is how to get the plots and data:

Requirements:
1. Make sure you have Python as a command.
2. Make sure you have numpy and matplotlib Python environments.
3. Make sure you have other modules installed.
    Run the code and see what is missing.


Steps:

# Go to the sources directory
cd sources

# Find out what are the arguments
python main.py -h

# Run the code by typing the following
# --time_limit specifies how long the simulation should be 
# The longer, the more accurate the optimal choice suggestion would be

# --weights specifies the probability for each face
# If not weights are specified, all dice will be fair

python main.py --time_limit 10000 --weights 1,3,1,1,1,1


