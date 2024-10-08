import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import itertools

def computing(inputs_df):
    # Compute the average and span for each variable in the inputs DataFrame
    # The average is calculated as the midpoint between 'low' and 'high' values
    inputs_df['average'] = inputs_df.apply(lambda z: (z['high'] + z['low']) / 2, axis=1)

    # The span is calculated as half the difference between 'high' and 'low' values
    inputs_df['span'] = inputs_df.apply(lambda z: (z['high'] - z['low']) / 2, axis=1)

    # Encode the data using standardized values for 'low', 'center', and 'high'
    # The encoding formula centers the data around the average and scales it by the span
    inputs_df['encoded_low'] = inputs_df.apply(lambda z: (z['low'] - z['average']) / z['span'], axis=1)
    inputs_df['encoded_center'] = inputs_df.apply(lambda z: (z['center'] - z['average']) / z['span'], axis=1)
    inputs_df['encoded_high'] = inputs_df.apply(lambda z: (z['high'] - z['average']) / z['span'], axis=1)

    # Drop the 'average' and 'span' columns as they are no longer needed for further analysis
    inputs_df = inputs_df.drop(['average', 'span'], axis=1)

    # Display the modified inputs DataFrame
    inputs_df

    # Generate all combinations of -1 and 1 for two variables using itertools.product
    encoded_inputs = list(itertools.product([-1, 1], [-1, 1]))
    
    # Append the tuple (0, 0) five times to the list of encoded inputs
    for i in range(0, 5):
        encoded_inputs.append((0, 0))

    # Create a DataFrame from the list of encoded inputs
    results = pd.DataFrame(encoded_inputs)

    # Reverse the order of the columns in the DataFrame
    results = results[results.columns[::-1]]

    #   Rename the columns to 't' for the first column and 'T' for the second column
    results.columns = ['c', 'T']
    
    # Create a copy of results for real_experiment
    real_experiment = results.copy()
    var_labels = []

    # Loop through the existing variables in inputs_df
    for var in inputs_df.index:
        # Get the label for the variable
        var_label = inputs_df.loc[var]['label']
        var_labels.append(var_label)
        
        # Apply the function to create a new column based on conditions
        real_experiment[var_label] = results.apply(
            lambda z: inputs_df.loc[var]['low'] if z[var] < 0 else 
                    (inputs_df.loc[var]['high'] if z[var] > 0 else 
                        inputs_df.loc[var]['center']),
            axis=1
        )
    
    return real_experiment, results