# -*- coding: utf-8 -*-

import random
import string
import math
import copy

WORDLIST_FILENAME = 'words.txt'
SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 
                          'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 
                          'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 
                          'p': 3, 'q': 10,'r': 1, 's': 1, 't': 1, 
                          'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 
                          'z': 10,'*': 0}
VOWELS = ['a', 'e', 'i', 'o', 'u']
CONSONANTS = ['b', 'c', 'd', 'f', 'g', 'h', 'j',
              'k', 'l', 'm', 'n', 'p', 'q', 'r',
              's', 't', 'v', 'w', 'x', 'y', 'z']

# end of preparation

# -----------------------------------

# Definition for load_words():
def load_words():
    """
    Loads a list of valid words from a file ‘word.txt’
    """
    inFile = open(WORDLIST_FILENAME, 'r')
    line = str.lower(inFile.read())
    wordlist = line.split()
    return wordlist

# Definition for get_word_score():
def get_word_score(chosen_word, n):
    """
    Calculate the score for a single word
    """
    score = 0
    first_component = 0
    second_component = 0
    for letter in chosen_word:
        first_component += SCRABBLE_LETTER_VALUES[letter]
    second_component = (7 * len(chosen_word) - 3 * (n - 
                       len(chosen_word)))
    second_component = max(second_component,1)
    score = first_component * second_component
    return score

# Definition for get_frequency_dict():
def get_frequency_dict(input_letters):
    """
    Converts words into dictionary representation.
    When given a string of letters as an input, it returns a dictionary where the keys are letters and the values are the number of times that letter is represented in the input string.
    """
    frequency_dict = {}
    for letter in input_letters:
        if letter in frequency_dict:
            continue
        else:
            frequency_dict[letter] = input_letters.count(letter)
    return frequency_dict

# Definition for display_hand():
def display_hand(hand):
    """
    displays a hand represented as a dictionary.
    """
    display = ''
    for letter in hand.keys():
        for i in range (0, hand[letter]):
            display += letter
            display += ' '
    return display

# Definition for deal_hand() with wildcards:
def deal_hand(n):
    """
    Generates a random hand. 
    The function takes as input a positive integer n, and returns a new dictionary representing a hand of n lowercase letters.
    """
    vowel_number = math.ceil(n / 3)
    vowel_list = random.choices(VOWELS, k = vowel_number - 1)
    consonant_list = random.choices(CONSONANTS, k = (n - vowel_number))
    wildcard_list = ['*']
    hand_list = vowel_list + consonant_list + wildcard_list
    deal_dict = {}
    for letter in hand_list:
        if letter in deal_dict:
            continue
        else:
            deal_dict[letter] = hand_list.count(letter)
    return deal_dict

# Definition for update_hand():
def update_hand(hand, chosen_word):
    """
    Remove spelled letters from a hand. 
    The player starts with a full hand of n letters.
    """
    for i in range(0, len(chosen_word)):
        if chosen_word[i] not in hand:
            continue
        else:
           if hand[chosen_word[i]] > 1:
               hand[chosen_word[i]] -= 1
           else:
               del hand[chosen_word[i]]
    return hand

# Definition for is_valid_word() with wildcards
def is_valid_word(chosen_word, wordlist):
    """
    verify that a word given by a player obeys the rules of the game
    """
    verify_result = 0
    if '*' in chosen_word:
        for i in VOWELS:
            chosen_word_new = chosen_word.replace('*', i)
            if chosen_word_new not in wordlist:
                continue
            else:
                verify_result = 1
    else:
        verify_result = (chosen_word in wordlist)
    return bool(verify_result)

# Load the list of words into the variable wordlist
wordlist = load_words()

