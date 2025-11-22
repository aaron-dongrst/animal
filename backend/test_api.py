"""
Simple test script for the backend API.
Run this after starting the server to test the /analyze endpoint.
"""

import requests
import os

# Configuration
API_URL = "http://localhost:5000"
TEST_VIDEO_PATH = "../data/raw_videos/Not Healthy/polarBearPacing.mp4"  # Adjust path as needed

def test_health_endpoint():
    """Test the health check endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_analyze_endpoint():
    """Test the analyze endpoint with a video file."""
    print("\nTesting /analyze endpoint...")
    
    if not os.path.exists(TEST_VIDEO_PATH):
        print(f"Test video not found: {TEST_VIDEO_PATH}")
        print("Please update TEST_VIDEO_PATH in this script or add a test video.")
        return False
    
    try:
        with open(TEST_VIDEO_PATH, 'rb') as video_file:
            files = {'video': (os.path.basename(TEST_VIDEO_PATH), video_file, 'video/mp4')}
            data = {
                'species': 'bear',
                'age': '5 years',
                'diet': 'omnivore',
                'health_conditions': 'none'
            }
            
            print(f"Uploading video: {TEST_VIDEO_PATH}")
            print(f"Parameters: {data}")
            
            response = requests.post(f"{API_URL}/analyze", files=files, data=data)
            
            print(f"\nStatus: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ Analysis Results:")
                print(f"  Species: {result.get('species')}")
                print(f"  Behavior: {result.get('behavior_observed')}")
                print(f"  Length: {result.get('length_seconds')} seconds ({result.get('length_minutes')} minutes)")
                print(f"  Repeating: {result.get('is_repeating')}")
                print(f"  Healthy: {result.get('is_healthy')}")
                print(f"  Confidence: {result.get('confidence')}")
                print(f"\n  Reasoning: {result.get('reasoning', 'N/A')}")
                print(f"\n  Recommendations: {result.get('recommendations', 'N/A')}")
                return True
            else:
                print(f"❌ Error: {response.json()}")
                return False
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("FaunaVision Backend API Test")
    print("=" * 60)
    print(f"\nMake sure the server is running on {API_URL}")
    print("Start it with: python backend/app.py\n")
    
    # Test health endpoint
    if test_health_endpoint():
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
        print("Make sure the server is running!")
        exit(1)
    
    # Test analyze endpoint
    if test_analyze_endpoint():
        print("\n✅ Analysis test passed")
    else:
        print("\n❌ Analysis test failed")
    
    print("\n" + "=" * 60)

