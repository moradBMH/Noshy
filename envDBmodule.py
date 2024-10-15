
###########
# Imports #
###########

# External librairies

import pandas as pd



# Local modules

import myutils


#############################
# Class EnvironmentalImpact #
#############################

class EnvironmentalImpact(object):
  
  def __init__(self, Values=[]):
    """
    Parameters passed in data mode: Values
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: self
    Preconditions: 
      - if specified, Values is a list of five floats corresponding to (in this order):
        the land use (in square meters), the amount of greenhouse gas emissions (in kg CO2eq),
        the amount of acidifying emissions (in g SO2eq), the amount of eutrophying emissions (in g PO43-eq) 
        and the stress-weighted water use (in L).
    Postconditions: 
      - the attributes land_use, GHG_emissions, acidifying_emissions, eutrophying_emissions and water_use are initialized
        to None if no list has been passed, or the values contained in Values.
    Result: self
    """
    if Values == []:
      self.land_use = 0
      self.GHG_emissions = 0
      self.acidifying_emissions = 0
      self.eutrophying_emissions = 0
      self.water_use = 0
    else:
      self.land_use = Values[0]
      self.GHG_emissions = Values[1]
      self.acidifying_emissions = Values[2]
      self.eutrophying_emissions = Values[3]
      self.water_use = Values[4]

  def __str__(self):
    my_template = '[{0:.1f}, {1:.1f}, {2:.1f}, {3:.1f}, {4:.1f}]'
    return my_template.format(self.land_use, self.GHG_emissions, self.acidifying_emissions, self.eutrophying_emissions, self.water_use)

  def deepcopy(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none]
    Result: an independent copy of self
    """
    new_impact = EnvironmentalImpact(self.toList())
    return new_impact


  def toList(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none] 
    Result: a list of floats corresponding to (in this order): the land use (in square meters), the amount of greenhouse gas emissions (in kg CO2eq),
    the amount of acidifying emissions (in g SO2eq), the amount of eutrophying emissions (in g PO43-eq) and the stress-weighted water use (in L).
    """
    return [self.land_use, self.GHG_emissions, self.acidifying_emissions, self.eutrophying_emissions, self.water_use]


  def __add__(self, Other): # implementation of operator +
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Other is an instance of EnvironmentalImpact 
      - attributes land_use, GHG_emissions, ... must have been set in self in in Other
    Postconditions (alterations of program state outside this function): [none]
    Returned result: an instance of EnvironmentalImpact containing the sum of self and Other for each attribute
    """
    V1 = self.toList()
    V2 = Other.toList()
    values = [ (V1[i]+V2[i]) for i in range(len(V1)) ]
    return EnvironmentalImpact(values)


  def __sub__(self, Other): # implementation of operator -
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Other is an instance of EnvironmentalImpact 
      - attributes land_use, GHG_emissions, ... must have been set in self in in Other
    Postconditions (alterations of program state outside this function): [none]
    Returned result: an instance of EnvironmentalImpact containing the self.attr - Other.attr for each attribute
    """
    V1 = self.toList()
    V2 = Other.toList()
    values = [ (V1[i]-V2[i]) for i in range(len(V1)) ]
    return EnvironmentalImpact(values)


  def __eq__(self, Other): # implementation of operator ==
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Other is an instance of EnvironmentalImpact 
      - attributes land_use, GHG_emissions, ... must have been set in self in in Other
    Postconditions (alterations of program state outside this function): [none]
    Returned result: a Boolean, True if all components of V1 are approximately equal to their 
    counterpart in V2, with absolute tolerance AbsoluteEpsilon
    or with relative tolerance RelativeEpsilon.
    """
    V1 = self.toList()
    V2 = Other.toList()
    return myutils.approxEqualVect(V1, V2, 1e-6, 1e-10)



  def __le__(self, Other): # implementation of operator <=
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Other is an instance of EnvironmentalImpact 
      - attributes land_use, GHG_emissions, ... must have been set in self in in Other
    Postconditions: [none]
    Result: True if all components of self are lower or equal to their counterparts in Other,
    False if at least one component of Impact exceeds its counterpart in Other.
    """
    self_list = self.toList()
    other_list = Other.toList()
    self_is_lower_or_equal = True
    for k in range(len(self_list)):
      if self_list[k] > other_list[k]:
        self_is_lower_or_equal = False
        break
    return self_is_lower_or_equal


  def __lt__(self, Other): # implementation of operator <
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Other is an instance of EnvironmentalImpact 
      - attributes land_use, GHG_emissions, ... must have been set in self in in Other
    Postconditions: [none]
    Result: True if all components of self are strictly lower than their counterparts in Other,
    False if at least one component of Impact exceeds its counterpart in Other.
    """
    self_list = self.toList()
    other_list = Other.toList()
    self_is_lower= True
    for k in range(len(self_list)):
      if self_list[k] >= other_list[k]:
        self_is_lower = False
        break
    return self_is_lower


  def __ge__(self, Other): # implementation of operator >=
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Other is an instance of EnvironmentalImpact 
      - attributes land_use, GHG_emissions, ... must have been set in self in in Other
    Postconditions: [none]
    Result: True if all components of self are greater or equal to their counterparts in Other,
    False if at least one component of Impact is strictly lower than its counterpart in Other.
    """
    self_list = self.toList()
    other_list = Other.toList()
    self_is_greater_or_equal = True
    for k in range(len(self_list)):
      if self_list[k] < other_list[k]:
        self_is_greater_or_equal = False
        break
    return self_is_greater_or_equal


  def __gt__(self, Other): # implementation of operator >
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions:
      - Other is an instance of EnvironmentalImpact  
      - attributes land_use, GHG_emissions, ... must have been set in self in in Other
    Postconditions: [none]
    Result: True if all components of self are strictly greater than their counterparts in Other,
    False if at least one component of Impact is lower or equal to its counterpart in Other.
    """
    self_list = self.toList()
    other_list = Other.toList()
    self_is_greater = True
    for k in range(len(self_list)):
      if self_list[k] <= other_list[k]:
        self_is_greater = False
        break
    return self_is_greater


  def saveToFile(self, Filepath):
    """
    Parameters passed in data mode: [all]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions:
      - attributes land_use, GHG_emissions, ... must have been set 
    Postconditions: 
      - a text file named Filepath is created (or overwritten if it pre-existed)
      - it contains one line per attribute
      - each line contains the string conversion of the float value of the attribute
      - attributes are saved in the following order: the land use (in square meters), 
        the amount of greenhouse gas emissions (in kg CO2eq), the amount of acidifying emissions (in g SO2eq), 
        the amount of eutrophying emissions (in g PO43-eq) and the stress-weighted water use (in L).
    Result: [none]
    """
    file = open(Filepath,'w')
    file.write(str(self.land_use) + '\n')
    file.write(str(self.GHG_emissions) + '\n')
    file.write(str(self.acidifying_emissions) + '\n')
    file.write(str(self.eutrophying_emissions) + '\n')
    file.write(str(self.water_use) + '\n')
    file.close()   


  def loadFromFile(self, Filepath):
    """
    Parameters passed in data mode: Filepath
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions: 
      - Filepath is the location and name of a text file containaing 5 lines 
      - each line contains a string conversion of a float value
      - the successive lines contain (in the following order): the land use (in square meters), 
        the amount of greenhouse gas emissions (in kg CO2eq), the amount of acidifying emissions (in g SO2eq), 
        the amount of eutrophying emissions (in g PO43-eq) and the stress-weighted water use (in L).   
    Postconditions: 
      - the attributes land_use, GHG_emissions, acidifying_emissions, eutrophying_emissions and water_use are set 
        to the values contained in the file.
    Result: [none]
    """
    file = open(Filepath,'r')
    line = file.readline()
    self.land_use = float(line.split()[0])
    line = file.readline()
    self.GHG_emissions = float(line.split()[0])
    line = file.readline()
    self.acidifying_emissions = float(line.split()[0])
    line = file.readline()
    self.eutrophying_emissions = float(line.split()[0])
    line = file.readline()
    self.water_use  = float(line.split()[0])
    file.close() 


  def printToScreen(self):
    """
    Parameters passed in data mode: self
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - attributes land_use, GHG_emissions, ... must have been set 
    Postconditions: 
      - the values of the attributes land_use, GHG_emissions, acidifying_emissions, eutrophying_emissions and water_use
        are printed to screen.
    Result: [none]
    """
    print('Land use              : {0:8.2f} square meters'.format(self.land_use))
    print('GHG emissions         : {0:8.2f} kg CO2 eq.'.format(self.GHG_emissions))
    print('Acidifying emissions  : {0:8.2f} g SO2 eq.'.format(self.acidifying_emissions))
    print('Eutrophying emissions : {0:8.2f} g PO43- eq.'.format(self.eutrophying_emissions))
    print('Water use             : {0:8.2f} L'.format(self.water_use))



###############################
# Class EnvironmentalDatabase #
###############################


class EnvironmentalDatabase(object):

  def __init__(self, Filepath=''):
    """
    Parameters passed in data mode: Filepath
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: self
    Preconditions:       
      - Filepath, when given, is the path to an XLSX file containing a sheet called 'Results - Retail Weight'
      - In this sheet, the following columns contain the following data:
          - A : Food name
          - E : Median land use across all producers, in sq meters per retail unit
          - K : Median greenhouse gas emissions across all producers, in kgCO2eq. per retail unit
          - W : Median acidifying emissions across all producers, in gSO2eq. per retail unit
          - AC: Median eutrophying emissions across all producers, in gPO43-eq. per retail unit  
          - AO: Median stress-weighted water use across all producers, in L per retail unit.
    Postconditions:       
      - self.land_use_dict associates to each food the median land use across all producers, in sq meters per retail unit
      - self.GHG_emissions_dict associates to each food the median greenhouse gas emissions across all producers, in kgCO2eq. per retail unit
      - self.acidifying_emissions_dict associates to each food the median acidifying emissions across all producers, in gSO2eq. per retail unit
      - self.eutrophying_emissions_dict associates to each food the median eutrophying emissions across all producers, in gPO43-eq. per retail unit
      - self.water_use_dict associates to each food the median stress-weighted water use across all producers, in L per retail unit. 
    Result: self
    """
    self.land_use_dict              = {}
    self.GHG_emissions_dict         = {}
    self.acidifying_emissions_dict  = {}
    self.eutrophying_emissions_dict = {}
    self.water_use_dict             = {}
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
      - self.land_use_dict associates to each food the median land use across all producers, in sq meters per retail unit
      - self.GHG_emissions_dict associates to each food the median greenhouse gas emissions across all producers, in kgCO2eq. per retail unit
      - self.acidifying_emissions_dict associates to each food the median acidifying emissions across all producers, in gSO2eq. per retail unit
      - self.eutrophying_emissions_dict associates to each food the median eutrophying emissions across all producers, in gPO43-eq. per retail unit
      - self.water_use_dict associates to each food the median stress-weighted water use across all producers, in L per retail unit.  
    Result: [none]
    """
    self.land_use_dict = {'Wheat & Rye (Bread)': 2.7,
                    'Maize (Meal)': 1.8,
                    'Potatoes': 0.8,
                    'Beet Sugar': 1.5,
                    'Tofu': 3.4,
                    'Rapeseed Oil': 9.4,
                    'Olive Oil': 17.3,
                    'Tomatoes': 0.2,
                    'Root Vegetables': 0.3,
                    'Other Vegetables': 0.2,
                    'Bananas': 1.4,
                    'Apples': 0.5,
                    'Berries & Grapes': 2.6,
                    'Coffee': 11.9,
                    'Dark Chocolate': 53.8,
                    'Bovine Meat (beef herd)': 170.4,
                    'Poultry Meat': 11.0,
                    'Eggs': 5.7
                  }

    self.GHG_emissions_dict = {'Wheat & Rye (Bread)': 1.3,
                      'Maize (Meal)': 1.2,
                      'Potatoes': 0.5,
                      'Beet Sugar': 1.8,
                      'Tofu': 2.6,
                      'Rapeseed Oil': 3.5,
                      'Olive Oil': 5.1,
                      'Tomatoes': 0.7,
                      'Root Vegetables': 0.4,
                      'Other Vegetables': 0.4,
                      'Bananas': 0.8,
                      'Apples': 0.4,
                      'Berries & Grapes': 1.4,
                      'Coffee': 8.2,
                      'Dark Chocolate': 5.0,
                      'Bovine Meat (beef herd)': 60.4,
                      'Poultry Meat': 7.5,
                      'Eggs': 4.2
                    }

    self.acidifying_emissions_dict = {'Wheat & Rye (Bread)': 13.3,
                      'Maize (Meal)': 10.2,
                      'Potatoes': 3.6,
                      'Beet Sugar': 12.4,
                      'Tofu': 6.0,
                      'Rapeseed Oil': 23.2,
                      'Olive Oil': 33.9,
                      'Tomatoes': 5.2,
                      'Root Vegetables': 2.9,
                      'Other Vegetables': 3.7,
                      'Bananas': 6.1,
                      'Apples': 4.0,
                      'Berries & Grapes': 6.9,
                      'Coffee': 87.2,
                      'Dark Chocolate': 29.0,
                      'Bovine Meat (beef herd)': 270.9,
                      'Poultry Meat': 64.7,
                      'Eggs': 54.2
                    }

    self.eutrophying_emissions_dict = {'Wheat & Rye (Bread)': 5.4,
                      'Maize (Meal)': 2.4,
                      'Potatoes': 4.4,
                      'Beet Sugar': 4.3,
                      'Tofu': 6.6,
                      'Rapeseed Oil': 16.4,
                      'Olive Oil': 39.1,
                      'Tomatoes': 1.9,
                      'Root Vegetables': 1.0,
                      'Other Vegetables': 1.8,
                      'Bananas': 2.1,
                      'Apples': 2.0,
                      'Berries & Grapes': 1.0,
                      'Coffee': 49.9,
                      'Dark Chocolate': 67.3,
                      'Bovine Meat (beef herd)': 320.7,
                      'Poultry Meat': 34.5,
                      'Eggs': 21.3
                    }

    self.water_use_dict = {'Wheat & Rye (Bread)': 12822,
                      'Maize (Meal)': 350,
                      'Potatoes': 78,
                      'Beet Sugar': 115,
                      'Tofu': 32,
                      'Rapeseed Oil': 14,
                      'Olive Oil': 24396,
                      'Tomatoes': 4481,
                      'Root Vegetables': 38,
                      'Other Vegetables': 2940,
                      'Bananas': 31,
                      'Apples': 1025,
                      'Berries & Grapes': 16245,
                      'Coffee': 341,
                      'Dark Chocolate': 220,
                      'Bovine Meat (beef herd)': 441,
                      'Poultry Meat': 334,
                      'Eggs': 18621
                    }

    

  def loadFromFile(self, Filepath):
    """
    Parameters passed in data mode: Filepath
    Parameters passed in data/result mode: self
    Parameters passed in result mode: [none]
    Preconditions:
      - Filepath, when given, is the path to an XLSX file containing a sheet called 'Results - Retail Weight'
      - In this sheet, the following columns contain the following data:
          - A : Food name
          - E : Median land use across all producers, in sq meters per retail unit
          - K : Median greenhouse gas emissions across all producers, in kgCO2eq. per retail unit
          - W : Median acidifying emissions across all producers, in gSO2eq. per retail unit
          - AC: Median eutrophying emissions across all producers, in gPO43-eq. per retail unit  
          - AO: Median stress-weighted water use across all producers, in L per retail unit.
    Postconditions:       
      - self.land_use_dict associates to each food the median land use across all producers, in sq meters per retail unit
      - self.GHG_emissions_dict associates to each food the median greenhouse gas emissions across all producers, in kgCO2eq. per retail unit
      - self.acidifying_emissions_dict associates to each food the median acidifying emissions across all producers, in gSO2eq. per retail unit
      - self.eutrophying_emissions_dict associates to each food the median eutrophying emissions across all producers, in gPO43-eq. per retail unit
      - self.water_use_dict associates to each food the median stress-weighted water use across all producers, in L per retail unit.  
    Result: [none]
    """
    env_data = pd.read_excel(Filepath, 
      sheet_name='Results - Retail Weight',
      skiprows=[0,1,46,47,48], # row 2 is used as a header maybe
      usecols='A,E,K,W,AC,AO',
      names=['Product', 'LandUse', 'GHGEmissions', 'AcidifyingEmissions', 'EutrophyingEmissions', 'WaterUse'])
    self.land_use_dict              = dict(zip(env_data['Product'], env_data['LandUse']))
    self.GHG_emissions_dict         = dict(zip(env_data['Product'], env_data['GHGEmissions']))
    self.acidifying_emissions_dict  = dict(zip(env_data['Product'], env_data['AcidifyingEmissions']))
    self.eutrophying_emissions_dict = dict(zip(env_data['Product'], env_data['EutrophyingEmissions']))
    self.water_use_dict             = dict(zip(env_data['Product'], env_data['WaterUse']))


  def isConsistentWith(self, NutrDB):
    """
    Parameters passed in data mode: self, NutrDB
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: [none]
    Postconditions: [none]
    Result: True is all foods listed in NutrDB exist as keys in all dictionaries in self
    """
    consistent = True
    for food in NutrDB.protein_sources + NutrDB.carb_sources + NutrDB.fat_sources + NutrDB.vegetables + NutrDB.fruits + NutrDB.extras:
      if food not in self.land_use_dict:
        print('Warning: missing land use for ' + food)
        consistent = False
      if food not in self.GHG_emissions_dict:
        print('Warning: missing GH emissions for ' + food)
        consistent = False
      if food not in self.acidifying_emissions_dict:
        print('Warning: missing acidifying emissions for ' + food)
        consistent = False
      if food not in self.eutrophying_emissions_dict:
        print('Warning: missing eutrophying emissions for ' + food)
        consistent = False
      if food not in self.water_use_dict:
        print('Warning: missing water use for ' + food)
        consistent = False
    return consistent


  def getLandUse(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.land_use_dict
      - Qty is a float
    Postconditions: [none]
    Result: land use (in square meters) of the given Qty of Food
    """
    return (Qty*self.land_use_dict[Food])

  def getGHGEmissions(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.GHG_emissions_dict
      - Qty is a float
    Postconditions: [none]
    Result: amount of GHG emissions (kgCO2eq.) of the given Qty of Food
    """
    return (Qty*self.GHG_emissions_dict[Food])

  def getAcidifyingEmissions(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.acidifying_emissions_dict
      - Qty is a float
    Postconditions: [none]
    Result: amount of acidifying emissions (gSO2eq.) of the given Qty of Food
    """
    return (Qty*self.acidifying_emissions_dict[Food])

  def getEutrophyingEmissions(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.eutrophying_emissions_dict
      - Qty is a float
    Postconditions: [none]
    Result: amount of acidifying emissions (gPO43-eq.) of the given Qty of Food
    """
    return (Qty*self.eutrophying_emissions_dict[Food])

  def getWaterUse(self, Food, Qty=1.0):
    """
    Parameters passed in data mode: [all of them]
    Parameters passed in data/result mode: [none]
    Parameters passed in result mode: [none]
    Preconditions: 
      - Food is a string
      - Food exists as a key in self.water_use_dict
      - Qty is a float
    Postconditions: [none]
    Result: stress-weighted freshwater use (in L) of the given Qty of Food
    """
    return (Qty*self.water_use_dict[Food])



if __name__=="__main__":

  envimpact1 = EnvironmentalImpact([1.5, 25, 5, 10, 2000])
  envimpact2 = EnvironmentalImpact([3.0, 20, 3, 11, 1800])
  envimpact3 = envimpact1 + envimpact2
  envimpact3.printToScreen()