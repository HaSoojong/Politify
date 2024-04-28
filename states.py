import numpy as np
import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import Base, Trend
import ast

def convert_to_dict(top_region_str):
    try:
        # Safely evaluate the string to a tuple
        evaluated_tuple = ast.literal_eval(top_region_str)
        # Convert the tuple to a dictionary
        return {evaluated_tuple[0]: evaluated_tuple[1]}
    except (SyntaxError, ValueError) as e:
        print(f"Error converting to dictionary: {e}")
        return {}


# Democratic
political_weights = {
    "Massachusetts" : .5230,
    "Arizona" : .4211,
    "Georgia" : .4778,
    "Michigan" : .4886,
    "Nevada" : .4681,
    "North Carolina" : .4713,
    "Pennsylvania" : .5111,
    "Wisconsin" : .4946,
    "New York" : .5595,
    "Florida" : .4494,
    "Texas" : .4457,
    "California" : .6353,
    "Tennessee" : .3605,
    "Minnesota" : .5116,
    "Colorado" : .5568,
    "New Jersey" : .5412,
    "Ohio" : .4382,
    "Alaska" : .4362,
    "Indiana" : .3820,
    "Montana" : .3721,
    "Iowa" : .4302,
    "Maine" : .4571,
    "South Carolina" : .4091,
    "Washington" : .5870,
    "Maryland" : .6279,
    "Utah" : .4342,
    "Missouri" : .3951,
    "South Dakota" : .3210,
    "New Hampshire" : .5517,
    "Virginia" : .5326,
    "Wyoming" : .1807,
    "Arkansas" : .2963,
    "Illinois" : .5584,
    "North Dakota" : .2394,
    "Nebraska" : .3974,
    "West Virginia" : .2805,
    "Kansas" : .3523,
    "Idaho" : .3210,
    "Oklahoma" : .3293,
    "Kentucky" : .3210,
    "New Mexico" : .5444,
    "Alabama" : .4012,
    "Connecticut" : .5526,
    "Delaware" : .5306,
    "District of Columbia" : 0,
    "Rhode Island" : .6049,
    "Mississippi" : .4000,
    "Louisiana" : .3913,
    "Vermont" : .6782,
    "Hawaii" : 6073,
    "Oregon" : .5930,
    "Nevada" : .4574
    }

def compute_final_state_weightings(dataframe):
    #from the dataframe, get the state's average google weight from last column using iloc, divide by 100, multiply by the political weight of that state
    for index, row in dataframe.iterrows():
        state = index
        print(state)
        google_weight = row['Average']
        #sum the google weights for each state and divide by 100
        print(google_weight)
        dataframe.at[index, 'final_weight'] = google_weight / 100 * political_weights.get(state)

    #now sum the final weights for all states and divide 
    percentagesSum = dataframe['Average'].sum() / 100
    final_weight_sum = dataframe['final_weight'].sum()
    return final_weight_sum/percentagesSum

    
