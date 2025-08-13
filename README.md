# Kaikai Technical Test: Data & DevOps Engineer Junior 🚀

## Description
This repository contains my solution for the Kaikai Technical Test for the Ingénieur Data & DevOps Junior position. It demonstrates skills in Python data analysis, DevOps automation (Docker, CI/CD, Ansible), and SQL database management using real IoT air quality sensor data from `capteur_temp.csv` (~319,110 lines). The project processes sensor data for PM2.5 pollution insights, containerizes the application, sets up CI/CD pipelines, and creates a SQLite database with queries.
Key outputs include data visualizations (e.g., PM2.5 evolution over 24h), Docker images, and SQL scripts. All code is tested locally on Windows WSL2 with Docker and Prometheus running.

## Fonctionnalités principales
- **Part A (Python/Data)**: Load/clean large CSV, temporal analysis (daily averages, pollution peaks), correlations, dashboard visuals, reusable processing function.
- **Part B (DevOps)**: Dockerfile for containerization, Docker Compose for orchestration, GitLab CI pipeline (tests/build/deploy/notify), Ansible playbook for deployment/cron, Prometheus monitoring with alerts.
- **Part C (SQL)**: SQLite tables for sensors/measurements, data insertions from CSV, queries (simple, aggregate, temporal, CTE for problem sensors).
- Outputs: Plots (`evolution_24h.png`, `dashboard.png`, `correlations.png`), console logs for results.

## Technologies utilisées
- Python 3.12 (pandas, matplotlib, seaborn for data; prometheus_client for metrics)
- Docker & Docker Compose
- GitLab CI/CD
- Ansible
- Prometheus (for monitoring)
- SQLite (via SQLiteOnline or local tool)
- pytest for unit tests

## Installation 💻
### Prérequis
- Python 3.12 or higher
- pip (Python package manager)
- Docker Desktop (with WSL2 on Windows)
- Ansible (install via `pip install ansible`)
- Git

### Étapes d'installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/kaikai-technical-test.git
   cd kaikai-technical-test
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place the dataset:
   - Copy `capteur_temp.csv` to the `data/` folder (not included in repo due to size; use your provided file).

## Exécution du projet
1. **Run Python Analysis (Part A)**:
   ```bash
   python analyze_sensor_data.py
   ```
   - Outputs: Console results (averages, correlations, insights), plots saved as `evolution_24h.png`, `correlations.png`, and `dashboard.png`.

2. **Build and Run Docker Containers (Part B)**:
   - Build the Docker image:
     ```bash
     docker build -t technical-test-sensor-analysis:latest .
     ```
   - Start services with Docker Compose:
     ```bash
     docker-compose up -d
     ```
   - Access the container:
     ```bash
     docker exec -it sensor-analysis bash
     ```
   - Verify running containers:
     ```bash
     docker ps
     ```

3. **Run Prometheus Monitoring (Part B)**:
   ```bash
   docker run -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
   ```
   - View metrics at http://localhost:9090 (ensure `analyze_sensor_data.py` exposes metrics on port 8000).
   - Note: Update `prometheus.yml` to scrape your app if needed.

4. **Run Ansible Playbook (Local Simulation, Part B)**:
   ```bash
   ansible-playbook deploy.yml --extra-vars "ansible_connection=local"
   ```
   - Deploys the `sensor-analysis` container and sets a cron job for daily execution at 2:00 AM.

5. **Run SQL Script (Part C)**:
   - Open `scripts.sql` in SQLiteOnline (https://sqliteonline.com/).
   - Execute sections sequentially: Create tables, insert data, run queries.

6. **CI/CD Pipeline**:
   - Push to GitLab repo.
   - Pipeline runs automatically (tests via pytest, build/push Docker, deploy sim, Slack notify).

## Structure du projet
```
kaikai-technical-test/
├── data/                  # Dataset folder (add capteur_temp.csv here)
│   └── capteur_temp.csv   # Large sensor data file (not committed)
├── __pycache__/           # Python cache (ignore)
├── analyze_sensor_data.py # Main Python script for data processing
├── correlations.png       # Correlation heatmap visualization
├── dashboard.png          # 4-key visualizations dashboard
├── deploy.yml             # Ansible playbook for deployment
├── docker-compose.yml     # Docker orchestration
├── Dockerfile             # Container build file
├── evolution_24h.png      # PM2.5 evolution plot
├── .gitlab-ci.yml         # CI/CD pipeline config
├── prometheus.yml         # Prometheus config for monitoring
├── requirements.txt       # Python dependencies
├── scripts.sql            # SQL creation, inserts, queries
├── test_analyze.py        # Unit tests for Python functions
└── README.md              # This file
```

## Tests
Run unit tests:
```bash
pytest test_analyze.py
```

## Contributeurs
- Asse Badiane: Développeur principal (all parts implemented).

## Contribution
Fork the repo, create a branch, commit changes, and open a PR if needed.

## Licence
This project is for Kaikai technical evaluation and is unlicensed for public use.

---
Ready to showcase data-driven air quality insights with DevOps automation! 🌟.
