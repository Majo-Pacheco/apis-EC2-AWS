# MELI API Challenge

A RESTful API for managing EC2 instances with mock data, built with Flask and Python.

## Features

- List all EC2 instances with detailed information
- Start stopped EC2 instances
- Stop running EC2 instances
- Comprehensive error handling
- Unit tests with pytest
- Clean architecture with separation of concerns

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- AWS account with the following IAM permissions:
  - `ec2:DescribeInstances`
  - `ec2:StartInstances`
  - `ec2:StopInstances`
  - `ec2:DescribeInstanceStatus`

## Setup

1. Clone the repository
git clone <your-repo-url>

Go to the project directory
cd C:\Path\To\Your\Project

2. Create and activate virtual environment
python -m venv venv --> create (a folder named 'venv' will be created in your proyect directory)

.\venv\Scripts\activate --> activate

3. Install dependencies
pip install -r requirements.txt


Environment Variables
4. Set up .env file
copy .env.example .env --> a new .env will be created in your proyect directory

Edit .env in your proyect folder and add:

AWS_ACCESS_KEY_ID=<ACCESSKEYID>
AWS_SECRET_ACCESS_KEY=<SECRETACCESSKEY>
AWS_DEFAULT_REGION=us-east-1

Save the .env with the credentials you have just configured

⚠ **Important:** The credentials `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` provided are real and can be used for this project demo only.  
The IAM user created for this purpose has **limited permissions**, restricted to starting, stopping, and describing a single EC2 instance used in this project.  
No other AWS resources can be modified or accessed with these credentials.


Run the App
5. Start the app
python app.py

Test the Endpoints (PowerShell) --> Open another PowerShell window while still running the app
Go to the project directory
cd C:\Path\To\Your\Project

6. List EC2 instances
Invoke-RestMethod -Uri "http://localhost:5000/instances" -Method Get | ConvertTo-Json -Depth 10

7. Start an EC2 instance --> Change the id if needed
Invoke-RestMethod -Uri "http://localhost:5000/instances/start/i-0b44921f1151aa857" -Method Post | ConvertTo-Json

9. Stop an EC2 instance --> Change the id if needed
Invoke-RestMethod -Uri "http://localhost:5000/instances/stop/i-0b44921f1151aa857" -Method Post | ConvertTo-Json

## Project Structure

```
meli-api/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── config.py             # Configuration settings
├── models/               # Data models
│   └── ec2_instance.py
├── services/             # Business logic
│   └── ec2_service.py
├── tests/                # Unit tests
│   └── test_api.py
└── README.md             # This file
```

## License

This project is for interview/portfolio purposes.
