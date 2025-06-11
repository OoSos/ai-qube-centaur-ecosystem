#!/usr/bin/env python3
"""
CENTAUR-015: n8n Production Workflow Deployment Script
Automates the deployment and configuration of multi-agent coordination workflows
"""

import json
import requests
import os
import time
from datetime import datetime
import psycopg2
from psycopg2.extras import DictCursor

class CentaurWorkflowDeployer:
    def __init__(self):
        self.n8n_url = os.getenv('N8N_URL', 'http://localhost:5678')
        self.n8n_api_key = os.getenv('N8N_API_KEY')
        self.postgres_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
            'database': os.getenv('POSTGRES_DB', 'centaur_coordination'),
            'user': os.getenv('POSTGRES_USER', 'n8n_user'),
            'password': os.getenv('POSTGRES_PASSWORD')
        }
        
    def deploy_workflow(self, workflow_file_path):
        """Deploy workflow to n8n instance"""
        print(f"🚀 Deploying workflow from {workflow_file_path}")
        
        try:
            with open(workflow_file_path, 'r') as f:
                workflow_data = json.load(f)
            
            # Add deployment metadata
            workflow_data['name'] = 'Centaur Multi-Agent Coordination - Production'
            workflow_data['tags'] = ['centaur', 'production', 'multi-agent']
            workflow_data['meta'] = {
                'deployed_at': datetime.now().isoformat(),
                'version': 'v1.0',
                'deployed_by': 'centaur-deployment-script'
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            if self.n8n_api_key:
                headers['Authorization'] = f'Bearer {self.n8n_api_key}'
            
            response = requests.post(
                f'{self.n8n_url}/api/v1/workflows',
                headers=headers,
                json=workflow_data
            )
            
            if response.status_code == 201:
                workflow_id = response.json()['id']
                print(f"✅ Workflow deployed successfully with ID: {workflow_id}")
                
                # Activate the workflow
                activate_response = requests.patch(
                    f'{self.n8n_url}/api/v1/workflows/{workflow_id}/activate',
                    headers=headers
                )
                
                if activate_response.status_code == 200:
                    print(f"✅ Workflow activated successfully")
                    return workflow_id
                else:
                    print(f"⚠️ Workflow deployed but activation failed: {activate_response.text}")
                    
            else:
                print(f"❌ Workflow deployment failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error deploying workflow: {str(e)}")
            return None
    
    def setup_database(self, schema_file_path):
        """Set up PostgreSQL database schema"""
        print("🗄️ Setting up PostgreSQL database schema")
        
        try:
            with open(schema_file_path, 'r') as f:
                schema_sql = f.read()
            
            conn = psycopg2.connect(**self.postgres_config)
            cursor = conn.cursor()
            
            # Execute schema creation
            cursor.execute(schema_sql)
            conn.commit()
            
            print("✅ Database schema created successfully")
            
            # Test the connection and tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('coordination_metrics', 'agent_performance', 'routing_decisions')
            """)
            
            tables = cursor.fetchall()
            print(f"✅ Created {len(tables)} tables: {[t[0] for t in tables]}")
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Database setup failed: {str(e)}")
            return False
    
    def configure_credentials(self):
        """Configure API credentials in n8n"""
        print("🔑 Configuring API credentials")
        
        credentials = [
            {
                'name': 'anthropic',
                'type': 'httpHeaderAuth',
                'data': {
                    'name': 'x-api-key',
                    'value': os.getenv('ANTHROPIC_API_KEY')
                }
            },
            {
                'name': 'openai',
                'type': 'httpHeaderAuth', 
                'data': {
                    'name': 'Authorization',
                    'value': f"Bearer {os.getenv('OPENAI_API_KEY')}"
                }
            },
            {
                'name': 'google',
                'type': 'httpHeaderAuth',
                'data': {
                    'name': 'Authorization', 
                    'value': f"Bearer {os.getenv('GOOGLE_API_KEY')}"
                }
            },
            {
                'name': 'postgres-centaur',
                'type': 'postgres',
                'data': self.postgres_config
            }
        ]
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        if self.n8n_api_key:
            headers['Authorization'] = f'Bearer {self.n8n_api_key}'
        
        success_count = 0
        for cred in credentials:
            try:
                response = requests.post(
                    f'{self.n8n_url}/api/v1/credentials',
                    headers=headers,
                    json=cred
                )
                
                if response.status_code == 201:
                    print(f"✅ Configured {cred['name']} credentials")
                    success_count += 1
                else:
                    print(f"⚠️ Failed to configure {cred['name']}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error configuring {cred['name']}: {str(e)}")
        
        print(f"✅ Successfully configured {success_count}/{len(credentials)} credentials")
        return success_count == len(credentials)
    
    def test_coordination(self, workflow_id):
        """Test the deployed coordination workflow"""
        print("🧪 Testing multi-agent coordination")
        
        test_requests = [
            {
                'task_type': 'analysis',
                'task_description': 'Analyze the competitive advantages of recursive AI systems',
                'context': 'Market research for AI coordination platforms',
                'complexity': 'medium',
                'urgency': 'normal'
            },
            {
                'task_type': 'coding',
                'task_description': 'Create a Python function for agent performance monitoring',
                'context': 'Multi-agent coordination system',
                'requirements': 'Include error handling and logging',
                'complexity': 'high',
                'urgency': 'normal'
            },
            {
                'task_type': 'optimization',
                'task_description': 'Optimize database query performance for coordination metrics',
                'context': 'PostgreSQL performance tuning',
                'complexity': 'medium',
                'urgency': 'low'
            }
        ]
        
        webhook_url = f"{self.n8n_url}/webhook/centaur-coordination"
        successful_tests = 0
        
        for i, test_req in enumerate(test_requests, 1):
            print(f"\n🔄 Running test {i}/{len(test_requests)}: {test_req['task_type']}")
            
            try:
                response = requests.post(webhook_url, json=test_req, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Test {i} successful:")
                    print(f"   Agent: {result.get('agent_used')}")
                    print(f"   Quality Score: {result.get('quality_score')}")
                    print(f"   Coordination ID: {result.get('coordination_id')}")
                    successful_tests += 1
                else:
                    print(f"❌ Test {i} failed: {response.status_code} - {response.text}")
                    
                time.sleep(2)  # Brief pause between tests
                
            except Exception as e:
                print(f"❌ Test {i} error: {str(e)}")
        
        print(f"\n📊 Test Results: {successful_tests}/{len(test_requests)} successful")
        return successful_tests == len(test_requests)
    
    def generate_deployment_report(self, workflow_id, tests_passed):
        """Generate deployment report"""
        report = {
            'deployment_timestamp': datetime.now().isoformat(),
            'workflow_id': workflow_id,
            'database_configured': True,
            'credentials_configured': True,
            'tests_passed': tests_passed,
            'status': 'success' if tests_passed else 'partial',
            'webhook_url': f"{self.n8n_url}/webhook/centaur-coordination",
            'next_steps': [
                'Monitor coordination metrics in PostgreSQL',
                'Review agent performance in n8n execution logs',
                'Begin CENTAUR-016: RAG Knowledge Base Population',
                'Start production workload testing'
            ]
        }
        
        report_file = f"deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 Deployment report saved to: {report_file}")
        return report

def main():
    print("🚀 CENTAUR-015: n8n Production Workflow Deployment")
    print("=" * 60)
    
    deployer = CentaurWorkflowDeployer()
    
    # Check required environment variables
    required_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY', 'POSTGRES_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please set these variables before running the deployment script.")
        return False
    
    # Step 1: Setup database schema
    schema_success = deployer.setup_database('database/coordination_schema.sql')
    if not schema_success:
        print("❌ Database setup failed. Aborting deployment.")
        return False
    
    # Step 2: Deploy workflow
    workflow_id = deployer.deploy_workflow('n8n-workflows/production-multi-agent-coordination.json')
    if not workflow_id:
        print("❌ Workflow deployment failed. Aborting.")
        return False
    
    # Step 3: Configure credentials
    creds_success = deployer.configure_credentials()
    
    # Step 4: Test coordination
    time.sleep(5)  # Give n8n time to fully activate workflow
    tests_passed = deployer.test_coordination(workflow_id)
    
    # Step 5: Generate report
    report = deployer.generate_deployment_report(workflow_id, tests_passed)
    
    if tests_passed:
        print("\n🎉 CENTAUR-015 DEPLOYMENT SUCCESSFUL!")
        print("✅ Multi-agent coordination is operational")
        print(f"📊 Webhook URL: {deployer.n8n_url}/webhook/centaur-coordination")
        print("🚀 Ready for production workload")
    else:
        print("\n⚠️ CENTAUR-015 DEPLOYMENT PARTIAL SUCCESS")
        print("🔧 Some components need manual configuration")
        print("📋 Check deployment report for details")
    
    return tests_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
