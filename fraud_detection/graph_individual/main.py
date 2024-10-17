import numpy as np
import torch
import random
from pyod.models.copod import COPOD
from pyod.models.iforest import IForest
from pyod.models.dif import DIF
from pyod.models.lof import LOF
from pyod.models.vae import VAE
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from utils import GraphDatasetGenerator

def eval_roc_auc(label, score):
    roc_auc = roc_auc_score(y_true=label, y_score=score)
    if roc_auc < 0.5:
        score = [1 - s for s in score]
        roc_auc = roc_auc_score(y_true=label, y_score=score)
    return roc_auc

def eval_average_precision(label, score):
    return average_precision_score(y_true=label, y_score=score)

def tune_and_find_best_params(model, params, x_train, y_train, x_val, y_val):
    best_auc = 0
    best_params = None
    for param_set in params:
        model.set_params(**param_set)
        model.fit(x_train, y_train)
        scores_pred = model.predict_proba(x_val)[:, 1]
        auc_score = eval_roc_auc(y_val, scores_pred)
        if auc_score > best_auc:
            best_auc = auc_score
            best_params = param_set
    return best_params

def evaluate_model_with_seeds(model, best_params, x, y, seeds):
    auc_results = []
    ap_results = []
    for seed in seeds:
        x_train_val, x_test, y_train_val, y_test = train_test_split(x, y, test_size=0.1, random_state=seed)
        x_train, x_val, y_train, y_val = train_test_split(x_train_val, y_train_val, test_size=1/9, random_state=seed)        
        model.set_params(**best_params)
        model.fit(x_train, y_train)
        scores_pred = model.predict_proba(x_test)[:, 1]
        auc_score = eval_roc_auc(y_test, scores_pred)
        ap_score = eval_average_precision(y_test, scores_pred)
        auc_results.append(auc_score)
        ap_results.append(ap_score)
    return np.mean(auc_results), np.std(auc_results), np.mean(ap_results), np.std(ap_results)

def main():
    chain = 'polygon'
    dataset_generator = GraphDatasetGenerator(f'../../data/features/{chain}_basic_metrics_processed.csv')
    data_list = dataset_generator.get_pyg_data_list()
    x = torch.cat([data.x for data in data_list], dim=0).numpy()
    y = torch.cat([data.y.unsqueeze(0) if data.y.dim() == 0 else data.y for data in data_list]).numpy()

    # Handling NaN values
    imputer = SimpleImputer(strategy='mean')
    x = imputer.fit_transform(x)

    # Initial data split
    x_train_val, x_test, y_train_val, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
    x_train, x_val, y_train, y_val = train_test_split(x_train_val, y_train_val, test_size=0.1, random_state=42)

    num_features = x.shape[1]
    hidden_size = min(20, num_features // 2)

    models = {
        "COPOD": (COPOD(), [{"contamination": f} for f in np.linspace(0.01, 0.1, 10)]),
        "Isolation Forest": (IForest(), [{"n_estimators": n, "max_samples": s} for n in [100, 200] for s in [256, 512]]),
        "DIF": (DIF(), [{"contamination": f} for f in np.linspace(0.01, 0.05, 5)]), 
        "VAE": (VAE(encoder_neurons=[hidden_size], decoder_neurons=[hidden_size], contamination=0.1), 
                [{"encoder_neurons": [n], "decoder_neurons": [n], "contamination": f}
                for n in [hidden_size//2, hidden_size, hidden_size*2] 
                for f in np.linspace(0.1, 0.3, 3)])
    }

    seeds = [42, 43, 44]
    for model_name, (model, param_grid) in models.items():
        best_params = tune_and_find_best_params(model, param_grid, x_train, y_train, x_val, y_val)
        if best_params:
            avg_auc, std_auc, avg_ap, std_ap = evaluate_model_with_seeds(model, best_params, x, y, seeds)
            print(f"{model_name} Results: Average AUC = {avg_auc:.4f} ± {std_auc:.4f}, Average AP = {avg_ap:.4f} ± {std_ap:.4f}")
        else:
            print(f"{model_name} failed to find suitable parameters.")

if __name__ == "__main__":
    main()