# Definition for play_hand():
def play_hand(n, hand):
    """
    n: int, hand_size of this hand.
    hand: dict, a hand represented as a dictionary
    
    Starts up an interactive game of Word Game.
    
    * The hand is displayed.
    
    * The user may input a word.
    
    * When any word is entered (valid or invalid), it uses up letters from the hand.
    
    * An invalid word is rejected, and a message is displayed asking the user to choose another word.
    
    * After every valid word: the score for that word is displayed, the remaining letters in the hand are displayed, and the user is asked to input another word.
    
    * The sum of the word scores is displayed when the hand finishes.
    
    * hand finishes when there are no more unused letters.
    
    * The user can also finish playing the hand by inputing two exclamation points (the string '!!') instead of a word.
    
    """
    
    total_points = 0
    chosen_word_points = 0
    while n > 0:
        print('Current Hand: ', display_hand(hand), end = '')
        chosen_word = input("Please enter a word or '!!' to indicate you are done: ").lower()
        letter_outside = 0
        for i in chosen_word:
            if i not in hand:
                letter_outside += 1
        if chosen_word == '!!':
            print('Total score for this hand: ' + str(total_points) 
            + ' points', '\n')
            break
        else:
            if not is_valid_word(chosen_word, wordlist):
                if n == len(chosen_word) :
                    print('That is not a valid word.', '\n')
                    print('Ran out of letters. Total score for this hand: ' + str(total_points))
                    break
                else:
                    print('That is not a valid word. Please choose another word.', '\n')
            else:
                if letter_outside > 0:
                    chosen_word_points = 0
                    print(' Please use letters in the hand. ')
                else:
                    chosen_word_points = get_word_score(chosen_word, n)
                total_points += chosen_word_points
                print('"' + str(chosen_word) + '" earned ' 
                      + str(chosen_word_points) + ' points. Total: ' 
                      + str(total_points) + ' points')
        n -= (len(chosen_word) - letter_outside)
        hand = update_hand(hand, chosen_word)
    if n == 0:
        print('Ran out of letters')
        print('Total score for this hand: ' + str(total_points))
    print('--------------------')
    return total_points

# Definition for substitute_hand():
def substitute_hand(old_hand):
    """
    * Allow the user to replace all copies of one letter in the hand (chosen by user) with a new letter chosen from the VOWELS and CONSONANTS at random.
    
    * The new letter should be different from user's choice, and should not be any of the
letters already in the hand.

    * If user provide a letter not in the hand, the hand should be the same.
    """

    global substitute_number
    choose_letters = string.ascii_lowercase
    sub_choice = input('Would you like to substitute a letter? ')
    if sub_choice == 'yes':
        substitute_number = 0
        replace_letter = input('Which letter would you like to replace: ').lower()
        if replace_letter not in old_hand:
            new_hand = old_hand
        else:
            for i in range(len(choose_letters)):
                if choose_letters[i] not in old_hand:
                    continue
                else:
                    choose_letters = (choose_letters[: i] + '_' 
                                      + choose_letters[i+1: ])
            choose_letters = choose_letters.replace('_', '')
            new_letter = random.choice(choose_letters)
            change_hand = display_hand(old_hand)
            for i in range(len(change_hand)) :
                if change_hand[i] != replace_letter:
                    continue
                else:
                    change_hand = (change_hand[: i] + new_letter 
                                   + change_hand[i+1: ])
            change_hand = change_hand.replace(' ', '')
            new_hand = get_frequency_dict(change_hand)
    else:
        new_hand = old_hand
    return new_hand

def play_game():
    """
    * Allow the user to play a series of hands.
    
    * Asks the user to input a total number of hands.
    
    * Accumulates the score for each hand into a total score for the entire series.

    * For each hand, before playing, ask the user if they want to substitute one letter for another. If the user inputs 'yes', prompt them for their desired letter. This can only be done once during the game.
    
    * For each hand, ask the user if they would like to replay the hand. If the user inputs 'yes', they will replay the hand and keep the better of the two scores for that hand. This can only be done once during the game.

    * If you replay a hand, you do not get the option to substitute a letter - you must play whatever hand you just had.
    
    * Returns the total score for the series of hands

    """
    
    number_of_hands =int(input('Enter total number of hands: '))
    total_game_score = 0
    global substitute_number
    substitute_number = 1
    replay_number = 1
    for i in range(number_of_hands):
        HAND_SIZE = int(input('Enter hand_size of this hand: '))
        initial_hand = deal_hand(HAND_SIZE)
        hand = copy.deepcopy(initial_hand)
        #print('sub', substitute_number,'re', replay_number)
        if substitute_number and replay_number:
            print('Current Hand: ', display_hand(hand))
            hand = substitute_hand(hand)
        #print('sub', substitute_number)
        hand_score = play_hand(HAND_SIZE, hand)
        #print('re', replay_number)
        #print('--------------------')
        if replay_number:
            replay_choice = input('Would you like to replay the hand? ')
            if replay_choice == 'yes':
                replay_number = 0
                hand_score = max(hand_score, 
                                 play_hand(HAND_SIZE, initial_hand))
                #print('--------------------')
            elif i == number_of_hands - 1:
                print('--------------------')
        total_game_score += hand_score
    #print('--------------------')
    print('Total score over all hands: ', total_game_score)
    return

play_game()

