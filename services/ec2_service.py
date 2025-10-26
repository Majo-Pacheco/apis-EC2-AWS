import boto3
from botocore.exceptions import ClientError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EC2Service:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')
    
    def get_all_instances(self):
        """Get all EC2 instances"""
        try:
            response = self.ec2_client.describe_instances()
            instances = []
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_data = {
                        'id': instance['InstanceId'],
                        'type': instance['InstanceType'],
                        'state': instance['State']['Name'],
                        'region': self.ec2_client.meta.region_name,
                        'launch_time': instance['LaunchTime'].isoformat(),
                        'public_ip': instance.get('PublicIpAddress', 'N/A'),
                        'private_ip': instance.get('PrivateIpAddress', 'N/A'),
                        'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    }
                    instances.append(instance_data)
                    
            return instances
            
        except ClientError as e:
            logger.error(f"Error fetching instances: {str(e)}")
            raise
    
    def stop_instance(self, instance_id):
        """Stop a running EC2 instance"""
        try:
            # First check instance state
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            
            if instance['State']['Name'] == 'stopped':
                return {
                    'success': False,
                    'error': 'InstanceAlreadyStopped',
                    'message': f'Instance {instance_id} is already stopped',
                    'status_code': 400
                }
                
            if instance['State']['Name'] != 'running':
                return {
                    'success': False,
                    'error': 'IncorrectInstanceState',
                    'message': f'Instance {instance_id} is not in a state that can be stopped',
                    'status_code': 400
                }
            
            # Stop the instance
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            
            return {
                'success': True,
                'data': {
                    'instance_id': instance_id,
                    'current_state': 'stopping',
                    'previous_state': instance['State']['Name'],
                    'state_transition_reason': 'User initiated stop'
                }
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidInstanceID.NotFound':
                return {
                    'success': False,
                    'error': 'InstanceNotFound',
                    'message': f'Instance {instance_id} not found',
                    'status_code': 404
                }
            logger.error(f"Error stopping instance {instance_id}: {str(e)}")
            raise

    def start_instance(self, instance_id):
        """Start a stopped EC2 instance"""
        try:
            # First check instance state
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            
            if instance['State']['Name'] == 'running':
                return {
                    'success': False,
                    'error': 'InstanceAlreadyRunning',
                    'message': f'Instance {instance_id} is already running',
                    'status_code': 400
                }
                
            if instance['State']['Name'] not in ['stopped', 'stopping']:
                return {
                    'success': False,
                    'error': 'IncorrectInstanceState',
                    'message': f'Instance {instance_id} is not in a state that can be started',
                    'status_code': 400
                }
            
            # Start the instance
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            
            return {
                'success': True,
                'data': {
                    'instance_id': instance_id,
                    'current_state': 'pending',
                    'previous_state': instance['State']['Name'],
                    'state_transition_reason': 'User initiated start'
                }
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidInstanceID.NotFound':
                return {
                    'success': False,
                    'error': 'InstanceNotFound',
                    'message': f'Instance {instance_id} not found',
                    'status_code': 404
                }
            logger.error(f"Error starting instance {instance_id}: {str(e)}")
            raise
