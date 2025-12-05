"""
Facebook Posting - Quick Testing Script
========================================
Test the Facebook posting functionality before deploying to Streamlit.

Usage:
    python facebook_test.py
"""

from utils.facebook_posting import FacebookPoster, publish_post
from datetime import datetime
import sys


# Fix for Windows Unicode issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_header(title):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_validation():
    """Test credential validation."""
    print_header("TEST 1: Credential Validation")
    
    # Test 1a: Empty credentials
    print("Test 1a: Empty credentials")
    poster = FacebookPoster("", "")
    is_valid, msg = poster.validate_credentials()
    print(f"  Valid: {is_valid}")
    print(f"  Message: {msg}\n")
    
    # Test 1b: Only token provided
    print("Test 1b: Only token provided")
    poster = FacebookPoster("token123", "")
    is_valid, msg = poster.validate_credentials()
    print(f"  Valid: {is_valid}")
    print(f"  Message: {msg}\n")
    
    # Test 1c: Invalid page ID (non-numeric)
    print("Test 1c: Invalid page ID (contains dashes)")
    poster = FacebookPoster("token" * 20, "123-456-789")
    is_valid, msg = poster.validate_credentials()
    print(f"  Valid: {is_valid}")
    print(f"  Message: {msg}\n")
    
    # Test 1d: Valid format
    print("Test 1d: Valid format")
    poster = FacebookPoster("token" * 20, "123456789")
    is_valid, msg = poster.validate_credentials()
    print(f"  Valid: {is_valid}")
    print(f"  Message: {msg}\n")


def test_empty_message():
    """Test empty message handling."""
    print_header("TEST 2: Empty Message Handling")
    
    poster = FacebookPoster("token" * 20, "123456789")
    success, result = poster.publish_post("")
    
    print(f"Success: {success}")
    print(f"Error: {result.get('error')}")
    print(f"Details: {result.get('details')}\n")


def test_invalid_credentials():
    """Test posting with invalid credentials (will fail at Facebook)."""
    print_header("TEST 3: Invalid Credentials (Real API Call)")
    
    print("⚠️  This test will attempt to post with invalid token.")
    print("   It will fail at Facebook API but test error handling.\n")
    
    poster = FacebookPoster(
        page_token="invalid_token_12345",
        page_id="123456789"
    )
    
    success, result = poster.publish_post("Test message from InspiroAI")
    
    print(f"Success: {success}")
    print(f"Error: {result.get('error')}")
    print(f"Error Code: {result.get('error_code')}")
    print(f"Details: {result.get('details')}\n")


def test_standalone_function():
    """Test the standalone publish_post function."""
    print_header("TEST 4: Standalone Function")
    
    print("Testing publish_post() function with invalid credentials...\n")
    
    success, result = publish_post(
        page_token="test_token_" * 10,
        page_id="999999999",
        message="Hello from InspiroAI! 🚀"
    )
    
    print(f"Success: {success}")
    print(f"Response: {result}\n")


def test_with_real_credentials():
    """Template for testing with real credentials."""
    print_header("TEST 5: Real Credentials (TEMPLATE)")
    
    print("To test with real Facebook credentials:")
    print("""
    1. Get your credentials from Meta Developer Dashboard:
       - Page Access Token (from Settings → Developer Tokens)
       - Page ID (from page URL or Page Settings)
    
    2. Update the credentials below:
    """)
    
    # TEMPLATE - Replace with your actual credentials
    PAGE_TOKEN = "YOUR_PAGE_ACCESS_TOKEN_HERE"
    PAGE_ID = "YOUR_PAGE_ID_HERE"
    
    if PAGE_TOKEN == "YOUR_PAGE_ACCESS_TOKEN_HERE":
        print("    ⚠️  Credentials are placeholder. Replace with real values to test.")
        print("    📌 Never commit real tokens to Git!\n")
        return
    
    print("Testing with real credentials...\n")
    
    poster = FacebookPoster(page_token=PAGE_TOKEN, page_id=PAGE_ID)
    
    test_message = f"Test post from InspiroAI {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    success, result = poster.publish_post(message=test_message)
    
    if success:
        print(f"✅ SUCCESS!")
        print(f"Post ID: {result.get('post_id')}")
        print(f"URL: {result.get('url')}")
        print(f"Posted: {result.get('timestamp')}\n")
    else:
        print(f"❌ FAILED!")
        print(f"Error: {result.get('error')}")
        print(f"Code: {result.get('error_code')}")
        print(f"Details: {result.get('details')}\n")


def show_usage_examples():
    """Show Streamlit integration examples."""
    print_header("STREAMLIT INTEGRATION EXAMPLES")
    
    print("""
Example 1: Using FacebookPoster class
───────────────────────────────────────
from utils.facebook_posting import FacebookPoster

# Get from Streamlit inputs
token = st.sidebar.text_input("Facebook Token")
page_id = st.sidebar.text_input("Page ID")

if st.button("Post Now"):
    poster = FacebookPoster(token, page_id)
    success, result = poster.publish_post("Your caption here")
    
    if success:
        st.success(f"✅ Posted! ID: {result['post_id']}")
    else:
        st.error(f"❌ {result['error']}")


Example 2: Using standalone function
──────────────────────────────────────
from utils.facebook_posting import publish_post

if st.button("Post Now"):
    success, result = publish_post(
        page_token=token,
        page_id=page_id,
        message=caption_text
    )
    
    if success:
        st.success("✅ Posted!")
        st.json(result)
    else:
        st.error(result['error'])
        with st.expander("Details"):
            st.json(result)


Example 3: Error handling in Streamlit
────────────────────────────────────────
poster = FacebookPoster(token, page_id)
success, result = poster.publish_post(caption)

if success:
    st.success("✅ Post published successfully!")
    st.write(f"**Post ID:** {result['post_id']}")
    st.write(f"**URL:** {result['url']}")
    st.balloons()
    
else:
    st.error(f"❌ Failed to post: {result['error']}")
    
    with st.expander("📋 Error Details"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Error Code:** {result['error_code']}")
        with col2:
            st.write(f"**Type:** {result.get('error_type', 'Unknown')}")
        st.write(f"**Details:** {result['details']}")


Example 4: With media URL
──────────────────────────
success, result = poster.publish_post(
    message="Check this out! 📸",
    media_url="https://example.com/image.jpg"
)
    """)


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  Facebook Posting - Testing Suite")
    print("  InspiroAI Capstone Project")
    print("="*60)
    
    print("""
This script tests the Facebook posting functionality:
✓ Credential validation
✓ Error handling
✓ API integration
✓ Streamlit examples
    """)
    
    # Run tests
    test_validation()
    test_empty_message()
    test_invalid_credentials()
    test_standalone_function()
    test_with_real_credentials()
    show_usage_examples()
    
    print("\n" + "="*60)
    print("  All Tests Completed!")
    print("="*60 + "\n")
    print("Next Steps:")
    print("1. Update TEST 5 with your real Facebook credentials")
    print("2. Run: python facebook_test.py")
    print("3. Verify post appears on your Facebook page")
    print("4. Deploy to Streamlit!\n")


if __name__ == "__main__":
    main()
