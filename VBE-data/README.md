# VBE Data

This repository contains the first step in pulling data to calculate observable Voting Bloc Entropy (oVBE). This repo is used to get your database set up for DAO, proposal, and votes data, given a list of DAO metadata that is specified. The repository and work featured in the paper _Voting-Bloc Entropy: A New Metric for DAO Decentralization_ extracts off-chain and on-chain voting information from Snapshot and Tally API. Additionally, there is a group of scripts that calculate analytics on top of data previously extracted, including DAO, proposal, and voter level data. The information is aggregated, manipulated, and made easier for dashboard and reporting purposes. 

## Methodology

For details on our methodology, refer to [METHODOLOGY.md](METHODOLOGY.md). Below is an outline of the key steps:

1. DAO data retrieval from open source APIs such as Snapshot, Tally, Boardroom
2. Data standardization across different APIs, including significant cleaning and cross-referencing of data
3. Manually augmenting dataset according to expert consultation, and aggregating this data in a PostgreSQL database.
4. Data filtering to identify valid data for clustering and analysis, such as only counting voters that have voted on at least one proposal.
5. Calculating VBE across different organizations and within a signle organization.
6. Visualizing results.


## Setup

1. Clone repository 
   ```
   git clone git@github.com:DAO-Decentralization/VBE.git
   ```
2. Set up and activate virtual environment
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. If anything is missing, use ```pip install``` to complete

## Configure Environment Variables
We provide connections for a read-only database (no write capabilities) by default. This database has all information shown in figures in the paper _Voting-Bloc Entropy: A New Metric for DAO Decentralization_ and in the VBE DAO Dashboard. If you plan on saving data from Snapshot or Tally to perform your own VBE experiments, we highly recommend setting up your own database connection as a large quantity of records will be stored.
While we provide an option to save data to Excel csv format, this is only recommended for limited pulls (by proposal or DAOs with less votes). 

- How to get [Snapshot API Key](https://tally.so/r/3laKWp)
- How to get [Tally API Key](https://docs.tally.xyz/set-up-and-technical-documentation/welcome)
- How to get [Boardroom API Key](https://docs.boardroom.io/docs/api/cd5e0c8aa2bc1-overview) (optional)
- Steps for setting up an [AWS relational database (PostgreSQL)](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html)

Create a `.env` file in the root directory with the following variables:

```
DB_HOST=<DB_HOST>
DB_PORT=<DB_PORT>
DB_NAME=<DB_NAME>
DB_USER=<DB_USER>
DB_PASSWORD=<DB_PASSWORD>

TALLY_API_URL=https://api.tally.xyz/query
TALLY_API_KEY=<YOUR-API-KEY>

SNAPSHOT_GRAPHQL_ENDPOINT=https://hub.snapshot.org/graphql
SNAPSHOT_API_KEY=<YOUR-API-KEY>
BOARDROOM_API_KEY=<YOUR-API-KEY>
```

## Data Setup
1. Navigate to data_setup folder with `cd data_setup/` 
    1. First, update `dao_input.csv` to match whatever DAOs that you’re looking for.
    
    _Note: it is recommended to limit the number of DAOs listed. To pull all historical proposals associated with the default list of DAOs, you can expect for the code to run for 6+ hours. This is due to the limitation of Snapshot and Tally API and pagination through records._
   
    2. If pulling from Snapshot:
        1. Must insert ```dao_id``` and put “Snapshot” under platform column
        2. The DAO id in Snapshot can be found using the URL for DAOs, in the format [https://snapshot.box/#/s:](https://snapshot.box/#/s:gmx.eth)[dao_id] or https://snapshot.box/#/s:arbitrumfoundation.eth
    3. If pulling from Tally:
        1. Must insert ```dao_slug``` and put “Tally” under platform column
        2. The DAO slug in Tally can be found using the URL for individual DAOs in the format [https://www.tally.xyz/gov/](https://www.tally.xyz/gov/optimism)[dao_slug] or https://www.tally.xyz/gov/optimism
3. Set up database tables
    1. If you are setting up your own database connection, please use [`rdb.py`](http://rdb.py) to create your initial tables at the start. You can do this by uncommenting line 221.


## Data Extract 
1. Navigate to data_extract folder with `cd data_extract/` 
    1. Once set up, then run `snapshot_api.py` and `tally_api.py` as needed. These will save the information to a database connection specified in `.env`

   _Note that the Database initialization may take up to a few minutes. If you run into issues for connection, please check the security group rules and make sure that your IP address is allowed for TCP connections._
   
    _Note that these scripts are built in a way that they will add any DAOs, Proposals, and Votes not previously written to those tables. There should not be any duplicates written to the database records._

3. `boardroom_api.py` includes forum data. While not explicitly used in any experiments outlined in the paper, we find the information interesting and valuable for contextualizing VBE findings.

We recommend that after these steps, you query the information you saved with ```data_setup/rdb.py``` to understand your relational database, the schemas, and data field values.

## Usage

1. Data Extraction:
   ```
   python data_extract/tally_api.py
   python data_extract/snapshot_api.py
   ```

3. Analytics:
   ```
   python data_extract/data_analytics.py
   ```

## License

This project is licensed under the MIT License.
