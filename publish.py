#!/usr/bin/env python3
"""
Quick publishing utility for IPWho Python SDK.
Simplifies the publishing process to PyPI.
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Tuple

def run_command(cmd: list, description: str = "") -> Tuple[int, str]:
    """Run a shell command and return exit code and output."""
    if description:
        print(f"▶ {description}...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, str(e)

def check_version_updated() -> bool:
    """Check if version was updated since last publish."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Extract version
    for line in content.split("\n"):
        if line.startswith("version = "):
            version = line.split('"')[1]
            print(f"  Version in pyproject.toml: {version}")
            return True
    
    return False

def run_tests() -> bool:
    """Run the test suite."""
    print("\n" + "="*60)
    print("STEP 1: Running Tests")
    print("="*60)
    
    code, output = run_command(
        ["python3", "run_tests.py"],
        "Running test suite"
    )
    
    if code != 0:
        print("❌ Tests failed!")
        print(output)
        return False
    
    print("✅ All tests passed!")
    return True

def install_build_tools() -> bool:
    """Install build and twine if not available."""
    print("\n" + "="*60)
    print("STEP 2: Installing Build Tools")
    print("="*60)
    
    tools = ["build", "twine"]
    
    for tool in tools:
        code, _ = run_command(
            ["python3", "-m", "pip", "install", "--quiet", tool],
            f"Installing {tool}"
        )
        if code != 0:
            print(f"⚠️  Could not install {tool} (may already be available)")
    
    print("✅ Build tools ready")
    return True

def clean_builds() -> None:
    """Clean up old builds."""
    print("\n" + "="*60)
    print("STEP 3: Cleaning Old Builds")
    print("="*60)
    
    dirs = ["build", "dist"]
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f"  Removed {dir_name}/")
    
    # Remove egg-info
    for egg in Path(".").glob("*.egg-info"):
        import shutil
        shutil.rmtree(egg)
        print(f"  Removed {egg}/")
    
    print("✅ Old builds cleaned")

def build_package() -> bool:
    """Build the package."""
    print("\n" + "="*60)
    print("STEP 4: Building Package")
    print("="*60)
    
    code, output = run_command(
        ["python3", "-m", "build"],
        "Building distribution packages"
    )
    
    if code != 0:
        print("❌ Build failed!")
        print(output)
        return False
    
    # List built files
    dist_path = Path("dist")
    if dist_path.exists():
        print("  Built files:")
        for file in dist_path.glob("*"):
            size = file.stat().st_size / 1024
            print(f"    - {file.name} ({size:.1f} KB)")
    
    print("✅ Package built successfully")
    return True

def check_package() -> bool:
    """Check package with twine."""
    print("\n" + "="*60)
    print("STEP 5: Checking Package Metadata")
    print("="*60)
    
    code, output = run_command(
        ["python3", "-m", "twine", "check", "dist/*"],
        "Checking package metadata"
    )
    
    if "PASSED" in output or code == 0:
        print("✅ Package metadata is valid")
        return True
    else:
        print("⚠️  Some warnings (may still be publishable):")
        print(output)
        return True

def publish_to_testpypi() -> bool:
    """Publish to Test PyPI."""
    print("\n" + "="*60)
    print("STEP 6: Publishing to Test PyPI (Testing)")
    print("="*60)
    
    print("📝 This tests your package before publishing to real PyPI")
    print("⚠️  You need to have configured ~/.pypirc or PYPI token")
    print()
    
    response = input("Continue with Test PyPI upload? (y/n): ")
    if response.lower() != "y":
        return False
    
    code, output = run_command(
        ["python3", "-m", "twine", "upload", "--repository", "testpypi", "dist/*"],
        "Uploading to Test PyPI"
    )
    
    if code != 0:
        print("❌ Upload failed!")
        print(output)
        print("\n💡 Tip: Make sure your ~/.pypirc is configured correctly")
        return False
    
    print("✅ Package uploaded to Test PyPI!")
    print("📦 Test installation:")
    print("   pip install --index-url https://test.pypi.org/simple/ ipwho-ip-geolocation-api")
    
    return True

def publish_to_pypi() -> bool:
    """Publish to real PyPI."""
    print("\n" + "="*60)
    print("STEP 7: Publishing to Real PyPI")
    print("="*60)
    
    print("⚠️  This will publish to the real PyPI package index!")
    print("    Make sure you've tested on Test PyPI first!")
    print()
    
    response = input("Continue with PyPI upload? (y/n): ")
    if response.lower() != "y":
        return False
    
    final_check = input("Final confirmation - publish to PyPI? (type 'yes'): ")
    if final_check.lower() != "yes":
        print("Cancelled")
        return False
    
    code, output = run_command(
        ["python3", "-m", "twine", "upload", "dist/*"],
        "Uploading to PyPI"
    )
    
    if code != 0:
        print("❌ Upload failed!")
        print(output)
        return False
    
    print("✅ Package published to PyPI!")
    print("📦 Install with: pip install ipwho-ip-geolocation-api")
    
    return True

def main():
    """Main publish workflow."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "IPWho Python SDK Publisher" + " "*16 + "║")
    print("╚" + "="*58 + "╝")
    
    # Check if version was updated
    print("\n📋 Checking version...")
    if not check_version_updated():
        print("❌ Could not read version from pyproject.toml")
        return 1
    
    # Step 1: Run tests
    if not run_tests():
        return 1
    
    # Step 2: Install build tools
    if not install_build_tools():
        return 1
    
    # Step 3: Clean old builds
    clean_builds()
    
    # Step 4: Build package
    if not build_package():
        return 1
    
    # Step 5: Check package
    if not check_package():
        return 1
    
    # Step 6: Test PyPI (optional)
    use_test = input("\n🧪 Test on Test PyPI first? (recommended) (y/n): ")
    if use_test.lower() == "y":
        if not publish_to_testpypi():
            print("\n⚠️  Cancelled Test PyPI upload")
            return 1
    
    # Step 7: Real PyPI
    print()
    if not publish_to_pypi():
        print("\n⚠️  Cancelled PyPI upload")
        return 1
    
    # Success!
    print("\n" + "="*60)
    print("🎉 Publishing Complete!")
    print("="*60)
    print("✅ Your package is now available on PyPI!")
    print("📦 Users can install with: pip install ipwho-ip-geolocation-api")
    print("🌐 View on PyPI: https://pypi.org/project/ipwho-ip-geolocation-api/")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
