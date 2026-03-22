import os
import sys
import argparse
import subprocess
import psutil
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from github import Github
from dotenv import load_dotenv

load_dotenv()

try:
    import pyperclip
except ImportError:
    pyperclip = None

class GitCenter:
    @staticmethod
    def quick_push():
        print("[*] Starting Quick Push...")
        try:
            subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
            msg = input("Commit message (e.g., 'fixed bug'): ").strip() or "auto-commit"
            subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True, text=True)
            
            # Authentication Injection for Push
            token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
            remote_url = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
            
            if token and "github.com" in remote_url and "https://" in remote_url:
                auth_url = remote_url.replace("https://", f"https://{token}@")
                subprocess.run(["git", "push", auth_url, "main"], check=True, capture_output=True, text=True)
            else:
                subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True, text=True)
                
            print("[+] Push complete. Your code is LIVE!")
        except subprocess.CalledProcessError as e:
            print(f"[-] Push error: {e.stderr}")

    @staticmethod
    def pull_updates():
        print("[*] Pulling latest updates from GitHub...")
        try:
            branch = input("Branch to pull (default: main): ").strip() or "main"
            subprocess.run(["git", "fetch", "origin", branch], check=True)
            subprocess.run(["git", "reset", "--hard", f"origin/{branch}"], check=True)
            print(f"[+] SUCCESS: Your folder is perfectly synced with origin/{branch}")
        except subprocess.CalledProcessError as e:
            print(f"[-] Pull error: Ensure you are inside a Git repository.")

    @staticmethod
    def clone_repo():
        print("[*] Clone an existing GitHub repository to your PC")
        
        # Clipboard Detection Feature
        clipboard_content = ""
        if pyperclip:
            try:
                clipboard_content = pyperclip.paste().strip()
            except:
                pass
        
        suggested_url = ""
        if clipboard_content.startswith("https://github.com/"):
            suggested_url = clipboard_content
            print(f"[!] Detected GitHub URL in clipboard: {suggested_url}")
            use_clipboard = input("Do you want to use this URL? (y/n, default: y): ").strip().lower()
            if use_clipboard in ["y", "yes", ""]:
                repo_url = suggested_url
            else:
                repo_url = input("Enter the GitHub repository URL: ").strip()
        else:
            repo_url = input("Enter the GitHub repository URL: ").strip()

        if repo_url:
            try:
                subprocess.run(["git", "clone", repo_url], check=True)
                print(f"[+] Successfully cloned {repo_url}")
            except subprocess.CalledProcessError:
                print("[-] Failed to clone. Check the URL.")

