
###########
# Imports #
###########

# External librairies

import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Local modules

import myutils
import nutritionDBmodule
import envDBmodule


##############
# Class Meal #
##############

class Meal(object):

  def __init__(self, Foods, Quantities=None):
    """
    Parameters passed in data mode: Foods, Quantities
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: self
    Preconditions: 
      - if specified, Foods is a list of 6 strings, containing (in the following order) :
        a source of protein, a source of carbohydrates, a source of fat, a vegetable,
        a fruit and an extra 
      - if specified, Quantities is a list of 6 floats, giving the quantity of each meal
        component in the same units as in class NutritionDatabase (typically kg or L)
    Postconditions: 
      - the attributes of self are initialized
    Result: self
    """
    self.protein_source = Foods[0]
    self.carb_source = Foods[1]
    self.fat_source = Foods[2]
    self.vegetable = Foods[3]
    self.fruit = Foods[4]
    self.extra = Foods[5]
    self.is_nutritionally_valid = None
    self.impact = envDBmodule.EnvironmentalImpact()
    self.rating = 0
    if Quantities == None:
      self.protein_source_qty = None
      self.carb_source_qty = None
      self.fat_source_qty = None
      self.vegetable_qty = None
      self.fruit_qty = None
      self.extra_qty = None
    else:
      self.protein_source_qty = Quantities[0]
      self.carb_source_qty = Quantities[1]
      self.fat_source_qty = Quantities[2]
      self.vegetable_qty = Quantities[3]
      self.fruit_qty = Quantities[4]
      self.extra_qty = Quantities[5]


  def getFoods(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none]
    Result: a list of 6 strings containing (in this order): the source of protein, the source of carbohydrates, 
    the source of fat, the vegetable, the fruit and the extra 
    """
    return [self.protein_source, self.carb_source, self.fat_source, self.vegetable, self.fruit, self.extra]

  def getQuantities(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none]
    Result: a list of 6 floats containing the quantities of (in this order): the source of protein, the source of carbohydrates, 
    the source of fat, the vegetable, the fruit and the extra 
    """
    return [self.protein_source_qty, self.carb_source_qty, self.fat_source_qty, self.vegetable_qty, self.fruit_qty, self.extra_qty]


  def computeQuantities(self, MealKcalTarget, NutrDB, ExtraQtyDict):
    """
    Parameters passed in data mode: MealKcalTarget, NutrDB
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - Each meal component must exist as a key in NutrDB
      - The extra must exist as a key in ExtraQtyDict
    Postconditions: 
      - self.is_nutritionally_valid is set to True if we can reach if MealKcalTarget with 
        positive quantities of each component, or to False otherwise
      - if the meal is nutritionnally valid, then the quantity of each meal component 
        is set to the value that allows to:
           - reach exactly MealKcalTarget kcal for the whole meal
           - have 200g of vegetable
           - have 100g of fruit
           - have the extra quantity defined in ExtraQtyDict
           - have 15% of meal kcal should come from proteins
           - have 55% of meal kcal should come from carbs
           - have 30% of meal kcal should come from fat
    Result: [None]
    """

    # A meal should contain 200g of vegetable
    vegetable_qty = 0.200
    kcal_from_vegetable = NutrDB.getKcal(self.vegetable, vegetable_qty)
    prot_from_vegetable = NutrDB.getGProt(self.vegetable, vegetable_qty)
    carb_from_vegetable = NutrDB.getGCarb(self.vegetable, vegetable_qty)
    fat_from_vegetable = NutrDB.getGFat(self.vegetable, vegetable_qty)

    # A meal should contain 100g of fruit
    fruit_qty = 0.100
    kcal_from_fruit = NutrDB.getKcal(self.fruit, fruit_qty)
    prot_from_fruit = NutrDB.getGProt(self.fruit, fruit_qty)
    carb_from_fruit = NutrDB.getGCarb(self.fruit, fruit_qty)
    fat_from_fruit = NutrDB.getGFat(self.fruit, fruit_qty)

    # extra 
    extra_qty = ExtraQtyDict[self.extra] 
    kcal_from_extra = NutrDB.getKcal(self.extra, extra_qty)
    prot_from_extra = NutrDB.getGProt(self.extra, extra_qty)
    carb_from_extra = NutrDB.getGCarb(self.extra, extra_qty)
    fat_from_extra = NutrDB.getGFat(self.extra, extra_qty)

    # 15% of meal kcal should come from proteins, and 1g of protein brings 4 kcal
    # 55% of meal kcal should come from carbs, and 1g of carb brings 4 kcal
    # 30% of meal kcal should come from fat, and 1g of fat brings 8.8 kcal
    # 4*(prot_from_prot_source + prot_from_carb_source + prot_from_fat_source + prot_from_vegetable + prot_from_fruit + prot_from_extra) = 0.12*MealKcalTarget
    # 4*(carb_from_prot_source + carb_from_carb_source + carb_from_fat_source + carb_from_vegetable + carb_from_fruit + carb_from_extra) = 0.63*MealKcalTarget
    # 8.8*(fat_from_prot_source + fat_from_carb_source + fat_from_fat_source + fat_from_vegetable + fat_from_fruit + fat_from_extra) = 0.25*MealKcalTarget

    a = np.array([ [ 4*NutrDB.getGProt(self.protein_source), 4*NutrDB.getGProt(self.carb_source), 4*NutrDB.getGProt(self.fat_source) ],
                   [ 4*NutrDB.getGCarb(self.protein_source), 4*NutrDB.getGCarb(self.carb_source), 4*NutrDB.getGCarb(self.fat_source) ],
                   [ 8.8*NutrDB.getGFat(self.protein_source), 8.8*NutrDB.getGFat(self.carb_source), 8.8*NutrDB.getGFat(self.fat_source) ] ])
    b = np.array([ 0.15*MealKcalTarget - 4*prot_from_vegetable - 4*prot_from_fruit - 4*prot_from_extra,
                   0.55*MealKcalTarget - 4*carb_from_vegetable - 4*carb_from_fruit - 4*carb_from_extra,
                   0.30*MealKcalTarget - 8.8*fat_from_vegetable - 8.8*fat_from_fruit - 8.8*fat_from_extra])
    x = np.linalg.solve(a, b)

    prot_source_qty = x[0]
    carb_source_qty = x[1]
    fat_source_qty = x[2]

    if prot_source_qty < 0 or carb_source_qty < 0 or fat_source_qty < 0:
      self.is_nutritionally_valid = False
      # and we leave the self...._qty to None
    else:
      self.is_nutritionally_valid = True
      self.protein_source_qty = prot_source_qty
      self.carb_source_qty = carb_source_qty
      self.fat_source_qty = fat_source_qty
      self.vegetable_qty = vegetable_qty
      self.fruit_qty = fruit_qty
      self.extra_qty = extra_qty

      # Just a quick check that we actually reach the calorie target
      sum_kcal = kcal_from_vegetable + kcal_from_fruit + kcal_from_extra + NutrDB.getKcal(self.protein_source, prot_source_qty) + NutrDB.getKcal(self.carb_source, carb_source_qty) + NutrDB.getKcal(self.fat_source, fat_source_qty)
      assert(myutils.approxEqual(sum_kcal, MealKcalTarget, 1e-3, 1e-6))


  def printNutritionalInfo(self, NutrDB):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Foods is a list of strings containing (in this order): a source of protein, a source of carbs, a source of fat, a vegetable, a fruit, an extra
      - Quantities is a list of floats containing the quantity for each food, in kg or L depending on food type
      - both lists must have the same size
      - each food listed in Foods mut exist as a key in KcalDict, GProtDict, GCarbDict, GFatDict
    Postconditions: A nutritional description of the meal is printed to screen.
    Result: [none]
    """
    print('')
    print("The meal is composed of :")
    hrule     = '-'*102
    print(hrule)

    print(NutrDB.getStringDesc(self.protein_source, self.protein_source_qty))
    print(NutrDB.getStringDesc(self.carb_source, self.carb_source_qty))
    print(NutrDB.getStringDesc(self.fat_source, self.fat_source_qty))
    print(NutrDB.getStringDesc(self.vegetable, self.vegetable_qty))
    print(NutrDB.getStringDesc(self.fruit, self.fruit_qty))
    print(NutrDB.getStringDesc(self.extra, self.extra_qty))
    
    print(hrule)

    sum_kcal = NutrDB.getKcal(self.protein_source, self.protein_source_qty) + NutrDB.getKcal(self.carb_source, self.carb_source_qty) + NutrDB.getKcal(self.fat_source, self.fat_source_qty) + NutrDB.getKcal(self.vegetable, self.vegetable_qty) + NutrDB.getKcal(self.fruit, self.fruit_qty) + NutrDB.getKcal(self.extra, self.extra_qty)  
    sum_gprot = NutrDB.getGProt(self.protein_source, self.protein_source_qty) + NutrDB.getGProt(self.carb_source, self.carb_source_qty) + NutrDB.getGProt(self.fat_source, self.fat_source_qty) + NutrDB.getGProt(self.vegetable, self.vegetable_qty) + NutrDB.getGProt(self.fruit, self.fruit_qty) + NutrDB.getGProt(self.extra, self.extra_qty)  
    sum_gcarb = NutrDB.getGCarb(self.protein_source, self.protein_source_qty) + NutrDB.getGCarb(self.carb_source, self.carb_source_qty) + NutrDB.getGCarb(self.fat_source, self.fat_source_qty) + NutrDB.getGCarb(self.vegetable, self.vegetable_qty) + NutrDB.getGCarb(self.fruit, self.fruit_qty) + NutrDB.getGCarb(self.extra, self.extra_qty)  
    sum_gfat = NutrDB.getGFat(self.protein_source, self.protein_source_qty) + NutrDB.getGFat(self.carb_source, self.carb_source_qty) + NutrDB.getGFat(self.fat_source, self.fat_source_qty) + NutrDB.getGFat(self.vegetable, self.vegetable_qty) + NutrDB.getGFat(self.fruit, self.fruit_qty) + NutrDB.getGFat(self.extra, self.extra_qty)  

    template = 'TOTAL:' + 42*' ' + '{0:5.0f} kcal, {1:5.1f} g protein, {2:5.1f} g carb, {3:5.1f} g fat'
    print(template.format(sum_kcal, sum_gprot, sum_gcarb, sum_gfat))
    print('')



  def computeEnvironmentalImpact(self, EnvDB):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - each food of the meal must exist as a key in EnvDB
      - the quantities of each food must have been defined
    Postconditions: 
      - self.impact contains the 5D environmental assessement of the meal (EnvironmentalImpact object) 
    Result: [none]
    """
    land_use = 0
    ghg = 0
    acid = 0
    eutroph = 0
    water = 0
    quantities = self.getQuantities()
    foods = self.getFoods()
    for i, food in enumerate(foods):
      qty = quantities[i]
      land_use += EnvDB.getLandUse(food, qty)
      ghg += EnvDB.getGHGEmissions(food, qty)
      acid += EnvDB.getAcidifyingEmissions(food, qty)
      eutroph += EnvDB.getEutrophyingEmissions(food, qty)
      water += EnvDB.getWaterUse(food, qty)
    self.impact = envDBmodule.EnvironmentalImpact([land_use, ghg, acid, eutroph, water])



  def printEnvironmentalImpact(self, EnvDB):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - each food of the meal must exist as a key in LandUseDict, GHGEmissionsDict, AcidifyingEmissionsDict, EutrophyingEmissionsDict, WaterUseDict
      - the quantities of each food must have been defined
    Postconditions: A description of the meal environmental impact is printed to screen.
    Result: [none]
    """
    print('This meal uses  {0:6.1f} square meters of land.'.format(self.impact.land_use))
    print('This meal emits {0:6.1f} kg CO2 eq. (greenhouse gas emissions).'.format(self.impact.GHG_emissions))
    print('This meal emits {0:6.1f} g SO2 eq. (acidifying emissions).'.format(self.impact.acidifying_emissions))
    print('This meal emits {0:6.1f} g PO43- eq. (eutrophying emissions).'.format(self.impact.eutrophying_emissions))
    print('This meal uses  {0:6.0f} L of freshwater.'.format(self.impact.water_use))
    print('')


  def isEnvironmentFriendly(self, Thresholds):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - self.impact must have been computed
      - both self.impact and Threshold are instances of class EnvironentalImpact
    Postconditions: [none]
    Result: True if all components of Impact are lower or equal to their counterparts in Thresholds,
    False if at least one component of Impact exceeds its counterpart in Thresholds.
    """
    return (self.impact <= Thresholds)


  def containsAVetoedFood(self, FoodRatings):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - FoodRatings is a dictionary associating a rating between 0 and 5 to each food
    Postconditions: [none]
    Result: True if all components of the meal have a strictly positive rating in FoodRatings
    """
    for food in self.getFoods():
      if FoodRatings[food] <= 0:
        return True
    return False


  def computeRating(self, FoodRatings):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - FoodRatings is a dictionary associating a rating between 0 and 5 to each food
    Postconditions: [none]
    Result: The sum of the ratings of the 6 meal components
    """
    self.rating = 0
    for food in self.getFoods():
      self.rating += FoodRatings[food]
    



