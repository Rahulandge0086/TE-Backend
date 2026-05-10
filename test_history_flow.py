#!/usr/bin/env python3
"""Test script for the history endpoint with JWT authentication."""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_history_flow():
    print("=" * 70)
    print("Testing History API Flow with JWT Authentication")
    print("=" * 70)
    
    # ── 1. Login with existing credentials ────────────────────────────
    print("\n[1] Logging in with user credentials...")
    login_payload = {
        "email": "test@example.com",
        "password": "qwert123",
    }
    
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_payload
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    login_data = login_response.json()
    token = login_data.get("token")
    user = login_data.get("user", {})
    org_id = user.get("orgId")
    
    print(f"✅ Login successful!")
    print(f"   User ID: {user.get('id')}")
    print(f"   Email: {user.get('email')}")
    print(f"   Org ID: {org_id}")
    print(f"   Token: {token[:50]}...")
    
    # ── 2. Test get history with JWT token ────────────────────────────
    print("\n[2] Fetching history with JWT token...")
    history_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Optional request body (can be empty)
    history_payload = {}
    
    history_response = requests.post(
        f"{BASE_URL}/api/history",
        json=history_payload,
        headers=history_headers
    )
    
    if history_response.status_code != 200:
        print(f"❌ History fetch failed: {history_response.status_code}")
        print(f"   Response: {history_response.text}")
        return
    
    history_data = history_response.json()
    sessions = history_data.get("sessions", [])
    
    print(f"✅ History fetch successful!")
    print(f"   Total sessions: {len(sessions)}")
    print(f"   Success: {history_data.get('success')}")
    
    if sessions:
        print(f"\n   Sample session:")
        session = sessions[0]
        print(f"     - Session ID: {session.get('session_id')}")
        print(f"     - Query: {session.get('query')[:50]}...")
        print(f"     - Domain: {session.get('domain')}")
        print(f"     - Created: {session.get('created_at')}")
        print(f"     - Causes: {session.get('cause_count')}")
    else:
        print("   (No previous sessions found)")
    
    # ── 3. Test history without token (should fail) ────────────────────
    print("\n[3] Testing history endpoint without token (should fail)...")
    no_token_response = requests.post(
        f"{BASE_URL}/api/history",
        json={}
    )
    
    if no_token_response.status_code != 401:
        print(f"⚠️  Expected 401, got {no_token_response.status_code}")
    else:
        print(f"✅ Correctly rejected request without token")
        print(f"   Response: {no_token_response.json().get('detail')}")
    
    # ── 4. Test history with invalid token (should fail) ───────────────
    print("\n[4] Testing history endpoint with invalid token (should fail)...")
    invalid_token_response = requests.post(
        f"{BASE_URL}/api/history",
        json={},
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    if invalid_token_response.status_code != 401:
        print(f"⚠️  Expected 401, got {invalid_token_response.status_code}")
    else:
        print(f"✅ Correctly rejected request with invalid token")
        print(f"   Response: {invalid_token_response.json().get('detail')}")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed successfully!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_history_flow()
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
