import subprocess
import os
import json

def get_github_credentials():
    if os.name == 'nt':  # Windows
        result = subprocess.run(['cmdkey', '/list'], capture_output=True, text=True)
        creds = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'github.com' in line]
    else:  # macOS/Linux
        result = subprocess.run(['git', 'credential-osxkeychain', 'get'], input='host=github.com\n\n', capture_output=True, text=True)
        creds = [line.split('=')[1].strip() for line in result.stdout.split('\n') if line.startswith('username=')]
    return creds

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
    
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url])
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])
    
    print(f"Successfully pushed to {remote_url}")

if __name__ == "__main__":
    push_to_github()
