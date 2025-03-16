# VBE Data

This repository contains the first step in pulling data to calculate observable Voting Bloc Entropy (oVBE), including DAO, proposal, and voter data. Data is retrieved from off-chain and on-chain voting platforms Snapshot and Tally API. Post-data extract, analytics are run to get aggregate data for reporting purposes. 

## Methodology

For details on our methodology, refer to [METHODOLOGY.md](METHODOLOGY.md). Below is an outline of the key steps:

1. DAO data retrieval from open source APIs such as Snapshot, Tally, Boardroom
2. Data standardization across different APIs, including significant cleaning and cross-referencing of data
3. Manually augmenting dataset according to expert consultation, and aggregating this data in a PostgreSQL database.
4. Data filtering to identify valid data for clustering and analysis, such as only counting voters that have voted on at least one proposal.
5. Calculating VBE across different organizations and within a signle organization.
6. Visualizing results.


## Steps to Run 

1. Clone Github repo into local home directory using Terminal
   ```
   git clone https://github.com/DAO-Decentralization/VBE.git
   ```

**Install and Set up Multipass Ubuntu Virtual Machine**

2. Install Multipass VM at https://canonical.com/multipass
3. Click on “Install Now”
4. Select OS and instructions to install. After installation, open Multipass for monitoring instances
5. In Terminal, use the following command to launch a VM named “ovbe”
   ```
   multipass launch --name ovbe --cpus 4 --memory 8G --disk 20G
   ```
6. Once VM is running, use the following command to enter the VM. You should receive a message “Welcome to Ubuntu 24.04.2 LTS” and your directory location will change to ```ubuntu@ovbe```:
   ```
   multipass shell ovbe
   ```
   _Optional command  to confirm Linux kernel:_ ```uname -a```

7. Switch back to your local home directory in Terminal to mount the VBE repository into Multipass. Use the following command in a new tab:
   ```
   multipass mount ~/VBE ovbe 
   ```
   
8. Once complete, switch over to the ubuntu ovbe VM Terminal tab to make sure that it was mounted properly. The below should return ```VBE``` in the output:
   ```
   ubuntu@ovbe:~$ ls
   ```
9. Set up virtual environment. All steps below to be completed inside Ubuntu VM: 
   ```
   cd VBE/
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip
   sudo apt install python3-venv libpq-dev
   ```
10. To create and activate the virtual environment, use commands below. The environment should start even if you receive messages in the Terminal:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
11. Change to the VBE-data directory and install the required dependencies. This may take a few minutes:
   ```
   cd VBE-data/
   pip install -r requirements.txt
   ```
12. Because your VBE folder is now mounted, any changes made to local folder will be updated in the VM as well. Copy the ```.env.example``` file and rename the file to ```.env``` using:
   ```
   cp ./".env.example" .env
   ```
   _To edit the env file, use_ ```nano .env```

13. If using your own database, update the database variables in the ```.env``` file. If not, the existing credentials in the .env.example file will provide read-only access to the database If provided any API keys, fill them into ```TALLY_API_KEY```, ```SNAPSHOT_API_KEY```, and ```BOARDROOM_API_KEY``` respectively.

14. The default data pull is limited to 1 Tally and 1 Snapshot record to limit the data retrieval overhead. The full file is `dao_input_full.csv`. To view or edit the DAO inputs, use the following:
   ```
   cd data_setup/
   nano dao_input.csv
   ```

15. Once all DAOs are entered, navigate to the data extract folder and run the Tally and Snapshot files. Enter “Y” if prompted to write to local CSV. 
   ```
   cd ../data_extract/
   python tally_api.py
   ```
16. After message “Process completed successfully.”, run the next script:
   ```
   python snapshot_api.py
   ```
17. Once complete, run the analytics script used to generate metrics:
   ```
   python data_analytics.py
   ```
18. To view the data that has been generated from Tally, Snapshot, and analytics scripts:
   ```
   cd ../data_output/
   ```
19. When ready to apply VBE using the VBE-library:
   ```
   cd ../../VBE-library
   ```

---

### Database Configuration (optional)
If not setting up a database, proceed to the next section on configuring environment variables. 

- Steps for setting up an [AWS relational database (PostgreSQL)](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html)
- If experiencing issues with access, edit the security groups to allow TCP interactions from an IP address whitelist. Additionally, you may need to change AWS DB settings to be publicly accessible.
- If you do not create a DB name, the default provided is ```postgres```.

### Configuring Environment Variables
We provide connections for a read-only database (no write capabilities) by default. If you plan on saving data from Snapshot or Tally to perform your own VBE experiments, we highly recommend setting up your own database connection as a large quantity of records will be stored. An option to save data to csv format is provided, but is only recommended for limited data pulls.

- How to get [Snapshot API Key](https://tally.so/r/3laKWp)
- How to get [Tally API Key](https://docs.tally.xyz/set-up-and-technical-documentation/welcome)
- How to get [Boardroom API Key](https://docs.boardroom.io/docs/api/cd5e0c8aa2bc1-overview) (optional)

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

### Data Setup
1. Navigate to data_setup folder with `cd data_setup/` 
    1. First, update `dao_input.csv` to match whatever DAOs that you’re looking for.
    
    _Note: it is recommended to limit the number of DAOs listed. To pull all historical proposals associated with the default list of DAOs, you can expect for the code to run for 6+ hours. This is due to the limitation of Snapshot and Tally API and pagination through records._
   
    2. If pulling from Snapshot:
        1. Must insert ```dao_id``` and put “Snapshot” under platform column
        2. The DAO id in Snapshot can be found using the URL for DAOs, in the format [https://snapshot.box/#/s:](https://snapshot.box/#/s:gmx.eth)[dao_id] or https://snapshot.box/#/s:arbitrumfoundation.eth
    3. If pulling from Tally:
        1. Must insert ```dao_slug``` and put “Tally” under platform column
        2. The DAO slug in Tally can be found using the URL for individual DAOs in the format [https://www.tally.xyz/gov/](https://www.tally.xyz/gov/optimism)[dao_slug] or https://www.tally.xyz/gov/optimism

### Data Extract 
1. Navigate to data_extract folder with `cd data_extract/` 
    1. Set up database tables (optional)
         1. If you are setting up your own database connection, please use [`rdb.py`](http://rdb.py) to create your initial tables at the start. You can do this by uncommenting line 221.

    1. Once set up, then run `snapshot_api.py` and `tally_api.py` as needed. These will save the information to a database connection specified in `.env`

   _Note that the Database initialization may take up to a few minutes. If you run into issues for connection, please check the security group rules and make sure that your IP address is allowed for TCP connections._
   
    _Note that these scripts are built in a way that they will add any DAOs, Proposals, and Votes not previously written to those tables. There should not be any duplicates written to the database records._

3. `boardroom_api.py` includes forum data. While not explicitly used in any experiments outlined in the paper, we find the information interesting and valuable for contextualizing VBE findings.

We recommend that after these steps, you query the information you saved with ```data_setup/rdb.py``` to understand your relational database, the schemas, and data field values.

## License

This project is licensed under the MIT License.
