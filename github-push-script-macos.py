import subprocess
import os
import json

def get_github_credentials():
    # Read the Git configuration file
    home = os.path.expanduser("~")
    git_config_path = os.path.join(home, ".gitconfig")
    
    if not os.path.exists(git_config_path):
        print("Git config file not found.")
        return []

    with open(git_config_path, 'r') as f:
        config = f.read()

    # Parse the config file to find GitHub accounts
    creds = []
    for line in config.split('\n'):
        if line.strip().startswith("user ="):
            creds.append(line.split('=')[1].strip())
    
    return creds

def push_to_github():
    repo_name = input("Enter the name for your GitHub repository: ")
    
    creds = get_github_credentials()
    if not creds:
        print("No GitHub accounts found in .gitconfig.")
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
