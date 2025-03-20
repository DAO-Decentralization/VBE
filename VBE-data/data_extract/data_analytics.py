"""
data_analytics.py

This module provides functionality to analyze and generate various analytics from DAO proposal and voting data.
"""

import database as db
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class DataProcessor:
    @staticmethod
    def format_output(daopercentile_df, protocol, describe_output, measure):
        percentiles = np.arange(10, 100, 10)
        formatted_rows = []
        for percentile in percentiles:
            formatted_row = {
                'id': len(daopercentile_df) + len(formatted_rows) + 1,
                "protocol": protocol,
                "measure": measure,
                "percentile": float(percentile),
                "value": describe_output.get(f'{percentile}%', np.nan),  # Handle missing percentiles
                "mean": describe_output['mean'],
                "std": describe_output['std']
            }
            formatted_rows.append(formatted_row)
        
        formatted_df = pd.DataFrame(formatted_rows)
        daopercentile_df = pd.concat([daopercentile_df, formatted_df], ignore_index=True)

        return daopercentile_df

    @staticmethod
    def votes_by_choice(proposal_df, field, measure, choice):
        choice_df = proposal_df[proposal_df['choice'] == choice]
        if measure == "sum_choice":
            return choice_df['voter_address'].nunique()
        
        if measure in ["sum_voting_power", "avg_voting_power"]:
            numeric_field = pd.to_numeric(choice_df[field], errors='coerce')  # Convert to numeric, set errors to NaN
        
            if measure == "sum_voting_power":
                return numeric_field.sum()
            
            elif measure == "avg_voting_power":
                return numeric_field.mean() if not numeric_field.isna().all() else 0  # Return 0 if all values are NaN

class AnalyticsGenerator:
    def __init__(self, merged_df):
        self.merged_df = merged_df

    def generate_dao_level_analytics(self):
        protocol_list = self.merged_df['dao_id'].unique()
        print("DAO list:", protocol_list)
        daolevel_df = pd.DataFrame(columns=['id', 'protocol', 'dao_name', 'unique_voters', 'total_proposals', 'total_votes_cast', 'avg_votes_on_proposal', 'avg_votes_voter', 'avg_vp_voter', 'avg_voter_participation', 'gini_index', 'nakamoto_coefficient', 'min_entropy'])
        daopercentile_df = pd.DataFrame(columns=['id', 'protocol', 'measure', 'mean', 'std', 'percentile', 'value'])

        for dao_id in protocol_list:
            print("DAO id:", dao_id)
            dao_df = self.merged_df[self.merged_df['dao_id'] == dao_id]
            if len(dao_df) == 0:
                continue
            
            total_votes_cast = float(len(dao_df['voter_address']))  # Convert to float
            unique_voter_ct = float(len(dao_df['voter_address'].unique()))  # Convert to float
            total_proposals = float(len(dao_df['proposal_id'].unique()))  # Convert to float
            avg_votes_voter = float(dao_df.groupby('voter_address').size().mean())  # Convert to float
            average_vp = dao_df.groupby('voter_address')['voting_power'].max().astype(float)  # Convert to float # vag
            average_vp_per_voter = float(average_vp.mean())  # Convert to float

            # Gini index
            sorted_vp = average_vp.sort_values().values
            if len(sorted_vp) > 0:
                cumulative_vp = np.cumsum(sorted_vp)
                total_vp = cumulative_vp[-1]
                normalized_cumulative_vp = cumulative_vp / total_vp
                x = np.linspace(0, 1, len(normalized_cumulative_vp))
                gini_index = 1 - 2 * np.trapz(normalized_cumulative_vp, x)
            else:
                gini_index = float('nan')
            
            # Average voter participation
            votes_cast = dao_df.groupby('proposal_id')['voter_address'].nunique().tolist()
            participation_rate = [votes / unique_voter_ct for votes in votes_cast]
            avg_voter_participation = sum(participation_rate) / len(participation_rate)

            # Nakamoto coefficient
            sorted_vp_desc = average_vp.sort_values(ascending=False)
            cumulative_vp_desc = np.cumsum(sorted_vp_desc)
            threshold = 0.5 * cumulative_vp_desc[-1]  # 50% of the total voting power
            index_of_threshold = np.argmax(cumulative_vp_desc >= threshold)
            nakamoto_coefficient = int(index_of_threshold) + 1

            # Minimum entropy
            normalized_vp = average_vp / average_vp.sum()  # Normalize to get probabilities
            min_entropy = -np.sum(normalized_vp * np.log2(normalized_vp + 1e-10))  # Add epsilon to avoid log(0)

            new_row_df = pd.DataFrame([{
                'id': len(daolevel_df) + 1,
                'dao_name': dao_df['dao_name'].iloc[0],
                'protocol': dao_id,
                'total_votes_cast': total_votes_cast,
                'total_proposals': total_proposals,
                'unique_voters': unique_voter_ct,
                'avg_votes_on_proposal': total_votes_cast / total_proposals,
                'avg_vp_voter': average_vp_per_voter,
                'avg_votes_voter': avg_votes_voter,
                'avg_voter_participation': avg_voter_participation,
                'gini_index': gini_index,
                'nakamoto_coefficient': nakamoto_coefficient,
                'min_entropy': min_entropy
            }])
            daolevel_df = pd.concat([daolevel_df, new_row_df], ignore_index=True)

            # Create percentile df
            avg_vp_describe = average_vp.describe(percentiles=np.arange(0.1, 1.0, 0.1)).to_dict()
            vote_counts = dao_df['voter_address'].value_counts()
            avg_vc_describe = vote_counts.describe(percentiles=np.arange(0.1, 1.0, 0.1)).to_dict()

            # Create DataFrame for percentiles
            daopercentile_df = DataProcessor.format_output(daopercentile_df, dao_id, avg_vp_describe, 'voting_power')
            daopercentile_df = DataProcessor.format_output(daopercentile_df, dao_id, avg_vc_describe, 'vote_counts')

        return daolevel_df, daopercentile_df

    def generate_proposal_level_analytics(self, proposal_stats_df):
        proposal_list = self.merged_df['proposal_id'].unique()
        proposallevel_df = pd.DataFrame(columns=['id', 'proposal_id', 'choice', 'measure', 'value'])
        if len(proposal_stats_df) > 0:
            existing_proposals = proposal_stats_df['proposal_id'].unique()
        else:
            existing_proposals = []
        
        for proposal in proposal_list:
            if proposal in existing_proposals:
                continue
            
            print("Proposal id:", proposal)
            proposal_df = self.merged_df[self.merged_df['proposal_id'] == proposal]
            for choice in proposal_df['choice'].unique():
                for measure in ['sum_choice', 'sum_voting_power', 'avg_voting_power']:
                    field = 'voting_power' if 'voting_power' in measure else 'choice'
                    value = DataProcessor.votes_by_choice(proposal_df, field, measure, choice)
                    # Append the new row with the calculated metrics
                    new_row = {
                        'id': len(proposallevel_df) + 1,
                        'proposal_id': proposal,
                        'choice': choice,
                        'measure': measure,
                        'value': value
                    }
                    proposallevel_df = pd.concat([proposallevel_df, pd.DataFrame([new_row])], ignore_index=True)

        return proposallevel_df

