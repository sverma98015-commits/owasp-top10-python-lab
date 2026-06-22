#  OWASP Top 10 Vulnerability Lab & Secure Code Patches

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Security](https://img.shields.io/badge/Cybersecurity-OWASP%20Top%2010-red)


A containerized web security lab built with **Python (Flask)** and **Docker** to demonstrate real-world web application vulnerabilities from the OWASP Top 10 and their corresponding secure code remediations.

This project focuses on understanding how vulnerabilities occur, reproducing attacks in a controlled environment, and implementing industry-standard defensive fixes.

![Docker Running](screenshots/5.JPG)
---


##  Learning Objectives

* Understand common OWASP Top 10 vulnerabilities
* Practice manual exploitation techniques
* Analyze vulnerable backend code
* Implement secure coding practices
* Learn defensive remediation strategies
* Work with Dockerized security environments

---

##  Architecture

```text
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Requests
       ▼
┌─────────────┐
│ Flask App   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ SQLite DB   │
└─────────────┘
```

The application runs entirely inside Docker containers to ensure isolation and safe experimentation.

---

##  Quick Start

### Prerequisites

* Docker
* Docker Compose
* Git

### Installation

```bash
git clone https://github.com/sverma98015-commits/owasp-top10-python-lab.git

cd owasp-top10-python-lab

docker-compose up --build
```

### Access the Application

```text
http://localhost:5000
```

---

# Vulnerability Matrix

| Vulnerability | OWASP Category                 | Severity | Status |
| ------------- | ------------------------------ | -------- | ------ |
| SQL Injection | A03:2021 Injection             | Critical | ✅      |
| Reflected XSS | A03:2021 Injection             | High     | ✅      |
| IDOR          | A01:2021 Broken Access Control | High     | ✅      |

---

#  SQL Injection (SQLi)

### OWASP Category

A03:2021 – Injection

### Severity

 Critical (CVSS 8.5)

### Attack Scenario

The login endpoint directly concatenates user-controlled input into a SQL query.

### Exploit Payload

```sql
' OR '1'='1
```

### Result

Authentication bypass occurs because the resulting SQL statement evaluates as TRUE.


---

## Vulnerable Code

```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
```

## Secure Patch

```python
query = "SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, password))
```

### Security Impact

Parameterized queries eliminate SQL injection by separating executable SQL from user-supplied data.

---

# 2️⃣ Reflected Cross-Site Scripting (XSS)

### OWASP Category

A03:2021 – Injection

### Severity

🟠 High (CVSS 6.1)

### Attack Scenario

User-controlled input is reflected directly into HTML output.

### Exploit Payload

```html
<script>alert('XSS')</script>
```

### Result

The browser executes arbitrary JavaScript within the application's origin.


---

## Vulnerable Code

```python
html_template = f"<h3>{search_query}</h3>"
return render_template_string(html_template)
```

## Secure Patch

```python
return render_template(
    "search_results.html",
    query=search_query
)
```

### Security Impact

Flask/Jinja2 automatically escapes dangerous HTML characters, preventing script execution.

---

# 3️⃣ Insecure Direct Object Reference (IDOR)

### OWASP Category

A01:2021 – Broken Access Control

### Severity

🔴 High (CVSS 7.5)

### Attack Scenario

Users can modify URL parameters to access records belonging to other users.

### Example

```text
/profile?id=2
```

Changed to:

```text
/profile?id=3
```

### Result

Unauthorized access to another user's private information.



## Vulnerable Code

```python
user_id = request.args.get('id')
```

## Secure Patch

```python
user_id = session['logged_in_user_id']
```

### Security Impact

Authorization decisions are enforced server-side rather than trusting user-controlled parameters.

---

# Skills Demonstrated

* OWASP Top 10
* Secure Coding
* Web Application Security
* Flask Security
* SQL Injection Testing
* XSS Testing
* Access Control Validation
* Docker
* Python
* Vulnerability Analysis

---

#  Security Principles Applied

* Parameterized Queries
* Output Encoding
* Input Validation
* Principle of Least Privilege
* Server-Side Authorization
* Secure Session Management

---

# 📁 Repository Structure

```text
owasp-top10-python-lab/
│
├── app/
│   ├── templates/
│   ├── static/
│   ├── app.py
│   └── database.db
│
├── screenshots/
│   ├── dashboard.png
│   ├── sqli-demo.png
│   ├── xss-demo.png
│   └── idor-demo.png
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

##  Ankit Kumar

Cybersecurity enthusiast focused on:

* Web Application Security
* Penetration Testing
* Secure Code Review
* Vulnerability Research
* Defensive Security Engineering

---

⭐ If you found this project useful, consider giving it a star.
