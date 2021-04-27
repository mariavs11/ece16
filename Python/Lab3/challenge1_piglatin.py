import enchant as e
dictionary = e.Dict('en_US')
dictionary.check('quarter') # this will return True
dictionary.check('dsa;lojawsoefi;wq') # this will return False

# english to pig latin
vowel_list = 'aeiouAEIOU'



def secondstep1(my_string):
    i = -1
    a = -1
    b = -1

    # creates variable 'end' for punctuation, assuming word ends with punctuation
    # saves punctuation for further usage
    if my_string.endswith('?'):
        end = my_string[-1] # saves '.' in end

        my_string= my_string[:-1] # removes punctuation from string
    elif my_string.endswith('!'):
        end = my_string[-1] # saves '.' in end

        my_string= my_string[:-1] # removes punctuation from string

    elif my_string.endswith('.'):
        end = my_string[-1] # saves '.' in end
        my_string= my_string[:-1] # removes punctuation from string
    else:
      end = 0 # word does not end with punctuation

    if (('qu') in my_string[0:2])or (('Qu') in my_string[0:2]) or (('QU') in my_string[0:2])or (('qU') in my_string[0:2]): # checks if word starts with qu
        i+=2 # i=1

        for x in my_string[2:]: # iterates through string beginning after qu encountered
        # now check for consonant
            i+= 1
            if (x in vowel_list) or (x == 'Y') or (x == 'y'):  # checking from left to right if vowel is encountered
              #in such case :
              pieceofword = my_string[i:]
              anotherpiece = my_string[0:i]
              my_string = pieceofword + anotherpiece
              my_string+= "ay"

              if end == 0 : # if punctuation present add to the end
                  return my_string
              my_string+=end
              return my_string
    if my_string[0] =='y' or my_string[0] =='Y':
        for x in my_string: # iterates
        # now check for consonant
            a+= 1
            if x in vowel_list:
                pieceofword = my_string[a:]
                anotherpiece = my_string[0:a]
                my_string = pieceofword + anotherpiece
                my_string += "ey"
                if end == 0  : # if punctuation present add to the end
                    return my_string
                my_string+= end
                return my_string

    if my_string[0] in vowel_list:
        my_string += "yay"
        if end == 0:  # if punctuation present add to the end
            return my_string
        my_string += end
        return my_string

    else:
        for x in my_string: # iterates
        # now check for consonant
            b+= 1
            if (x in vowel_list) or (x == 'Y') or (x == 'y') :
                pieceofword = my_string[b:]
                anotherpiece = my_string[0:b]
                my_string = pieceofword + anotherpiece
                my_string+= "ay"

                if end == 0 :  # if punctuation present add to the end
                    return my_string
                my_string+= end
                return my_string

def english_to_pig_latin(my_string):
     if "-" in my_string:

        my_string =my_string.split('-') # creates list with 2 strings
        # call function for each string
        x = secondstep1(my_string[0])  # gets translation back
        y = secondstep1(my_string[1])  # gets translation back
        my_string = x +'-' + y       # adds them together
        return my_string
     else:
        z = secondstep1(my_string)
        return z






def secondstep2(my_string):
    #check if word ends with ey, ay or yay
    i=0
    if my_string.endswith('?'):
        end = my_string[-1] # saves '?' in end
        my_string= my_string[:-1] # removes punctuation from string

    elif my_string.endswith('!'):
        end = my_string[-1] # saves '!' in end
        my_string= my_string[:-1] # removes punctuation from string

    elif my_string.endswith('.'):
        end = my_string[-1] # saves '.' in end
        my_string= my_string[:-1] # removes punctuation from string
    else:
      end = 0 # word does not end with punctuation

    # checks if word ends with ey, ay or yay
    if my_string.endswith("ey"):
        # remove ey
        my_string = my_string[:-2]
    elif my_string.endswith("yay"):
        my_string = my_string[:-3]
        return my_string

    elif my_string.endswith("ay"):
        my_string = my_string[:-2]
    for x in my_string:
        i-=1 # starts with i=-1


        pieceofword = my_string[i:]

        otherpiece = my_string[:i]

        translated = pieceofword + otherpiece
        fordict = translated.casefold() # changes the letters to lower case
        if dictionary.check(fordict):
            if end == 0:

              return translated
            else:
                translated+= end
                return translated



def pig_latin_to_english(my_string):
    if "-" in my_string:
        my_string = my_string.split('-')
        x = secondstep2(my_string[0])
        y = secondstep2(my_string[1])
        z = x + '-' + y
        return z
    else:
        z = secondstep2(my_string)
        return z





