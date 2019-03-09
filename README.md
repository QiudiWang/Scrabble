# Scrabble
This is a word game that players can construct words using letters provided to them from the and win the score.

Here is the game architecture:
1. A player is dealt with a hand of HAND_SIZE letters of the alphabet, chosen at random and th playe arranges the hand into as 
   many words as they want out of the letters but using each letter at most once.
2. If the player guesses a word that is invalid, either because it is not a real word or because they used letters that they 
   don't actually have in their hand, they still lose the letters from their hand that they did guess as a penalty.
3. If the player guesses a word that is valid in the word list, s/he would win a score which would be displayed until all the    
   letters are used up or the player choose to end the game.

Here are the game rules:
1. The hand is displayed, and the HAND_SIZE is set by the user.
2. The score for the hand is the sum of the score for each word formed.
   (1) First component: the sum of the points for letters in the word.
   (2) Second component: either [7 * word_length - 3 * (n-word_length)] or 1, whichever value is greater, where:
       word_length is the number of letters used in the word.
       n is the number of letters available in the current hand (it can be integer value from 1 to 10).
3. An asterisk (*) is denoted in the hand, and it can pnly replace vowels. The player does not receive any points for using the "*" (unlike all the other letters), though it does count as a used or unused letter when scoring.

Let's enjoy the word game!!
