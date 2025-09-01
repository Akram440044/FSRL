# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Essential Development Commands

### Environment Setup
```bash
# Create virtual environment (Python 3.8+ required, tested with 3.13)
python3 -m venv fsrl_env
source fsrl_env/bin/activate  # On Windows: fsrl_env\Scripts\activate

# Install core dependencies
pip install --upgrade pip
pip install pandas numpy scikit-learn scipy matplotlib
pip install stable-baselines3 tensorboard gymnasium
pip install yfinance pandas_datareader
pip install akshare baostock beautifulsoup4 colorama colorlog
pip install tushare langchain transformers langchain_community langchain_core
pip install openai langchain-openai pytest fastapi uvicorn pydantic python-multipart

# Install TA-Lib (required for technical analysis)
pip install TA-Lib

# Install empyrical for financial metrics (use reloaded version for Python 3.13+)
pip install empyrical-reloaded

# Test the installation
python test_setup.py
```

### Configuration Setup
```bash
# 1. Configure email settings in config/global_config.json
# 2. Set Tushare token in config/test_account.json for market data
# 3. Configure task parameters in config/test_mainlab.json or config/test_llmlab.json
```

### Training & Testing Commands

#### Traditional RL Training
```bash
# Train a model
python -u run.py --task_name=hDJIADQN --env_type=train --start_time=20101201 --end_time=20210101

# Test trained model
python -u run.py --task_name=hDJIADQN --env_type=test --start_time=20201201 --end_time=20230101

# Continue training from saved model
python -u run.py --task_name=hDJIADQN --env_type=load --start_time=20101201 --end_time=20210101 --load_time_steps=50000
```

#### LLM-based Trading
```bash
# Run LLM-powered trading agent
python -u run.py --task_name=h000905llm5Strategy --env_type=llm --start_time=20201201 --end_time=20230101 --proxy=10809
```

### Web Interface
```bash
# Start backend API server
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Start frontend (Vue.js)
cd frontend
npm install
npm run serve
# Access at http://localhost:8080
```

### Monitoring
```bash
# View training metrics
tensorboard --logdir=tensorboard_logs
```

### Testing
```bash
# Run specific tests
pytest tests/llm/test_llm.py
pytest tests/data/test_mjdtushare.py
```

## High-Level Architecture

### Core Framework Structure
FSRL is built around a three-layer reinforcement learning architecture:

1. **Strategy Layer**: Implements multiple financial trading strategies (dual moving average, RSI, VWAP, Bollinger Bands)
2. **Agent Layer**: RL agents that learn to dynamically select among strategies
3. **Market Environment Layer**: Simulates market conditions and provides rewards

### Key Components

#### Environment Management (`env/`)
- `EnvironmentInit`: Factory for creating train/test environments
- `env_strategy_train.py` & `env_strategy_test.py`: RL environment implementations
- Handles observation spaces, action spaces, and reward calculations

#### Strategy Implementation (`strategy/`)
- `Strategy` class: Base for implementing multiple trading strategies
- Strategies include: two moving averages, RSI, VWAP with configurable parameters
- Each strategy manages its own state machine (IDLE, BUY, HOLD, SELL)

#### Algorithm Integration (`algomodel/`)
- `AlgoCenter`: Abstracts RL algorithm implementations
- Currently integrates Stable-Baselines3 (DQN, PPO)
- Designed to support multiple RL frameworks (tensorforce, ElegantRL)

#### Data Pipeline (`data/`)
- `get_data.py`: Fetches market data via Tushare/yfinance APIs
- `get_factors.py`: Processes raw data into technical indicators
- Supports both Chinese (A-shares) and US markets

#### Configuration System (`config/`)
- JSON-based configuration for tasks, algorithms, and environments
- `test_mainlab.json`: Main RL training configurations
- `test_llmlab.json`: LLM agent configurations
- `global_config.json`: Global settings (email, etc.)

#### Execution Labs
- `MainLab` (`mainlab/`): Traditional RL training/testing pipeline
- `LLMLab` (`llmlab/`): LLM-powered trading agent execution
- Both labs handle model lifecycle and result analysis

#### Backtesting (`backtest/`)
- `BaoBackTest`: Custom backtesting engine
- Handles order execution, position management, commission calculation
- Integrates with strategy layer for performance evaluation

### Multi-Strategy Selection
The core innovation is dynamic strategy switching:
- Agent observes market conditions (technical factors, price data)
- Selects which strategy to execute based on learned policy
- Reward system evaluates strategy performance in context

### LLM Integration
- `TradeAgent`: Uses OpenAI API for decision-making
- Receives market observations and previous rewards as context
- Outputs strategy selection decisions in natural language
- Logs all interactions for analysis

### Key Data Flow
1. Market data fetched and processed into factors
2. Environment provides observations to agent
3. Agent selects strategy action
4. Strategy executes trades via backtesting engine
5. Rewards calculated and fed back to agent
6. Process repeats until episode termination

## Important Implementation Details

### Task Naming Convention
Task names follow pattern: `{market_code}{algorithm}{num_strategies}Strategy`
- Examples: `h000905DQN5Strategy`, `hDJIADQN`, `h000300PPOsingle`
- Prefix 'h' indicates index/ETF data

### Configuration Parameters
- `strategyNum`: Number of strategies available for selection
- `strategyInitDay`: Warmup period for technical indicators
- `maxStrategyStepLimit`: Maximum steps per episode
- `actionStrategyId`: Defines action space (strategy selection vs simple buy/sell)

### Model Persistence
- Trained models saved to `resultmodel/{task_name}`
- Results and analysis saved to `resultdata/`
- TensorBoard logs in `tensorboard_logs/`

### Market Support
- Chinese markets: Uses baostock/tushare for A-share data
- US markets: Uses yfinance for index data
- Market-specific backtesting logic handles different trading rules
