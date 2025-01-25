# **AI-Driven Alien Invasion Game**
An engaging arcade game where players defend against waves of aliens, featuring adaptive difficulty powered by machine learning.

**Features**
**Adaptive Difficulty:** Utilizes a Random Forest Regressor model to adjust alien speed based on player metrics (reaction time, accuracy, lives lost).

**Power-Up System:** Temporary boosts to enhance gameplay and challenge.

**Sound & Visual Effects:** Immersive laser, explosion, and power-up sounds with dynamic visuals.

**Metrics Tracking:** Player performance is logged for analysis and difficulty prediction.

**Game Architecture:** Modular design for bullet-alien interactions, scoring, and fleet management.

### **Tools & Technologies**
Programming Language: Python

Libraries: Pygame, Scikit-learn

Machine Learning Model: Random Forest Regressor

Additional Tools: Joblib (model persistence), CSV for logging metrics

## How to Run
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the game with `python main.py`.
