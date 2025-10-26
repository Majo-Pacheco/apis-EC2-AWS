from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime
from services.ec2_service import EC2Service
from config import Config
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize EC2 service
ec2_service = EC2Service()

@app.route('/instances', methods=['GET'])
def get_instances():
    """
    GET /instances
    Returns a list of EC2 instances with their details
    """
    try:
        logger.info("Fetching EC2 instances")
        instances = ec2_service.get_all_instances()
        return jsonify({
            "success": True,
            "data": instances,
            "count": len(instances),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        status_code = 500
        if error_code == 'AuthFailure':
            status_code = 403  # Forbidden - invalid credentials
        
        logger.error(f"AWS API Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": error_code,
            "message": f"Failed to fetch instances: {str(e)}"
        }), status_code
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "InternalServerError",
            "message": "An unexpected error occurred"
        }), 500

@app.route('/instances/stop/<instance_id>', methods=['POST'])
def stop_instance(instance_id):
    """
    POST /instances/stop/{instance_id}
    Stops a running EC2 instance
    """
    try:
        if not instance_id:
            return jsonify({
                "success": False,
                "error": "MissingParameter",
                "message": "Instance ID is required"
            }), 400

        logger.info(f"Attempting to stop instance: {instance_id}")
        result = ec2_service.stop_instance(instance_id)
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": f"Instance {instance_id} is stopping",
                "data": result['data']
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'OperationFailed'),
                "message": result.get('message', 'Failed to stop instance')
            }), result.get('status_code', 400)
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        status_code = 500
        if error_code == 'UnauthorizedOperation':
            status_code = 403  # Forbidden
        
        logger.error(f"AWS API Error: {error_code} - {str(e)}")
        return jsonify({
            "success": False,
            "error": error_code,
            "message": f"Failed to stop instance: {str(e)}"
        }), status_code
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "InternalServerError",
            "message": "An unexpected error occurred"
        }), 500

@app.route('/instances/start/<instance_id>', methods=['POST'])
def start_instance(instance_id):
    """
    POST /instances/start/{instance_id}
    Starts a stopped EC2 instance
    """
    try:
        if not instance_id:
            return jsonify({
                "success": False,
                "error": "MissingParameter",
                "message": "Instance ID is required"
            }), 400

        logger.info(f"Attempting to start instance: {instance_id}")
        result = ec2_service.start_instance(instance_id)
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": f"Instance {instance_id} is starting",
                "data": result['data']
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'OperationFailed'),
                "message": result.get('message', 'Failed to start instance')
            }), result.get('status_code', 400)
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        status_code = 500
        if error_code == 'UnauthorizedOperation':
            status_code = 403  # Forbidden
        
        logger.error(f"AWS API Error: {error_code} - {str(e)}")
        return jsonify({
            "success": False,
            "error": error_code,
            "message": f"Failed to start instance: {str(e)}"
        }), status_code
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "InternalServerError",
            "message": "An unexpected error occurred"
        }), 500

if __name__ == '__main__':
    # Check AWS credentials are configured
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        logger.info(f"AWS Identity: {identity['Arn']}")
    except Exception as e:
        logger.warning(f"AWS Credentials not properly configured: {str(e)}")
    
    app.run(debug=True)
