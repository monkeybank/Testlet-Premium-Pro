'''
Testlet Premium Pro
By: Luke Goddard

Ever get tired of the big coroprations charging you inordinate amounts of 
money just to study for flashcards? Well, fret no longer because Teslet is
the ultimate terminal-based study tool for students and lifelong learners
alike. I may be overselling it a little bit, but who cares? It's free.
'''

import csv
import os
import random
from tabulate import tabulate
from termcolor import colored

def clear_terminal():
  '''
  Clears the terminal screen and scroll back to present
  the user with a nice clean, new screen. Useful for managing
  menu screens in terminal applications.
  '''
  os.system('cls' if os.name == 'nt' else 'clear')

def csv_to_list(csv_file):
  '''
  Function to open csv file and pop out the headers.
  '''
  with open(csv_file, mode='r') as open_csv_file:
    csv_list = list(csv.reader(open_csv_file))
  headers = csv_list.pop(0)
  return csv_list,headers

def free_response(flashcard_csv,answer_with='back',order='random',num_cards='all'):
  '''
  Test yourself on a flashcard set using free response questions
  answering with front or back, either in order of the set file 
  or a random order, and with all or a subset of the cards 
  avaliable.
  '''
  # creates a list with the flashcards and a list with the categories
  set_list,headers = csv_to_list(flashcard_csv)

  # applies user parameters to the flashcard list
  if answer_with == 'front':
    headers = list(reversed(headers))
    set_list = [list(reversed(card)) for card in set_list]
  if not order == 'normal':
    random.shuffle(set_list)
  if num_cards == 'all' or num_cards>len(set_list):
    num_cards = len(set_list)

  # variables to track user stats
  num_correct = 0
  missed_cards = []
  incorrect_answers = []

  # iterates through flashcard list and asks the user for answers
  for index,flashcard in enumerate(set_list):
    clear_terminal()
    print(f'You will be given the {headers[0]}\nPlease answer with the {headers[1]}')

    # takes user input for the answer
    user_answer = input(f'\n{flashcard[0]}: ').lower()

    # checks whether user input is correct, incorrect, or quit
    if user_answer == '/quit':
      num_cards = index
      break
    if user_answer == flashcard[1].lower():
      print(colored('Correct','green'))
      num_correct += 1
    else:
      print(f'{colored("Incorrect","red")}, Correct Answer: {colored(flashcard[1],"green")}')
      missed_cards.append(flashcard)
      incorrect_answers.append(user_answer)
    input()
    if (index+1)==num_cards: break
  
  # synthesizes missed cards and incorrect answers into one list for display purposes
  missed_cards_and_incorrect_answers = [[missed_cards[i][0],colored(incorrect_answers[i],'red'),colored(missed_cards[i][1],'green')] for i in range(len(incorrect_answers))]
  missed_cards_and_incorrect_answers = [['Card','You answered','Correct answer']] + missed_cards_and_incorrect_answers
  
  # displays the number of questions the user answered correctly and displays incorrect answers
  clear_terminal()
  print(f'You scored {num_correct}/{str(num_cards)}')
  print(f'Take a look at the cards you missed\n')
  print(f'{tabulate(missed_cards_and_incorrect_answers,headers="firstrow")}')
  input()
  
def main():
  # creates a dictionary to access flashcard csv files
  flashcard_sets = {'poly ions': 'common_polyatomic_ions_and_acids.csv'}

  # acquires user input to configure testing mode
  clear_terminal()
  while True:
    try:
      print(f'{tabulate(list(flashcard_sets.items()),headers=["Keyword","File Name"])}')
      flashcard_set = flashcard_sets[input('\nChoose a flashcard set using its keyword: ')]
      break
    except KeyError:
      clear_terminal()
      print('Not a valid keyword\n')

  clear_terminal()
  answer_with_side = input('Choose a side to answer with (front or back): ').lower()

  clear_terminal()
  flashcard_order = input('Choose an order (normal or random): ')

  # calls main testing function
  free_response(flashcard_set,answer_with_side,flashcard_order)

main()