# DAO VBE Library
The purpose of VBE library is to take data extracted from VBE-data and calculate VBE. If not using your own database connection built from VBE-data step, then we provide the ability to calculate VBE over the read-only version of our database. Please refer to ```clustering-guidance.md``` for more information on clustering and parameter selection.

For reproducibility of the results:
We used the following default clustering model and parameters: Kmeans, k = 3, random_state=42, n_init=10, minimum entropy. Minimum Entropy VBE across all windows (from ```run_vbe.py```) are averaged to get the average VBE for a DAO.

In this repo, the below scripts provide the following functions:
- ```rds_readonly.py```: loads data from relational database given the variables in the .env file. Query can be changed to retrieve DAO, proposal, voter, and other data tables.
- ```load_data.py```: loads and formats the data from voting or governance sources. Cleans data, removes duplicates, and flags issues.
- ```run_vbe.py```: performs clustering for voter feature data, and computes VBE as a function on the size of the largest cluster.
- ```vbe_parameters```: creates an output of model parameters to be used in run_vbe.py.
- ```utils.py```: used for supporting functions in loading data, calculating optimal model parameters, and saving data.
- ```data_output/```: saves report for VBE and model parameters, as well as clustering data.

## Setup

1. Please follow the previous steps in [VBE-data/README.md](../VBE-data/README.md) to clone the directory, set up virtual environment, and install dependencies.
2. Set up your .env file. We provide by default credentials to a read-only version of our database. If you would like to use the information that you have saved instead, then please update to your own credentials. 

## Connect to Read-only Database
1.  To view or pull in new data, use ```python rds_readonly.py```. Change the variables ```table_name```, ```query_name```, ```csv_flag``` to determine the query and whether the information is saved. 
2. The default output file will save to ```VBE-data/data_output/db_output.csv```. These file names should be changed to ```proposals.csv``` or ```votes.csv``` for VBE calculations.

## Test Model Parameters
The script ```vbe_parameters.py``` is an optional step to test parameters for clustering and entropy calculations. It can be used to generate VBE on a single instance rather than all DAOs, proposals and votes. 
1. Change directory to ```vbe```
1. Make sure the correct data is located at ```VBE-data/data_output/votes.csv``` and ```VBE-data/data_output/proposals.csv```
3. To test calculating VBE with different model parameters, run ```python vbe_parameters.py```
4. View outputs in ```VBE-library/data_output/parameters.csv``` or ```VBE-library/data_output/saved_clusters.csv```

## Calculate VBE
The script ```run_vbe.py``` calculates VBE across windows of proposals and voters across all DAOs. 
1. There are two options for how to calculate VBE using input data. You can use either previously pulled CSV data from ```VBE-data/data_output```, or use a live database connection. 
3. Enter ```python run_vbe.py ``` to begin.
4. The parameters are set by default for result reproducibility, but can be changed on line 67. 

To save model parameters and VBE, make sure to enter "Y" when prompted. Alternatively, if you want to save the cluster groupings against the original voter data, make sure to change the default "N" to "Y" when prompted.

## VBE Reproducibility
After running the script above, you should have a data_output file called ```vbe_dao.csv``` or data saved to the ```vbe_dao``` database table. Minimum Entropy VBE across all windows are averaged (by DAO) to get the average VBE for a DAO.

### VBE Parameters 
Below parameters can be set, including:

- **Clustering Model:** (K-means (default), DBSCAN, Hierarchical Gaussian Mixture Models, Spectral Clustering)
- **Optimization methods:** (Silhouette Score (default), Gap Statistic, Davies-Bouldin, Calinski Harabasz, K-distance, BIC, AIC, Log-Likelihood)
- **Distance Metric for model:** (Euclidean (default), Manhattan, Cosine, Cityblock, L1, L2)
- **Distance Metric for optimization:** (Euclidean (default), Manhattan, Cosine, Cityblock, L1, L2)
- **Data Scaler:** (Min-Max (default), Standard)
- **Entropy Function:** (Min Entropy (default), Max Entropy, Shannon Entropy)
- Entry data path
- Data save path

## Running the model directly
You may run the model directly by entering all relevant parameters using a format like below:
- ```python calculate_vbe.py --model "K-means (default)" --num_clusters 3 --optimization_method "Silhouette Score (default)" --dist_method "Euclidean (default)" --save_clusters "Y" ```
<br />
To view the full information in the command line, you can use ```python calculate_vbe.py --help```

### Model hyperparameters

    parser.add_argument('--model', type=str, default=None, help='Model to use for training')
    parser.add_argument('--num_clusters', type=int, default=2, help='Number of clusters to use')
    parser.add_argument('--dist_model', type=str, default='Euclidean', help='Distance method for clustering')
    parser.add_argument('--optimization_method', type=str, default='Silhouette Score (default)', help='Method to find optimal cluster')
    parser.add_argument('--dist_method', type=str, default='Euclidean (default)', help='Distance method for parameter optimization')
    parser.add_argument('--optimize', type=str, default='Y', help='Flag to use optimal number of clusters calculated')
    parser.add_argument('--entropy', type=str, default='Min Entropy (default)', help='Entropy function for VBE calculation')

### Data hyperparameters
    parser.add_argument('--scale', type=str, default='Min-Max (default)', help='Standard or Min-max scaled data')
    parser.add_argument('--save_data', type=str, default='Y', help='Flag to save parameters and VBE')
    parser.add_argument('--save_clusters', type=str, default='N', help='Flag to save clusters and labels')
    parser.add_argument('--save_cluster_path', type=str, default=os.path.join(os.pardir, 'results', 'cluster_data.csv'), help='Path for saving cluster data')
    parser.add_argument('--path', type=str, default=os.path.join(os.pardir, 'data', 'dummy_data.csv'), help='Path for data')