#################
# Class MealSet #
#################


class MealSet(object):

  def __init__(self):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: self
    Preconditions: [none]
    Postconditions: 
      - the attributes of self are initialized
    Result: self
    """
    self.meals = []
    self.total_impact = envDBmodule.EnvironmentalImpact()
    self.total_rating = 0


  def deepcopy(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none]
    Result: an independent copy of self
    """
    new_set = MealSet()
    new_set.meals = self.meals[:]
    new_set.total_impact = (self.total_impact).deepcopy()
    new_set.total_rating = self.total_rating
    return new_set

  def __str__(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none]
    Result: a string description of the MealSet 
    """
    my_string = '['
    for m in self.meals:
      my_string += str(m.getFoods())
    my_string += '], '
    my_string += str(self.total_impact)
    my_string += ', ' + str(self.total_rating)
    return my_string

  def getFirst(self):
    return (self.meals)[0]

  def __len__(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none]
    Result: an integer equal to the number of meals in the MealSet
    """
    return len(self.meals)

  def __getitem__(self, index):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none]
    Result: the Meal at position index in the MealSet, i.e. self.meals[index]
    """
    return (self.meals)[index]

  def __setitem__(self, index, NewMeal):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - NewMeal is a Meal instance
    Postconditions: 
      - the Meal at position index is replaced by NewMeal
    Result: [none]
    """
    self.total_impact =  self.total_impact - (self.meals)[index].impact
    self.total_rating = self.total_rating - (self.meals)[index].rating
    (self.meals)[index] = NewMeal
    self.total_impact =  self.total_impact + NewMeal.impact
    self.total_rating =  self.total_rating + NewMeal.rating

  def __delitem__(self, index):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: 
      - the Meal at position index is removed from the MealSet
    Result: [none]
    """
    self.total_impact =  self.total_impact - (self.meals)[index].impact
    self.total_rating = self.total_rating - (self.meals)[index].rating
    del (self.meals)[index]

  def addMeal(self, NewMeal):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - NewMeal is a Meal instance
    Postconditions: 
      - NewMeal is added at the end of the MealSet
    Result: [none]
    """
    (self.meals).append(NewMeal)
    self.total_impact =  self.total_impact + NewMeal.impact
    self.total_rating =  self.total_rating + NewMeal.rating

  def addMeals(self, NewMeals):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - NewMeals is a list of Meal instances
    Postconditions: 
      - NewMeals are added at the end of the MealSet (concatenation)
    Result: [none]
    """
    self.meals = self.meals + NewMeals
    for m in NewMeals:
      self.total_impact = self.total_impact + m.impact
      self.total_rating = self.total_rating + m.rating

  def saveToFile(self, Filename):
    """
    Parameters passed in data mode: self, Filename
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Meals is a list of instances of class Meal from module nutritionfacts
    Postconditions: 
      - a text file named according to Filename is created or overwritten, with one line for each meal
    Result: None
    """
    with open(Filename, 'w') as output_file: # no need to explicitly close the file when we use the 'with' block
      for meal in self.meals:
        foods = meal.getFoods()
        qty = meal.getQuantities()
        mystrings = []
        for i in range(len(foods)):
          mystrings.append('{0:4.0f} g or mL of {1}'.format(1000*qty[i], foods[i]))
        output_file.write(', '.join(mystrings))
        output_file.write('\n')


  def computeAllEnvironmentalImpacts(self, EnvDB):
    """
    Parameters passed in data mode: EnvDB
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
     - each meal in self.meals must have its quantities set
    Postconditions: 
     - each meal has its environmental impact computed
    Result: [none]
    """
    self.total_impact = envDBmodule.EnvironmentalImpact()
    for meal in self.meals:
      meal.computeEnvironmentalImpact(EnvDB)
      self.total_impact = self.total_impact + meal.impact




  def drawEnvironmentalImpactHistograms(self, Type='standalone'):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
     - each meal in self.meals has its environmental impact computed
    Postconditions: A window opens, containing five histograms, one for each environmental indicator.
    Result: None
    """
    impacts = []
    for meal in self.meals:
      impacts.append(meal.impact.toList())

    df = pd.DataFrame(impacts, columns=['LandUse', 'GHGEmissions', 'AcidifyingEmissions', 'EutrophyingEmissions', 'WaterUse'])
    myfig = plt.figure(figsize=(10, 10))
    
    axs = myfig.add_subplot(3, 2, 1)
    axs.hist(df['LandUse'])
    axs.set_xlabel('Land use (square meters)')


    axs = myfig.add_subplot(3, 2, 2)
    axs.hist(df['GHGEmissions'])
    axs.set_xlabel('Greenhouse gas emissions (kg CO2 eq.)')

    axs = myfig.add_subplot(3, 2, 3)
    axs.hist(df['AcidifyingEmissions'])
    axs.set_xlabel('Acidifying emissions (g SO2 eq.)')

    axs = myfig.add_subplot(3, 2, 4)
    axs.hist(df['EutrophyingEmissions'])
    axs.set_xlabel('Eutrophying emissions (g PO43- eq.)')

    axs = myfig.add_subplot(3, 2, 5)
    axs.hist(df['WaterUse'])
    axs.set_xlabel('Stress-weighted water use (L)')

    if Type == 'standalone':
      plt.show()
      return None
    elif Type == 'embedded':
      return myfig


  def filterBasedOnEnvironmentalImpact(self, Thresholds):
    """
    Parameters passed in data mode: self, Thresholds
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
     - each meal in self.meals has its environmental impact computed
     - Thresholds is an instance of class EnvironmentalImpact
    Postconditions: [none]
    Result: A MealSet containing the subset of self.meals whose impact is lower than Thresholds
    """
    winning_meals = MealSet()
    for meal in self.meals:
      if meal.isEnvironmentFriendly(Thresholds):
        winning_meals.addMeal(meal)
    return winning_meals


  def computeAllRatings(self, FoodRatings):
    """
    Parameters passed in data mode: NutrDB
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
     -  FoodRatings is a dictionary associating a rating between 0 and 5 to each food
    Postconditions: 
     - each meal has its rating computed
     - the mealset (self) has its total_rating computed
    Result: [none]
    """
    self.total_rating = 0
    for meal in self.meals:
      meal.computeRating(FoodRatings)
      self.total_rating = self.total_rating + meal.rating


  def filterBasedOnUserVeto(self, FoodRatings):
    """
    Parameters passed in data mode: self, FoodRatings, MinTotalRating
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
     - FoodRatings is a dictionary associating a rating between 0 and 5 to each food
    Postconditions: [none]
    Result: A MealSet containing the subset of self.meals that do not contain a 0-rated food
    """
    winning_meals = MealSet()
    for meal in self.meals:
      if (not meal.containsAVetoedFood(FoodRatings)):
        winning_meals.addMeal(meal)
    return winning_meals


  def filterBasedOnMinimalMealSatisfaction(self, FoodRatings, MinimalMealRating):
    """
    Parameters passed in data mode: self, FoodRatings, MinTotalRating
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
     - FoodRatings is a dictionary associating a rating between 0 and 5 to each food
    Postconditions: [none]
    Result: A MealSet containing the subset of self.meals that have a rating larger or
    equal to MinimalMealRating
    """
    self.computeAllRatings(FoodRatings)
    winning_meals = MealSet()
    for meal in self.meals:
      if meal.rating >= MinimalMealRating:
        winning_meals.addMeal(meal)
    return winning_meals


