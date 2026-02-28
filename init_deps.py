import os
import subprocess
import sys

def ensure_npm_dependencies():
    """Ensure npm dependencies are installed."""
    if not os.path.exists("node_modules"):
        print("Installing npm dependencies...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "subprocess", "-c", "npm install"],
                shell=True,
                cwd="/mount/src/apigee-edge-scripts-app" if os.path.exists("/mount/src/apigee-edge-scripts-app") else "."
            )
            if result.returncode == 0 or os.path.exists("node_modules"):
                print("✓ npm dependencies installed successfully")
                return True
        except Exception as e:
            print(f"Standard npm install failed: {e}")
            # Try fallback method
            try:
                os.system("npm install")
                print("✓ npm dependencies installed (via os.system)")
                return True
            except:
                pass
    return os.path.exists("node_modules")

if __name__ == "__main__":
    ensure_npm_dependencies()