class ProjectArchitect:
    @staticmethod
    def initialize():
        folder = input("New project folder name: ").strip()
        if not folder: return
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            original_dir = os.getcwd()
            os.chdir(folder)
            subprocess.run(["git", "init"], check=True)
            
            with open("LICENSE", "w") as f:
                f.write("MIT License\n\nCopyright (c) 2026 Crizneil Bucio\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
            
            with open("README.md", "w") as f:
                f.write(f"# {folder}\n\nProject initialized by CRIZ TOOLS.")
            
            with open(".gitignore", "w") as f:
                f.write("__pycache__/\n.env\n*.log\n")
            
            print(f"[+] Project '{folder}' architected successfully. Ready to code!")
            os.chdir(original_dir)
        except Exception as e:
            print(f"[-] Architect error: {e}")

class PersonalTools:
    @staticmethod
    def github_streak():
        print("[*] Triggering Daily Streak Commit...")
        streak_dir = "streak"
        streak_file = os.path.join(streak_dir, "contribute.txt")
        
        if not os.path.exists(streak_dir):
            os.makedirs(streak_dir)
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(streak_file, "a") as f:
            f.write(f"Streak updated at: {timestamp}\n")
            
        try:
            subprocess.run(["git", "add", streak_file], check=True, capture_output=True, text=True)
            subprocess.run(["git", "commit", "-m", f"daily streak: {timestamp}"], check=True, capture_output=True, text=True)
            
            # Authentication Injection for Push
            token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
            remote_url = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
            
            if token and "github.com" in remote_url and "https://" in remote_url:
                auth_url = remote_url.replace("https://", f"https://{token}@")
                subprocess.run(["git", "push", auth_url, "main"], check=True, capture_output=True, text=True)
            else:
                subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True, text=True)
                
            print(f"[+] Streak successfully updated and pushed! Graph is GREEN. [{timestamp}]")
        except subprocess.CalledProcessError as e:
            print(f"[-] Streak Error:")
            if "could not read from remote repository" in str(e.stderr).lower():
                print("    > Error: Cannot connect to GitHub. Check your internet or SSH/HTTPS access.")
            elif "src refspec main does not match any" in str(e.stderr).lower():
                print("    > Error: Your branch might not be 'main'. Try 'master'?")
            else:
                print(f"    > {e.stderr}")
        except Exception as e:
            print(f"[-] Unexpected Streak Error: {e}")

    @staticmethod
    def get_github_client():
        token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        if not token:
            print("[-] Error: GITHUB_TOKEN or GH_TOKEN not found in .env file.")
            print("[!] Please add GITHUB_TOKEN=your_token_here to your .env file.")
            return None
        return Github(token)

    @staticmethod
    def auto_follow():
        g = PersonalTools.get_github_client()
        if not g: return
        
        query = input("Enter search query for users to follow (e.g., 'python developer'): ").strip()
        if not query: return
        
        limit = input("Limit (default: 5): ").strip() or "5"
        try:
            limit = int(limit)
        except ValueError:
            limit = 5
            
        print(f"[*] Searching for users matching '{query}'...")
        users = g.search_users(query)
        
        count = 0
        for user in users:
            if count >= limit: break
            try:
                g.get_user().add_to_following(user)
                print(f"[+] Followed: {user.login}")
                count += 1
            except Exception as e:
                print(f"[-] Failed to follow {user.login}: {e}")
        
        print(f"[+] Done. Followed {count} users.")

    @staticmethod
    def auto_unfollow():
        g = PersonalTools.get_github_client()
        if not g: return
        
        print("[*] Fetching followers and following lists...")
        user = g.get_user()
        following = user.get_following()
        followers = [f.login for f in user.get_followers()]
        
        print(f"[*] You are following {following.totalCount} users.")
        unfollow_count = 0
        
        for f_user in following:
            if f_user.login not in followers:
                print(f"[*] {f_user.login} is not following you back. Unfollowing...")
                try:
                    user.remove_from_following(f_user)
                    print(f"[+] Unfollowed: {f_user.login}")
                    unfollow_count += 1
                except Exception as e:
                    print(f"[-] Failed to unfollow {f_user.login}: {e}")
        
        print(f"[+] Done. Unfollowed {unfollow_count} non-followers.")

class WindowsTools:
    @staticmethod
    def flush_dns():
        print("[*] Flushing DNS Cache...")
        subprocess.run(["ipconfig", "/flushdns"])
    
    @staticmethod
    def clean_temp():
        print("[*] Cleaning Windows Temporary Files...")
        temp_dir = os.environ.get('TEMP')
        if temp_dir:
            try:
                subprocess.run(['del', '/q/f/s', f'{temp_dir}\\*'], shell=True, stderr=subprocess.DEVNULL)
                print("[+] Temp files wiped. Disk space recovered!")
            except:
                print("[-] Failed to clear some temp files (they might be actively used by Windows).")
                
    @staticmethod
    def ping_test():
        print("[*] Pinging Google (8.8.8.8) to check internet dropouts...")
        subprocess.run(["ping", "8.8.8.8"])
        
    @staticmethod
    def update_apps():
        print("[*] Commands Windows to find updates for all your installed software...")
        subprocess.run(["winget", "upgrade"])
        print("\n[!] To automatically install all updates, run: winget upgrade --all")

