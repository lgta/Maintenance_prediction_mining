"""Command‑line example: python main_example.py data.csv"""
import argparse
from data_loader import load_and_preprocess_data
from analysis import describe_numeric, correlation_with_target
from model import train_failure_classifier

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', help='Input CSV file')
    args = parser.parse_args()

    print('⏳ Loading & preprocessing…')
    X, y = load_and_preprocess_data(args.csv_path)

    print('\n📊 Descriptive statistics (numeric):')
    print(describe_numeric(X).head())

    print('\n🔗 Top correlations with target:')
    df = X.copy()
    df['target'] = y
    print(correlation_with_target(df, 'target').head(10))

    print('\n🤖 Training model…')
    model, auc = train_failure_classifier(X, y)
    print(f'Hold‑out ROC‑AUC: {auc:.3f}')

if __name__ == '__main__':
    main()