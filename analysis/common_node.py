import pandas as pd
import json
from tqdm import tqdm
import os 

chain = 'polygon'

chain_labels = pd.read_csv(f'../data/labels.csv').query('Chain == @chain')
chain_class = list(chain_labels.Contract.values)

output_file = f'../graphs/{chain}/{chain}_common_nodes_except_null_labels.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', newline='') as csvfile:
    csvfile.write('Contract1,Contract2,Common_Nodes,Unique_Addresses\n')
    errors = []
    contract_addresses = {}

    for addr in tqdm(chain_class):
        try:
            file_path = f'../data/transactions/{chain}/{addr}.csv'
            df = pd.read_csv(file_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            cutoff_date = pd.Timestamp('2024-03-01')  # transactions before 2024-03-01
            tx = df[df['timestamp'] < cutoff_date]
            addresses = pd.concat([tx['from'], tx['to']]).unique()
            contract_addresses[addr] = set(addresses)
        
        except Exception as e:
            errors.append((addr, str(e)))
            print(f'Error with address {addr}: {e}')

    
    # Load exchanges list
    null_addresses = ['0x0000000000000000000000000000000000000000']

    # Compute common nodes except for exchange addresses
    for i in tqdm(range(len(chain_class))):
        con1 = chain_class[i]
        for con2 in chain_class[i+1:]:
            try:
                address1, address2 = contract_addresses[con1], contract_addresses[con2]
                address1 -= set(null_addresses)
                address2 -= set(null_addresses)
                common_nodes = len(address1 & address2)
                unique_addresses = len(address1 | address2)
                csvfile.write(f"{con1},{con2},{common_nodes},{unique_addresses}\n")
            
            except KeyError as e:
                errors.append((con1, con2, str(e)))
    
# Futher create the global graph based on threshold.
# threshold = 1
# global_graph = pd.read_csv(output_file)
# global_graph['Jaccard_Coefficient'] = global_graph['Common_Nodes']/global_graph['Unique_Addresses']
# global_graph = global_graph.query('Jaccard_Coefficient > @threshold')
# global_graph.to_csv(f'../data/global_graph/{chain}_graph_more_than_{threshold}_ratio.csv', index = 0) 