import requests
import json

def test_gradio_endpoint():
    """Simple test of your Gradio MCP endpoint"""
    
    base_url = "https://sam522-demo-mcp.hf.space"
    
    print("🧪 Testing your Gradio MCP server...")
    print(f"🔗 Base URL: {base_url}")
    print("-" * 50)
    
    # Test 1: Check if the main page loads
    try:
        response = requests.get(base_url, timeout=10)
        print(f"✅ Main page status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Your Gradio app is running!")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing main page: {e}")
        return
    
    # Test 2: Check if MCP endpoint exists
    mcp_url = f"{base_url}/gradio_api/mcp/sse"
    try:
        print(f"\n🔍 Testing MCP endpoint: {mcp_url}")
        response = requests.get(mcp_url, timeout=5, stream=True)
        print(f"📡 MCP endpoint status: {response.status_code}")
        print(f"📋 Content type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200:
            print("✅ MCP endpoint is accessible!")
            
            # Read first few lines of SSE stream
            print("📥 First few lines from SSE stream:")
            lines_read = 0
            for line in response.iter_lines(decode_unicode=True):
                if line.strip():
                    print(f"  {line}")
                    lines_read += 1
                    if lines_read >= 3:  # Only read first 3 lines
                        break
        else:
            print(f"❌ MCP endpoint returned status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing MCP endpoint: {e}")
    
    # Test 3: Check Gradio API info
    try:
        print(f"\n📋 Checking Gradio API info...")
        api_url = f"{base_url}/info"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            print("✅ Gradio API info accessible")
            # Don't print the full response as it might be large
        else:
            print(f"⚠️  API info status: {response.status_code}")
    except Exception as e:
        print(f"ℹ️  API info not accessible (normal for some Gradio versions)")

def test_with_curl_command():
    """Show curl command for manual testing"""
    print("\n" + "="*60)
    print("🛠️  Manual Testing")
    print("="*60)
    print("You can also test manually with curl:")
    print(f"curl -N https://sam522-demo-mcp.hf.space/gradio_api/mcp/sse")
    print("\nThis should show a stream of SSE data starting with:")
    print("  event: endpoint")
    print("  data: /gradio_api/mcp/messages/...")
    print("  : ping - [timestamp]")

if __name__ == "__main__":
    test_gradio_endpoint()
    test_with_curl_command()