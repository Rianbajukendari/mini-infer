@echo off
REM Benchmark Runner Script for Mini-Infer (Windows)
REM Runs all benchmarks and generates visualizations

echo ============================================================
echo Mini-Infer Benchmark Suite
echo ============================================================
echo.

REM Check if conda environment is activated
python -c "import sys; exit(0 if 'mini-infer' in sys.prefix else 1)" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] mini-infer environment not activated.
    echo Attempting to activate...
    call conda activate mini-infer
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to activate environment!
        echo Please run: conda activate mini-infer
        pause
        exit /b 1
    )
)

echo [INFO] Running in environment: %CONDA_DEFAULT_ENV%
echo.

REM Create results directory if it doesn't exist
if not exist "benchmarks\results\" (
    echo Creating results directory...
    mkdir benchmarks\results
)

echo ============================================================
echo Step 1: Throughput Benchmark
echo ============================================================
echo.

python benchmarks/benchmark_throughput.py ^
    --batch-sizes 1 4 8 16 32 64 ^
    --num-prompts 100 ^
    --max-tokens 128

if %errorlevel% neq 0 (
    echo [ERROR] Throughput benchmark failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Step 2: Latency Benchmark
echo ============================================================
echo.

python benchmarks/benchmark_latency.py ^
    --num-runs 100 ^
    --max-tokens 50

if %errorlevel% neq 0 (
    echo [ERROR] Latency benchmark failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Step 3: Generating Visualizations
echo ============================================================
echo.

python benchmarks/plot_results.py

if %errorlevel% neq 0 (
    echo [ERROR] Visualization generation failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Benchmark Complete!
echo ============================================================
echo.
echo Results saved in: benchmarks\results\
echo.
echo Generated files:
echo   - throughput.json
echo   - latency.json
echo   - throughput_chart.png
echo   - latency_chart.png
echo   - performance_overview.png
echo.
echo ============================================================

REM Open results folder
set /p OPEN_FOLDER="Open results folder? (y/n): "
if /i "%OPEN_FOLDER%"=="y" (
    start benchmarks\results
)

pause
