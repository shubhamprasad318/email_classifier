import sys
from models import train_model

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python train.py <path_to_csv>")
        sys.exit(1)
    data_path = sys.argv[1]
    train_model(data_path)
    print("✅ Model training completed. Artifacts saved under 'models/' directory.")