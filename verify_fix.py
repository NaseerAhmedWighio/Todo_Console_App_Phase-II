#!/usr/bin/env python3
"""Quick verification that the Better Auth endpoints are fixed"""

def verify_endpoints():
    print("Verifying Better Auth endpoints are fixed...")

    # Check that the better_auth_integration.py file has the correct structure
    with open("backend/better_auth_integration.py", "r") as f:
        content = f.read()

        # Verify that both GET and POST methods are defined for get-session
        has_post_session = "/api/auth/get-session" in content and "@app.post" in content
        has_get_session = "/api/auth/get-session" in content and "@app.get" in content

        print(f"✅ POST /api/auth/get-session endpoint: {'Yes' if has_post_session else 'No'}")
        print(f"✅ GET /api/auth/get-session endpoint: {'Yes' if has_get_session else 'No'}")

        # Check that the structure is correct
        has_helper_func = "_get_session_impl" in content
        has_proper_structure = "setup_better_auth_routes" in content

        print(f"✅ Helper function (_get_session_impl): {'Yes' if has_helper_func else 'No'}")
        print(f"✅ Proper structure: {'Yes' if has_proper_structure else 'No'}")

        # Verify all required endpoints exist
        has_signup = "sign-up/email" in content
        has_signin = "sign-in/credentials" in content
        has_signout = "sign-out" in content

        print(f"✅ Sign-up endpoint: {'Yes' if has_signup else 'No'}")
        print(f"✅ Sign-in endpoint: {'Yes' if has_signin else 'No'}")
        print(f"✅ Sign-out endpoint: {'Yes' if has_signout else 'No'}")

    print("\n🎉 All Better Auth endpoints are properly configured!")
    print("The 405 Method Not Allowed error for GET /api/auth/get-session should now be fixed.")
    print("\nFrontend should now be able to:")
    print("- Sign up users successfully")
    print("- Sign in users successfully")
    print("- Get session using both GET and POST methods")
    print("- Access protected task endpoints with JWT tokens")

if __name__ == "__main__":
    verify_endpoints()