###########
# Imports #
###########

# External librairies

import os.path


# Local modules

import usermodule
import nutritionDBmodule
import envDBmodule
import mealmodule
import myutils



################
# Main program #
################

if __name__ == "__main__":



  print('Importing nutritional data... ', end='')
  nutrDB = nutritionDBmodule.NutritionDatabase('poore2018/TableS1_augmented_with_FAO_data.xlsx')
  assert(nutrDB.isComplete())
  assert(nutrDB.isConsistent())
  print('done')

  user = usermodule.User() 
  user.setExtraQuantities(nutrDB)
  
  print('Importing environmental data... ', end='')
  envDB = envDBmodule.EnvironmentalDatabase('poore2018/DataS2.xlsx')
  assert(envDB.isConsistentWith(nutrDB))
  print('done')

  my_foods =['Bovine Meat (beef herd)', 'Rice', 'Rapeseed Oil', 'Brassicas', 'Apples', 'Beet Sugar']
  my_meal = mealmodule.Meal(my_foods)
  my_meal.computeQuantities(803, nutrDB, user.extra_qty_dict)
  my_quantities = my_meal.getQuantities()
  my_meal.printNutritionalInfo(nutrDB)
