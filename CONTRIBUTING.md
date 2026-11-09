# Contributing to LangVoi Voice Studio Pro

Thank you for your interest in contributing to **LangVoi Voice Studio Pro**! We welcome community contributions, bug reports, and enhancements from developers around the world.

---

## 🛠️ Code of Conduct & Development Philosophy

LangVoi is built as an enterprise-grade, clean, human-written native desktop audio workstation. When contributing:
- Maintain clean, self-documenting code with comprehensive docstrings and type annotations.
- Respect acoustic physics and digital signal processing standards.
- Keep UI responsive and threaded (avoid blocking the Tkinter event loop).
- Ensure memory efficiency (use in-memory streams and NumPy vectorization).

---

## 🚀 Getting Started

### 1. Fork & Clone Repository
```bash
git clone https://github.com/PrinceSanchela/LangVoi.git
cd LangVoi
```

### 2. Set Up a Python Virtual Environment
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements-dev.txt
```

### 4. Run the Test Suite
```bash
python -m unittest discover -s tests
```

---

## 🧪 Development Workflow

1. **Branching**: Create a feature branch with a descriptive name:
   ```bash
   git checkout -b feature/audio-dsp-optimization
   # or
   git checkout -b fix/sample-rate-resampling
   ```

2. **Code Standards**:
   - Follow PEP 8 style guidelines.
   - Run linter checks:
     ```bash
     flake8 app core tests
     ```

3. **Running the Application**:
   ```bash
   python run.py
   ```

4. **Testing**: Add unit tests in `tests/` for any new logic:
   ```bash
   pytest tests/
   ```

5. **Submitting a Pull Request**:
   - Push your branch to GitHub.
   - Open a Pull Request against `main`.
   - Describe what changed and provide verification steps.

---

## 📜 Authorship & Licensing

By contributing to this repository, you agree that your contributions will be licensed under the project's license terms.
For questions, architectural discussions, or commercial partnerships, reach out to Lead Architect **Prince Sanchela** (`contact.princesanchela@gmail.com`).
