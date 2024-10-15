import tkinter as tk
import tkinter.filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



import usermodule 
import nutritionDBmodule
import envDBmodule

####################################
# Class View (inherits from tk.Tk) #
####################################

class View(tk.Tk):

  def __init__(self, controller):
    tk.Tk.__init__(self)
    self.controller = controller
    self.title("Eco-friendly meal generator")
    self.buildUI()


  def buildUI(self):
    tk.Label(self, text='Gender:', anchor="sw", justify="left").grid(row=0, column=0, sticky="WS")
    self.gender_radio_btn = tk.StringVar(self)
    tk.Radiobutton(self, text="Male",value = "M", variable = self.gender_radio_btn).grid(row=0, column=1, sticky="W")
    tk.Radiobutton(self, text="Female",value = "F", variable = self.gender_radio_btn).grid(row=0, column=2, sticky="W")
    self.gender_radio_btn.set("F")

    tk.Label(self, text='Height (cm):', anchor="sw", justify="left").grid(row=1, column=0, sticky="WS")
    self.height_scale = tk.Scale(self, from_=80, to=220, resolution=1, orient='horizontal', length=200)
    self.height_scale.set(165)
    self.height_scale.grid(row=1, column=1, columnspan = 2, sticky="W")

    tk.Label(self, text='Body weight (kg):', anchor="sw", justify="left").grid(row=2, column=0, sticky="WS")
    self.weight_scale = tk.Scale(self, from_=20, to=200, resolution=1, orient='horizontal', length=200)
    self.weight_scale.set(58)
    self.weight_scale.grid(row=2, column=1, columnspan = 2, sticky="W")

    buttons_frame = tk.Frame(self)
    tk.Button(buttons_frame, text='Update parameters', command=self.controller.updateUserParameters).pack(side="left")
    tk.Button(buttons_frame, text='Compute energy requirements', command=self.controller.computeEnergyRequirement).pack(side="left")
    buttons_frame.grid(row = 3, column = 0, columnspan = 4)

    tk.Label(self, text='Basal metabolic rate: ', anchor="sw", justify="left").grid(row=4, column=0, sticky="WS")
    self.message0 = tk.Message(self, text='', width=200, anchor="w")
    self.message0.grid(row = 4, column = 1)
    tk.Label(self, text='Daily energy requirement: ', anchor="sw", justify="left").grid(row=5, column=0, sticky="WS")
    self.message1 = tk.Message(self, text='', width=200, anchor="w")
    self.message1.grid(row = 5, column = 1)
    tk.Label(self, text='Lunch or dinner should bring: ', anchor="sw", justify="left").grid(row=6, column=0, sticky="WS")
    self.message2 = tk.Message(self, text='', width=200, anchor="w")
    self.message2.grid(row = 6, column = 1)

    tk.Button(self, text='Compute possible meals', command=self.controller.computePossibleMeals).grid(row = 7, column = 0)
    tk.Button(self, text='Draw histograms', command=self.controller.drawHistograms).grid(row = 7, column = 1)

  def drawHisto(self, TheFigure):
    self.canvas = FigureCanvasTkAgg(TheFigure, master=self)  
    self.canvas.draw()
    self.canvas.get_tk_widget().grid(row = 8, column = 0, columnspan=2)


  def get_gender(self):
    return self.gender_radio_btn.get()

  def get_height(self):
    return self.height_scale.get()

  def get_weight(self):
    return self.weight_scale.get()



####################
# Class Controller #
####################

class Controller(object):
  
  def __init__(self):
    print('Importing nutritional data... ', end='')
    self.nutrDB = nutritionDBmodule.NutritionDatabase('poore2018/TableS1_augmented_with_FAO_data.xlsx')
    assert(self.nutrDB.isComplete())
    assert(self.nutrDB.isConsistent())
    print('done')

    print('Importing environmental data... ', end='')
    self.envDB = envDBmodule.EnvironmentalDatabase('poore2018/DataS2.xlsx')
    assert(self.envDB.isConsistentWith(self.nutrDB))
    print('done')

    self.view = View(self)
    self.user = usermodule.User()
    self.user.setExtraQuantities(self.nutrDB)

    self.meal_kcal_target = None
    self.all_valid_meals = None
    self.view.mainloop()


  def updateUserParameters(self):
    self.user.gender = self.view.get_gender()
    self.user.height = self.view.get_height()
    self.user.body_weight = self.view.get_weight()

  def computeEnergyRequirement(self):
    self.updateUserParameters()
    bmr = self.user.basalMetabolicRate()
    daily_req = self.user.dailyEnergyRequirement()
    self.meal_kcal_target = 0.4*daily_req
    self.view.message0.config(text=str(bmr)+' kcal')
    self.view.message1.config(text=str(daily_req)+' kcal')
    self.view.message2.config(text=str(self.meal_kcal_target)+' kcal')

  def computePossibleMeals(self):
    self.all_valid_meals = self.nutrDB.enumerateAllPossibleMealsWithQuantities(self.meal_kcal_target, self.user.extra_qty_dict)

  def drawHistograms(self):
    self.all_valid_meals.computeAllEnvironmentalImpacts(self.envDB)
    fig = self.all_valid_meals.drawEnvironmentalImpactHistograms('embedded')
    self.view.drawHisto(fig)



################
# Main program #
################

if __name__=="__main__":
  app = Controller()




