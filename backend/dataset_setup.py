# backend/dataset_setup.py
import kagglehub
import pandas as pd
import os
import json

def download_lexglue_dataset():
    """Download and setup the LexGLUE dataset"""
    try:
        print("Downloading LexGLUE dataset...")
        path = kagglehub.dataset_download("thedevastator/lexglue-legal-nlp-benchmark-dataset")
        print(f"✅ Dataset downloaded to: {path}")
        return path
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return None

def explore_dataset(path):
    """Explore what's in the dataset"""
    print("\n📁 Exploring dataset structure...")
    
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}📂 {os.path.basename(root)}/")
        
        for file in files[:3]:  # Show first 3 files
            print(f"{indent}  📄 {file}")

if __name__ == "__main__":
    print("🚀 Starting LexGLUE dataset setup...")
    dataset_path = download_lexglue_dataset()
    
    if dataset_path:
        explore_dataset(dataset_path)
        print("\n✅ Dataset setup complete!")
    else:
        print("\n❌ Dataset setup failed!")