import os
import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        sys.exit(1)

def install_brave():
    if os.geteuid() != 0:
        print("This script must be run as root. Please use 'sudo'.")
        sys.exit(1)

    print("--- Starting Brave Browser Installation ---")

    print("[1/5] Installing prerequisites (curl)...")
    run_command(['apt', 'update'])
    run_command(['apt', 'install', '-y', 'curl'])

    print("[2/5] Adding Brave GPG key...")
    keyring_path = '/usr/share/keyrings/brave-browser-archive-keyring.gpg'
    key_url = 'https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg'
    run_command(['curl', '-fsSLo', keyring_path, key_url])

    print("[3/5] Adding Brave repository to sources...")
    repo_file_path = '/etc/apt/sources.list.d/brave-browser-release.list'
    repo_entry = "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"
    
    try:
        with open(repo_file_path, 'w') as f:
            f.write(repo_entry + '\n')
    except IOError as e:
        print(f"Failed to write repository file: {e}")
        sys.exit(1)

    print("[4/5] Updating package lists...")
    run_command(['apt', 'update'])

    print("[5/5] Installing brave-browser...")
    run_command(['apt', 'install', '-y', 'brave-browser'])

    print("\n--- Installation Complete! ---")

if __name__ == "__main__":
    install_brave()
