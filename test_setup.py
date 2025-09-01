#!/usr/bin/env python3

"""
Test script to validate FSRL environment setup
"""

import sys
import subprocess
import pkg_resources

def test_imports():
    """Test if all core modules can be imported"""
    try:
        # Test core dependencies
        import pandas as pd
        import numpy as np
        import stable_baselines3
        import talib
        import torch
        import gymnasium
        print("✅ Core dependencies imported successfully")
        
        # Test FSRL modules
        from config.config import ConfigJson
        from strategy.strategy import Strategy
        from env.environment_init import EnvironmentInit
        from algomodel.algo_center import AlgoCenter
        print("✅ FSRL core modules imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    try:
        from config.config import ConfigJson
        config = ConfigJson()
        print("✅ Configuration system works")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def print_package_versions():
    """Print versions of key packages"""
    packages = [
        'pandas', 'numpy', 'stable-baselines3', 'torch', 
        'gymnasium', 'yfinance', 'scikit-learn', 'matplotlib'
    ]
    
    print("\n📦 Package versions:")
    for package in packages:
        try:
            version = pkg_resources.get_distribution(package).version
            print(f"  {package}: {version}")
        except pkg_resources.DistributionNotFound:
            print(f"  {package}: Not found")

def main():
    print("🚀 Testing FSRL Environment Setup")
    print("=" * 40)
    
    # Test Python version
    py_version = sys.version.split()[0]
    print(f"🐍 Python version: {py_version}")
    
    if not py_version.startswith('3.'):
        print("❌ Python 3.x is required")
        return False
    
    print_package_versions()
    
    print("\n🧪 Testing imports...")
    imports_ok = test_imports()
    
    print("\n⚙️ Testing configuration...")
    config_ok = test_configuration()
    
    print("\n" + "=" * 40)
    if imports_ok and config_ok:
        print("✅ Environment setup is working correctly!")
        print("\n🎯 Ready to run FSRL training and testing!")
        print("\nExample commands:")
        print("  # Train a model:")
        print("  python run.py --task_name=hDJIADQN --env_type=train --start_time=20201201 --end_time=20210101")
        print("\n  # Test a model:")
        print("  python run.py --task_name=hDJIADQN --env_type=test --start_time=20210101 --end_time=20220101")
        return True
    else:
        print("❌ Environment setup has issues that need to be resolved")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
