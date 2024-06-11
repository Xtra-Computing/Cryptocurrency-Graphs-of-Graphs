# Multi-Chain Graphs of Graphs Dataset

This is the repository for "Multi-Chain Graphs of Graphs: A New Paradigm in Blockchain Dataset". This comprehensive study introduces a pioneering, large-scale, cross-chain dataset using a graphs-of-graphs approach to analyze complex blockchain networks. 

## Table of Contents
- [Repository Overview](#repository-overview)
- [Dataset Schema](#dataset-schema)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Requirements](#requirements)
  - [Dataset Overview](#dataset-overview)
  - [Dataset Access and Usage](#dataset-access-and-usage)
- [Using the Dataset](#using-the-dataset)
  - [Data Analysis](#data-analysis)
  - [Fraud Detection](#fraud-detection)
  - [Multi-Class Classification](#multi-class-classification)
- [License](#license)
- [Contributing](#contributing)

## Repository Overview
This repository contains both the datasets used in our research and the code for analysis and model training. Here you can find everything needed to replicate our studies or use our data and models for your own research.

## Dataset Schema
Below are key statistics for each blockchain included in our dataset:

| Chain     | # Tokens | Start Months | End Months | # Transactions | # Addresses | # Categories |
|-----------|----------|--------------|------------|----------------|-------------|--------------|
| Ethereum  | 14,464   | 2016-02      | 2024-02    | 81,788,211     | 10,247,767  | 290          |
| Polygon   | 2,353    | 2020-08      | 2024-02    | 64,882,233     | 1,801,976   | 112          |
| BNB       | 7,499    | 2020-09      | 2024-02    | 121,612,480    | 6,550,399   | 149          |

## Getting Started
### Installation
Clone this repository to your local machine using:
```bash
git clone https://github.com/YourUsername/Graph-of-graphs-dataset.git
cd Graph-of-graphs-dataset
```

### Requirements
Ensure your environment meets the following specifications to run the scripts and models:
- Python 3.10.14
- Libraries: NumPy 1.26.2, pandas 1.3.5, PyTorch 2.3.0+cu118, networkx 3.3

Install required packages using:
```bash
pip install numpy==1.26.2 pandas==1.3.5 torch==2.3.0+cu118 networkx==3.3
```

### Dataset Overview
#### Global Graphs
- Contains data for Ethereum, Polygon, and BNB within the `global graph` folder:
  - `{chain}_graph_more_than_1_ratio.csv`
  - `{chain}_contract_to_number_mapping.json`

#### Transactions
- Transaction records are stored in zipped files for each chain (`ethereum.zip`, `polygon.zip`, `bnb.zip`), including detailed data like block number, sender, receiver, transaction hash, value, and timestamp.

#### Labels
- `labels.csv` categorizes each contract across chains with fields for Chain, Contract, and Category.

### Dataset Access and Usage
The dataset is available via [this link](https://drive.google.com/drive/folders/1VV5ht9Eh8WGtKfkS0ipIk0FNI7g-WJfJ?usp=share_link). Follow these steps for effective utilization:
1. Download and decompress the necessary files.
2. Use the JSON mapping files to interpret the global graphs.
3. Consult `labels.csv` to understand contract categorizations.

## Using the Dataset
### Data Analysis
Scripts for analyzing both local and global graphs are located under `code/analysis/`. Run the following commands for respective analyses:
```bash
python analyze_local_graphs.py
python analyze_global_graphs.py
```

### Fraud Detection
Navigate to `code/fraud_detection/` to access scripts for anomaly detection across graph structures:
```bash
cd graph_individual/
python main.py

cd ../graph_of_graphs/
python main.py
```

### Multi-Class Classification
Classification scripts can be found under `code/multi-class_classification/`. Execute models as follows:
```bash
cd graph_individual/
python main.py --chain polygon --model GCN

cd ../graph_of_graphs/
python main.py --chain polygon --model SEAL
```

## License
The dataset is released under the Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) license. This means that anyone can use, distribute, and modify the data for non-commercial purposes as long as they give proper attribution and share the derivative works under the same license terms.
