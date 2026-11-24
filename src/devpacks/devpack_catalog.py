"""
NEXUS OS — Developer Packs Catalog (`devpack_catalog.py`)
Defines the 15 Developer Packs with required/optional tools, languages, frameworks,
editors, dependencies, installation sources, storage estimates, and hardware requirements.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class HardwareRequirement:
    min_ram_gb: int = 4
    recommended_ram_gb: int = 8
    gpu_required: bool = False
    gpu_recommended: bool = False
    min_storage_gb: int = 5
    notes: str = ""


@dataclass
class DevPackTool:
    id: str
    name: str
    category: str
    description: str
    backend: str          # "dnf", "flatpak", "mise", "container", "appimage", "vendor_pkg"
    package_ref: str
    size_mb: int
    check_binary: str
    is_required: bool = True
    dependencies: List[str] = field(default_factory=list)


@dataclass
class DeveloperPack:
    id: str
    name: str
    icon: str
    tagline: str
    description: str
    programming_languages: List[str]
    frameworks: List[str]
    editors: List[str]
    dependencies: List[str]
    required_tools: List[str]
    optional_tools: List[str]
    installation_sources: List[str]
    estimated_storage_mb: int
    hardware: HardwareRequirement


# ============================================================================
# MASTER TOOLS DEFINITIONS DATABASE (Referenced by Developer Packs)
# ============================================================================

MASTER_TOOLS_CATALOG: Dict[str, DevPackTool] = {
    # Core Runtimes & Version Managers
    "git": DevPackTool("git", "Git VCS", "DevOps", "Distributed version control system", "dnf", "git", 85, "git", True),
    "gh": DevPackTool("gh", "GitHub CLI", "DevOps", "Official GitHub command line tool", "dnf", "gh", 45, "gh", True, ["git"]),
    "mise": DevPackTool("mise", "Mise Toolchain", "DevOps", "Fast polyglot runtime and tool manager", "dnf", "mise", 35, "mise", True),
    "podman": DevPackTool("podman", "Podman", "DevOps", "Rootless, daemonless OCI container engine", "dnf", "podman", 140, "podman", True),
    "curl": DevPackTool("curl", "cURL", "DevOps", "Command line tool for transferring data with URLs", "dnf", "curl", 15, "curl", True),
    "zsh": DevPackTool("zsh", "Zsh & Starship", "DevOps", "Advanced shell with prompt enhancements", "dnf", "zsh", 30, "zsh", False),

    # Programming Languages
    "python": DevPackTool("python", "Python 3.13", "Languages", "Modern Python runtime and standard library", "mise", "python@3.13", 220, "python3", True),
    "nodejs": DevPackTool("nodejs", "Node.js 22 LTS", "Languages", "JavaScript runtime built on Chrome's V8 engine", "mise", "node@22", 180, "node", True),
    "rust": DevPackTool("rust", "Rust & Cargo", "Languages", "Fast, memory-safe systems programming language", "mise", "rust@latest", 450, "cargo", True),
    "go": DevPackTool("go", "Go Language", "Languages", "Concurrent and simple systems programming language", "mise", "go@latest", 310, "go", True),
    "gcc": DevPackTool("gcc", "GCC & C++ Toolchain", "Languages", "GNU Compiler Collection and build utilities", "dnf", "gcc gcc-c++ make", 290, "gcc", True),
    "clang": DevPackTool("clang", "Clang & LLVM", "Languages", "High-performance compiler and LLVM tooling", "dnf", "clang llvm", 420, "clang", False),
    "openjdk": DevPackTool("openjdk", "OpenJDK 21 LTS", "Languages", "Open-source implementation of Java Platform", "dnf", "java-21-openjdk-devel", 360, "java", True),
    "kotlin": DevPackTool("kotlin", "Kotlin Compiler", "Languages", "Modern, concise multiplatform programming language", "mise", "kotlin@latest", 140, "kotlinc", True, ["openjdk"]),

    # Editors & IDEs
    "antigravity": DevPackTool("antigravity", "Google Antigravity", "AI Development", "Next-gen AI coding agent and developer platform", "flatpak", "com.google.Antigravity", 480, "antigravity", True),
    "vscode": DevPackTool("vscode", "Visual Studio Code", "IDEs", "Popular extensible source code editor", "flatpak", "com.visualstudio.code", 320, "code", True),
    "cursor": DevPackTool("cursor", "Cursor AI Editor", "AI Development", "AI-first code editor with deep codebase indexing", "appimage", "cursor", 410, "cursor", True),
    "windsurf": DevPackTool("windsurf", "Windsurf IDE", "AI Development", "Agentic AI development environment by Codeium", "appimage", "windsurf", 390, "windsurf", False),
    "zed": DevPackTool("zed", "Zed Editor", "IDEs", "High-performance, multiplayer Rust-native editor", "flatpak", "dev.zed.Zed", 160, "zed", False),
    "neovim": DevPackTool("neovim", "Neovim", "IDEs", "Hyperextensible, Lua-scriptable Vim-based text editor", "dnf", "neovim", 65, "nvim", False),
    "android_studio": DevPackTool("android_studio", "Android Studio", "Mobile", "Official IDE for Android app development", "flatpak", "com.google.AndroidStudio", 1250, "android-studio", True, ["openjdk"]),

    # AI & ML Infrastructure
    "ollama": DevPackTool("ollama", "Ollama", "AI Development", "Local GGUF model execution daemon", "dnf", "ollama", 850, "ollama", True),
    "omniroute": DevPackTool("omniroute", "OmniRoute Service", "AI Development", "Intelligent multi-model router and context compressor", "vendor_pkg", "omniroute", 220, "omniroute", True),
    "pytorch": DevPackTool("pytorch", "PyTorch & CUDA Tools", "AI/ML", "Tensors and dynamic neural networks in Python", "mise", "pip:torch torchvision torchaudio", 2400, "python3", True, ["python"]),
    "jupyter": DevPackTool("jupyter", "JupyterLab", "AI/ML", "Web-based interactive development environment for notebooks", "mise", "pip:jupyterlab", 310, "jupyter-lab", True, ["python"]),
    "huggingface": DevPackTool("huggingface", "Hugging Face CLI & Hub", "AI/ML", "Model repository and transformers toolkit", "mise", "pip:transformers huggingface_hub", 350, "huggingface-cli", True, ["python"]),
    "claude_code": DevPackTool("claude_code", "Claude Code CLI", "AI Development", "Anthropic's terminal agent for software engineering", "mise", "npm:@anthropic-ai/claude-code", 95, "claude", False, ["nodejs"]),
    "aider": DevPackTool("aider", "Aider AI Pair Programmer", "AI Development", "Terminal AI pair programming tool with Git integration", "mise", "pip:aider-chat", 120, "aider", False, ["python", "git"]),

    # Databases & Backend Tools
    "postgresql": DevPackTool("postgresql", "PostgreSQL Server & CLI", "Databases", "Powerful open source object-relational database", "dnf", "postgresql-server postgresql-contrib", 180, "psql", True),
    "dbeaver": DevPackTool("dbeaver", "DBeaver Community", "Databases", "Universal multi-platform database tool", "flatpak", "io.dbeaver.DBeaverCommunity", 240, "dbeaver", True),
    "sqlite": DevPackTool("sqlite", "SQLite3 Tools", "Databases", "Self-contained serverless SQL database engine", "dnf", "sqlite sqlite-devel", 25, "sqlite3", True),
    "redis": DevPackTool("redis", "Redis In-Memory Store", "Databases", "Fast in-memory data structure store", "dnf", "redis", 45, "redis-cli", False),

    # Web & Testing Utilities
    "bruno": DevPackTool("bruno", "Bruno API Client", "Web Development", "Fast, Git-friendly, offline-first open-source API client", "flatpak", "com.usebruno.Bruno", 160, "bruno", True),
    "chromium": DevPackTool("chromium", "Chromium Dev Browser", "Web Development", "Open-source web browser with Chrome DevTools", "dnf", "chromium", 280, "chromium-browser", True),

    # Build Systems & Systems Utilities
    "cmake": DevPackTool("cmake", "CMake & Ninja", "Languages", "Cross-platform build system generator and fast assembler", "dnf", "cmake ninja-build", 80, "cmake", True),
    "gdb": DevPackTool("gdb", "GDB & Valgrind", "Languages", "GNU Debugger and memory error detector", "dnf", "gdb valgrind", 110, "gdb", True),

    # Robotics & Computer Vision
    "ros2": DevPackTool("ros2", "ROS 2 Jazzy Core", "Robotics", "Robot Operating System 2 robotics framework", "container", "docker.io/osrf/ros:jazzy-desktop", 3800, "ros2", True),
    "gazebo": DevPackTool("gazebo", "Gazebo Sim", "Robotics", "Advanced 3D multi-robot physics simulator", "flatpak", "org.gazebosim.Gazebo", 1650, "gz", True),
    "rviz": DevPackTool("rviz", "RViz2 Visualizer", "Robotics", "3D robotics visualization tool for ROS 2", "container", "ros2-rviz2", 750, "rviz2", True, ["ros2"]),
    "opencv": DevPackTool("opencv", "OpenCV Library & Python", "Robotics", "Open Source Computer Vision Library", "dnf", "opencv opencv-devel python3-opencv", 480, "opencv_version", True, ["python"]),

    # Embedded & Microcontrollers
    "arduino": DevPackTool("arduino", "Arduino IDE 2", "Embedded", "Electronics prototyping platform IDE", "flatpak", "cc.arduino.IDE2", 340, "arduino-ide", True),
    "platformio": DevPackTool("platformio", "PlatformIO Core", "Embedded", "Next-gen professional collaborative platform for embedded", "mise", "pip:platformio", 160, "pio", True, ["python"]),
    "arm_none_eabi": DevPackTool("arm_none_eabi", "ARM Embedded Toolchain", "Embedded", "GNU toolchain for Cortex-M and Cortex-R bare-metal", "dnf", "arm-none-eabi-gcc-cs arm-none-eabi-newlib", 620, "arm-none-eabi-gcc", True),
    "openocd": DevPackTool("openocd", "OpenOCD Debugger", "Embedded", "On-Chip Debugger, in-system programming and boundary-scan", "dnf", "openocd", 75, "openocd", False),

    # Game Development & Creative
    "godot": DevPackTool("godot", "Godot Engine 4", "Game Development", "Feature-packed, multi-platform 2D and 3D game engine", "flatpak", "org.godotengine.Godot", 260, "godot", True),
    "blender": DevPackTool("blender", "Blender 3D", "Game Development", "Professional 3D modeling, animation, rendering suite", "flatpak", "org.blender.Blender", 890, "blender", True),
    "krita": DevPackTool("krita", "Krita Digital Painting", "Design", "Professional sketching, painting, and sprite creation suite", "flatpak", "org.kde.krita", 310, "krita", False),

    # Cybersecurity
    "wireshark": DevPackTool("wireshark", "Wireshark Packet Analyzer", "Cybersecurity", "Network protocol analyzer and packet sniffer", "dnf", "wireshark", 190, "wireshark", True),
    "nmap": DevPackTool("nmap", "Nmap Network Scanner", "Cybersecurity", "Network discovery and vulnerability scanning tool", "dnf", "nmap", 45, "nmap", True),
    "ghidra": DevPackTool("ghidra", "Ghidra Reverse Engineering", "Cybersecurity", "NSA software reverse engineering framework", "flatpak", "org.ghidra_sre.Ghidra", 850, "ghidra", True, ["openjdk"]),
    "metasploit": DevPackTool("metasploit", "Metasploit Framework", "Cybersecurity", "Penetration testing and exploit research suite", "container", "metasploitframework/metasploit-framework", 1100, "msfconsole", False),

    # Cloud & DevOps Infrastructure
    "kubectl": DevPackTool("kubectl", "Kubectl & Helm", "DevOps", "Kubernetes cluster command line and package manager", "mise", "kubectl@latest helm@latest", 130, "kubectl", True),
    "terraform": DevPackTool("terraform", "Terraform / OpenTofu", "Cloud", "Declarative Infrastructure as Code provisioning tool", "mise", "opentofu@latest", 95, "tofu", True),
    "awscli": DevPackTool("awscli", "AWS Command Line Interface", "Cloud", "Unified tool to manage Amazon Web Services", "mise", "awscli@latest", 140, "aws", False, ["python"]),
    "gcloud": DevPackTool("gcloud", "Google Cloud SDK", "Cloud", "Command-line interface for Google Cloud Platform", "dnf", "google-cloud-cli", 290, "gcloud", False),
    "ansible": DevPackTool("ansible", "Ansible Automation", "DevOps", "Radically simple IT automation system", "mise", "pip:ansible-core", 180, "ansible", False, ["python"])
}


# ============================================================================
# 15 DEVELOPER PACKS DEFINITIONS
# ============================================================================

DEVELOPER_PACKS: List[DeveloperPack] = [
    # 1. Full-Stack Developer
    DeveloperPack(
        id="fullstack",
        name="Full-Stack Developer",
        icon="🌐",
        tagline="Modern web engineering with frontend, backend, containers, and databases",
        description="Complete web development stack including Node.js, Python, TypeScript, React tooling, PostgreSQL, Podman, and VS Code.",
        programming_languages=["JavaScript", "TypeScript", "Python 3.13", "SQL", "HTML/CSS"],
        frameworks=["React", "Next.js", "Express", "Tailwind CSS", "FastAPI"],
        editors=["Visual Studio Code", "Cursor"],
        dependencies=["git", "curl", "podman", "mise"],
        required_tools=["git", "gh", "mise", "nodejs", "python", "podman", "vscode", "postgresql", "dbeaver", "bruno"],
        optional_tools=["cursor", "redis", "zsh", "chromium"],
        installation_sources=["dnf", "flatpak", "mise"],
        estimated_storage_mb=3200,
        hardware=HardwareRequirement(min_ram_gb=8, recommended_ram_gb=16, min_storage_gb=10, notes="Solid SSD recommended for node_modules and container images.")
    ),

    # 2. AI/ML Developer
    DeveloperPack(
        id="aiml",
        name="AI/ML Developer",
        icon="🧠",
        tagline="Machine learning, deep neural networks, local LLMs, and model development",
        description="State-of-the-art AI/ML stack with PyTorch, CUDA acceleration tooling, JupyterLab, Hugging Face transformers, and Ollama model execution.",
        programming_languages=["Python 3.13", "CUDA C++", "Julia (optional)"],
        frameworks=["PyTorch", "Hugging Face Transformers", "vLLM", "NumPy", "Pandas", "Scikit-Learn"],
        editors=["Cursor", "Visual Studio Code"],
        dependencies=["git", "python", "mise", "curl"],
        required_tools=["git", "mise", "python", "pytorch", "jupyter", "huggingface", "ollama", "cursor"],
        optional_tools=["vscode", "omniroute", "aider"],
        installation_sources=["mise", "dnf", "appimage"],
        estimated_storage_mb=5400,
        hardware=HardwareRequirement(min_ram_gb=16, recommended_ram_gb=32, gpu_required=False, gpu_recommended=True, min_storage_gb=25, notes="NVIDIA GPU with >= 6GB VRAM strongly recommended for local inference and training.")
    ),

    # 3. Vibe Coder
    DeveloperPack(
        id="vibecoder",
        name="Vibe Coder",
        icon="✨",
        tagline="AI-native prompt-driven development, agentic coding, and instant iteration",
        description="Designed specifically for AI-assisted programmers and vibe coders: Google Antigravity, Claude Code, Cursor, Ollama local model execution, OmniRoute integration, and rapid prototyping tools.",
        programming_languages=["TypeScript", "Python 3.13", "HTML/CSS", "Markdown"],
        frameworks=["Next.js", "Vite", "FastAPI", "Tailwind CSS", "Shadcn UI"],
        editors=["Google Antigravity", "Cursor", "Windsurf"],
        dependencies=["git", "curl", "mise", "podman"],
        required_tools=["git", "gh", "mise", "nodejs", "python", "podman", "antigravity", "cursor", "ollama", "omniroute", "chromium", "sqlite"],
        optional_tools=["windsurf", "claude_code", "aider", "dbeaver"],
        installation_sources=["flatpak", "appimage", "mise", "dnf", "vendor_pkg"],
        estimated_storage_mb=3900,
        hardware=HardwareRequirement(min_ram_gb=8, recommended_ram_gb=16, gpu_required=False, gpu_recommended=True, min_storage_gb=15, notes="Local AI agents benefit from GPU acceleration; cloud fallbacks configured via OmniRoute.")
    ),

    # 4. Software Engineer
    DeveloperPack(
        id="swe",
        name="Software Engineer",
        icon="💻",
        tagline="Core enterprise engineering, scalable systems, algorithms, and microservices",
        description="Comprehensive polyglot engineering suite with GCC/Clang, Rust, Go, Python, OpenJDK, Git LFS, debugging tools, and container runtimes.",
        programming_languages=["C++20", "Rust", "Go", "Python 3.13", "Java 21"],
        frameworks=["Spring Boot", "Tokio", "Gin", "Standard Libraries"],
        editors=["Visual Studio Code", "Neovim"],
        dependencies=["git", "podman", "mise", "cmake"],
        required_tools=["git", "gh", "mise", "gcc", "rust", "go", "python", "openjdk", "cmake", "gdb", "podman", "vscode"],
        optional_tools=["clang", "neovim", "zed", "postgresql"],
        installation_sources=["dnf", "mise", "flatpak"],
        estimated_storage_mb=4100,
        hardware=HardwareRequirement(min_ram_gb=8, recommended_ram_gb=16, min_storage_gb=15, notes="Multi-core CPU recommended for parallel compilation.")
    ),

    # 5. Python Developer
    DeveloperPack(
        id="python_dev",
        name="Python Developer",
        icon="🐍",
        tagline="Pythonic application development, data analysis, scripting, and APIs",
        description="Clean, optimized Python environment with Python 3.13, uv/pip, JupyterLab, SQLite, VS Code, and backend API frameworks.",
        programming_languages=["Python 3.13", "SQL"],
        frameworks=["FastAPI", "Flask", "Django", "Pydantic", "Pytest", "SQLAlchemy"],
        editors=["Visual Studio Code", "Cursor"],
        dependencies=["git", "mise", "curl"],
        required_tools=["git", "mise", "python", "sqlite", "vscode", "jupyter", "bruno"],
        optional_tools=["cursor", "postgresql", "dbeaver"],
        installation_sources=["dnf", "mise", "flatpak"],
        estimated_storage_mb=1900,
        hardware=HardwareRequirement(min_ram_gb=4, recommended_ram_gb=8, min_storage_gb=8, notes="Lightweight footprint; runs smoothly on almost any modern laptop.")
    ),

    # 6. C/C++ Developer
    DeveloperPack(
        id="cpp_dev",
        name="C/C++ Developer",
        icon="⚙️",
        tagline="High-performance systems programming, game engines, and native libraries",
        description="Modern C++20/C++23 toolchain featuring GCC, Clang, CMake, Ninja, GDB, Valgrind, and VS Code with C/C++ extensions.",
        programming_languages=["C17", "C++20", "C++23", "Assembly"],
        frameworks=["STL", "Boost", "Qt6", "POSIX APIs"],
        editors=["Visual Studio Code", "Neovim", "Zed"],
        dependencies=["git", "curl"],
        required_tools=["git", "gcc", "clang", "cmake", "gdb", "vscode"],
        optional_tools=["neovim", "zed", "podman"],
        installation_sources=["dnf", "flatpak"],
        estimated_storage_mb=2100,
        hardware=HardwareRequirement(min_ram_gb=8, recommended_ram_gb=16, min_storage_gb=10, notes="Fast SSD and multi-threaded CPU significantly improve build times.")
    ),

    # 7. Android Developer
    DeveloperPack(
        id="android_dev",
        name="Android Developer",
        icon="📱",
        tagline="Native mobile application development, Jetpack Compose, and Kotlin",
        description="Complete Android app development environment with Android Studio, OpenJDK 21, Kotlin compiler, Gradle, and Android SDK command-line utilities.",
        programming_languages=["Kotlin", "Java 21", "C++ (NDK)"],
        frameworks=["Jetpack Compose", "Android SDK", "Coroutines", "Ktor"],
        editors=["Android Studio", "Visual Studio Code"],
        dependencies=["git", "openjdk", "curl"],
        required_tools=["git", "openjdk", "kotlin", "android_studio", "vscode"],
        optional_tools=["nodejs", "bruno"],
        installation_sources=["flatpak", "dnf", "mise"],
        estimated_storage_mb=4800,
        hardware=HardwareRequirement(min_ram_gb=16, recommended_ram_gb=32, min_storage_gb=20, notes="16GB+ RAM strongly recommended for Android Studio + Android Virtual Device (AVD) emulator.")
    ),

    # 8. Game Developer
    DeveloperPack(
        id="gamedev",
        name="Game Developer",
        icon="🎮",
        tagline="2D and 3D game engines, asset creation, physics, and gameplay scripting",
        description="Comprehensive game creator setup featuring Godot Engine 4, Blender 3D, C++ build tools, Python, and Krita for textures and sprites.",
        programming_languages=["GDScript", "C++20", "C#", "Python 3.13"],
        frameworks=["Godot 4", "Vulkan SDK", "OpenGL", "SDL2"],
        editors=["Godot Engine", "Visual Studio Code"],
        dependencies=["git", "gcc", "cmake"],
        required_tools=["git", "gcc", "cmake", "godot", "blender", "vscode"],
        optional_tools=["krita", "python"],
        installation_sources=["flatpak", "dnf"],
        estimated_storage_mb=3100,
        hardware=HardwareRequirement(min_ram_gb=8, recommended_ram_gb=16, gpu_required=True, gpu_recommended=True, min_storage_gb=15, notes="Dedicated GPU supporting Vulkan 1.2+ required for 3D viewport rendering.")
    ),

    # 9. Robotics Developer
    DeveloperPack(
        id="robotics",
        name="Robotics Developer",
        icon="🦾",
        tagline="Autonomous systems, sensor fusion, 3D simulation, and robotic middleware",
        description="Industrial robotics development stack featuring ROS 2 Jazzy, Gazebo 3D simulation, RViz2 visualization, OpenCV, and C++/Python tooling.",
        programming_languages=["C++20", "Python 3.13"],
        frameworks=["ROS 2 (Robot Operating System)", "OpenCV", "Gazebo Sim", "URDF"],
        editors=["Visual Studio Code"],
        dependencies=["git", "gcc", "cmake", "python", "podman"],
        required_tools=["git", "gcc", "cmake", "python", "podman", "ros2", "gazebo", "rviz", "opencv", "vscode"],
        optional_tools=["arduino", "platformio"],
        installation_sources=["dnf", "container", "flatpak"],
        estimated_storage_mb=7200,
        hardware=HardwareRequirement(min_ram_gb=16, recommended_ram_gb=32, gpu_required=True, gpu_recommended=True, min_storage_gb=30, notes="Dedicated GPU required for Gazebo 3D physics rendering and sensor simulation.")
    ),

    # 10. Embedded Developer
    DeveloperPack(
        id="embedded",
        name="Embedded Developer",
        icon="📟",
        tagline="Bare-metal microcontrollers, ARM Cortex, IoT firmware, and hardware debugging",
        description="Electronics and firmware engineering environment with ARM GCC cross-compiler, PlatformIO, OpenOCD, Arduino IDE 2, and serial tools.",
        programming_languages=["C11", "C++17", "Assembly"],
        frameworks=["FreeRTOS", "CMSIS", "ESP-IDF", "Arduino Core"],
        editors=["Visual Studio Code", "Arduino IDE 2"],
        dependencies=["git", "gcc", "python", "mise"],
        required_tools=["git", "gcc", "python", "mise", "arm_none_eabi", "platformio", "arduino", "vscode"],
        optional_tools=["openocd", "cmake", "gdb"],
        installation_sources=["dnf", "flatpak", "mise"],
        estimated_storage_mb=2600,
        hardware=HardwareRequirement(min_ram_gb=4, recommended_ram_gb=8, min_storage_gb=10, notes="USB ports required for hardware programmer / UART debugging.")
    ),

    # 11. Cybersecurity Learner
    DeveloperPack(
        id="cybersecurity",
        name="Cybersecurity Learner",
        icon="🛡️",
        tagline="Network analysis, reverse engineering, ethical penetration testing, and security auditing",
        description="Comprehensive security research environment including Wireshark, Nmap, Ghidra reverse engineering suite, Metasploit, Python, and GDB.",
        programming_languages=["Python 3.13", "C", "x86/ARM Assembly", "Bash"],
        frameworks=["Scapy", "PyCryptodome", "Ghidra Decompiler"],
        editors=["Visual Studio Code", "Ghidra"],
        dependencies=["git", "python", "openjdk", "podman"],
        required_tools=["git", "python", "openjdk", "wireshark", "nmap", "ghidra", "gdb", "vscode"],
        optional_tools=["metasploit", "podman", "curl"],
        installation_sources=["dnf", "flatpak", "container"],
        estimated_storage_mb=3400,
        hardware=HardwareRequirement(min_ram_gb=8, recommended_ram_gb=16, min_storage_gb=15, notes="8GB+ RAM recommended for Ghidra Java heap analysis.")
    ),

    # 12. DevOps Engineer
    DeveloperPack(
        id="devops",
        name="DevOps Engineer",
        icon="🔄",
        tagline="Infrastructure as Code, CI/CD pipelines, container orchestration, and telemetry",
        description="Cloud infrastructure and operations toolkit featuring Podman, Kubectl, Helm, Terraform/OpenTofu, Ansible, GitHub CLI, and Zsh.",
        programming_languages=["Go", "Python 3.13", "HCL", "YAML", "Bash"],
        frameworks=["Kubernetes", "OpenTofu", "Ansible", "OCI Containers"],
        editors=["Visual Studio Code", "Neovim"],
        dependencies=["git", "curl", "mise"],
        required_tools=["git", "gh", "mise", "podman", "kubectl", "terraform", "python", "vscode"],
        optional_tools=["ansible", "awscli", "zsh", "neovim"],
        installation_sources=["dnf", "mise", "flatpak"],
        estimated_storage_mb=2300,
        hardware=HardwareRequirement(min_ram_gb=8, recommended_ram_gb=16, min_storage_gb=15, notes="Containerized testing benefits from >= 8GB RAM.")
    ),

    # 13. Cloud Developer
    DeveloperPack(
        id="cloud_dev",
        name="Cloud Developer",
        icon="☁️",
        tagline="Cloud-native microservices, serverless functions, multi-cloud CLIs, and IaC",
        description="Cloud application development pack with AWS CLI, Google Cloud SDK, Terraform, Podman, Node.js, Python, and Go.",
        programming_languages=["Go", "Python 3.13", "TypeScript", "HCL"],
        frameworks=["AWS CDK", "Serverless", "OpenTofu", "FastAPI"],
        editors=["Visual Studio Code", "Cursor"],
        dependencies=["git", "curl", "mise", "podman"],
        required_tools=["git", "gh", "mise", "python", "nodejs", "go", "podman", "terraform", "vscode"],
        optional_tools=["awscli", "gcloud", "cursor", "bruno"],
        installation_sources=["dnf", "mise", "flatpak"],
        estimated_storage_mb=2700,
        hardware=HardwareRequirement(min_ram_gb=8, recommended_ram_gb=16, min_storage_gb=15, notes="Broadband internet required for cloud deployments.")
    ),

    # 14. Student
    DeveloperPack(
        id="student",
        name="Student",
        icon="🎓",
        tagline="Lightweight, approachable multi-language environment for CS courses and labs",
        description="Balanced, distraction-free environment for computer science coursework: Python, C/C++, Java, Git, SQLite, JupyterLab, and VS Code.",
        programming_languages=["Python 3.13", "C++", "Java 21", "SQL"],
        frameworks=["Standard Libraries", "Pytest", "JUnit"],
        editors=["Visual Studio Code"],
        dependencies=["git", "curl", "mise"],
        required_tools=["git", "gh", "mise", "python", "gcc", "openjdk", "sqlite", "jupyter", "vscode"],
        optional_tools=["dbeaver", "bruno"],
        installation_sources=["dnf", "mise", "flatpak"],
        estimated_storage_mb=2800,
        hardware=HardwareRequirement(min_ram_gb=4, recommended_ram_gb=8, min_storage_gb=10, notes="Runs comfortably on budget and student laptops.")
    ),

    # 15. Complete Developer
    DeveloperPack(
        id="complete",
        name="Complete Developer",
        icon="👑",
        tagline="The ultimate developer environment covering web, systems, AI/ML, mobile, cloud, and devops",
        description="Everything a professional needs in one comprehensive installation: Antigravity, Cursor, VS Code, Python, Rust, Go, Node.js, C++, Podman, Ollama, OmniRoute, Git, and full database tooling.",
        programming_languages=["Python 3.13", "TypeScript", "Rust", "Go", "C++20", "Java 21", "SQL"],
        frameworks=["PyTorch", "React", "Next.js", "ROS 2", "Godot 4", "OpenTofu"],
        editors=["Google Antigravity", "Cursor", "Visual Studio Code"],
        dependencies=["git", "curl", "mise", "podman", "cmake"],
        required_tools=[
            "git", "gh", "mise", "python", "nodejs", "rust", "go", "gcc", "openjdk",
            "podman", "antigravity", "cursor", "vscode", "ollama", "omniroute",
            "postgresql", "sqlite", "dbeaver", "bruno", "cmake", "gdb", "kubectl", "terraform"
        ],
        optional_tools=["pytorch", "jupyter", "godot", "blender", "wireshark", "zsh", "redis"],
        installation_sources=["dnf", "flatpak", "mise", "appimage", "vendor_pkg"],
        estimated_storage_mb=9800,
        hardware=HardwareRequirement(min_ram_gb=16, recommended_ram_gb=32, gpu_required=False, gpu_recommended=True, min_storage_gb=40, notes="Complete multi-disciplinary development workstation.")
    )
]


def get_all_packs() -> List[DeveloperPack]:
    """Returns the full list of 15 developer packs."""
    return list(DEVELOPER_PACKS)


def get_pack_by_id(pack_id: str) -> Optional[DeveloperPack]:
    """Lookup pack by its ID."""
    for p in DEVELOPER_PACKS:
        if p.id == pack_id:
            return p
    return None


def get_tool_by_id(tool_id: str) -> Optional[DevPackTool]:
    """Lookup tool by ID in master catalog."""
    return MASTER_TOOLS_CATALOG.get(tool_id)
