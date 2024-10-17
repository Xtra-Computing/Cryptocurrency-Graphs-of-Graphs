import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def main():

    chain = 'polygon'
    graphs1 = pd.read_csv(f'../result/{chain}_basic_metrics.csv')
    graphs2 = pd.read_csv(f'../result/{chain}_advanced_metrics_labels.csv')
    
    features = pd.merge(graphs1, graphs2, on='Contract')
    
    labels = pd.read_csv('../data/labels.csv').query('Chain == @chain')
    labels['binary_category'] = labels['Category'].apply(lambda x: 1 if x == 0 else 0)
    label_dict = dict(zip(labels.Contract, labels.binary_category))
    
    features['label'] = features['Contract'].apply(lambda x: label_dict.get(x, 0))  # Default to 0 if not found
    features.replace([np.inf, -np.inf], np.nan, inplace=True)
    features.fillna(0, inplace=True)
    
    scaler = StandardScaler()
    columns = ['Num_nodes', 'Num_edges', 'Density', 'Assortativity', 'Reciprocity', 
               'Effective_Diameter', 'Clustering_Coefficient']
    features[columns] = scaler.fit_transform(features[columns])
    
    features.to_csv(f'../data/features/{chain}_basic_metrics_processed.csv', index=False)

if __name__ == "__main__":
    main()
