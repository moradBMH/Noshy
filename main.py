###########
# Imports #
###########

# External librairies

import os.path
import calendar
import random

# Local modules

import usermodule
import nutritionDBmodule
import envDBmodule
import mealmodule
import myutils



########################
# Function definitions #
########################

def buildMealSets(Meals, NbMealsPerSet, EnvThresholds):
  meal_sets = []
  
  my_stack = []
  my_restricted_meals = mealmodule.MealSet()
  for m in Meals.meals:
    if m.impact < EnvThresholds:
      my_restricted_meals.addMeal(m)
      my_meal_set = mealmodule.MealSet()
      my_meal_set.addMeal(m)
      my_stack.append(my_meal_set)
  print(len(my_restricted_meals))

  while len(my_stack)>0:
    current_set = my_stack.pop()
    if len(current_set) == NbMealsPerSet:
      # we have found a complete meal set !
      meal_sets.append(current_set)
      print(current_set)
    else:
      # keep expanding the current set
      for m in my_restricted_meals.meals:
        new_impact = current_set.total_impact + m.impact
        if new_impact < EnvThresholds:
          if m not in current_set.meals:
            new_set = current_set.deepcopy()
            new_set.addMeal(m)
            my_stack.append(new_set)
         
  return meal_sets




################
# Main program #
################

if __name__ == "__main__":

  user = usermodule.User() 
  user.setPhysiologicalParameters()
  daily_energy_req = user.dailyEnergyRequirement()
  print('Your daily energy requirement is', daily_energy_req, 'kcal.')
  print('The breakfast should bring', 0.2*daily_energy_req, 'kcal.')
  print('The lunch and dinner should each bring', 0.4*daily_energy_req, 'kcal.')

  print('Importing nutritional data... ', end='')
  nutrDB = nutritionDBmodule.NutritionDatabase('poore2018/TableS1_augmented_with_FAO_data.xlsx')
  assert(nutrDB.isComplete())
  assert(nutrDB.isConsistent())
  print('done')

  #user.setRatings(nutrDB)
  user.setExtraQuantities(nutrDB)
  
  all_valid_meals_with_quantities = nutrDB.enumerateAllPossibleMealsWithQuantities(0.4*daily_energy_req, user.extra_qty_dict)
  print('There are', len(all_valid_meals_with_quantities), 'nutritionnally valid meals.')

  #all_valid_meals_with_quantities.computeAllRatings(user.ratings)
  #acceptable_meals = all_valid_meals_with_quantities.filterBasedOnUserVeto(user.ratings)
  #print(len(acceptable_meals), 'meals are acceptable (= do not contain any vetoed food).')

  #liked_meals = acceptable_meals.filterBasedOnMinimalMealSatisfaction(user.ratings, 20)
  #print(len(liked_meals), 'meals are liked.')

  print('Importing environmental data... ', end='')
  envDB = envDBmodule.EnvironmentalDatabase('poore2018/DataS2.xlsx')
  assert(envDB.isConsistentWith(nutrDB))
  print('done')

  all_valid_meals_with_quantities.computeAllEnvironmentalImpacts(envDB)
  
  print('Here are the distributions of environmental impacts for all nutritionnally valid meals.')  
  all_valid_meals_with_quantities.drawEnvironmentalImpactHistograms()
  user.setEnvironmentalThresholds()


  env_friendly_meals = all_valid_meals_with_quantities.filterBasedOnEnvironmentalImpact(user.env_thresholds)
  print(len(env_friendly_meals), 'meals are compatible with the environmental impact thresholds.')

  result_file_name = 'meals.txt'  
  env_friendly_meals.saveToFile(result_file_name)
  print(len(env_friendly_meals), 'meals written to file', result_file_name, '.')


  # my_calendar= calendar.Calendar()
  # nb_days_in_the_year = 0
  # for month in range(1, 13):
  #   for day in my_calendar.itermonthdates(2021, month):
  #     nb_days_in_the_year += 1

  # indices = [i for i in range(len(env_friendly_meals))]
  # selected_indices = random.sample(indices, 2*nb_days_in_the_year)
  # i = 0
  # for month in range(1, 13):
  #   for day in my_calendar.itermonthdates(2021, month):
  #     print(day, 'lunch:')
  #     env_friendly_meals[i].printNutritionalInfo(nutrDB)    
  #     env_friendly_meals[i].printEnvironmentalImpact(envDB)
  #     print('') 
  #     print(day, 'dinner:')
  #     env_friendly_meals[i+1].printNutritionalInfo(nutrDB)     
  #     env_friendly_meals[i+1].printEnvironmentalImpact(envDB) 
  #     print('') 
  #     i += 2


