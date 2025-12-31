@echo off
REM Setup Script for Mini-Infer Development Environment (Windows)
REM This script creates a conda environment and installs all dependencies

echo ============================================================
echo Mini-Infer Development Environment Setup
echo ============================================================
echo.

REM Check if conda is installed
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Conda not found! Please install Miniconda or Anaconda first.
    echo Download from: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo [1/6] Checking existing environment...
conda env list | findstr "mini-infer" >nul
if %errorlevel% equ 0 (
    echo.
    echo Environment 'mini-infer' already exists.
    set /p OVERWRITE="Do you want to remove and recreate it? (y/n): "
    if /i "%OVERWRITE%"=="y" (
        echo Removing existing environment...
        call conda env remove -n mini-infer -y
    ) else (
        echo Keeping existing environment. Updating packages...
        goto :update_env
    )
)

echo [2/6] Creating conda environment 'mini-infer' with Python 3.10...
call conda create -n mini-infer python=3.10 -y
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create conda environment!
    pause
    exit /b 1
)

:update_env
echo.
echo [3/6] Activating environment...
call conda activate mini-infer
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate environment!
    pause
    exit /b 1
)

echo.
echo [4/6] Installing PyTorch with CUDA 11.8...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install PyTorch with CUDA. Installing CPU version...
    pip install torch torchvision torchaudio
)

echo.
echo [5/6] Installing project dependencies from requirements.txt...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo [WARNING] requirements.txt not found, skipping...
)

echo.
echo [6/6] Installing Mini-Infer in development mode...
pip install -e .

echo.
echo ============================================================
echo Verifying installation...
echo ============================================================

python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Activate the environment:
echo      conda activate mini-infer
echo.
echo   2. Verify GPU (if available):
echo      python -c "import torch; print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU')"
echo.
echo   3. Run tests:
echo      pytest tests/
echo.
echo   4. Run benchmarks:
echo      python benchmarks/benchmark_throughput.py
echo.
echo ============================================================

pause
