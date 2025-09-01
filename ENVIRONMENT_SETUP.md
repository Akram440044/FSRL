# FSRL Environment Setup Guide

This guide helps you set up a complete Python virtual environment for the FSRL project.

## Prerequisites

- Python 3.8 or higher (tested with Python 3.13)
- Git (for cloning the repository)

## Quick Setup

1. **Navigate to the FSRL directory** (you should already be here):
   ```bash
   cd /path/to/FSRL
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv fsrl_env
   source fsrl_env/bin/activate  # On Windows: fsrl_env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   # Upgrade pip first
   pip install --upgrade pip
   
   # Install core scientific computing packages
   pip install pandas numpy scikit-learn scipy matplotlib
   
   # Install RL and ML frameworks
   pip install stable-baselines3 tensorboard gymnasium torch
   
   # Install financial data sources
   pip install yfinance pandas_datareader akshare baostock tushare
   
   # Install technical analysis library
   pip install TA-Lib
   
   # Install LLM and web framework dependencies
   pip install langchain transformers langchain_community langchain_core
   pip install openai langchain-openai
   pip install fastapi uvicorn pydantic python-multipart
   
   # Install testing and utility packages
   pip install pytest beautifulsoup4 colorama colorlog
   pip install empyrical-reloaded  # Use reloaded version for Python 3.13+
   ```

4. **Test the installation**:
   ```bash
   python test_setup.py
   ```

   You should see:
   ```
   ✅ Environment setup is working correctly!
   🎯 Ready to run FSRL training and testing!
   ```

## Configuration

Before running FSRL, configure these files:

1. **config/global_config.json** - Email settings for notifications
2. **config/test_account.json** - API tokens for market data providers
3. **config/test_mainlab.json** - RL training task configurations  
4. **config/test_llmlab.json** - LLM agent configurations

## Running FSRL

### Traditional RL Training
```bash
# Activate environment
source fsrl_env/bin/activate

# Train a model
python run.py --task_name=hDJIADQN --env_type=train --start_time=20201201 --end_time=20210101

# Test the trained model  
python run.py --task_name=hDJIADQN --env_type=test --start_time=20210101 --end_time=20220101
```

### LLM-based Trading
```bash
# Run LLM agent (requires OpenAI API key in config)
python run.py --task_name=h000905llm5Strategy --env_type=llm --start_time=20201201 --end_time=20230101
```

### Web Interface
```bash
# Backend (in one terminal)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (in another terminal)  
cd frontend
npm install
npm run serve
```

## Troubleshooting

### Common Issues

1. **TA-Lib installation fails**:
   - On macOS: `brew install ta-lib` then `pip install TA-Lib`
   - On Linux: Install ta-lib development package first
   - On Windows: Use pre-compiled wheels

2. **empyrical import errors**:
   - Use `empyrical-reloaded` instead of `empyrical` for Python 3.13+

3. **gym vs gymnasium**:
   - The code has been updated to use `gymnasium` (new version of gym)

4. **yfinance API changes**:
   - Updated to use `yf.download()` instead of deprecated `pdr_override()`

### Environment Validation

Run the test script anytime to validate your setup:
```bash
python test_setup.py
```

### Deactivating Environment

When done working:
```bash
deactivate
```

## Notes

- The virtual environment `fsrl_env/` is already in `.gitignore`
- All dependencies are compatible with Python 3.8-3.13
- The setup includes both traditional RL and LLM capabilities
- Market data requires API keys for full functionality

## Support

If you encounter issues:
1. Check the `test_setup.py` output for specific error messages
2. Verify Python version compatibility  
3. Ensure all configuration files are properly set up
4. Review the main WARP.md for additional guidance
