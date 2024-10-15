import argparse

def parameter_parser():
    """
    Parses command line parameters for different graph models.
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Run Graph Models")
    
    # Model selection
    parser.add_argument("--model", type=str, default="GOGNN", choices=["DVGGA", "GOGNN", "SEAL"], 
                        help="Type of the graph model to run.")

    # Data paths
    parser.add_argument("--graphs", nargs="?",
                        default="../GoG/polygon/",
                        help="Folder containing training graph JSON files.")
    parser.add_argument("--hierarchical-graph", nargs="?",
                        default="../GoG/polygon/edges/global_edges.csv",
                        help="Path to the hierarchical edge list CSV file.")

    # Training parameters
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs.")
    parser.add_argument("--learning-rate", type=float, default=0.1, help="Learning rate for optimizer.")
    parser.add_argument("--weight-decay", type=float, default=5e-5, help="Weight decay for Adam optimizer.")
    parser.add_argument("--gamma", type=float, default=1e-5, help="Regularization coefficient for model.")
    parser.add_argument("--dropout", type=float, default=0, help="Dropout ratio.")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Ratio of data to use for training.")
    parser.add_argument("--device", default="cpu", help="Device to run the model on (e.g., cpu, cuda:0).")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size for training.")

    # Common model architecture parameters
    parser.add_argument("--first-gcn-dimensions", type=int, default=16,
                        help="Number of filters in the first graph convolution layer.")
    parser.add_argument("--second-gcn-dimensions", type=int, default=16,
                        help="Number of filters in the second graph convolution layer.")
    parser.add_argument("--first-dense-neurons", type=int, default=16,
                        help="Number of neurons in the first dense layer.")
    parser.add_argument("--second-dense-neurons", type=int, default=8,
                        help="Number of neurons in the second dense layer.")

    # SEAL-specific parameters
    parser.add_argument("--macro-gcn-dimensions", type=int, default=16,
                        help="Number of filters in the macro graph convolution layer (SEAL model).")

    # DVGGA-specific parameters
    parser.add_argument("--vgae-hidden-dimensions", type=int, default=8,
                        help="Hidden dimensions for variational graph autoencoder (DVGGA model).")

    # GOGNN-specific parameters
    parser.add_argument("--nhid", type=int, default=32,
                        help="Number of hidden units in specific layers (GOGNN model).")
    parser.add_argument("--ddi-nhid", type=int, default=32,
                        help="Hidden dimensions for drug-drug interaction layers (GOGNN model).")
    parser.add_argument("--pooling-ratio", type=float, default=0.6,
                        help="Graph pooling ratio (GOGNN model).")

    return parser.parse_args()