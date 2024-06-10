import json
from collections import defaultdict
import numpy as np
import os
from tqdm import tqdm
import torch
import pandas as pd


class JSONEncoderWithNumpy(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super().default(obj)

def save_transaction_graph(df, label, idx, directory):
    os.makedirs(directory, exist_ok=True)

    unique_addresses = pd.concat([df['from'], df['to']]).unique()
    address_to_index = {address: i for i, address in enumerate(unique_addresses)}
    
    # Initialize dictionaries to store degrees and transaction values
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    in_value = defaultdict(float)
    out_value = defaultdict(float)
    
    edges = []
    for index, row in df.iterrows():
        from_idx = address_to_index[row['from']]
        to_idx = address_to_index[row['to']]
        value = float(row['value'].replace(',', '')) if isinstance(row['value'], str) else float(row['value'])
        
        edges.append([from_idx, to_idx])
        
        # Update degrees
        out_degree[from_idx] += 1
        in_degree[to_idx] += 1
        
        # Update transaction values
        out_value[from_idx] += value
        in_value[to_idx] += value

   
    features = {}
    for address, i in address_to_index.items():
        total_degree = in_degree[i] + out_degree[i]
        features[str(i)] = [total_degree, in_degree[i], out_degree[i], in_value[i], out_value[i]]

    # Construct the graph dictionary
    graph_dict = {
        "label": label,
        "features": features,
        "edges": edges
    }

    file_name = os.path.join(directory, f'{idx}.json')
    with open(file_name, 'w') as file:
        json.dump(graph_dict, file, cls=JSONEncoderWithNumpy, indent=None)  # No indentation for compactness

    print(f"Graph {idx} saved in {directory}")


if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    chain = 'Polygon'
    labels = pd.read_csv('../data/labels.csv').query('Chain == @chain')

    transaction_dfs = []

    for i in tqdm(labels.Address.values):
        tx = pd.read_csv(f'../data/transactions/{chain}/{i}.csv')
        tx['date'] = pd.to_datetime(tx['timestamp'], unit='s')
        transaction_dfs.append(tx)

    directory = f'../GoG/{chain}'

    transaction_dfs_select = transaction_dfs
    labels_select = list(labels.multi_class.values)

    for idx, (df, label) in enumerate(zip(transaction_dfs_select, labels_select)):
        save_transaction_graph(df, label, idx, directory)
    



