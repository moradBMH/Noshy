###########
# Imports #
###########

# External librairies

import os.path


# Local modules

import myutils
import nutritionDBmodule
import envDBmodule


##############
# Class User #
##############

class User(object):

  def __init__(self, Gender='F', BodyWeight=58,  Height=165,  Age=40, PhysicalActivityLevel='sedentary'):
    """
    Parameters passed in data mode: Gender, BodyWeight, Height, Age, PhysicalActivityLevel
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: self
    Preconditions: 
      - if specified, Gender is either 'F' or 'M'
      - if specified, BodyWeight is an int or a float, in kg
      - if specified, Height is an int, in cm
      - if specified, Age is an int, in years
      - if specified, PhysicalActivityLevel is one of the following strings: 'sedentary', 'light', 'moderate', 'intense', or 'very intense'
    Postconditions: 
      - the attributes of self are initialized to the values passed as parameters, or to default values 
        (40-year-old female of 58 kg and 165 cm with sedentary activity)
    Result: self
    """
    self.gender = Gender
    self.age = Age
    self.body_weight = BodyWeight
    self.height = Height
    self.physical_activity_level = PhysicalActivityLevel 
    self.extra_qty_dict = {}
    self.ratings = {}
    self.env_thresholds = None


  def setPhysiologicalParameters(self):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: If a file called 'physiological_parameters.txt' exists in the current directory,
    then it must contain:
      - on the first line: either 'F' or 'M' (gender)
      - on the second line: an int (age)
      - on the third line: a float (body weight in kg) 
      - on the fourth line: an int (height in cm) 
      - on the fifth line: either 'sedentary', 'light', 'moderate', 'intense', or 'very intense'
    Postconditions : 
      - the attributes gender, age, body_weight, height, physical_activity_level are set to values 
        that were either asked to the user or restored from a backup file
      -  a file called 'physiological_parameters.txt' will be created or overwritten in the current directory
    Returned result: a tuple (gender, age, body_weight, height, physical_activity_level), either restored
    from the backup of the previous execution, or asked to the user
    """
    physiol_params_file_name = 'physiological_parameters.txt'
    if os.path.isfile(physiol_params_file_name):
      yes_or_no = input('Would you like to re-use the physiological parameters of the last execution? (Y/n)? ')
      if yes_or_no.lower() == 'n':   
        self.askPhysiologicalParameters() 
      else:
        physiol_params_file = open(physiol_params_file_name,'r')
        line = physiol_params_file.readline()
        self.gender = line.split()[0]
        line = physiol_params_file.readline()
        self.age = int(line.split()[0])
        line = physiol_params_file.readline()
        self.body_weight = float(line.split()[0])
        line = physiol_params_file.readline()
        self.height = int(line.split()[0])
        line = physiol_params_file.readline()
        self.physical_activity_level  = line.split()[0]
        physiol_params_file.close()  
        print('Gender                  : {0:>5} '.format(self.gender))
        print('Age                     : {0:>5} years'.format(self.age))
        print('Body weight             : {0:5.1f} kg'.format(self.body_weight))
        print('Height                  : {0:>5} cm'.format(self.height))
        print('Physical activity level : {0}'.format(self.physical_activity_level))
    else:
      self.askPhysiologicalParameters()
    
    physiol_params_file = open(physiol_params_file_name,'w')
    physiol_params_file.write(self.gender + '\n')
    physiol_params_file.write(str(self.age) + '\n')
    physiol_params_file.write(str(self.body_weight) + '\n')
    physiol_params_file.write(str(self.height) + '\n')
    physiol_params_file.write(self.physical_activity_level + '\n')
    physiol_params_file.close()   
    



  def askPhysiologicalParameters(self):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: the attributes gender, age, body_weight, height, physical_activity_level
    are set to values asked to the user
    Returned result: [none]
    """
    self.gender =         myutils.strInput('Gender (M for male, F for female): ', ['M', 'F'])
    self.age =            myutils.intInput('Age                              : ')
    self.body_weight =  myutils.floatInput('Body weight (kg)                 : ')
    self.height =         myutils.intInput('Height (cm)                      : ')
    self.physical_activity_level = myutils.strInput('Physical activity level (sedentary, light, moderate, intense, very intense)? ', ['sedentary', 'light', 'moderate', 'intense', 'very intense'])


  def basalMetabolicRate(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Gender is either 'F' or 'M'
      - Age >= 18
      - Height > 0, in centimeters
      - BodyWeight > 0, in kg
    Postconditions (alterations of program state outside this function): 
      - a ValueError exception is thrown if Gender is neither 'F' nor 'M',
        if Age < 18, if Height <= 0 or if BodyWeight <= 0
    Returned result: a float containing the basal metabolic rate in kcal, computed according to   
    (reference: Mifflin MD, St Jeor ST, Hill LA, Scott BJ, Daugherty SA, Koh YO (1990). "A new predictive equation 
    for resting energy expenditure in healthy individuals". The American Journal of Clinical Nutrition. 51 (2): 241–247.)
    """
    if self.gender != 'F' and self.gender != 'M':
      raise ValueError('Gender should be either F or M.')
    if self.age < 18:
      raise ValueError('The computation of basal metabolic rate is currently implemented for adult food requirements, sorry.')
    if self.body_weight < 0:
      raise ValueError('Body weight should be a positive number.')
    if self.height < 0:
      raise ValueError('Height should be a positive integer.')
    BMR = 10*self.body_weight + 6.25*self.height - 5.0*self.age
    if self.gender == 'F':
      BMR -= 161
    elif self.gender == 'M':
      BMR += 5
    return BMR


  def dailyEnergyRequirement(self):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - Gender is either 'F' or 'M'
      - Age > 18
      - Height > 0, in centimeters
      - BodyWeight > 0, in kg
      - Physical activity level is one of the following strings: 'sedentary', 'light', 'moderate', 'intense', 'very intense'
    Postconditions (alterations of program state outside this function): 
      - a ValueError exception is thrown if one of the parameter values is not valid
    Returned result: a float equal to the daily energy requirement in kcal, computed as PhysicalActivityLevel*BasalMetabolicRate.
    """
    if self.physical_activity_level == 'sedentary':
      PAL = 1.4
    elif self.physical_activity_level == 'light':
      PAL = 1.6
    elif self.physical_activity_level == 'moderate':
      PAL = 1.75
    elif self.physical_activity_level == 'intense':
      PAL = 1.9
    elif self.physical_activity_level == 'very intense':
      PAL = 2.1
    else:
      raise ValueError('Physical activity level should be one of "sedentary", "light", "moderate", "intense", "very intense"')
    return PAL*self.basalMetabolicRate()



  def getExtraQuantity(self, Extra):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
    - Extra exists as a key in self.extra_qty_dict
    Postconditions: [none]
    Returned result: the typical serving serving of Extra fro this user
    """
    return self.extra_qty_dict[Extra]
  

  def askRatings(self, NutrDB):
    """
    Parameters passed in data mode: NutrDB
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
    - NutrDB is a complete and consistent NutritionDatabase instance
    Postconditions: self.ratings is a dictionary associating the user rating (asked to the user)
    to each food in the database
    Returned result: [none]
    """
    self.ratings = {}
    for food in NutrDB.getAllFoods():
      rating = myutils.intInput('How much do you like ' + food + ' (from 0 to 5)? ' )
      self.ratings[food] = rating



  def setRatings(self, NutrDB):
    """
    Parameters passed in data mode: NutrDB
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - NutrDB is a complete and consistent NutritionDatabase instance
      - if the current directory contains a file called ratings.txt,
        then this file must contain one line for each food, with the food name and 
        the associated rating separated by a tabulation character
    Postconditions: 
      - self.ratings is a dictionary associating the user's rating
        to each food listed in NutrDB
      - a file called ratings.txt is created in the current directory
    Result: [none]
    """
    ratings_file_name = 'ratings.txt'
    if os.path.isfile(ratings_file_name):
      yes_or_no = input('Would you like to re-use the food ratings from last execution? (Y/n)? ')
      if yes_or_no.lower() == 'n':   
        self.askRatings(NutrDB)
      else:
        ratings_file = open(ratings_file_name,'r')
        self.ratings = {}
        for line in ratings_file:
          items = line.split('\t')
          food = items[0]
          rating = int(items[1])
          self.ratings[food] = rating
        ratings_file.close()
        for food in self.ratings:
          print('{0:<25} : {1} '.format(food, self.ratings[food]))
        for food in NutrDB.getAllFoods():
          if food not in self.ratings:
            print('No saved rating for', food, '.')
            rating = myutils.intInput('How much do you like ' + food + ' (from 0 to 5)? ' )
            self.ratings[food] = rating
    else:
      self.askRatings(NutrDB)

    ratings_file = open(ratings_file_name,'w')  
    for (food, rating) in self.ratings.items():
      ratings_file.write(food + "\t" + str(rating) + '\n')
    ratings_file.close()   
      



  def askExtraQuantities(self, NutrDB):
    """
    Parameters passed in data mode: NutrDB
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
    - NutrDB is a complete and consistent NutritionDatabase instance
    Postconditions: self.extra_qty_dict is a dictionary associating the typical serving size (asked to the user)
    to each food listed in self.extras
    Returned result: [none]
    """
    self.extra_qty_dict = {}
    for extra in NutrDB.extras:
      qty = myutils.floatInput('What is the typical serving for ' + extra + ' (in L or kg)? ' )
      self.extra_qty_dict[extra] = qty


  def setExtraQuantities(self, NutrDB, ExtraQtyDict=None):
    """
    Parameters passed in data mode: NutrDB, ExtraQtyDict
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - NutrDB is a complete and consistent NutritionDatabase instance
      - if a parameter ExtraQtyDict is passed, then each food is self.extras must exist
        as a key in ExtraQtyDict 
      - if the current directory contains a file called extra_serving_sizes.txt,
        then this file must contain one line for each food, with the food name and 
        the associated quantity separated by a tabulation character
    Postconditions: 
      - self.extra_qty_dict is a dictionary associating the typical serving size 
        to each food listed in NutrDB.extras
      - if a parameter ExtraQtyDict is passed, then self.extra_qty_dict is simply 
        set with it; otherwise, is is either restored from a backup or asked to the user
      - a file called extra_serving_sizes.txt is created in the current directory
    Result: [none]
    """
    extra_serving_sizes_file_name = 'extra_serving_sizes.txt'
    if ExtraQtyDict is not None:
      for food in NutrDB.extras:
        if food not in ExtraQtyDict:
          print('Warning: The passed dictionary does not contain an entry for ' + food)
      self.extra_qty_dict = ExtraQtyDict
    else:
      if os.path.isfile(extra_serving_sizes_file_name ):
        yes_or_no = input('Would you like to re-use the extra serving sizes from last execution? (Y/n)? ')
        if yes_or_no.lower() == 'n':   
          self.askExtraQuantities(NutrDB)
        else:
          extra_serving_sizes_file = open(extra_serving_sizes_file_name,'r')
          self.extra_qty_dict = {}
          for line in extra_serving_sizes_file:
            items = line.split('\t')
            extra = items[0]
            qty = float(items[1])
            self.extra_qty_dict[extra] = qty
          extra_serving_sizes_file.close()
          for extra in self.extra_qty_dict:
            print('{0:<25} : {1:5.3f} '.format(extra, self.extra_qty_dict[extra]))
          for extra in NutrDB.extras:
            if extra not in self.extra_qty_dict:
              print('No saved serving size for', extra, '.')
              qty = myutils.floatInput('What is the typical serving for ' + extra + ' (in L or kg)? ' )
              self.extra_qty_dict[extra] = qty
      else:
        self.askExtraQuantities(NutrDB)

    extra_serving_sizes_file = open(extra_serving_sizes_file_name,'w')  
    for (extra, qty) in self.extra_qty_dict.items():
      extra_serving_sizes_file.write(extra + "\t" + str(qty) + '\n')
    extra_serving_sizes_file.close()   
      



  def askEnvironmentalThresholds(self):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: 
      - self.env_thresholds, an instance of class EnvironmentalImpact, is defined with maximal values asked to the user 
    Returned result: [none]
    """
    self.env_thresholds = envDBmodule.EnvironmentalImpact() 
    self.env_thresholds.land_use              = myutils.floatInput('Please define the maximal land use per meal (square meters)           : ')
    self.env_thresholds.GHG_emissions         = myutils.floatInput('Please define the maximal GHG emissions per meal (kg CO2 eq.)         : ')
    self.env_thresholds.acidifying_emissions  = myutils.floatInput('Please define the maximal acidifying emissions per meal (g SO2 eq.)   : ')
    self.env_thresholds.eutrophying_emissions = myutils.floatInput('Please define the maximal eutrophying emissions per meal (g PO43- eq.): ')
    self.env_thresholds.water_use             = myutils.floatInput('Please define the maximal water use per meal (L)                      : ')



  def setEnvironmentalThresholds(self):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: If a file called 'environmental_thresholds.txt' exists in the current directory,
    then it must contain:
      - on the first line: a float corresponding to the maximal land use per meal (square meters)
      - on the second line: a float corresponding to the maximal GHG emissions per meal (kg CO2 eq.)
      - on the third line: a float corresponding to the maximal acidifying emissions per meal (g SO2 eq.)
      - on the fourth line: a float corresponding to the maximal eutrophying emissions per meal (g PO43- eq.)
      - on the fifth line: a float corresponding to the maximal water use per meal (L)
    Postconditions: 
      - self.env_thresholds, an instance of class EnvironmentalImpact, is defined with maximal values asked to the user 
        or restored from the backup file
      - a file called 'environmental_thresholds.txt' will be created or overwritten in the current directory
    Returned result: a tuple (max_land_use, max_GHG_emissions, max_acidifying_emissions, max_eutrophying_emissions, max_water_use),
    either restored from the backup of the previous execution, or asked to the user
    """
    env_thresholds_file_name = 'environmental_thresholds.txt'
    self.env_thresholds = envDBmodule.EnvironmentalImpact()
    if os.path.isfile(env_thresholds_file_name):
      yes_or_no = input('Would you like to re-use the environmental thresholds of the last execution? (Y/n)? ')
      if yes_or_no.lower() == 'n':   
        self.askEnvironmentalThresholds() 
      else:
        self.env_thresholds.loadFromFile(env_thresholds_file_name) 
        print('Here are your environmental thresholds (maximal values per meal):')
        self.env_thresholds.printToScreen()
    else:
      self.askEnvironmentalThresholds()
    
    self.env_thresholds.saveToFile(env_thresholds_file_name)
  
    




################
# Main program #
################


if __name__ == "__main__":
  # The program below (unit tests) will be run only if the Python interpreter is launched with energyrequirement.py as an argument,
  # not if this file is included as a module in another main program.

  abseps = 1e-15
  releps = 1e-6

  ####################################
  # Unit tests of basalMetabolicRate #
  ####################################


  print("Unit tests of User.basalMetabolicRate:")

  try:
    my_user = User('X', 60, 165, 40, 'light')
    print(my_user.basalMetabolicRate())
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (wrong Gender)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)

  try:
    my_user = User('F', 60, 165, 15, 'light')
    print(my_user.basalMetabolicRate())
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (Age < 18)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)

  try:
    my_user= User('F', -6, 165, 40, 'light')
    print(my_user.basalMetabolicRate())
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (BodyWeight < 0)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)


  try:
    my_user = User('F', 60, -165, 40, 'light')
    print(my_user.basalMetabolicRate())
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (Height < 0)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)

  try:
    my_user = User('F', 60, 165, 40, 'light')
    bmr = my_user.basalMetabolicRate()
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(False) # throwing a ValueError exception is not the expected behavior here 
  else:
    # code that must be executed if the try clause does not raise an exception
    print(myutils.approxEqual(bmr, 1270.25, releps, abseps))

  try:
    my_user = User('M', 60, 165, 40, 'light')
    bmr = my_user.basalMetabolicRate()
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(False) # throwing a ValueError exception is not the expected behavior here 
  else:
    # code that must be executed if the try clause does not raise an exception
    print(myutils.approxEqual(bmr, 1436.25, releps, abseps))



  ########################################
  # Unit tests of dailyEnergyRequirement #
  ########################################

  print("Unit tests of User.dailyEnergyRequirement:")

  try:
    my_user = User('F', 60, 165, 40, 'lalala')
    der = my_user.dailyEnergyRequirement()
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (invalid value for PhysicalActivityLevel)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)


  try:
    my_user = User('F', 60, 165, 40, 'light')
    der = my_user.dailyEnergyRequirement()
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(False) # throwing a ValueError exception is not the expected behavior here 
  else:
    # code that must be executed if the try clause does not raise an exception
    print(myutils.approxEqual(der, 2032.4, releps, abseps))



  ####################################
  # Unit tests of setExtraQuantities #
  ####################################

  print('Unit tests of User.setExtraQuantities:')

  my_user = User('F', 60, 165, 40, 'light')
  myDB = nutritionDBmodule.NutritionDatabase()
  
  my_user.setExtraQuantities(myDB, {'Beet Sugar': 0.012, 'Coffee': 0.008, 'Dark Chocolate': 0.020})
  print(my_user.extra_qty_dict == {'Beet Sugar': 0.012, 'Coffee': 0.008, 'Dark Chocolate': 0.020})

  my_user.setExtraQuantities(myDB)
  print(my_user.extra_qty_dict)


