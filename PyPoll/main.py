# -*- coding: utf-8 -*-
""" Main.py

Election results calculation module

This module takes a directory path as the argument, and analyzes all CSV files in that directory, calculating
each of the following:
    * The total number of votes cast
    * A complete list of candidates who received votes
    * The percentage of votes each candidate won
    * The total number of votes each candidate won
    * The winner of the election based on popular vote. 

Use cases:
    * If there are no CSVs to process in the supplied directory, the user is alerted to enter another directory
    * If there are CSVs to process, after they are processed, a summary table is printed to the console, and
      output to a text file called "election_results.txt" in the same directory.

Example:

        $ python PyPoll.py "[relative directory]"

        Election Results
        -------------------------
        Total Votes: 620100
        -------------------------
        Rogers: 36.0% (223236)
        Gomez: 54.0% (334854)
        Brentwood: 4.0% (24804)
        Higgins: 6.0% (37206)
        -------------------------
        Winner: Gomez
        -------------------------

        $ ls
        10/27/2017  12:02 AM    <DIR>          ..
        10/27/2017  10:33 AM             4,724 PyPoll.py
        10/27/2017  10:40 AM               583 election_results.txt
        10/26/2017  11:19 PM    <DIR>          raw_data
                    2 File(s)            5,307 bytes
""" 
import sys
import csv
import glob

# ------------------------------------
# ------- FUNCTION DEFINITION  -------
# ------------------------------------
def process_csv(filename):
    """ Given a CSV file with columns in following order - Voter ID, County, Candidate - process the file to:
        * Count the total number of votes in the file
        * Return a list of candidates
    """
    # Open the CSV file in the current iteration
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the header row
        next(csvreader, None)

        # Loop through all rows in the current file
        candidates = []
        for row in csvreader:
            # Add the candidate to a list for this file (assumes the candidate is always the 3rd column)
            candidates.append(row[2])
        
        # Return the whole candidates list for this file
        return candidates

# ------------------------------------
# -------- MAIN PROGRAM BODY  --------
# ------------------------------------
# Parse directory from command-line argument
args = sys.argv
arg_directory = args[1]

# Locate files in directory
csvs_in_path = f"{arg_directory}/*.csv"

# Master candidates list
candidate_list = []

# Loop through all csv files in the specified path and append each file's candidate list to master
#  candidate list
for file in glob.glob(csvs_in_path):
    candidate_list += process_csv(file)

# If we haven't found any CSVs to process, "candidate_list" length will be 0 (alert the user in this case)
num_candidates = len(candidate_list)
if num_candidates == 0:

    print("Please enter a valid directory where we can find CSV files")

# Okay, let's process stats on our master candidates list!
else:
    # Get the unique list of candidates who received votes, and convert it back to an iterable list 
    unique_candidates_set = set(candidate_list)
    unique_candidates_list = list(unique_candidates_set)
 
    # Create dictionaries to store candidate information, and highest votes variable
    candidate_votes = {}
    candidate_percentages = {}
    highest_candidate_votes = 0

    # Loop through all unique candidate names, and determine their count in the master list
    for unique_candidate in unique_candidates_list:
        # Store the number of this candidate's occurrences in the master list
        candidate_vote_count = candidate_list.count(unique_candidate)

        # Keep track of the highest "candidate_vote_count" (for our winner)
        if (candidate_vote_count > highest_candidate_votes):
            highest_candidate_votes = candidate_vote_count
            candidate_leader = unique_candidate

        # Store the number of this candidate's occurrences in the candidate-specific record in "candidate_votes" dictionary
        candidate_votes[unique_candidate] = candidate_vote_count

        # Calculate the percentage of total votes for candidate, and place in another dictionary
        vote_count_total = len(candidate_list)
        candidate_percentages[unique_candidate] = (candidate_vote_count/vote_count_total)*100
    
    # *** Write summary table to variable ***
    summary_table_spacer = "-------------------------\n"
    summary_table = "\nElection Results\n"
    summary_table += summary_table_spacer
    summary_table += f"Total Votes: {str(vote_count_total)}\n"
    summary_table += summary_table_spacer
    # Candidate percentage and vote tally
    for key, value in candidate_percentages.items():
        summary_table += (f"{key}: {str(round(value, 2))}% ({str(candidate_votes[key])})\n")
    summary_table += summary_table_spacer
    summary_table += f"Winner: {candidate_leader}\n"     
    summary_table += summary_table_spacer

    # *** Print summary table to console ***
    print(summary_table)

    # *** Write summary table to file ***
    output_file = open("election_results.txt","w")
    output_file.write(summary_table)
    output_file.close()
