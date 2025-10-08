"""
ml.py - Machine Learning Utilities

Purpose:
    Contains placeholder functions for classification and predictive analytics.

Responsibilities:
    - Predict ticket category or priority from user input
    - Generate dummy predictions for analytics dashboards
    - Serve as a base for integrating scikit-learn models later
"""

# Example placeholder imports (real model integration later)
from random import choice

def predict_category(title: str) -> str:
    """
    Predict ticket category from its title (dummy implementation).
    
    Args:
        title (str): Ticket title/description.
    
    Returns:
        str: Predicted category.
    """
    categories = ["Network", "Hardware", "Software", "Access", "Other"]
    return choice(categories)

def predict_priority(title: str) -> str:
    """
    Predict ticket priority from its title (dummy implementation).
    """
    priorities = ["Low", "Medium", "High"]
    return choice(priorities)

def forecast_ticket_load(days: int = 7):
    """
    Predict future ticket load (dummy linear projection).
    Returns a dict with day labels and values.
    """
    return {
        "labels": [f"Day {i+1}" for i in range(days)],
        "values": [10 + i * 2 for i in range(days)]
    }
