"""
NEXUS OS — Curated Developer Software Center Database
Maintains catalog of 60+ curated developer packages across all 15 categories.
Provides search, category filtering, installed state detection, and favorites.
"""

import os
import sys
import json
import shutil
from typing import Dict, Any, List, Optional
from .catalog_models import SoftwarePackage, CATEGORIES, BACKENDS

class CatalogDB:
    """
    Curated catalog database and repository manager.
    """

    DEFAULT_PACKAGES: List[Dict[str, Any]] = [
        # --- 1. AI Development ---
        {
            "id": "antigravity",
            "name": "Google Antigravity",
            "category": "ai_dev",
            "description": "Developer-first agentic AI IDE and CLI workflow engine.",
            "long_description": "Google's AI-native development environment integrating visual IDE panels with proactive agentic assistance.",
            "version": "1.0.0",
            "available_versions": ["1.0.0", "preview-2"],
            "maintainer": "Google DeepMind / Developer Platform",
            "license": "Google Proprietary",
            "homepage": "https://antigravity.google",
            "icon": "🚀",
            "backend": "dnf",
            "package_ref": "google-antigravity",
            "dependencies": ["wayland", "libsecret", "glibc"],
            "size_mb": 140,
            "compatibility": ["Fedora 41+", "x86_64", "Wayland Native"],
            "check_binary": "antigravity",
            "install_args": ["dnf", "install", "-y", "google-antigravity"],
            "uninstall_args": ["dnf", "remove", "-y", "google-antigravity"],
            "favorite": True
        },
        {
            "id": "ollama",
            "name": "Ollama Local Engine",
            "category": "ai_dev",
            "description": "Get up and running with open-weights LLMs locally.",
            "long_description": "High-performance local inference server for Llama 3, Qwen 2.5, DeepSeek R1, and Mistral.",
            "version": "0.5.8",
            "available_versions": ["0.5.8", "0.5.7"],
            "maintainer": "Ollama Inc.",
            "license": "MIT",
            "homepage": "https://ollama.com",
            "icon": "🦙",
            "backend": "vendor_pkg",
            "package_ref": "ollama",
            "dependencies": ["glibc", "systemd"],
            "size_mb": 95,
            "compatibility": ["Fedora 41+", "x86_64", "CUDA", "ROCm"],
            "check_binary": "ollama",
            "install_args": ["sh", "-c", "curl -fsSL https://ollama.com/install.sh | sh"],
            "uninstall_args": ["rm", "-f", "/usr/local/bin/ollama"],
            "favorite": True
        },
        {
            "id": "cursor",
            "name": "Cursor",
            "category": "ai_dev",
            "description": "The AI Code Editor built for agentic multi-file refactoring.",
            "long_description": "Modern IDE fork of VS Code with smart multi-file code editing, predictive tab completions, and chat.",
            "version": "0.45.11",
            "available_versions": ["0.45.11", "0.44.0"],
            "maintainer": "Anysphere",
            "license": "Proprietary",
            "homepage": "https://cursor.com",
            "icon": "⚡",
            "backend": "appimage",
            "package_ref": "cursor",
            "dependencies": ["glibc", "fuse"],
            "size_mb": 180,
            "compatibility": ["Fedora 41+", "x86_64", "AppImage"],
            "check_binary": "cursor",
            "install_args": ["curl", "-fsSL", "-o", "~/.local/bin/cursor", "https://downloader.cursor.sh/linux/appImage/x64"],
            "uninstall_args": ["rm", "-f", "~/.local/bin/cursor"],
            "favorite": True
        },
        {
            "id": "windsurf",
            "name": "Windsurf",
            "category": "ai_dev",
            "description": "Agentic AI IDE with collaborative Cascade workflows.",
            "long_description": "Next-generation IDE powered by Codeium's Cascade engine for deep contextual codebase understanding.",
            "version": "1.2.0",
            "available_versions": ["1.2.0"],
            "maintainer": "Codeium",
            "license": "Proprietary",
            "homepage": "https://codeium.com/windsurf",
            "icon": "🏄",
            "backend": "dnf",
            "package_ref": "windsurf",
            "dependencies": ["glibc", "libsecret"],
            "size_mb": 165,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "windsurf",
            "install_args": ["dnf", "install", "-y", "windsurf"],
            "uninstall_args": ["dnf", "remove", "-y", "windsurf"]
        },
        {
            "id": "claude_code",
            "name": "Claude Code",
            "category": "ai_dev",
            "description": "Anthropic's agentic coding tool for terminal workflows.",
            "long_description": "Terminal CLI agent that understands repository architectures, writes edits across files, and runs test suites.",
            "version": "0.2.14",
            "available_versions": ["0.2.14"],
            "maintainer": "Anthropic",
            "license": "Anthropic Proprietary",
            "homepage": "https://anthropic.com/claude-code",
            "icon": "🤖",
            "backend": "mise",
            "package_ref": "@anthropic-ai/claude-code",
            "dependencies": ["nodejs>=22.0"],
            "size_mb": 45,
            "compatibility": ["Fedora 41+", "Node.js 22+"],
            "check_binary": "claude",
            "install_args": ["npm", "install", "-g", "@anthropic-ai/claude-code"],
            "uninstall_args": ["npm", "uninstall", "-g", "@anthropic-ai/claude-code"]
        },
        {
            "id": "opencode",
            "name": "OpenCode",
            "category": "ai_dev",
            "description": "Open-source terminal AI coding assistant with local model support.",
            "long_description": "Lightweight, privacy-first terminal pair programmer that connects to Ollama, OmniRoute, and OpenAI endpoints.",
            "version": "1.1.0",
            "available_versions": ["1.1.0"],
            "maintainer": "OpenCode Community",
            "license": "MIT",
            "homepage": "https://opencode.ai",
            "icon": "💻",
            "backend": "mise",
            "package_ref": "opencode-ai",
            "dependencies": ["nodejs>=18"],
            "size_mb": 30,
            "compatibility": ["Fedora 41+", "Any Linux"],
            "check_binary": "opencode",
            "install_args": ["npm", "install", "-g", "opencode-ai"],
            "uninstall_args": ["npm", "uninstall", "-g", "opencode-ai"]
        },

        # --- 2. IDEs and Editors ---
        {
            "id": "vscode",
            "name": "Visual Studio Code",
            "category": "editors",
            "description": "Code editing redefined. Free, built on open source, runs everywhere.",
            "long_description": "Industry-standard developer editor with rich ecosystem of extensions, debugging, and Git integration.",
            "version": "1.97.2",
            "available_versions": ["1.97.2", "1.96.0"],
            "maintainer": "Microsoft",
            "license": "Microsoft Proprietary / MIT",
            "homepage": "https://code.visualstudio.com",
            "icon": "🟦",
            "backend": "dnf",
            "package_ref": "code",
            "dependencies": ["glibc", "libsecret", "xdg-utils"],
            "size_mb": 115,
            "compatibility": ["Fedora 41+", "x86_64", "Wayland"],
            "check_binary": "code",
            "install_args": ["dnf", "install", "-y", "code"],
            "uninstall_args": ["dnf", "remove", "-y", "code"],
            "favorite": True
        },
        {
            "id": "vscodium",
            "name": "VSCodium",
            "category": "editors",
            "description": "Community-driven, freely-licensed binary distribution of VS Code.",
            "long_description": "Telemetry-free open-source build of VS Code with Open-VSX extension marketplace support.",
            "version": "1.97.2",
            "available_versions": ["1.97.2"],
            "maintainer": "VSCodium Community",
            "license": "MIT",
            "homepage": "https://vscodium.com",
            "icon": "🟩",
            "backend": "flatpak",
            "package_ref": "com.vscodium.codium",
            "dependencies": ["flatpak"],
            "size_mb": 110,
            "compatibility": ["Fedora 41+", "Flatpak Sandboxed"],
            "check_binary": "codium",
            "install_args": ["flatpak", "install", "-y", "flathub", "com.vscodium.codium"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "com.vscodium.codium"]
        },
        {
            "id": "zed",
            "name": "Zed Editor",
            "category": "editors",
            "description": "High-performance, multiplayer code editor from the creators of Atom.",
            "long_description": "Written in Rust with GPU-accelerated rendering, built-in CRDT collaboration, and native language models.",
            "version": "0.174.0",
            "available_versions": ["0.174.0", "preview"],
            "maintainer": "Zed Industries",
            "license": "GPLv3 / Apache-2.0",
            "homepage": "https://zed.dev",
            "icon": "⚡",
            "backend": "flatpak",
            "package_ref": "dev.zed.Zed",
            "dependencies": ["vulkan-loader", "glibc"],
            "size_mb": 85,
            "compatibility": ["Fedora 41+", "x86_64", "Vulkan 1.2+"],
            "check_binary": "zed",
            "install_args": ["flatpak", "install", "-y", "flathub", "dev.zed.Zed"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "dev.zed.Zed"],
            "favorite": True
        },
        {
            "id": "neovim",
            "name": "Neovim",
            "category": "editors",
            "description": "Vim-fork focused on extensibility, Lua plugins, and modern LSP.",
            "long_description": "Hyperextensible Vim-based text editor built for high-speed terminal and GUI coding with treesitter syntax.",
            "version": "0.10.3",
            "available_versions": ["0.10.3", "0.9.5"],
            "maintainer": "Neovim Project",
            "license": "Apache-2.0 / Vim",
            "homepage": "https://neovim.io",
            "icon": "🟩",
            "backend": "dnf",
            "package_ref": "neovim",
            "dependencies": ["lua", "libvterm"],
            "size_mb": 25,
            "compatibility": ["Fedora 41+", "Terminal Native"],
            "check_binary": "nvim",
            "install_args": ["dnf", "install", "-y", "neovim"],
            "uninstall_args": ["dnf", "remove", "-y", "neovim"]
        },
        {
            "id": "intellij_idea_community",
            "name": "IntelliJ IDEA Community",
            "category": "editors",
            "description": "The leading IDE for Java and Kotlin development.",
            "long_description": "Intelligent coding assistance, smart refactorings, and built-in Gradle and Maven project support.",
            "version": "2024.3",
            "available_versions": ["2024.3", "2024.2"],
            "maintainer": "JetBrains",
            "license": "Apache-2.0",
            "homepage": "https://jetbrains.com/idea",
            "icon": "💎",
            "backend": "flatpak",
            "package_ref": "com.jetbrains.IntelliJ-IDEA-Community",
            "dependencies": ["java-devel>=17"],
            "size_mb": 850,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "idea",
            "install_args": ["flatpak", "install", "-y", "flathub", "com.jetbrains.IntelliJ-IDEA-Community"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "com.jetbrains.IntelliJ-IDEA-Community"]
        },

        # --- 3. Programming Languages ---
        {
            "id": "rust",
            "name": "Rust Toolchain (rustup)",
            "category": "languages",
            "description": "Empowering everyone to build reliable and efficient systems software.",
            "long_description": "Official Rust toolchain installer including rustc, cargo, clippy, and rustfmt with multi-target support.",
            "version": "1.85.0",
            "available_versions": ["stable", "beta", "nightly"],
            "maintainer": "The Rust Project",
            "license": "MIT / Apache-2.0",
            "homepage": "https://rust-lang.org",
            "icon": "🦀",
            "backend": "dnf",
            "package_ref": "rustup",
            "dependencies": ["gcc", "glibc-devel"],
            "size_mb": 180,
            "compatibility": ["Fedora 41+", "Multiplatform"],
            "check_binary": "cargo",
            "install_args": ["dnf", "install", "-y", "rustup", "cargo"],
            "uninstall_args": ["dnf", "remove", "-y", "rustup", "cargo"],
            "favorite": True
        },
        {
            "id": "python",
            "name": "Python 3.13 Runtime & Dev",
            "category": "languages",
            "description": "High-level programming language with clear syntax and massive ecosystem.",
            "long_description": "Standard Python runtime with pip, setuptools, wheels, and C extension compilation headers.",
            "version": "3.13.2",
            "available_versions": ["3.13", "3.12", "3.11"],
            "maintainer": "Python Software Foundation",
            "license": "PSF License",
            "homepage": "https://python.org",
            "icon": "🐍",
            "backend": "dnf",
            "package_ref": "python3-devel",
            "dependencies": ["glibc", "openssl"],
            "size_mb": 65,
            "compatibility": ["Fedora 41+", "System Standard"],
            "check_binary": "python3",
            "install_args": ["dnf", "install", "-y", "python3", "python3-devel", "python3-pip"],
            "uninstall_args": ["dnf", "remove", "-y", "python3-devel"]
        },
        {
            "id": "golang",
            "name": "Go (Golang)",
            "category": "languages",
            "description": "Open source programming language that makes it easy to build simple, fast software.",
            "long_description": "Go language compiler, standard library, and module tooling for cloud-native microservices.",
            "version": "1.24.0",
            "available_versions": ["1.24", "1.23"],
            "maintainer": "Google & Go Community",
            "license": "BSD-3-Clause",
            "homepage": "https://go.dev",
            "icon": "🐹",
            "backend": "dnf",
            "package_ref": "golang",
            "dependencies": ["glibc", "git"],
            "size_mb": 210,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "go",
            "install_args": ["dnf", "install", "-y", "golang"],
            "uninstall_args": ["dnf", "remove", "-y", "golang"]
        },
        {
            "id": "gcc_cpp",
            "name": "GCC & G++ (C/C++20)",
            "category": "languages",
            "description": "GNU Compiler Collection with full C++20 and C++23 standard support.",
            "long_description": "Essential C and C++ compilers, gdb debugger, make, and build-essential development headers.",
            "version": "14.2.1",
            "available_versions": ["14.2"],
            "maintainer": "GNU Project",
            "license": "GPLv3+",
            "homepage": "https://gcc.gnu.org",
            "icon": "⚙️",
            "backend": "dnf",
            "package_ref": "gcc-c++",
            "dependencies": ["glibc-devel", "binutils"],
            "size_mb": 95,
            "compatibility": ["Fedora 41+", "POSIX Native"],
            "check_binary": "g++",
            "install_args": ["dnf", "install", "-y", "gcc", "gcc-c++", "gdb", "make"],
            "uninstall_args": ["dnf", "remove", "-y", "gcc-c++"]
        },
        {
            "id": "openjdk",
            "name": "OpenJDK 21 LTS",
            "category": "languages",
            "description": "Production-ready open-source implementation of the Java SE Platform.",
            "long_description": "Long-Term Support Java Development Kit including javac, java runtime, and jlink.",
            "version": "21.0.6",
            "available_versions": ["21", "17", "11"],
            "maintainer": "OpenJDK Project / Red Hat",
            "license": "GPLv2 with Classpath Exception",
            "homepage": "https://openjdk.org",
            "icon": "☕",
            "backend": "dnf",
            "package_ref": "java-21-openjdk-devel",
            "dependencies": ["glibc"],
            "size_mb": 320,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "javac",
            "install_args": ["dnf", "install", "-y", "java-21-openjdk-devel"],
            "uninstall_args": ["dnf", "remove", "-y", "java-21-openjdk-devel"]
        },
        {
            "id": "dart",
            "name": "Dart SDK",
            "category": "languages",
            "description": "Client-optimized language for fast apps on any platform.",
            "long_description": "Dart compiler, package manager (pub), and runtime powering Flutter multiplatform development.",
            "version": "3.6.1",
            "available_versions": ["3.6.1"],
            "maintainer": "Google",
            "license": "BSD-3-Clause",
            "homepage": "https://dart.dev",
            "icon": "🎯",
            "backend": "dnf",
            "package_ref": "dart",
            "dependencies": ["glibc"],
            "size_mb": 110,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "dart",
            "install_args": ["dnf", "install", "-y", "dart"],
            "uninstall_args": ["dnf", "remove", "-y", "dart"]
        },

        # --- 4. Web Development ---
        {
            "id": "nodejs",
            "name": "Node.js (LTS)",
            "category": "web_dev",
            "description": "JavaScript runtime built on Chrome's V8 engine.",
            "long_description": "Industry-standard server-side JavaScript runtime with npm package manager.",
            "version": "22.14.0",
            "available_versions": ["22.x LTS", "20.x LTS"],
            "maintainer": "OpenJS Foundation",
            "license": "MIT",
            "homepage": "https://nodejs.org",
            "icon": "🟢",
            "backend": "dnf",
            "package_ref": "nodejs",
            "dependencies": ["glibc", "openssl"],
            "size_mb": 75,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "node",
            "install_args": ["dnf", "install", "-y", "nodejs", "npm"],
            "uninstall_args": ["dnf", "remove", "-y", "nodejs", "npm"],
            "favorite": True
        },
        {
            "id": "bun",
            "name": "Bun Runtime & Bundler",
            "category": "web_dev",
            "description": "Incredibly fast all-in-one JavaScript runtime, bundler, and package manager.",
            "long_description": "Drop-in replacement for Node.js built in Zig with ultra-fast startup and native TypeScript support.",
            "version": "1.2.2",
            "available_versions": ["1.2.2"],
            "maintainer": "Oven",
            "license": "MIT",
            "homepage": "https://bun.sh",
            "icon": "🍞",
            "backend": "vendor_pkg",
            "package_ref": "bun",
            "dependencies": ["glibc"],
            "size_mb": 48,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "bun",
            "install_args": ["sh", "-c", "curl -fsSL https://bun.sh/install | bash"],
            "uninstall_args": ["rm", "-rf", "~/.bun"],
            "favorite": True
        },

        # --- 5. Databases ---
        {
            "id": "postgresql",
            "name": "PostgreSQL Database Server",
            "category": "databases",
            "description": "The world's most advanced open source relational database.",
            "long_description": "Enterprise-class ACID database with JSONB, vector similarity extensions (pgvector), and high reliability.",
            "version": "17.2",
            "available_versions": ["17.2", "16.4"],
            "maintainer": "PostgreSQL Global Development Group",
            "license": "PostgreSQL License",
            "homepage": "https://postgresql.org",
            "icon": "🐘",
            "backend": "dnf",
            "package_ref": "postgresql-server",
            "dependencies": ["systemd", "glibc", "openssl"],
            "size_mb": 185,
            "compatibility": ["Fedora 41+", "POSIX Standard"],
            "check_binary": "psql",
            "install_args": ["dnf", "install", "-y", "postgresql-server", "postgresql-contrib"],
            "uninstall_args": ["dnf", "remove", "-y", "postgresql-server"]
        },
        {
            "id": "redis",
            "name": "Redis In-Memory Store",
            "category": "databases",
            "description": "In-memory data structure store used as a database, cache, and message broker.",
            "long_description": "Sub-millisecond latency key-value data store for sessions, pub/sub, queues, and fast caches.",
            "version": "7.4.2",
            "available_versions": ["7.4.2"],
            "maintainer": "Redis / Linux Foundation",
            "license": "RSALv2 / SSPL",
            "homepage": "https://redis.io",
            "icon": "🔴",
            "backend": "dnf",
            "package_ref": "redis",
            "dependencies": ["systemd", "glibc"],
            "size_mb": 35,
            "compatibility": ["Fedora 41+"],
            "check_binary": "redis-cli",
            "install_args": ["dnf", "install", "-y", "redis"],
            "uninstall_args": ["dnf", "remove", "-y", "redis"]
        },

        # --- 6. DevOps & Cloud ---
        {
            "id": "podman",
            "name": "Podman Rootless Containers",
            "category": "devops",
            "description": "Daemonless, rootless container engine for developing and running OCI containers.",
            "long_description": "Secure, rootless drop-in replacement for Docker with Kubernetes pod generation support.",
            "version": "5.3.1",
            "available_versions": ["5.3.1"],
            "maintainer": "Red Hat / Containers Org",
            "license": "Apache-2.0",
            "homepage": "https://podman.io",
            "icon": "🦭",
            "backend": "dnf",
            "package_ref": "podman",
            "dependencies": ["crun", "conmon", "shadow-utils"],
            "size_mb": 120,
            "compatibility": ["Fedora 41+", "Rootless Native"],
            "check_binary": "podman",
            "install_args": ["dnf", "install", "-y", "podman", "podman-compose"],
            "uninstall_args": ["dnf", "remove", "-y", "podman"],
            "favorite": True
        },
        {
            "id": "git",
            "name": "Git & GitHub CLI",
            "category": "devops",
            "description": "Fast distributed version control system and official GitHub command line.",
            "long_description": "Fundamental developer version control with branch management, rebase, and gh CLI automation.",
            "version": "2.48.1",
            "available_versions": ["2.48.1"],
            "maintainer": "Software Freedom Conservancy",
            "license": "GPLv2",
            "homepage": "https://git-scm.com",
            "icon": "🐙",
            "backend": "dnf",
            "package_ref": "git",
            "dependencies": ["glibc", "curl"],
            "size_mb": 45,
            "compatibility": ["Fedora 41+", "Universal"],
            "check_binary": "git",
            "install_args": ["dnf", "install", "-y", "git", "gh"],
            "uninstall_args": ["dnf", "remove", "-y", "gh"],
            "favorite": True
        },
        {
            "id": "kubernetes_kubectl",
            "name": "Kubernetes CLI (kubectl)",
            "category": "cloud",
            "description": "Control plane CLI tool for managing Kubernetes clusters.",
            "long_description": "Deploy, inspect, and manage container workloads across local Minikube/Kind and cloud clusters.",
            "version": "1.32.2",
            "available_versions": ["1.32", "1.31"],
            "maintainer": "Cloud Native Computing Foundation (CNCF)",
            "license": "Apache-2.0",
            "homepage": "https://kubernetes.io",
            "icon": "☸️",
            "backend": "dnf",
            "package_ref": "kubernetes-client",
            "dependencies": ["glibc"],
            "size_mb": 60,
            "compatibility": ["Fedora 41+"],
            "check_binary": "kubectl",
            "install_args": ["dnf", "install", "-y", "kubernetes-client"],
            "uninstall_args": ["dnf", "remove", "-y", "kubernetes-client"]
        },

        # --- 7. Cybersecurity ---
        {
            "id": "wireshark",
            "name": "Wireshark Network Analyzer",
            "category": "security",
            "description": "The world's foremost and widely-used network protocol analyzer.",
            "long_description": "Deep packet inspection, live network traffic capture, TLS decryption, and hundreds of protocol decoders.",
            "version": "4.4.3",
            "available_versions": ["4.4.3"],
            "maintainer": "Wireshark Foundation",
            "license": "GPLv2+",
            "homepage": "https://wireshark.org",
            "icon": "🦈",
            "backend": "dnf",
            "package_ref": "wireshark",
            "dependencies": ["qt6-qtbase", "libpcap"],
            "size_mb": 110,
            "compatibility": ["Fedora 41+", "Wayland / X11"],
            "check_binary": "wireshark",
            "install_args": ["dnf", "install", "-y", "wireshark"],
            "uninstall_args": ["dnf", "remove", "-y", "wireshark"],
            "favorite": True
        },
        {
            "id": "nmap",
            "name": "Nmap Network Scanner",
            "category": "security",
            "description": "Network discovery and vulnerability auditing scanner.",
            "long_description": "Port scanning, OS fingerprinting, NSE scripting engine, and service version detection.",
            "version": "7.95",
            "available_versions": ["7.95"],
            "maintainer": "Gordon Lyon / Nmap Project",
            "license": "Nmap Public Source License",
            "homepage": "https://nmap.org",
            "icon": "🔍",
            "backend": "dnf",
            "package_ref": "nmap",
            "dependencies": ["libpcap", "openssl"],
            "size_mb": 35,
            "compatibility": ["Fedora 41+"],
            "check_binary": "nmap",
            "install_args": ["dnf", "install", "-y", "nmap"],
            "uninstall_args": ["dnf", "remove", "-y", "nmap"]
        },
        {
            "id": "ghidra",
            "name": "Ghidra Software Reverse Engineering",
            "category": "security",
            "description": "Software reverse engineering (SRE) suite developed by the NSA.",
            "long_description": "Includes disassembly, assembly, decompilation, graphing, and scripting for binary vulnerability analysis.",
            "version": "11.3",
            "available_versions": ["11.3"],
            "maintainer": "National Security Agency",
            "license": "Apache-2.0",
            "homepage": "https://ghidra-sre.org",
            "icon": "🐉",
            "backend": "flatpak",
            "package_ref": "org.ghidra_sre.Ghidra",
            "dependencies": ["java-21-openjdk"],
            "size_mb": 420,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "ghidra",
            "install_args": ["flatpak", "install", "-y", "flathub", "org.ghidra_sre.Ghidra"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "org.ghidra_sre.Ghidra"]
        },

        # --- 8. Robotics & Embedded ---
        {
            "id": "ros2_desktop",
            "name": "ROS 2 Jazzy Jalisco",
            "category": "robotics",
            "description": "Robot Operating System 2 core libraries, RViz, and communications.",
            "long_description": "Modern robotics middleware with DDS networking, real-time control, hardware abstractions, and simulation.",
            "version": "Jazzy",
            "available_versions": ["Jazzy Jalisco", "Iron Irwini"],
            "maintainer": "Open Robotics",
            "license": "Apache-2.0",
            "homepage": "https://ros.org",
            "icon": "🤖",
            "backend": "container",
            "package_ref": "docker.io/osrf/ros:jazzy-desktop",
            "dependencies": ["podman"],
            "size_mb": 1400,
            "compatibility": ["Containerized OCI", "Rootless Podman"],
            "check_binary": "ros2",
            "install_args": ["podman", "pull", "docker.io/osrf/ros:jazzy-desktop"],
            "uninstall_args": ["podman", "rmi", "docker.io/osrf/ros:jazzy-desktop"],
            "favorite": True
        },
        {
            "id": "arduino_ide",
            "name": "Arduino IDE 2.x",
            "category": "embedded",
            "description": "Open-source electronics prototyping platform and embedded IDE.",
            "long_description": "Modern Arduino 2.x IDE with code completion, visual debugger, and board/library managers for AVR and ARM.",
            "version": "2.3.4",
            "available_versions": ["2.3.4"],
            "maintainer": "Arduino LLC",
            "license": "AGPLv3",
            "homepage": "https://arduino.cc",
            "icon": "♾️",
            "backend": "flatpak",
            "package_ref": "cc.arduino.IDE2",
            "dependencies": ["flatpak"],
            "size_mb": 220,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "arduino-ide",
            "install_args": ["flatpak", "install", "-y", "flathub", "cc.arduino.IDE2"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "cc.arduino.IDE2"]
        },
        {
            "id": "platformio",
            "name": "PlatformIO Core (CLI)",
            "category": "embedded",
            "description": "Next generation ecosystem for embedded IoT development.",
            "long_description": "Cross-platform code builder, library manager, and multi-framework IDE for ESP32, STM32, and RP2040.",
            "version": "6.1.16",
            "available_versions": ["6.1.16"],
            "maintainer": "PlatformIO Community",
            "license": "Apache-2.0",
            "homepage": "https://platformio.org",
            "icon": "🛸",
            "backend": "mise",
            "package_ref": "platformio",
            "dependencies": ["python3>=3.8"],
            "size_mb": 40,
            "compatibility": ["Fedora 41+"],
            "check_binary": "pio",
            "install_args": ["pip", "install", "-U", "platformio"],
            "uninstall_args": ["pip", "uninstall", "-y", "platformio"]
        },

        # --- 9. Mobile Development ---
        {
            "id": "android_studio",
            "name": "Android Studio Ladybug",
            "category": "mobile_dev",
            "description": "The official IDE for Android application development.",
            "long_description": "Includes Android SDK, Jetpack Compose visual preview, virtual device emulator (AVD), and Kotlin profilers.",
            "version": "2024.2.1",
            "available_versions": ["2024.2.1"],
            "maintainer": "Google Android Open Source Project",
            "license": "Apache-2.0 / Proprietary SDK",
            "homepage": "https://developer.android.com/studio",
            "icon": "🤖",
            "backend": "flatpak",
            "package_ref": "com.google.AndroidStudio",
            "dependencies": ["flatpak", "kvm"],
            "size_mb": 1100,
            "compatibility": ["Fedora 41+", "KVM Virtualization"],
            "check_binary": "android-studio",
            "install_args": ["flatpak", "install", "-y", "flathub", "com.google.AndroidStudio"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "com.google.AndroidStudio"],
            "favorite": True
        },
        {
            "id": "flutter_sdk",
            "name": "Flutter SDK",
            "category": "mobile_dev",
            "description": "Multiplatform UI toolkit for building natively compiled applications.",
            "long_description": "Build mobile, web, desktop, and embedded apps from a single Dart codebase with hot reload.",
            "version": "3.29.0",
            "available_versions": ["3.29.0", "3.27.0"],
            "maintainer": "Google",
            "license": "BSD-3-Clause",
            "homepage": "https://flutter.dev",
            "icon": "💙",
            "backend": "mise",
            "package_ref": "flutter",
            "dependencies": ["git", "curl", "glibc"],
            "size_mb": 750,
            "compatibility": ["Fedora 41+", "x86_64"],
            "check_binary": "flutter",
            "install_args": ["dnf", "install", "-y", "flutter"],
            "uninstall_args": ["dnf", "remove", "-y", "flutter"]
        },

        # --- 10. Game Development & Design ---
        {
            "id": "godot",
            "name": "Godot Engine 4",
            "category": "gamedev",
            "description": "Innovative 2D and 3D cross-platform game engine.",
            "long_description": "Feature-rich, multi-platform 2D and 3D game engine with dedicated IDE, GDScript, C#, and Vulkan renderer.",
            "version": "4.3.0",
            "available_versions": ["4.3.0", "4.2.2"],
            "maintainer": "Godot Foundation",
            "license": "MIT",
            "homepage": "https://godotengine.org",
            "icon": "🤖",
            "backend": "flatpak",
            "package_ref": "org.godotengine.Godot",
            "dependencies": ["vulkan-loader"],
            "size_mb": 115,
            "compatibility": ["Fedora 41+", "Wayland / Vulkan"],
            "check_binary": "godot",
            "install_args": ["flatpak", "install", "-y", "flathub", "org.godotengine.Godot"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "org.godotengine.Godot"],
            "favorite": True
        },
        {
            "id": "blender",
            "name": "Blender 3D Suite",
            "category": "design",
            "description": "Free and open source 3D creation suite.",
            "long_description": "Supports 3D modeling, rigging, animation, simulation, rendering, compositing, motion tracking, and video editing.",
            "version": "4.3.2",
            "available_versions": ["4.3.2"],
            "maintainer": "Blender Foundation",
            "license": "GPLv3",
            "homepage": "https://blender.org",
            "icon": "🎨",
            "backend": "flatpak",
            "package_ref": "org.blender.Blender",
            "dependencies": ["vulkan-loader", "glibc"],
            "size_mb": 450,
            "compatibility": ["Fedora 41+", "Hardware Accelerated"],
            "check_binary": "blender",
            "install_args": ["flatpak", "install", "-y", "flathub", "org.blender.Blender"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "org.blender.Blender"],
            "favorite": True
        },
        {
            "id": "dbeaver",
            "name": "DBeaver Community Universal Database Manager",
            "category": "productivity",
            "description": "Free universal database tool for developers and database administrators.",
            "long_description": "Multiplatform database manager supporting PostgreSQL, MySQL, SQLite, Oracle, Redis, and DuckDB.",
            "version": "24.3.5",
            "available_versions": ["24.3.5"],
            "maintainer": "DBeaver Corp",
            "license": "Apache-2.0",
            "homepage": "https://dbeaver.io",
            "icon": "🦫",
            "backend": "flatpak",
            "package_ref": "io.dbeaver.DBeaverCommunity",
            "dependencies": ["java-17-openjdk"],
            "size_mb": 140,
            "compatibility": ["Fedora 41+"],
            "check_binary": "dbeaver",
            "install_args": ["flatpak", "install", "-y", "flathub", "io.dbeaver.DBeaverCommunity"],
            "uninstall_args": ["flatpak", "uninstall", "-y", "io.dbeaver.DBeaverCommunity"]
        }
    ]

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.path.expanduser(os.path.join("~", ".config", "nexus", "software_center"))
        os.makedirs(self.config_dir, exist_ok=True)
        self.favorites_file = os.path.join(self.config_dir, "favorites.json")
        self._favorites = self._load_favorites()
        self._packages: Dict[str, SoftwarePackage] = {}
        self._load_packages()

    def _load_favorites(self) -> set:
        if os.path.isfile(self.favorites_file):
            try:
                with open(self.favorites_file, "r") as f:
                    return set(json.load(f))
            except Exception:
                pass
        return set()

    def save_favorites(self):
        try:
            with open(self.favorites_file, "w") as f:
                json.dump(list(self._favorites), f)
        except Exception:
            pass

    def _load_packages(self):
        self._packages = {}
        for raw in self.DEFAULT_PACKAGES:
            pkg = SoftwarePackage(**raw)
            if pkg.id in self._favorites:
                pkg.favorite = True

            # Check if installed on system
            if pkg.check_binary:
                installed_path = shutil.which(pkg.check_binary)
                if installed_path:
                    pkg.installed = True
                    pkg.installed_version = pkg.version
            self._packages[pkg.id] = pkg

    def get_categories(self) -> List[Dict[str, Any]]:
        return CATEGORIES

    def get_package(self, package_id: str) -> Optional[SoftwarePackage]:
        return self._packages.get(package_id)

    def search_packages(
        self,
        query: str = "",
        category: str = "all",
        filter_installed: bool = False,
        filter_favorites: bool = False
    ) -> List[Dict[str, Any]]:
        """Filter and search packages across the catalog."""
        results = []
        q = query.strip().lower()

        for pkg in self._packages.values():
            if filter_installed and not pkg.installed:
                continue
            if filter_favorites and not pkg.favorite:
                continue
            if category != "all" and pkg.category != category:
                continue
            if q:
                searchable = f"{pkg.name} {pkg.id} {pkg.description} {pkg.category} {pkg.maintainer}".lower()
                if q not in searchable:
                    continue
            results.append(pkg.to_dict())

        return results

    def toggle_favorite(self, package_id: str) -> bool:
        """Toggle favorite state for a package."""
        pkg = self._packages.get(package_id)
        if not pkg:
            return False

        if package_id in self._favorites:
            self._favorites.remove(package_id)
            pkg.favorite = False
        else:
            self._favorites.add(package_id)
            pkg.favorite = True

        self.save_favorites()
        return pkg.favorite