def main():
    pd.set_option('display.max_columns', None)
    load_from_csv = input("Do you want to **load** from CSV instead of using the database? (Y/N): ").strip().upper()
    save_to_csv = input("Do you want to **save** to CSV instead of using the database? (Y/N): ").strip().upper()
    run_dao = input("Do you want to run DAO-level stats? (Y/N): ").strip().upper()
    run_proposal = input("Do you want to run proposal-level stats? (Y/N): ").strip().upper()
    
    if load_from_csv == "Y":
        print("Loading data from CSV files...")
        voter_df = pd.read_csv("../data_output/votes.csv")
        proposal_df = pd.read_csv("../data_output/proposals.csv")
        dao_df = pd.read_csv("../data_output/dao.csv")
        proposal_stats_df = pd.DataFrame()
    else:
        print("Loading data from database...")
        sql_handler = db.DatabaseHandler()
        voter_df = sql_handler.db_to_df("votes")
        proposal_df = sql_handler.db_to_df("proposals")
        dao_df = sql_handler.db_to_df("dao")
        proposal_stats_df = sql_handler.db_to_df("proposal_stats")
    
    print("All data loaded, merging voters and proposals...")
    merged_df = pd.merge(voter_df, proposal_df, how="left", on=['proposal_id'], suffixes=('', '_proposal'))
    merged_df.drop(merged_df.filter(regex='_proposal$').columns, axis=1, inplace=True)
    
    print("Merging DAOs...")
    merged_df = pd.merge(merged_df, dao_df, how="left", on=['dao_id'], suffixes=('', '_dao'))
    merged_df.drop(merged_df.filter(regex='_dao$').columns, axis=1, inplace=True)

    analytics_generator = AnalyticsGenerator(merged_df)
    if run_dao == "Y":
        print("Generating DAO level analytics...")
        dao_stats_df, dao_percentile_df = analytics_generator.generate_dao_level_analytics()

        if save_to_csv == "Y":
            print("Saving DAO stats and percentiles to CSV...")
            dao_stats_df.to_csv("../data_output/dao_stats.csv", index=False)
            dao_percentile_df.to_csv("../data_output/dao_percentile.csv", index=False)
        else:
            print("Updating DAO stats and percentiles in database...")
            sql_handler.df_to_sql(dao_stats_df, 'dao_stats', if_exists='replace')
            sql_handler.df_to_sql(dao_percentile_df, 'dao_percentile', if_exists='replace')
    
    if run_proposal == "Y":
        print("Generating proposal level analytics...")
        proposal_stats_df = analytics_generator.generate_proposal_level_analytics(proposal_stats_df)

        if len(proposal_stats_df) > 0:
            if save_to_csv == "Y":
                print("Saving proposal stats to CSV...")
                proposal_stats_df.to_csv("../data_output/proposal_stats.csv", index=False)
            else:
                print("Adding proposal stats to database...")
                sql_handler.df_to_sql(proposal_stats_df, 'proposal_stats', if_exists='append')

if __name__ == "__main__":
    main()
