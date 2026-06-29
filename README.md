# Flask App Integration with AWS RDS (MySQL)

This repository contains a **Flask** web application designed to manage and search records within a relational database. The primary objective of this project is to demonstrate the migration of a local, monolithic application (originally using SQLite) toward a decoupled, secure, and production-ready Cloud architecture on **AWS**. The system leverages an **EC2** instance for back-end logic and an **RDS (MySQL)** instance for data persistence.

## 🏗️ System Architecture

The infrastructure follows the Cloud best practice of **decoupling** application layers:

* **Front-end / Client:** A web interface accessible via browser using the HTTP protocol on port `8080`.
* **Compute Layer (EC2):** A Linux instance on AWS hosting the Flask application, responsible for routing and business logic.
* **Database Layer (RDS MySQL):** A managed relational database instance, isolated at the network level, accepting secure traffic on the standard MySQL port `3306`.

---

## 🛠️ Step-by-Step Implementation & Troubleshooting

### 1. Decoupling & Credential Security
To prevent sensitive information (like master passwords) from leaking into public source control, environment variable management was implemented:
* Installed the `python-dotenv` package on the EC2 instance.
* Configured a local, hidden `.env` file containing the RDS endpoint and master credentials.
* Created a `.gitignore` file to systematically exclude the `.env` file from Git tracking.

### 2. Database Refactoring (From SQLite to Raw SQL on RDS)
The original application was configured to write to a local file. The codebase was refactored to support the MySQL dialect via the `pymysql` driver:
* Updated the database connection string to `mysql+pymysql://`.
* Implemented explicit schema initialization logic directly within the application context (`CREATE TABLE IF NOT EXISTS`) to resolve the absence of native ORM models in the script.
* Added automated, controlled data seeding with sample records (`dora`, `cansın`, `sencer`, etc.) executed only when the RDS instance is empty.

### 3. Component Realignment (Resolving HTTP 400 Bad Request)
Conducted deep-dive debugging into the HTML form payload:
* Fixed an HTTP 400 (*Bad Request*) error by mapping the Flask POST request parser to the exact `name="user_keyword"` attribute defined in the provided front-end `emails.html` template.

### 4. Network Connection Certification
Verified correct routing within the AWS VPC. Socket analysis on the EC2 server using network utilities (`ss` / `netstat`) certified an active, stable connection pipeline:
```text
ESTABLISHED: EC2_Private_IP ---> RDS_Private_IP:3306 (MySQL)
