# DAO VBE Repository
The DAO Voting Bloc Entropy (VBE) Repository contains code used to get results in the paper _Voting-Bloc Entropy: A New Metric for DAO Decentralization_. VBE is a decentralization measure tailored to DAO governance, defining centralization as the existence of large voting blocs. The main components in the repository are data extraction, data processing, and calculating clusters and VBE.

In this repo, the following two sections are used as follows:
- ```VBE-data```: data input, optional database setup, data extraction, and data analysis
- ```VBE-library```: tooling to run clusters and calculate VBE on governance data

## Replicating results

1. Please follow the steps in [VBE-data/README.md](/VBE-data/README.md) first, followed by the steps in [VBE-library/README.md](/VBE-library/README.md)
2. Users may select option to save to database or locally to a csv file (not recommended for large data pulls)
