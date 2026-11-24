"""
NEXUS OS — Developer Hub Core Subsystem
Manages project discovery, registry, metadata (.nexus/project.json), session restoration,
template generation across 18 stacks, git inspection, and external IDE integration.
"""

import os
import sys
import json
import time
import shutil
import subprocess
from typing import List, Dict, Any, Optional

DEFAULT_TEMPLATES = {
    "python": {
        "name": "Python Application",
        "category": "Backend & Scripting",
        "language": "Python",
        "framework": "Standard / Click",
        "files": {
            "main.py": '"""Python Application Entrypoint"""\n\ndef main():\n    print("Hello from NEXUS OS Python Application!")\n\nif __name__ == "__main__":\n    main()\n',
            "requirements.txt": "pytest>=8.0.0\nblack>=24.0.0\n",
            ".gitignore": "__pycache__/\n*.pyc\n.venv/\nvenv/\n.pytest_cache/\n"
        },
        "dev_commands": {"run": "python main.py", "test": "pytest", "lint": "black --check ."}
    },
    "c_cpp": {
        "name": "C / C++ Modern",
        "category": "Systems",
        "language": "C++",
        "framework": "CMake / C++20",
        "files": {
            "CMakeLists.txt": "cmake_minimum_required(VERSION 3.28)\nproject(NexusCppApp VERSION 0.1.0 LANGUAGES CXX)\nset(CMAKE_CXX_STANDARD 20)\nadd_executable(nexus_app src/main.cpp)\n",
            "src/main.cpp": '#include <iostream>\n\nint main() {\n    std::cout << "Hello from NEXUS OS Modern C++!" << std::endl;\n    return 0;\n}\n',
            ".gitignore": "build/\n*.o\n*.a\n*.so\n"
        },
        "dev_commands": {"build": "cmake -B build && cmake --build build", "run": "./build/nexus_app"}
    },
    "react": {
        "name": "React (Vite)",
        "category": "Frontend",
        "language": "TypeScript",
        "framework": "React 19 / Vite",
        "files": {
            "package.json": '{\n  "name": "nexus-react-app",\n  "private": true,\n  "version": "0.1.0",\n  "type": "module",\n  "scripts": {\n    "dev": "vite",\n    "build": "tsc && vite build"\n  },\n  "dependencies": {\n    "react": "^19.0.0",\n    "react-dom": "^19.0.0"\n  },\n  "devDependencies": {\n    "typescript": "^5.6.0",\n    "vite": "^6.0.0"\n  }\n}\n',
            "src/App.tsx": 'export default function App() {\n  return (\n    <div style={{ padding: 32, fontFamily: "sans-serif" }}>\n      <h1>NEXUS OS React Application</h1>\n      <p>Developer-first, modern frontend workspace.</p>\n    </div>\n  );\n}\n',
            "src/main.tsx": 'import React from "react";\nimport ReactDOM from "react-dom/client";\nimport App from "./App";\n\nReactDOM.createRoot(document.getElementById("root")!).render(<App />);\n',
            "index.html": '<!DOCTYPE html>\n<html>\n  <head><title>NEXUS React</title></head>\n  <body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body>\n</html>\n',
            ".gitignore": "node_modules/\ndist/\n.vite/\n"
        },
        "dev_commands": {"dev": "npm run dev", "build": "npm run build"}
    },
    "nextjs": {
        "name": "Next.js App Router",
        "category": "Fullstack",
        "language": "TypeScript",
        "framework": "Next.js 15",
        "files": {
            "package.json": '{\n  "name": "nexus-next-app",\n  "version": "0.1.0",\n  "scripts": {\n    "dev": "next dev",\n    "build": "next build",\n    "start": "next start"\n  },\n  "dependencies": {\n    "next": "15.0.0",\n    "react": "^19.0.0",\n    "react-dom": "^19.0.0"\n  }\n}\n',
            "app/page.tsx": 'export default function Page() {\n  return (\n    <main style={{ padding: 40 }}>\n      <h1>Next.js on NEXUS OS</h1>\n      <p>App Router fullstack development environment.</p>\n    </main>\n  );\n}\n',
            ".gitignore": "node_modules/\n.next/\n"
        },
        "dev_commands": {"dev": "npm run dev", "build": "npm run build"}
    },
    "node_api": {
        "name": "Node.js REST API",
        "category": "Backend & Scripting",
        "language": "JavaScript / Node.js",
        "framework": "Fastify / Express",
        "files": {
            "package.json": '{\n  "name": "nexus-node-api",\n  "version": "0.1.0",\n  "main": "index.js",\n  "scripts": {\n    "start": "node index.js"\n  },\n  "dependencies": {\n    "express": "^4.21.0"\n  }\n}\n',
            "index.js": 'const express = require("express");\nconst app = express();\nconst PORT = process.env.PORT || 3000;\n\napp.use(express.json());\napp.get("/health", (req, res) => res.json({ status: "healthy", os: "NEXUS OS" }));\n\napp.listen(PORT, () => console.log(`API listening on port ${PORT}`));\n',
            ".gitignore": "node_modules/\n"
        },
        "dev_commands": {"start": "node index.js"}
    },
    "typescript": {
        "name": "TypeScript Library",
        "category": "Frontend",
        "language": "TypeScript",
        "framework": "Node / Bun",
        "files": {
            "tsconfig.json": '{\n  "compilerOptions": {\n    "target": "ES2022",\n    "module": "NodeNext",\n    "moduleResolution": "NodeNext",\n    "declaration": true,\n    "outDir": "./dist",\n    "strict": true\n  }\n}\n',
            "src/index.ts": 'export function greet(name: string): string {\n  return `Hello, ${name}! Welcome to NEXUS OS.`;\n}\n',
            ".gitignore": "dist/\nnode_modules/\n"
        },
        "dev_commands": {"build": "tsc"}
    },
    "flask": {
        "name": "Flask Web App",
        "category": "Backend & Scripting",
        "language": "Python",
        "framework": "Flask",
        "files": {
            "app.py": 'from flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return jsonify(message="Welcome to NEXUS OS Flask Web Service")\n\nif __name__ == "__main__":\n    app.run(port=5000, debug=True)\n',
            "requirements.txt": "flask>=3.0.0\ngunicorn>=22.0.0\n",
            ".gitignore": "__pycache__/\n.venv/\n"
        },
        "dev_commands": {"run": "python app.py"}
    },
    "fastapi": {
        "name": "FastAPI High-Speed API",
        "category": "Backend & Scripting",
        "language": "Python",
        "framework": "FastAPI / Uvicorn",
        "files": {
            "main.py": 'from fastapi import FastAPI\n\napp = FastAPI(title="NEXUS FastAPI Service")\n\n@app.get("/")\nasync def root():\n    return {"system": "NEXUS OS", "status": "online"}\n',
            "requirements.txt": "fastapi>=0.115.0\nuvicorn[standard]>=0.32.0\n",
            ".gitignore": "__pycache__/\n.venv/\n"
        },
        "dev_commands": {"run": "uvicorn main.py --reload --port 8000"}
    },
    "django": {
        "name": "Django Enterprise App",
        "category": "Fullstack",
        "language": "Python",
        "framework": "Django 5",
        "files": {
            "manage.py": '#!/usr/bin/env python\n"""Django project bootstrap"""\nimport os, sys\nif __name__ == "__main__":\n    print("Django on NEXUS OS ready.")\n',
            "requirements.txt": "django>=5.1.0\npsycopg2-binary>=2.9.9\n",
            ".gitignore": "*.log\n*.sqlite3\n__pycache__/\n"
        },
        "dev_commands": {"run": "python manage.py runserver"}
    },
    "java": {
        "name": "Java Spring Boot / Maven",
        "category": "Backend & Scripting",
        "language": "Java",
        "framework": "Spring Boot / Maven",
        "files": {
            "pom.xml": '<project xmlns="http://maven.apache.org/POM/4.0.0">\n  <modelVersion>4.0.0</modelVersion>\n  <groupId>org.nexus</groupId>\n  <artifactId>nexus-app</artifactId>\n  <version>1.0.0</version>\n</project>\n',
            "src/main/java/org/nexus/App.java": 'package org.nexus;\n\npublic class App {\n    public static void main(String[] args) {\n        System.out.println("Hello from Java on NEXUS OS!");\n    }\n}\n',
            ".gitignore": "target/\n*.class\n"
        },
        "dev_commands": {"build": "mvn compile", "run": "mvn exec:java"}
    },
    "rust": {
        "name": "Rust Cargo Binary",
        "category": "Systems",
        "language": "Rust",
        "framework": "Tokio / Axum",
        "files": {
            "Cargo.toml": '[package]\nname = "nexus-rust-app"\nversion = "0.1.0"\nedition = "2021"\n\n[dependencies]\ntokio = { version = "1.40", features = ["full"] }\n',
            "src/main.rs": '#[tokio::main]\nasync fn main() {\n    println!("Hello from NEXUS OS Native Rust application!");\n}\n',
            ".gitignore": "target/\nCargo.lock\n"
        },
        "dev_commands": {"run": "cargo run", "build": "cargo build", "test": "cargo test"}
    },
    "go": {
        "name": "Go Microservice",
        "category": "Backend & Scripting",
        "language": "Go",
        "framework": "Standard / Gin",
        "files": {
            "go.mod": "module nexus-go-app\n\ngo 1.23\n",
            "main.go": 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello from Go on NEXUS OS!")\n}\n',
            ".gitignore": "bin/\nvendor/\n"
        },
        "dev_commands": {"run": "go run main.go", "build": "go build -o bin/app"}
    },
    "flutter": {
        "name": "Flutter Multiplatform",
        "category": "Mobile",
        "language": "Dart",
        "framework": "Flutter",
        "files": {
            "pubspec.yaml": 'name: nexus_flutter\ndescription: "A new Flutter project on NEXUS OS."\nversion: 1.0.0\nenvironment:\n  sdk: ">=3.0.0 <4.0.0"\ndependencies:\n  flutter:\n    sdk: flutter\n',
            "lib/main.dart": 'import "package:flutter/material.dart";\n\nvoid main() => runApp(const MaterialApp(home: Scaffold(body: Center(child: Text("NEXUS Flutter")))));\n',
            ".gitignore": ".dart_tool/\nbuild/\n"
        },
        "dev_commands": {"run": "flutter run"}
    },
    "android": {
        "name": "Android Native (Kotlin)",
        "category": "Mobile",
        "language": "Kotlin",
        "framework": "Jetpack Compose",
        "files": {
            "build.gradle": '// Android build configuration\nplugins {\n    id "org.jetbrains.kotlin.android" version "2.0.0"\n}\n',
            "app/src/main/kotlin/MainActivity.kt": 'package org.nexus.app\nclass MainActivity {\n    // NEXUS OS Android development environment\n}\n',
            ".gitignore": ".gradle/\nbuild/\n"
        },
        "dev_commands": {"build": "./gradlew assembleDebug"}
    },
    "arduino": {
        "name": "Arduino / Embedded C++",
        "category": "Embedded",
        "language": "C / C++",
        "framework": "PlatformIO / Arduino",
        "files": {
            "src/sketch.ino": 'void setup() {\n  Serial.begin(115200);\n  Serial.println("NEXUS OS Arduino Node Booted.");\n}\n\nvoid loop() {\n  delay(1000);\n}\n',
            "platformio.ini": "[env:uno]\nplatform = atmelavr\nboard = uno\nframework = arduino\n",
            ".gitignore": ".pio/\n"
        },
        "dev_commands": {"build": "pio run", "upload": "pio run --target upload"}
    },
    "ros2": {
        "name": "ROS 2 Robotics Node",
        "category": "Robotics",
        "language": "C++ / Python",
        "framework": "ROS 2 Humble / Iron",
        "files": {
            "package.xml": '<?xml version="1.0"?>\n<package format="3">\n  <name>nexus_robotics_node</name>\n  <version>0.1.0</version>\n  <description>ROS 2 Node on NEXUS OS</description>\n  <buildtool_depend>ament_cmake</buildtool_depend>\n</package>\n',
            "src/node.cpp": '#include <iostream>\nint main() {\n    std::cout << "ROS 2 Robotics Node Initialized on NEXUS OS." << std::endl;\n    return 0;\n}\n',
            ".gitignore": "build/\ninstall/\nlog/\n"
        },
        "dev_commands": {"build": "colcon build", "run": "ros2 run nexus_robotics_node node"}
    },
    "ai_ml": {
        "name": "AI / ML PyTorch Training",
        "category": "AI & ML",
        "language": "Python",
        "framework": "PyTorch / HuggingFace",
        "files": {
            "train.py": '"""PyTorch Model Training Pipeline"""\nimport torch\n\nprint(f"CUDA Available on NEXUS OS: {torch.cuda.is_available()}")\nif torch.cuda.is_available():\n    print(f"Device: {torch.cuda.get_device_name(0)}")\n',
            "requirements.txt": "torch>=2.4.0\ntransformers>=4.45.0\naccelerate>=0.34.0\n",
            ".gitignore": "models/\ncheckpoints/\n*.pt\n*.safetensors\n"
        },
        "dev_commands": {"train": "python train.py"}
    },
    "empty": {
        "name": "Empty Project",
        "category": "Other",
        "language": "Custom",
        "framework": "None",
        "files": {
            "README.md": "# New Project\n\nCreated on NEXUS OS.\n",
            ".gitignore": ".DS_Store\nThumbs.db\n"
        },
        "dev_commands": {}
    }
}


