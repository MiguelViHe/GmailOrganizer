---

# Gmail Organizer

A modular **rule-based email automation pipeline** built with **Python and the Gmail API**.

This project implements an automated system that retrieves emails from Gmail, extracts relevant metadata, evaluates configurable classification rules, and applies actions such as labeling or marking emails as read.

It was developed as a hands-on project to explore **API integration, automation pipelines, rule engines, and maintainable backend architecture**.

---

# Overview

Email inboxes often accumulate large volumes of messages that require repetitive manual management. While Gmail offers search and filtering capabilities, building a programmable automation system allows more advanced workflows.

This project demonstrates how to build a lightweight **data processing pipeline for email automation**, integrating:

* Gmail API
* rule-based classification
* automated label management
* batch operations for efficiency
* modular Python architecture

---

# Architecture

The system follows a **pipeline-based architecture** separating data retrieval, rule evaluation, and action execution.

```
          Gmail API
              │
              ▼
     Email Retrieval Layer
              │
              ▼
       Metadata Extraction
              │
              ▼
        Rule Evaluation
              │
              ▼
        Action Executor
              │
              ▼
        Gmail Update
      (labels / read state)
```

Each component has a clearly defined responsibility, allowing the system to remain **extensible and maintainable**.

---

# Project Structure

```
gmail-organizer
│
├── src
│   │
│   ├── main.py
│   ├── auth.py
│   ├── gmail_service.py
│   ├── rules.py
│   ├── utils.py
│   │
│   ├── organizer
│   │   ├── classifier.py
│   │   ├── rule_engine.py
│   │   └── actions.py
│   │
│   └── jobs
│       ├── job_classify_recent.py
│       └── job_mark_old_as_read.py
│
├── credentials
├── requirements.txt
├── .env
└── README.md
```

---

# Pipeline Components

## Authentication

**auth.py**

Handles OAuth2 authentication with Gmail and manages token persistence.

Responsibilities:

* initiate OAuth flow
* store access tokens
* refresh tokens automatically when expired

---

## Gmail Service

**gmail_service.py**

Creates the Gmail API client used by the application.

This abstraction isolates Gmail API initialization from business logic.

---

## Classifier

**organizer/classifier.py**

Central orchestration module that coordinates the classification process.

Workflow:

1. extract email metadata
2. evaluate classification rules
3. apply corresponding actions

---

## Rule Engine

**organizer/rule_engine.py**

Evaluates classification rules based on email attributes.

Rules may evaluate conditions such as:

* sender
* subject
* keywords
* existing labels

The rule engine is designed to remain independent from Gmail-specific logic.

---

## Actions

**organizer/actions.py**

Executes Gmail operations triggered by rule evaluation.

Supported actions include:

* adding labels
* removing labels
* marking messages as read

Batch operations are used when possible to reduce API calls.

---

# Jobs

The system executes tasks through **jobs**, allowing different automation workflows.

---

## Classify Recent Emails

**job_classify_recent.py**

Retrieves recent emails and classifies them using the rule engine.

Pipeline:

```
Fetch recent messages
        │
        ▼
Extract metadata
        │
        ▼
Evaluate rules
        │
        ▼
Apply Gmail actions
        │
        ▼
Log results
```

---

## Mark Old Emails as Read

**job_mark_old_as_read.py**

Marks older processed promotional emails as read.

Key characteristics:

* configurable query via environment variables
* efficient batch update using Gmail API
* designed for scheduled execution

---

# Environment Configuration

Example `.env` file:

```
CREDENTIALS_PATH=credentials/credentials.json
TOKEN_PATH=credentials/token.json

CLASSIFY_QUERY=newer_than:1d -label:Processed

OLD_EMAIL_READ=older_than:30d label:Processed label:Promos is:unread
```

This allows the system to adapt its behaviour without modifying the code.

---

# Installation

Clone the repository:

```
git clone https://github.com/MiguelViHe/GmailOrganizer.git
cd GmailOrganizer
```

Create a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Usage

Run the classification job:

```
python src/main.py --job classify_recent
```

Run the cleanup job:

```
python src/main.py --job mark_old_as_read
```

---

# Example Log Output

```
2026-02-27 09:00:04 - jobs.job_classify_recent - INFO - Processed msg_id=19c9a5086ce81510: Weekly offers from Store
2026-02-27 09:00:04 - jobs.job_classify_recent - INFO - Processed msg_id=19c9a54359f332fa: New promotion available
2026-03-03 09:55:26 - root - WARNING - Invalid refresh token. New login required.
```

Logging helps track system activity and debug potential issues.

---

## Scalability and Design Considerations

Although this project was initially designed as a lightweight personal automation tool, several architectural decisions were made to keep the system maintainable and extensible as the number of processed emails or automation rules grows.

### Modular Pipeline Architecture

The system separates responsibilities into independent components:

* **Email retrieval**
* **Metadata extraction**
* **Rule evaluation**
* **Action execution**

This modular approach allows new processing steps to be added without modifying the entire pipeline. For example, introducing additional classification strategies or analytics layers would only require extending the relevant module.

---

### Job-based Processing

Automation tasks are implemented as independent **jobs**, such as:

* `classify_recent`
* `mark_old_as_read`

This design allows the system to run different workflows depending on the context and makes it easy to integrate external schedulers such as:

* **cron**
* **workflow orchestrators**
* **background task runners**

Each job encapsulates a specific automation task, improving clarity and maintainability.

---

### Configurable Behaviour via Environment Variables

Query filters and execution parameters are defined through environment variables rather than hardcoded values.

Examples include:

* `CLASSIFY_QUERY`
* `OLD_EMAIL_READ`
* `CREDENTIALS_PATH`
* `TOKEN_PATH`

Benefits:

* Enables flexible behavior across different environments without modifying the source code.
* Keeps sensitive information such as API tokens and credentials out of the repository.
* Simplifies deployment and scaling while maintaining security best practices.

---

### Efficient Gmail API Usage

The system minimizes API calls by:

* retrieving only the necessary message metadata
* using **batch operations** when updating multiple emails

For example, the cleanup job uses `batchModify` to mark many messages as read in a single request, reducing API overhead and improving performance.

---

### Extensible Rule Engine

The rule engine is designed to be easily extendable. New classification rules can be introduced without modifying the email retrieval or action layers.

Future extensions could include:

* rule prioritization
* rule indexing for faster evaluation
* configuration-driven rules (e.g. JSON or YAML)
* machine learning based classification

---

# Technologies Used

* Python
* Gmail API
* OAuth2 authentication
* environment-based configuration
* structured logging
* modular backend design

---

# Learning Objectives

This project explores practical topics frequently encountered in backend and data engineering:

* API integration
* authentication flows
* rule-based automation systems
* modular Python project structure
* automation pipelines interacting with external services

---

# Possible Future Improvements

Potential extensions include:

* machine learning based email classification
* persistence layer for processed messages
* Docker containerization
* monitoring and metrics

---

# Author

**Miguel Vidal**

GitHub
[https://github.com/MiguelViHe](https://github.com/MiguelViHe)

---