class TerminalUI:
    def __init__(self):
        self.console = Console()
        self.banner = """
[bold cyan]  ██████╗██████╗ ██╗███████╗  [/bold cyan] [bold yellow] ████████╗██████╗  ██████╗ ██╗     ███████╗[/bold yellow]
[bold cyan] ██╔════╝██╔══██╗██║╚══███╔╝  [/bold cyan] [bold yellow] ╚══██╔══╝██╔══██╗██╔═══██╗██║     ██╔════╝[/bold yellow]
[bold cyan] ██║     ██████╔╝██║  ███╔╝   [/bold cyan] [bold yellow]    ██║   ██║  ██║██║   ██║██║     ███████╗[/bold yellow]
[bold cyan] ██║     ██╔══██╗██║ ███╔╝    [/bold cyan] [bold yellow]    ██║   ██║  ██║██║   ██║██║     ╚════██║[/bold yellow]
[bold cyan] ╚██████╗██║  ██║██║███████╗  [/bold cyan] [bold yellow]    ██║   ██████╔╝╚██████╔╝███████╗███████║[/bold yellow]
[bold cyan]  ╚═════╝╚═╝  ╚═╝╚═╝╚══════╝  [/bold cyan] [bold yellow]    ╚═╝   ╚═════╝  ╚═════╝ ╚══════╝╚══════╝[/bold yellow]
        """

    def get_system_monitor(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        stats = f"CPU: {cpu}% | RAM: {ram}% | DISK: {disk}%"
        return Panel(Text(stats, justify="center", style="bold green"), style="green")

    def run(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.print(self.banner)
            self.console.print(self.get_system_monitor())
            
            self.console.print("\n[1] [bold magenta]PERSONAL TOOLS[/bold magenta] (Auto Streak & Social)")
            self.console.print("[2] [bold cyan]GITHUB TOOLS[/bold cyan] (Manage Code & Repositories)")
            self.console.print("[3] [bold yellow]WINDOWS TOOLS[/bold yellow] (Clean & Fix your PC)")
            self.console.print("[0] EXIT\n")
            
            choice = input("CRIZ@OMNI:~$ ").strip()

            try:
                if choice == "1":
                    self.personal_menu()
                elif choice == "2":
                    self.github_menu()
                elif choice == "3":
                    self.windows_menu()
                elif choice == "0":
                    print("STATION OFFLINE.")
                    break
            except Exception as e:
                print(f"\n[bold red]CRITICAL ERROR IN MAIN LOOP:[/bold red] {e}")
                input("Press ENTER to return to menu...")

    def github_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.print(self.banner)
            self.console.print("\n--- [bold cyan]GITHUB TOOLS[/bold cyan] ---")
            self.console.print("[1] PROJECT ARCHITECT (Auto-creates new repo folder, README, & License)")
            self.console.print("[2] GIT QUICK PUSH (Auto-adds all files, asks for commit message, and pushes)")
            self.console.print("[3] GIT PULL UPDATES (Force-downloads the newest code from GitHub)")
            self.console.print("[4] GIT CLONE REPO (Downloads an existing GitHub project to your PC)")
            self.console.print("[0] BACK TO MAIN\n")
            
            gh_choice = input("GITHUB@OMNI:~$ ").strip()
            
            if gh_choice == "1":
                ProjectArchitect.initialize()
            elif gh_choice == "2":
                GitCenter.quick_push()
            elif gh_choice == "3":
                GitCenter.pull_updates()
            elif gh_choice == "4":
                GitCenter.clone_repo()
            elif gh_choice == "0":
                break
                
            if gh_choice in ["1", "2", "3", "4"]:
                input("\nPress ENTER to continue...")

    def windows_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.print(self.banner)
            self.console.print("\n--- [bold yellow]WINDOWS TOOLS[/bold yellow] ---")
            self.console.print("[1] NETWORK PING TEST (Checks your internet stability)")
            self.console.print("[2] FLUSH DNS (Fixes internet routing issues)")
            self.console.print("[3] SYSTEM CLEAN-UP (Deletes junk %temp% files to save space)")
            self.console.print("[4] WINGET APP UPDATER (Checks for software updates)")
            self.console.print("[0] BACK TO MAIN\n")
            
            win_choice = input("WINDOWS@OMNI:~$ ").strip()
            
            if win_choice == "1":
                WindowsTools.ping_test()
            elif win_choice == "2":
                WindowsTools.flush_dns()
            elif win_choice == "3":
                WindowsTools.clean_temp()
            elif win_choice == "4":
                WindowsTools.update_apps()
            elif win_choice == "0":
                break
                
            if win_choice in ["1", "2", "3", "4"]:
                input("\nPress ENTER to continue...")

    def personal_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.print(self.banner)
            self.console.print("\n--- [bold magenta]PERSONAL TOOLS[/bold magenta] ---")
            self.console.print("[1] AUTO GITHUB STREAK (Trigger daily commit to current repo)")
            self.console.print("[2] AUTO FOLLOW (Find and follow users based on query)")
            self.console.print("[3] AUTO UNFOLLOW (Unfollow anyone who doesn't follow you back)")
            self.console.print("[0] BACK TO MAIN\n")
            
            p_choice = input("PERSONAL@OMNI:~$ ").strip()
            
            if p_choice == "1":
                PersonalTools.github_streak()
            elif p_choice == "2":
                PersonalTools.auto_follow()
            elif p_choice == "3":
                PersonalTools.auto_unfollow()
            elif p_choice == "0":
                break
                
            if p_choice in ["1", "2", "3"]:
                input("\nPress ENTER to continue...")

def main():
    ui = TerminalUI()
    ui.run()

if __name__ == "__main__":
    main()