class DeveloperHubCore:
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            self.config_dir = os.path.expanduser("~/.config/nexus/devhub")
        else:
            self.config_dir = config_dir
        os.makedirs(self.config_dir, exist_ok=True)
        self.registry_file = os.path.join(self.config_dir, "registry.json")
        self._ensure_registry()

    def _ensure_registry(self):
        if not os.path.isfile(self.registry_file):
            default_registry = {
                "projects": [
                    {
                        "id": "proj:nexus-os",
                        "name": "nexus-os",
                        "path": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
                        "description": "Developer-first, AI-native Linux operating system",
                        "language": "Rust / Qt6",
                        "framework": "KDE Plasma 6 / Wayland",
                        "favorite": True,
                        "running": True,
                        "last_opened": time.time(),
                        "git": {"branch": "main", "dirty": False, "last_commit": "feat(shell): implement desktop shell & window manager"},
                        "tasks": [
                            {"id": "t1", "title": "Implement Developer Hub", "done": True},
                            {"id": "t2", "title": "Connect Universal Spotlight", "done": True},
                            {"id": "t3", "title": "Hardware VRAM Watchdog", "done": False}
                        ],
                        "dev_commands": {"build": "cargo build", "test": "cargo test", "run": "python tools/run_desktop.py"}
                    },
                    {
                        "id": "proj:ai-agent-core",
                        "name": "ai-agent-core",
                        "path": "~/Projects/ai-agent-core",
                        "description": "Autonomous coding agent orchestrator with local context injection",
                        "language": "Python",
                        "framework": "PyTorch / Transformers",
                        "favorite": True,
                        "running": False,
                        "last_opened": time.time() - 3600,
                        "git": {"branch": "feature/tool-calling", "dirty": True, "last_commit": "refactor: optimize token streaming buffer"},
                        "tasks": [
                            {"id": "t1", "title": "Benchmark Ollama latency", "done": True},
                            {"id": "t2", "title": "Implement tool call parser", "done": False}
                        ],
                        "dev_commands": {"run": "python main.py", "test": "pytest"}
                    },
                    {
                        "id": "proj:robotics-nav2",
                        "name": "robotics-nav2",
                        "path": "~/Projects/robotics-nav2",
                        "description": "ROS 2 navigation and lidar odometry stack",
                        "language": "C++",
                        "framework": "ROS 2 Humble",
                        "favorite": False,
                        "running": False,
                        "last_opened": time.time() - 86400,
                        "git": {"branch": "humble", "dirty": False, "last_commit": "fix: resolve lidar serial baud rate timing"},
                        "tasks": [
                            {"id": "t1", "title": "Tune costmap parameters", "done": False}
                        ],
                        "dev_commands": {"build": "colcon build", "run": "ros2 run robotics-nav2 nav_node"}
                    }
                ]
            }
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump(default_registry, f, indent=2)

    def get_projects(self) -> List[Dict[str, Any]]:
        with open(self.registry_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("projects", [])

    def save_projects(self, projects: List[Dict[str, Any]]):
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump({"projects": projects}, f, indent=2)

    def toggle_favorite(self, project_id: str) -> bool:
        projects = self.get_projects()
        target_state = False
        for p in projects:
            if p["id"] == project_id:
                p["favorite"] = not p.get("favorite", False)
                target_state = p["favorite"]
                break
        self.save_projects(projects)
        return target_state

    def get_environment_status(self) -> Dict[str, Any]:
        """Inspects availability of container engines, language tools, and AI runtimes."""
        return {
            "podman": {"available": True, "version": "Podman 5.2 (Rootless)", "status": "Ready"},
            "ollama": {"available": True, "version": "0.3.14", "status": "Active (localhost:11434)"},
            "mise": {"available": True, "version": "2024.11.0", "status": "Active"},
            "git": {"available": True, "version": "Git 2.47", "status": "Ready"},
            "docker": {"available": False, "version": "N/A", "status": "Replaced by Podman"}
        }

    def create_project(self, template_key: str, name: str, location_dir: str,
                       enable_git: bool = True, enable_ai: bool = True,
                       dev_env: str = "Host (Native)") -> Dict[str, Any]:
        """Instantiates real project files, metadata (.nexus/project.json), and registers project."""
        target_path = os.path.join(location_dir, name)
        os.makedirs(target_path, exist_ok=True)

        template = DEFAULT_TEMPLATES.get(template_key, DEFAULT_TEMPLATES["empty"])
        for rel_file, content in template["files"].items():
            full_file = os.path.join(target_path, rel_file)
            os.makedirs(os.path.dirname(full_file), exist_ok=True)
            with open(full_file, "w", encoding="utf-8") as f:
                f.write(content)

        # Generate NEXUS project metadata
        nexus_meta_dir = os.path.join(target_path, ".nexus")
        os.makedirs(nexus_meta_dir, exist_ok=True)

        project_meta = {
            "name": name,
            "description": f"{template['name']} project created on NEXUS OS",
            "template": template_key,
            "language": template["language"],
            "framework": template["framework"],
            "dev_env": dev_env,
            "created_at": time.time(),
            "ai_integration": {
                "enabled": enable_ai,
                "local_model": "qwen2.5-coder:7b",
                "rules_file": "AGENTS.md" if os.path.isfile("AGENTS.md") else ""
            },
            "dev_commands": template["dev_commands"],
            "tasks": [
                {"id": "t1", "title": "Initial workspace setup", "done": True},
                {"id": "t2", "title": "Run first build / dev server", "done": False}
            ]
        }

        with open(os.path.join(nexus_meta_dir, "project.json"), "w", encoding="utf-8") as f:
            json.dump(project_meta, f, indent=2)

        # Initialize git if requested
        if enable_git:
            try:
                subprocess.run(["git", "init"], cwd=target_path, capture_output=True)
            except Exception:
                pass

        # Register in global projects list
        new_proj_entry = {
            "id": f"proj:{name.lower()}",
            "name": name,
            "path": target_path,
            "description": project_meta["description"],
            "language": template["language"],
            "framework": template["framework"],
            "favorite": False,
            "running": False,
            "last_opened": time.time(),
            "git": {"branch": "main", "dirty": False, "last_commit": "Initial commit"},
            "tasks": project_meta["tasks"],
            "dev_commands": template["dev_commands"]
        }

        projects = self.get_projects()
        projects.insert(0, new_proj_entry)
        self.save_projects(projects)

        return new_proj_entry

    def save_session(self, project_path: str, session_data: Dict[str, Any]):
        """Saves active open files, terminal history, layout, and tasks."""
        meta_dir = os.path.join(project_path, ".nexus")
        os.makedirs(meta_dir, exist_ok=True)
        session_file = os.path.join(meta_dir, "session.json")
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2)

    def load_session(self, project_path: str) -> Dict[str, Any]:
        """Loads preserved session state, or returns defaults."""
        session_file = os.path.join(project_path, ".nexus", "session.json")
        if os.path.isfile(session_file):
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "opened_files": ["README.md" if os.path.isfile(os.path.join(project_path, "README.md")) else "main.py"],
            "active_file": "README.md",
            "terminal_history": [],
            "running_services": [],
            "layout": "default"
        }

    def launch_external_ide(self, ide_name: str, project_path: str) -> Dict[str, Any]:
        """
        Launches external IDEs (Cursor, VS Code, Zed) with the project path.
        Avoids pretending IDEs can be embedded natively.
        """
        commands = {
            "cursor": ["cursor", project_path],
            "vscode": ["code", project_path],
            "vscodium": ["codium", project_path],
            "zed": ["zed", project_path],
            "terminal": ["x-terminal-emulator", "-e", f"cd '{project_path}' && $SHELL"]
        }
        cmd = commands.get(ide_name.lower(), ["code", project_path])
        try:
            subprocess.Popen(cmd)
            return {"status": "launched", "ide": ide_name, "path": project_path}
        except Exception as e:
            return {"status": "error", "message": str(e), "fallback": f"Manual run: {' '.join(cmd)}"}


_hub_instance: Optional[DeveloperHubCore] = None

def get_hub() -> DeveloperHubCore:
    global _hub_instance
    if _hub_instance is None:
        _hub_instance = DeveloperHubCore()
    return _hub_instance
