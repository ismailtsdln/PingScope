# PingScope - Modern Network Diagnostic Tool 🚀

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)

PingScope is a modern, feature-rich, and visually enhanced version of the classic ping tool. It allows you to perform advanced network diagnostics via both a professional CLI and a sleek web dashboard.

## ✨ Features

- **Modern CLI**: Colorized output, panels, and live tables using the `rich` library.
- **Advanced Metrics**: Real-time calculation of RTT (Min/Max/Avg), Jitter, and Packet Loss.
- **Multi-Host & Subnet Sweep**: Support for concurrent pinging of multiple targets and full subnet scanning (e.g., `/24`).
- **Traceroute**: Integrated cross-platform route tracing functionality.
- **History Tracking**: Automatically saves all test results to a local SQLite database.
- **Visualization**: Generates latency graphs using `matplotlib` and saves them as PNG.
- **Export Capabilities**: Save your results in JSON, CSV, or TXT formats.
- **Web Dashboard**: A modern, real-time web interface powered by Flask and Socket.IO.
- **Configuration Support**: Customizable default settings via `config.yaml`.
- **Dockerized**: Ready to be deployed as a container.

## 🛠 Installation

### Prerequisites

- Python 3.6 or higher
- Pip (Python package manager)

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/ismailtsdln/PingScope.git
cd PyPing
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Install the application in editable mode:

```bash
pip install -e .
```

## 🚀 Usage

### Command Line Interface (CLI)

**Basic Ping:**

```bash
pyping google.com
```

**Multi-Host Scanning:**

```bash
pyping -m google.com github.com 8.8.8.8
```

**Subnet Sweep:**

```bash
pyping -S 192.168.1.0/24 --threads 20
```

**Traceroute:**

```bash
pyping google.com -T
```

**View history:**

```bash
pyping -H
```

**Generate Latency Graph:**

```bash
pyping google.com -g -o latency_report.png
```

### Web Dashboard

To start the real-time web dashboard:

```bash
python3 web/app.py
```

Then visit `http://localhost:5000` in your web browser.

## 📁 Project Structure

- `source/`: Core logic and helper modules.
- `web/`: Flask-based web interface (Template/Static files).
- `tests/`: Unit and integration tests.
- `config.yaml`: Application configuration settings.
- `Dockerfile` & `docker-compose.yml`: Containerization setup.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🤝 Contributing

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---
Developed by **İsmail Taşdelen** - [LinkedIn](https://www.linkedin.com/in/ismailtasdelen)
