# DAO VBE Repository
The DAO Voting Bloc Entropy (VBE) Repository contains the artifacts from the paper _Voting-Bloc Entropy: A New Metric for DAO Decentralization_. VBE is a decentralization measure tailored to DAO governance, defining centralization as the existence of large voting blocs. The main components of the repository are data extraction scripts, data processing scripts, and a toolkit to calculate VBE.

This repository contains two main directories:
- ```VBE-data```: contains scripts for extracting governance data from DAOs, as well as preparing it in a format compatible with the VBE toolkit
- ```VBE-library```: contains the core logic of the VBE toolkit

## Replicating results

1. Please follow the steps in [VBE-data/README.md](/VBE-data/README.md) first, followed by the steps in [VBE-library/README.md](/VBE-library/README.md)
2. Users may select option to save to database or locally to a csv file (not recommended for large data pulls)
