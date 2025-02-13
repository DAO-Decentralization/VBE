import json
import pandas as pd
import numpy as np
from typing import List, Tuple, Set

def featurize_df(df: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame]:
    """
    Featurize the vote allocation DataFrame.
    
    Args:
        df (pd.DataFrame): The vote allocation DataFrame.
    
    Returns:
        Tuple[np.ndarray, pd.DataFrame]: A tuple containing the feature vectors and the pivoted DataFrame.
    """
    # pivot_df = df.pivot(index='voter_address', columns='proposal_id', values='choice_position').fillna(0)
    pivot_df = pd.pivot_table(df, values=['choice_position'], index=['voter_address', 'voting_power'], columns=['proposal_id'], fill_value=0)
    feature_vectors = pivot_df.values
    return feature_vectors, pivot_df

def load_data(path: str) -> Tuple[np.ndarray, pd.DataFrame]:
    """
    Load and process voter/proposal data from a CSV file.
    
    Args:
        path (str): The path to the CSV file.
    
    Returns:
        Tuple[np.ndarray, pd.DataFrame]: A tuple containing the feature vectors and the pivoted DataFrame.
    """
    pd.set_option('display.max_columns', None)  # Show all columns

    voter_df = pd.read_csv(path)
    proposal_df = pd.read_csv(path.replace('votes', 'proposals'))

    # Pick the first 10 proposals in the proposal_df
    first_dao_id = proposal_df.iloc[0]['dao_id']

    # Filter the proposal_df to include only rows with the same dao_id as the first record
    proposal_df_filtered = proposal_df[proposal_df['dao_id'] == first_dao_id]    
    proposal_df = proposal_df_filtered.iloc[:11]

    # Merge the two dataframes
    data = pd.merge(voter_df, proposal_df, on='proposal_id')
    data.drop(data.filter(regex='_y$').columns, axis=1, inplace=True)

    # Make a new column that represents the choice of the voter in integer (1, 2, 3, ...)
    data['choice_position'] = data.apply(lambda row: row['choice'].index(row['choice']) + 1, axis=1)

    # Make sure all voters are represented even if they don't vote on a proposal
    unique_voter_proposals = pd.MultiIndex.from_product([data['voter_address'].unique(), data['proposal_id'].unique()], names=['voter_address', 'proposal_id']).to_frame(index=False)
    new_voter_df = pd.merge(unique_voter_proposals, data, how='left', on=['voter_address', 'proposal_id'])
    new_voter_df['choice_position'] = new_voter_df['choice_position'].fillna(0)
    new_voter_df['voting_power'] = pd.to_numeric(new_voter_df['voting_power'], errors='coerce')

    grouped = new_voter_df.groupby('voter_address')['voting_power']

    def fill_voting_power(series):
        mean_value = series.mean(skipna=True)  
        return series.fillna(mean_value)
    
    transformed_voting_power = grouped.transform(fill_voting_power)
    new_voter_df['voting_power'] = transformed_voting_power
    new_voter_df['voting_power'] = new_voter_df.groupby('voter_address')['voting_power'].transform(lambda x: x.fillna(x.mean()))

    feature_vectors, pivot_df = featurize_df(new_voter_df)

    pivot_reset = pivot_df.reset_index()

    # Select only the 'voter_address' column
    voter_address_df = pivot_reset[['voter_address']]
    # print(len(new_voter_df.index)) # 1800 rows
    
    return feature_vectors, pivot_df, voter_address_df

# def main():
#     path = '../../VBE-data/data_output/votes.csv'
#     feature_vectors, pivot_df = load_data(path)
#     print(pivot_df)

# if __name__ == '__main__':
#     main()