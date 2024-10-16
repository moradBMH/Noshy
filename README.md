# Noshy: Sustainable Meal Generator

Noshy is a Python-based application that generates personalized meal plans tailored to your nutritional needs and environmental impact. Whether you're looking to meet specific energy requirements or make more eco-friendly food choices, Noshy simplifies the process with its user-friendly interface and database-driven recommendations.

## Features

**Personalized Meal Planning**: Input your gender, height, and weight to calculate your daily energy requirements.

**Eco-Friendly Choices**: Noshy suggests meals that balance both your nutritional needs and the environmental impact of the food you consume.

**Data Visualization**: Visualize your intake vs. your required nutritional needs with histograms.

**Simple Interface**: Built using `tkinter`, making it easy for users to interact with the application.

## Why Noshy is Useful

Noshy is designed for users who want to balance personal health and environmental responsibility. By providing meal suggestions that account for both nutritional value and eco-friendliness, it helps reduce your carbon footprint while maintaining a healthy diet.

## Getting Started

### Prerequisites

You will need **Python** installed on your machine. The required libraries can be installed using `requirements.txt`.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/moradBMH/Noshy.git
   cd Noshy
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Run the application**:
   ```bash
   python main.py

### How to use Noshy 

1. **Enter Personal Data**: Input your gender, height, and weight to calculate your daily energy needs.
2. **Generate Meals**: Get meal recommendations based on your energy requirements and environmental impact.
3. **Visualize Data**: View histograms comparing your actual intake to your nutritional needs.

### File structure

- **main.py**: Entry point for running the application.
- **gui.py**: Handles the graphical user interface.
- **usermodule.py**: Manages user-specific data like gender, height, and weight.
- **nutritionDBmodule.py**: Loads and manages the nutritional data.
- **envDBmodule.py**: Handles the environmental impact data for different foods.
  
### Maintainers and contributors 

This project is maintained by Morad Bel Melih. Contributions are welcome! Fork the repo, submit pull requests, or raise issues.

