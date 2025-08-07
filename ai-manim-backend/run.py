import os
from pathlib import Path

def setup_env():
    env_path = Path(__file__).resolve().parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

if __name__ == "__main__":
    setup_env()
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)