import os
import shutil
import subprocess
import json

def create_web_build():
    # Create build directory
    build_dir = "web_build"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    # Copy necessary files
    files_to_copy = [
        "main.py",
        "requirements.txt",
        "assets",
        "screens"
    ]
    
    for item in files_to_copy:
        if os.path.isfile(item):
            shutil.copy2(item, build_dir)
        elif os.path.isdir(item):
            shutil.copytree(item, os.path.join(build_dir, item))
    
    # Create web files
    create_html_file(build_dir)
    create_web_config(build_dir)
    
    print("Web build created in ./web_build directory")
    print("To deploy:")
    print("1. Install the required packages:")
    print("   pip install pygbag")
    print("2. Build and serve the game:")
    print("   pygbag web_build/main.py")
    print("3. Open http://localhost:8000 in your browser")

def create_html_file(build_dir):
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dungeon Quest</title>
    <style>
        body {
            margin: 0;
            background-color: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: Arial, sans-serif;
        }
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }
        canvas {
            display: block;
            margin: auto;
        }
    </style>
</head>
<body>
    <div id="loading">Loading game...</div>
    <script src="main.js" defer></script>
</body>
</html>"""
    
    with open(os.path.join(build_dir, "index.html"), "w") as f:
        f.write(html_content)

def create_web_config(build_dir):
    config = {
        "name": "Dungeon Quest",
        "description": "A roguelike dungeon exploration game",
        "version": "1.0.0",
        "dependencies": {
            "pygame": "2.5.2",
            "opencv-python-headless": "4.8.1.78"
        },
        "build": {
            "excludeFiles": [
                "**/__pycache__/**",
                "**/*.pyc"
            ]
        }
    }
    
    with open(os.path.join(build_dir, "web_config.json"), "w") as f:
        json.dump(config, f, indent=4)

if __name__ == "__main__":
    create_web_build()
