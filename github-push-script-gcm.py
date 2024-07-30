import subprocess
import json
import os

def get_github_credentials():
    try:
        result = subprocess.run(['/usr/local/share/gcm-core/git-credential-manager', 'get'], 
                                input='protocol=https\nhost=github.com\n\n', 
                                capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        creds = {}
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                creds[key.strip()] = value.strip()
        return [creds.get('username', '')]
    except Exception as e:
        print(f"Error getting credentials: {e}")
        return []

def push_to_github():
    repo_name = input("Enter the name for your GitHub repository: ")
    
    creds = get_github_credentials()
    if not creds:
        print("No GitHub credentials found.")
        return
    
    print("Available GitHub accounts:")
    for i, cred in enumerate(creds, 1):
        print(f"{i}. {cred}")
    
    choice = int(input("Choose the account number to use: ")) - 1
    if choice < 0 or choice >= len(creds):
        print("Invalid choice.")
        return
    
    chosen_account = creds[choice]
    
    remote_url = f"https://github.com/{chosen_account}/{repo_name}.git"
    
    # Check if 'origin' remote already exists
    check_remote = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
    if check_remote.returncode == 0:
        # If 'origin' exists, update it
        subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url])
        print("Updated existing 'origin' remote.")
    else:
        # If 'origin' doesn't exist, add it
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url])
        print("Added new 'origin' remote.")

    # Determine the current branch name
    current_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                    capture_output=True, text=True).stdout.strip()

    # Push to GitHub
    push_result = subprocess.run(['git', 'push', '-u', 'origin', current_branch], capture_output=True, text=True)
    
    if push_result.returncode == 0:
        print(f"Successfully pushed to {remote_url}")
    else:
        print(f"Failed to push. Error: {push_result.stderr}")

if __name__ == "__main__":
    push_to_github()
