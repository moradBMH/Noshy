
###########
# Imports #
###########

# External librairies

import pandas as pd


# Local modules

import myutils
import mealmodule

###########################
# Class NutritionDatabase #
###########################

class NutritionDatabase(object):

  def __init__(self, Filepath=''):
    """
    Parameters passed in data mode: Filepath
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: self
    Preconditions: 
      - Filepath, when given, is the path to an XLSX file containing a sheet called 'FAOdata'
      - In this sheet, the first line contains the headers 'Product', 'Type', 'kcalPerRetailUnit', 'gProteinPerRetailUnit', 'gCarbPerRetailUnit', 'gFatPerRetailUnit' 
    Postconditions:       
      - self.protein_sources, self.carb_sources, self.fat_sources, self.vegetables, self.fruits and self.extras are non-empty lists of strings
      - self.kcal_dict associates to each food the number of kcal brought by 1 retail unit (1kg or 1L) of that food
      - self.gProt_dict associates to each food the number of grams of protein brought by 1 retail unit (1kg or 1L) of that food
      - self.gCarb_dict associates to each food the number of grams of carbohydrates brought by 1 retail unit (1kg or 1L) of that food
      - self.gFat_dict associates to each food the number of grams of fat brought by 1 retail unit (1kg or 1L) of that food
    Result: self
    """
    self.protein_sources = []
    self.carb_sources = []
    self.fat_sources = []
    self.fruits = []
    self.vegetables = []
    self.extras = []
    self.kcal_dict = {}
    self.gProt_dict = {}
    self.gCarb_dict = {}
    self.gFat_dict = {}
    if Filepath == '':
      self.loadDefault()
    else:
      self.loadFromFile(Filepath)
  
  def loadDefault(self):
    """
    Parameters passed in data mode: [none]
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: [none] 
    Postconditions:       
      - self.protein_sources, self.carb_sources, self.fat_sources, self.vegetables, self.fruits and self.extras are non-empty lists of strings
      - self.kcal_dict associates to each food the number of kcal brought by 1 retail unit (1kg or 1L) of that food
      - self.gProt_dict associates to each food the number of grams of protein brought by 1 retail unit (1kg or 1L) of that food
      - self.gCarb_dict associates to each food the number of grams of carbohydrates brought by 1 retail unit (1kg or 1L) of that food
      - self.gFat_dict associates to each food the number of grams of fat brought by 1 retail unit (1kg or 1L) of that food
    Result: [none]
    """
    self.carb_sources = ['Wheat & Rye (Bread)', 'Maize (Meal)', 'Potatoes']
    self.extras = ['Beet Sugar', 'Coffee', 'Dark Chocolate']
    self.fat_sources = ['Rapeseed Oil', 'Olive Oil']
    self.fruits = ['Bananas', 'Apples', 'Berries & Grapes']
    self.protein_sources = ['Tofu', 'Bovine Meat (beef herd)', 'Poultry Meat', 'Eggs']
    self.vegetables = ['Tomatoes', 'Root Vegetables', 'Other Vegetables']

    self.kcal_dict = {'Wheat & Rye (Bread)': 2490, 
                'Maize (Meal)': 3630,
                'Potatoes': 670,
                'Beet Sugar': 3870,
                'Coffee': 560,
                'Dark Chocolate': 3930,
                'Rapeseed Oil': 8096,
                'Olive Oil': 8096, 
                'Bananas': 600,
                'Apples': 480,
                'Berries & Grapes': 530,
                'Tofu': 765, 
                'Bovine Meat (beef herd)': 1500, 
                'Poultry Meat': 1220, 
                'Eggs': 1630,
                'Tomatoes' : 170,
                'Root Vegetables': 380,
                'Other Vegetables': 220}

    self.gProt_dict = {'Wheat & Rye (Bread)': 82, 
                  'Maize (Meal)': 84,
                  'Potatoes': 16,
                  'Beet Sugar': 0,
                  'Coffee': 80,
                  'Dark Chocolate': 42,
                  'Rapeseed Oil': 0,
                  'Olive Oil': 0, 
                  'Bananas': 7,
                  'Apples': 1,
                  'Berries & Grapes': 5,
                  'Tofu': 82, 
                  'Bovine Meat (beef herd)': 185, 
                  'Poultry Meat': 123, 
                  'Eggs': 113,
                  'Tomatoes' : 8,
                  'Root Vegetables': 9,
                  'Other Vegetables': 14}

    self.gFat_dict = {'Wheat & Rye (Bread)': 12, 
                  'Maize (Meal)': 12,
                  'Potatoes': 1,
                  'Beet Sugar': 0,
                  'Coffee': 0,
                  'Dark Chocolate': 357,
                  'Rapeseed Oil': 920,
                  'Olive Oil': 920, 
                  'Bananas': 3,
                  'Apples': 3,
                  'Berries & Grapes': 4,
                  'Tofu': 42, 
                  'Bovine Meat (beef herd)': 79, 
                  'Poultry Meat': 77, 
                  'Eggs': 121,
                  'Tomatoes' : 2,
                  'Root Vegetables': 2,
                  'Other Vegetables': 2}

    self.gCarb_dict = {'Wheat & Rye (Bread)': 514.1, 
                  'Maize (Meal)': 797.1,
                  'Potatoes': 149.3,
                  'Beet Sugar': 967.5,
                  'Coffee': 60,
                  'Dark Chocolate': 155.1,
                  'Rapeseed Oil': 0,
                  'Olive Oil': 0, 
                  'Bananas': 136.4,
                  'Apples': 112.4,
                  'Berries & Grapes': 118.7,
                  'Tofu': 16.85, 
                  'Bovine Meat (beef herd)': 16.2, 
                  'Poultry Meat': 12.6, 
                  'Eggs': 28.3,
                  'Tomatoes' : 30.1,
                  'Root Vegetables': 81.6,
                  'Other Vegetables': 36.6}





  def loadFromFile(self, Filepath):
    """
    Parameters passed in data mode: Filepath
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - Filepath is the path to an XLSX file containing a sheet called 'FAOdata'
      - In this sheet, the first line contains the headers 'Product', 'Type', 'kcalPerRetailUnit', 'gProteinPerRetailUnit', 'gCarbPerRetailUnit', 'gFatPerRetailUnit' 
    Postconditions:       
      - self.protein_sources, self.carb_sources, self.fat_sources, self.vegetables, self.fruits and self.extras are non-empty lists of strings
      - self.kcal_dict associates to each food the number of kcal brought by 1 retail unit (1kg or 1L) of that food
      - self.gProt_dict associates to each food the number of grams of protein brought by 1 retail unit (1kg or 1L) of that food
      - self.gCarb_dict associates to each food the number of grams of carbohydrates brought by 1 retail unit (1kg or 1L) of that food
      - self.gFat_dict associates to each food the number of grams of fat brought by 1 retail unit (1kg or 1L) of that food
    Result: [none]
    """
    nutr_data = pd.read_excel(Filepath, sheet_name='FAOdata')
    self.protein_sources = list(nutr_data[nutr_data['Type']=='ProteinSource']['Product'])
    self.carb_sources    = list(nutr_data[nutr_data['Type']=='CarbSource']['Product'])
    self.fat_sources     = list(nutr_data[nutr_data['Type']=='FatSource']['Product'])
    self.vegetables      = list(nutr_data[nutr_data['Type']=='Vegetable']['Product'])
    self.fruits          = list(nutr_data[nutr_data['Type']=='Fruit']['Product'])
    self.extras          = list(nutr_data[nutr_data['Type']=='Extra']['Product'])
    self.kcal_dict  = dict(zip(nutr_data['Product'], nutr_data['kcalPerRetailUnit']))
    self.gProt_dict = dict(zip(nutr_data['Product'], nutr_data['gProteinPerRetailUnit']))
    self.gFat_dict  = dict(zip(nutr_data['Product'], nutr_data['gFatPerRetailUnit']))
    self.gCarb_dict = dict(zip(nutr_data['Product'], nutr_data['gCarbPerRetailUnit']))

    
  def isComplete(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
    Postconditions: [none]
    Result: True if all the strings appearing in in the lists self.protein_sources, self.carb_sources, self.fat_sources, self.vegetables, self.fruits and self.extras
        exist as keys in self.kcal_dict, in self.gProt_dict, in self.gCarb_dict, and in self.gFat_dict
      - KcalDict associates to each food the number of kcal brought by 1 retail unit (1kg or 1L) of that food
      - GProtDict associates to each food the number of grams of protein brought by 1 retail unit (1kg or 1L) of that food
      - GCarbDict associates to each food the number of grams of carbohydrates brought by 1 retail unit (1kg or 1L) of that food
      - GFatDict associates to each food the number of grams of fat brought by 1 retail unit (1kg or 1L) of that food
      - ExtraQtyDict is a dictionary associating to each extra in Extras the typical serving size (expressed in kg or L)
    """
    complete = True
    for food in self.getAllFoods():
      if food not in self.kcal_dict:
        print('Warning: missing number of calories for ' + food)
        complete = False
      if food not in self.gProt_dict:
        print('Warning: missing number of grams of proteins for ' + food)
        complete = False
      if food not in self.gCarb_dict:
        print('Warning: missing number of grams of carbohydrates for ' + food)
        complete = False
      if food not in self.gFat_dict:
        print('Warning: missing number of grams of fat for ' + food)
        complete = False
    return complete
    
  def isConsistent(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
    Postconditions: [none]
    Result: True if for all foods in the database, the number of calories is consistent with the
    number of grams of proteins, of carbohydrates and of fat
    """
    consistent = True
    for food in self.getAllFoods():
      kcal_in_db = self.kcal_dict[food]
      kcal_computed_from_compo = 4*self.gProt_dict[food] + 4*self.gCarb_dict[food] + 8.8*self.gFat_dict[food]
      if not myutils.approxEqual(kcal_in_db, kcal_computed_from_compo, 1e-3, 1e-6):
        print('Warning: For '+ food + ', the number of calories is not consistent with the number of g protein, g carb, g fat')
        consistent = False
    return consistent


  def getAllFoods(self):
    return self.protein_sources + self.carb_sources+ self.fat_sources + self.vegetables + self.fruits + self.extras


  def getKcal(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.kcal_dict
      - Qty is a float, expressed in the same units used in self (typically kg or L)
    Postconditions: [none]
    Result: number of calories brought by the given Qty of Food
    """
    return (Qty*self.kcal_dict[Food])

  def getGProt(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.gProt_dict
      - Qty is a float, expressed in the same units used in self (typically kg or L)
    Postconditions: [none]
    Result: number of grams of proteins brought by the given Qty of Food
    """
    return (Qty*self.gProt_dict[Food])

  def getGCarb(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.gCarb_dict
      - Qty is a float, expressed in the same units used in self (typically kg or L)
    Postconditions: [none]
    Result: number of grams of carbohydrates brought by the given Qty of Food
    """
    return (Qty*self.gCarb_dict[Food])

  def getGFat(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.gFat_dict
      - Qty is a float, expressed in the same units used in self (typically kg or L)
    Postconditions: [none]
    Result: number of grams of fat brought by the given Qty of Food
    """
    return (Qty*self.gFat_dict[Food])

  def getStringDesc(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in the four dictionary in self
      - Qty is a float, expressed in the same units used in self (typically kg or L)
    Postconditions: [none]
    Result: a string describing the nutritional value of the given Qty of Food, for instance
    "-    50 g of         Poultry Meat, contributing    61 kcal,   6.2 g protein,   0.6 g carb,   3.9 g fat"
    """
    template = '- {0:5.0f} g of {1:>20}, contributing {2:5.0f} kcal, {3:5.1f} g protein, {4:5.1f} g carb, {5:5.1f} g fat'
    kcal = self.getKcal(Food, Qty)
    gprot = self.getGProt(Food, Qty)
    gcarb = self.getGCarb(Food, Qty)
    gfat = self.getGFat(Food, Qty)
    return (template.format(1000*Qty, Food, kcal, gprot, gcarb, gfat))


  def enumerateAllPossibleMeals(self):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - self.protein_sources, self.carb_sources, self.fat_sources, self.vegetables, self.fruits and self.extras are non-empty lists of strings
    Postconditions: [none]
    Result: An instance of class MealSet containing the set of all possible meals from the database.
    """
    all_meals = mealmodule.MealSet()
    for prot_source in self.protein_sources:
      for carb in self.carb_sources:
        for fat in self.fat_sources:
          for veg in self.vegetables:
            for fruit in self.fruits:         
              for extra in self.extras:
                meal = mealmodule.Meal([prot_source, carb, fat, veg, fruit, extra])
                all_meals.addMeal(meal)
    return all_meals


  def enumerateAllPossibleMealsWithQuantities(self, MealKcalTarget, ExtraQtyDict):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - the database (self) is complete and consistent
      - MealKcalTarget is a positive integer or float 
      - ExtraQtyDict contains an entry for each food in self.extras
    Postconditions: [none]
    Result: An instance of class MealSet containing the set of all meals that can be assembled to reach MealKcalTarget
    """
    all_valid_meals_with_quantities = mealmodule.MealSet()
    nb_impossible_meals = 0
    for prot_source in self.protein_sources:
      for carb in self.carb_sources:
        for fat in self.fat_sources:
          for veg in self.vegetables:
            for fruit in self.fruits:         
              for extra in self.extras:
                meal = mealmodule.Meal([prot_source, carb, fat, veg, fruit, extra])
                quantities = meal.computeQuantities(MealKcalTarget, self, ExtraQtyDict)
                if meal.is_nutritionally_valid:
                  all_valid_meals_with_quantities.addMeal(meal)
                else:
                  nb_impossible_meals += 1

    fraction_impossible = nb_impossible_meals / (len(self.protein_sources)*len(self.carb_sources)*len(self.fat_sources)*len(self.vegetables)*len(self.fruits)*len(self.extras))
    print('There were', nb_impossible_meals, 'impossible meals (', 100*fraction_impossible, '%).')
    return all_valid_meals_with_quantities









################
# Main program #
################

if __name__ == "__main__":



  abseps = 1e-15
  releps = 1e-6

  myDB = NutritionDatabase()
  print(myDB.isComplete())
  print(myDB.isConsistent())


  print('Unit test of NutritionDatabase.enumerateAllPossibleMeals:')
  all_meals = myDB.enumerateAllPossibleMeals()
  print("There are", len(all_meals), "possible meals.")
  #print('The first one is: ', all_meals[0].getFoods())
  #first = all_meals.getFirst()
  #print('The first one is: ', mealmodule.Meal.getFoods(first))
  #print('The last one is: ', all_meals[-1].getFoods())
  print(len(all_meals)==len(myDB.protein_sources)*len(myDB.carb_sources)*len(myDB.fat_sources)*len(myDB.vegetables)*len(myDB.fruits)*len(myDB.extras))
  print('')


  print('Unit test of enumerateAllPossibleMealsWithQuantities:')
  daily_energy_req = 1800
  extra_qty_dict = {'Beet Sugar': 0.012, 'Coffee': 0.008, 'Dark Chocolate': 0.020}
  all_valid_meals_with_quantities = myDB.enumerateAllPossibleMealsWithQuantities(0.4*daily_energy_req, extra_qty_dict)
  print("There are", len(all_valid_meals_with_quantities), "nutritionally valid meals.")
  print('Here is the first one.')
  (all_valid_meals_with_quantities[0]).printNutritionalInfo(myDB)
  print('Here is the last one.')
  (all_valid_meals_with_quantities[-1]).printNutritionalInfo(myDB)

