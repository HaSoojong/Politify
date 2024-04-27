import numpy as np
import pandas as pd

stateWeight = {
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
    "New Mexico" : .5444
    }


def stateWeights():
    return stateWeight