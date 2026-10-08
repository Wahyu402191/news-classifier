"""
Setup script to prepare data and models from Ivan's folder
Run this once before deploying the application
"""

import pandas as pd
import shutil
from pathlib import Path

# Paths
IVAN_FOLDER = Path("../teman 2")
APP_FOLDER = Path(".")

# Data paths
IVAN_SPORT = IVAN_FOLDER / "hasil_scraping_detik_sport.csv"
IVAN_FINANCE = IVAN_FOLDER / "hasil_scraping_detik_finance.csv"
IVAN_SKIPGRAM = IVAN_FOLDER / "model_skipgram_terbaik.model"
IVAN_SVM = IVAN_FOLDER / "model_svm_terbaik.joblib"

# Target paths
TARGET_DATA = APP_FOLDER / "data"
TARGET_MODELS = APP_FOLDER / "models"


def prepare_dataset():
    """Prepare dataset by sampling from Ivan's data"""
    print("=" * 60)
    print("PREPARING DATASET")
    print("=" * 60)
    
    # Load Ivan's data
    print("\n1. Loading source data...")
    df_sport_full = pd.read_csv(IVAN_SPORT)
    df_finance_full = pd.read_csv(IVAN_FINANCE)
    
    print(f"   Sport articles (original): {len(df_sport_full)}")
    print(f"   Finance articles (original): {len(df_finance_full)}")
    
    # Sample 90 articles each (to differ from Ivan's 100)
    print("\n2. Sampling 90 articles per category...")
    df_sport = df_sport_full.sample(n=min(90, len(df_sport_full)), random_state=42).reset_index(drop=True)
    df_finance = df_finance_full.sample(n=min(90, len(df_finance_full)), random_state=42).reset_index(drop=True)
    
    # Clean data - remove rows with missing content
    df_sport = df_sport.dropna(subset=['isi_berita']).reset_index(drop=True)
    df_finance = df_finance.dropna(subset=['isi_berita']).reset_index(drop=True)
    
    print(f"   Sport articles (sampled): {len(df_sport)}")
    print(f"   Finance articles (sampled): {len(df_finance)}")
    
    # Save to target directory
    print("\n3. Saving datasets...")
    TARGET_DATA.mkdir(exist_ok=True)
    
    sport_path = TARGET_DATA / "detik_sport_90.csv"
    finance_path = TARGET_DATA / "detik_finance_90.csv"
    
    df_sport.to_csv(sport_path, index=False, encoding='utf-8-sig')
    df_finance.to_csv(finance_path, index=False, encoding='utf-8-sig')
    
    print(f"   ✓ Saved: {sport_path}")
    print(f"   ✓ Saved: {finance_path}")
    
    return True


def copy_models():
    """Copy models from Ivan's folder"""
    print("\n" + "=" * 60)
    print("COPYING MODELS")
    print("=" * 60)
    
    TARGET_MODELS.mkdir(exist_ok=True)
    
    # Copy Skip-Gram model
    print("\n1. Copying Skip-Gram model...")
    if IVAN_SKIPGRAM.exists():
        target_skipgram = TARGET_MODELS / "skipgram_model.model"
        shutil.copy2(IVAN_SKIPGRAM, target_skipgram)
        print(f"   ✓ Copied: {target_skipgram}")
        print(f"   Size: {target_skipgram.stat().st_size / 1024 / 1024:.2f} MB")
    else:
        print(f"   ✗ Source not found: {IVAN_SKIPGRAM}")
        return False
    
    # Copy SVM model
    print("\n2. Copying SVM classifier...")
    if IVAN_SVM.exists():
        target_svm = TARGET_MODELS / "svm_classifier.joblib"
        shutil.copy2(IVAN_SVM, target_svm)
        print(f"   ✓ Copied: {target_svm}")
        print(f"   Size: {target_svm.stat().st_size / 1024:.2f} KB")
    else:
        print(f"   ✗ Source not found: {IVAN_SVM}")
        return False
    
    return True


def verify_setup():
    """Verify that all files are in place"""
    print("\n" + "=" * 60)
    print("VERIFYING SETUP")
    print("=" * 60)
    
    required_files = [
        TARGET_DATA / "detik_sport_90.csv",
        TARGET_DATA / "detik_finance_90.csv",
        TARGET_MODELS / "skipgram_model.model",
        TARGET_MODELS / "svm_classifier.joblib"
    ]
    
    all_ok = True
    for file_path in required_files:
        exists = file_path.exists()
        status = "✓" if exists else "✗"
        print(f"\n{status} {file_path}")
        if exists:
            size = file_path.stat().st_size
            if size > 1024 * 1024:
                print(f"  Size: {size / 1024 / 1024:.2f} MB")
            else:
                print(f"  Size: {size / 1024:.2f} KB")
        else:
            all_ok = False
    
    return all_ok


def main():
    """Main setup function"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "NEWS CLASSIFIER SETUP SCRIPT" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # Step 1: Prepare dataset
        if not prepare_dataset():
            print("\n✗ Failed to prepare dataset")
            return
        
        # Step 2: Copy models
        if not copy_models():
            print("\n✗ Failed to copy models")
            return
        
        # Step 3: Verify
        if not verify_setup():
            print("\n✗ Setup verification failed")
            return
        
        # Success
        print("\n" + "=" * 60)
        print("SETUP COMPLETE!")
        print("=" * 60)
        print("\n✓ All files prepared successfully")
        print("\nYou can now run the application:")
        print("  streamlit run app.py")
        print()
        
    except Exception as e:
        print(f"\n✗ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
