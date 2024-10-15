
def approxEqual(X, Y, RelativeEpsilon, AbsoluteEspilon):
  """
  Parameters passed in data mode: [all of them]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: X, Y and Epsilon are floats
  Postconditions (alterations of program state outside this function): [none]
  Returned result: a Boolean, True if X and Y are equal with absolute tolerance AbsoluteEpsilon
  or with relative tolerance RelativeEpsilon.
  This function is recommended to compare two floating-point numbers. Instead 
  of testing whether they are exactly equal with ==, we test whether they are 
  close enough. For more details, see for example
  https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/
  """
  absX = abs(X)
  absY = abs(Y)
  absdiff = abs(X-Y)
  if (X == Y):
    # Shortcut, handles infinities and the case where both X and Y are exactly 0
    return True
  elif absdiff <= AbsoluteEspilon:
    # The idea of relative difference breaks down near zero.
    # Near zero, it is better to use the absolute difference.
    return True
  else:
    # Use relative error
    largest = max(absX, absY) # if X or Y is exactly 0, we divide by the other one
    return ((absdiff / largest) < RelativeEpsilon)


def approxEqualVect(V1, V2, RelativeEpsilon, AbsoluteEspilon):
  """
  Parameters passed in data mode: [all of them]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: V1 and V2 are lists of floats of the same length
  Postconditions (alterations of program state outside this function): [none]
  Returned result: a Boolean, True if all components of V1 are approximately equal to their 
  counterpart in V2, with absolute tolerance AbsoluteEpsilon
  or with relative tolerance RelativeEpsilon.
  """
  if len(V1) != len(V2):
    return False
  OK = True
  for i in range(len(V1)):
    if not approxEqual(V1[i], V2[i], RelativeEpsilon, AbsoluteEspilon):
      OK = False
      break
  return OK


def strInput(Message, ValidStrings):
  """
  Parameters passed in data mode: [all of them]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: 
   - ValidStrings is a list of acceptable strings
  Postconditions (alterations of program state outside this function): [none]
  Returned result: a string whose value is asked to the user with the Message
  passed as parameter. 
  """
  while True:  
      mystring = input(Message)
      mystring = mystring.strip()
      if mystring in ValidStrings:
        break
      else:
        print('Please type one of the following values:', ", ".join(ValidStrings))
  return mystring
  


def intInput(Message):
  """
  Parameters passed in data mode: [all of them]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: [none]
  Postconditions (alterations of program state outside this function): [none]
  Returned result: an int whose value is asked to the user with the Message
  passed as parameter. 
  """
  while True:
    try:  
      myint = int(input(Message))
      break
    except ValueError as e:
      print('Input error:', str(e))
      print('Please try again!')
  return myint


def floatInput(Message):
  """
  Parameters passed in data mode: [all of them]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: [none]
  Postconditions (alterations of program state outside this function): [none]
  Returned result: a float whose value is asked to the user with the Message
  passed as parameter. 
  """
  while True:
    try:  
      myfloat = float(input(Message))
      break
    except ValueError as e:
      print('Input error:', str(e))
      print('Please try again!')
  return myfloat