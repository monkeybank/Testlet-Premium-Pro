'''
Testlet Premium Pro
By: Luke Goddard

Ever get tired of the big coroprations charging you inordinate amounts of 
money just to study for flashcards? Well, fret no longer because Teslet is
the ultimate terminal-based study tool for students and lifelong learners
alike. I may be overselling it a little bit, but who cares? It's free.

 _              _ _                                                       
| |   _   _  __| (_) ___ _ __ ___  _   _ ___                              
| |  | | | |/ _` | |/ __| '__/ _ \| | | / __|                             
| |__| |_| | (_| | | (__| | | (_) | |_| \__ \                             
|_____\__,_|\______|\___|_|  \___/ \__,_|___/  ____                       
/ ___|  ___  / _| |___      ____ _ _ __ ___   / ___|_ __ ___  _   _ _ __  
\___ \ / _ \| |_| __\ \ /\ / / _` | '__/ _ \ | |  _| '__/ _ \| | | | '_ \ 
 ___) | (_) |  _| |_ \ V  V / (_| | | |  __/ | |_| | | | (_) | |_| | |_) |
|____/ \___/|_|  \__| \_/\_/ \__,_|_|  \___|  \____|_|  \___/ \__,_| .__/ 
                                                                   |_|    
                                                      all rights reserved
'''

import csv
import os
import sys
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

def find_files_in_folder(folder_path):
  files = os.listdir(folder_path)
  return files

def get_script_directory_path():
  return os.path.dirname(os.path.realpath(sys.argv[0]))

def csv_to_list(csv_file):
  '''
  Function to open csv file and pop out the headers.
  '''
  with open(csv_file, mode='r') as open_csv_file:
    csv_list = list(csv.reader(open_csv_file))
  headers = csv_list.pop(0)
  return csv_list,headers

def get_user_testing_options(flashcard_sets):
  # acquires user input to choose flashcard set
  clear_terminal()
  while True:
    try:
      print(f'{tabulate(list(flashcard_sets.items()),headers=["Index","File Name"])}')
      flashcard_set = flashcard_sets[input('\nChoose a flashcard set using its index: ')]
      break
    except KeyError:
      clear_terminal()
      print('Not a valid index\n')
  cards_in_set = len(csv_to_list(flashcard_set)[0])

  # asks user if they want to use default settings or customize them
  clear_terminal()
  while True:
    print('1 - use default settings')
    print('2 - customize settings')
    use_default_settings = input('\nEnter choice: ')
    if use_default_settings in ['1','2']:
      break
    elif use_default_settings == '':
      use_default_settings = '1'
      break
    elif use_default_settings == '/quit':
      main()
      quit()
    else:
      clear_terminal()
      print('Not a valid input\n')

  if use_default_settings == '1':
    answer_with_side = '1'
    flashcard_order = '1'
    num_cards_to_study = cards_in_set
  elif use_default_settings == '2':
    # acquires user input to choose answer mode
    clear_terminal()
    while True:
      print('1 - answer with back of flashcard')
      print('2 - answer with front of flashcard')
      answer_with_side = input('\nEnter choice: ')
      if answer_with_side in ['1','2']:
        break
      elif answer_with_side == '':
        answer_with_side = '1'
        break
      elif answer_with_side == '/quit':
        main()
        quit()
      else:
        clear_terminal()
        print('Not a valid input\n')

    # acquires user input to choose flashcard order
    clear_terminal()
    while True:
      print('1 - answer flashcards in random order')
      print('2 - answer flashcards in normal order')
      flashcard_order = input('\nEnter choice: ')
      if flashcard_order in ['1','2']:
        break
      elif flashcard_order == '':
        flashcard_order = '1'
        break
      elif flashcard_order == '/quit':
        main()
        quit()
      else:
        clear_terminal()
        print('Not a valid input\n')

    # aquires user input to choose number of flashcards to study
    clear_terminal()
    while True:
      print(f'Choose number of flashcards to study. Chosen set contains {cards_in_set} flashcards')
      print('Press enter or type "all" to sudy all cards in set')
      num_cards_to_study = input('\nEnter choice: ')
      if num_cards_to_study in [str(x+1) for x in range(cards_in_set)]:
        num_cards_to_study = int(num_cards_to_study)
        break
      elif num_cards_to_study == '' or num_cards_to_study.lower() == 'all':
        num_cards_to_study = cards_in_set
        break
      elif num_cards_to_study == '/quit':
        main()
        quit()
      else:
        clear_terminal()
        print('Not a valid input\n')

  return flashcard_set, answer_with_side, flashcard_order, num_cards_to_study

def free_response(set_list,headers,answer_with,order,num_cards):
  '''
  Test yourself on a flashcard set using free response questions
  answering with front or back, either in order of the set file 
  or a random order, and with all or a subset of the cards 
  avaliable.
  '''
  # applies user parameters to the flashcard list
  if answer_with == '2':
    headers = list(reversed(headers))
    set_list = [list(reversed(card)) for card in set_list]
  if order == '1':
    random.shuffle(set_list)

  # variables to track user stats
  num_correct = 0
  missed_cards = []
  incorrect_answers = []
  num_cards_tested = num_cards

  # iterates through flashcard list and asks the user for answers
  for index,flashcard in enumerate(set_list):
    clear_terminal()
    print(f'You will be given the {headers[0]}\nPlease answer with the {headers[1]}')

    # takes user input for the answer
    user_answer = input(f'\n{flashcard[0]}: ').lower().strip()

    # checks whether user input is correct, incorrect, or quit
    if user_answer == '/quit':
      num_cards_tested = index
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
  print(f'You scored {num_correct}/{str(num_cards_tested)}')
  if missed_cards:
    print(f'Take a look at the cards you missed\n')
    print(f'{tabulate(missed_cards_and_incorrect_answers,headers="firstrow")}')

  # asks the user if they want to study again
  print('\n1 - study set again')
  if missed_cards:
    print('2 - study missed answers')
  print('any other key - quit studying')
  study_again_choice = input('\nEnter choice: ')
  if study_again_choice == '1':
    free_response(set_list,headers,'',order,num_cards)
  elif study_again_choice == '2' and missed_cards:
    free_response(missed_cards,headers,'',order,len(missed_cards))
  
def main():
  # creates a dictionary to access flashcard csv files automatically from a given directory
  files_in_folder = find_files_in_folder(get_script_directory_path())
  csv_files_in_folder = [file for file in files_in_folder if file.endswith('.csv')]
  flashcard_sets = dict([str(index+1),file] for index,file in enumerate(csv_files_in_folder))

  flashcard_set, answer_with_side, flashcard_order, num_cards_to_study = get_user_testing_options(flashcard_sets)

  # creates a list with the flashcards and a list with the categories
  set_list,headers = csv_to_list(flashcard_set)

  # calls main testing function
  free_response(set_list,headers,answer_with_side,flashcard_order,num_cards_to_study)

main()