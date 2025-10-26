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

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd meli-api
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
4. Set up environment variables:
   - Copy the example environment file:
     ```bash
     # Windows
     copy .env.example .env
     
     # macOS/Linux
     cp .env.example .env
     ```
   - Edit the `.env` file and add your AWS credentials
   - Never commit the `.env` file to version control!

5. Configure AWS IAM User:
   - Create an IAM user in AWS Console
   - Attach a policy with the required permissions
   - Generate access keys (Access Key ID and Secret Access Key)
   - Add these to your `.env` file

## Running the Application

1. Ensure your virtual environment is activated
2. Start the development server:
   ```bash
   python app.py
   ```
3. The API will be available at `http://localhost:5000`

## Security Considerations

1. **Never commit sensitive information** to version control
2. The following files are in `.gitignore` for security:
   - `.env` (contains your AWS credentials)
   - `__pycache__/`
   - `venv/`
3. Use IAM roles with least privilege principle
4. Rotate your AWS credentials regularly
5. Consider using AWS credentials management tools like AWS Vault or AWS SSO

## API Endpoints

### List EC2 Instances
- `GET /instances`
- **Description**: Retrieves a list of all EC2 instances
- **Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "i-0123456789abcdef0",
        "type": "t2.micro",
        "state": "running",
        "region": "us-east-1",
        "public_ip": "54.210.167.204",
        "private_ip": "172.31.22.36"
      }
    ]
  }
  ```

### Stop an EC2 Instance
- `POST /instances/stop/{instance_id}`
- **Description**: Stops a running EC2 instance
- **Path Parameters**:
  - `instance_id` (required): The EC2 instance ID
- **Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Instance i-0123456789abcdef0 is stopping",
    "data": {
      "instance_id": "i-0123456789abcdef0",
      "current_state": "stopping",
      "previous_state": "running"
    }
  }
  ```

### Start an EC2 Instance
- `POST /instances/start/{instance_id}`
- **Description**: Starts a stopped EC2 instance
- **Path Parameters**:
  - `instance_id` (required): The EC2 instance ID
- **Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Instance i-0123456789abcdef0 is starting",
    "data": {
      "instance_id": "i-0123456789abcdef0",
      "current_state": "pending",
      "previous_state": "stopped"
    }
  }
  ```
- **Common Error Codes**:
  - `400`: Instance is already running or cannot be started
  - `403`: Insufficient permissions to start the instance
  - `404`: Instance not found

### Example Usage

#### Using curl (Linux/MacOS):
```bash
# List instances
curl http://localhost:5000/instances

# Stop an instance
curl -X POST http://localhost:5000/instances/stop/i-0123456789abcdef0

# Start an instance
curl -X POST http://localhost:5000/instances/start/i-0123456789abcdef0
```

#### Using PowerShell (Windows):
```powershell
# List instances
Invoke-RestMethod -Uri "http://localhost:5000/instances" -Method Get | ConvertTo-Json

# Stop an instance
Invoke-RestMethod -Uri "http://localhost:5000/instances/stop/i-0123456789abcdef0" -Method Post | ConvertTo-Json

# Start an instance
Invoke-RestMethod -Uri "http://localhost:5000/instances/start/i-0123456789abcdef0" -Method Post | ConvertTo-Json
```

> **Note for Windows Users**: In PowerShell, `curl` is an alias for `Invoke-WebRequest`. For REST API calls, it's recommended to use `Invoke-RestMethod` as shown above for better JSON handling.

## Running Tests

Run the test suite using:

```bash
pytest
```

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