################
# Main program #
################

if __name__ == "__main__":



  abseps = 1e-15
  releps = 1e-6

  nutrDB = nutritionDBmodule.NutritionDatabase()
  envDB = envDBmodule.EnvironmentalDatabase()

  print('Unit test of Meal.printNutritionalInfo:')
  my_foods =['Poultry Meat', 'Wheat & Rye (Bread)', 'Olive Oil', 'Root Vegetables', 'Berries & Grapes', 'Coffee']
  my_quantities = [0.050, 0.120, 0.016, 0.125, 0.050, 0.008]
  my_meal = Meal(my_foods, my_quantities)
  my_meal.printNutritionalInfo(nutrDB)
  print('')


  print("Unit test of Meal.computeEnvironmentalImpact:")
  my_meal.computeEnvironmentalImpact(envDB)
  expected_impact = envDBmodule.EnvironmentalImpact([1.413500, 0.798200, 6.778500, 3.572800, 2765.404000]) # computed independently with Excel
  print(my_meal.impact == expected_impact) # I have implemented the operator == for the class EnvironmentalImpact (see method __eq__)
  print('')


  print("Unit test of printMealEnvironmentalImpact:")
  my_meal.printEnvironmentalImpact(envDB)
  print('')


  print("Unit test of isEnvironmentFriendly:")
  my_thresholds = envDBmodule.EnvironmentalImpact([2.0, 1.5, 7.0, 7.0, 1000])
  print(my_meal.isEnvironmentFriendly(my_thresholds)==False)


  print('Unit test of Meal.computeQuantities:')
  extra_qty_dict = {'Beet Sugar': 0.012, 'Coffee': 0.008, 'Dark Chocolate': 0.020}
  daily_energy_req = 1800
  my_meal.computeQuantities(0.4*daily_energy_req, nutrDB, extra_qty_dict)
  # or, equivalently (procedural style): Meal.computeQuantities(my_meal, 0.4*daily_energy_req, extra_qty_dict)
  my_quantities = my_meal.getQuantities()
  print(myutils.approxEqualVect(my_quantities, [0.027161553, 0.1980991333, 0.01421888129, 0.125, 0.05, 0.008], releps, abseps))
