"""
InspiroAI - Main Entry Point
Run the application with: python main.py
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))


def check_dependencies():
    """Check if all required packages are installed."""
    print("\n" + "="*60)
    print("🔍 Checking dependencies...")
    print("="*60)
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'scikit-learn',
        'xgboost', 'lightgbm', 'catboost', 'plotly',
        'sentence-transformers', 'joblib', 'textblob',
        'emoji', 'textstat', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (MISSING)")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n" + "="*60)
        print("⚠️  Installing missing dependencies...")
        print("="*60)
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-q'] + missing_packages
        )
        print("✓ Dependencies installed successfully!")
    else:
        print("\n✓ All dependencies are installed!")
    
    print()


def check_models():
    """Check if model artifacts exist."""
    print("="*60)
    print("🤖 Checking model artifacts...")
    print("="*60)
    
    models_dir = PROJECT_ROOT / 'models'
    
    required_models = [
        'emotion_svm_pipeline.joblib',
        'emotion_label_encoder.joblib',
        'reach_voting.joblib',
        'reach_scaler.joblib',
        'reach_ohe.joblib',
        'reach_meta.json',
        'reach_thresh.joblib',
        'status_xgb.joblib',
        'status_rf.joblib',
        'status_lgb.joblib',
        'status_style_features.joblib',
        'status_meta.json'
    ]
    
    all_exist = True
    for model in required_models:
        model_path = models_dir / model
        if model_path.exists():
            size = model_path.stat().st_size / 1024  # KB
            print(f"✓ {model} ({size:.1f} KB)")
        else:
            print(f"✗ {model} (MISSING)")
            all_exist = False
    
    if not all_exist:
        print("\n" + "="*60)
        print("⚠️  Generating missing models...")
        print("="*60)
        export_script = PROJECT_ROOT / 'export_models.py'
        subprocess.check_call([sys.executable, str(export_script)])
        print("✓ Models exported successfully!")
    else:
        print("\n✓ All model artifacts are present!")
    
    print()


def run_tests():
    """Run system tests."""
    print("="*60)
    print("🧪 Running system tests...")
    print("="*60)
    
    test_script = PROJECT_ROOT / 'test_system.py'
    result = subprocess.run(
        [sys.executable, str(test_script)],
        capture_output=False
    )
    
    if result.returncode != 0:
        print("\n⚠️  Some tests failed. Continuing anyway...")
    else:
        print("\n✓ All tests passed!")
    
    print()


def run_streamlit_app():
    """Run the Streamlit application."""
    print("="*60)
    print("🚀 Starting InspiroAI Application...")
    print("="*60)
    print("\n📱 Opening in browser at: http://localhost:8501")
    print("📝 Press Ctrl+C to stop the server\n")
    
    app_script = PROJECT_ROOT / 'app.py'
    
    # Run streamlit
    subprocess.run(
        [sys.executable, '-m', 'streamlit', 'run', str(app_script)],
        cwd=str(PROJECT_ROOT)
    )


def main():
    """Main entry point."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*12 + "🎨 InspiroAI - Caption Optimizer 🎨" + " "*11 + "║")
    print("╚" + "="*58 + "╝")
    
    print(f"\n📍 Project Root: {PROJECT_ROOT}")
    print(f"🖥️  Platform: {platform.system()} {platform.release()}")
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    
    try:
        # Step 1: Check dependencies
        check_dependencies()
        
        # Step 2: Check/Export models
        check_models()
        
        # Step 3: Run the app directly
        run_streamlit_app()
    
    except KeyboardInterrupt:
        print("\n\n⛔ Application stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nFor help, check:")
        print("  - README.md (overview)")
        print("  - SETUP_GUIDE.md (installation)")
        print("  - API_REFERENCE.md (documentation)")
        sys.exit(1)


if __name__ == "__main__":
    main()
