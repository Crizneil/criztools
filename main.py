import os
import sys
import time
import argparse
import datetime
import psutil
import logging
from github import Github
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.logging import RichHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
)
logger = logging.getLogger("rich")

class GitHubManager:
    def __init__(self, token):
        try:
            self.gh = Github(token)
            self.user = self.gh.get_user()
            logger.info(f"Connected to GitHub as: {self.user.login}")
        except Exception as e:
            logger.error(f"Authentication Failed: {e}")
            sys.exit(1)

    def pulse_heartbeat(self):
        """Feature 1: Daily Streak Generator"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = os.path.join(log_dir, "pulse.log")
        
        with open(log_path, "a") as f:
            f.write(f"Pulse Check: {timestamp} - System Active\n")
        
        logger.info(f"[bold green]✔ Heartbeat recorded at {timestamp}[/bold green]")

    def follow_users(self, keyword='Laravel Philippines', limit=5):
        """Feature 2: Auto-Follow Logic"""
        logger.info(f"Searching for new connections: '{keyword}'...")
        users = self.gh.search_users(keyword)
        count = 0
        for user in users:
            if count >= limit: break
            try:
                # Direct check if already following to avoid API spam
                if user.login != self.user.login:
                    self.user.add_to_following(user)
                    logger.info(f"[+] Followed: {user.login}")
                    count += 1
                    time.sleep(1) # Safety delay
            except Exception as e:
                logger.error(f"Error following {user.login}: {e}")
        return count

    def unfollow_non_backers(self):
        """Feature 2: Clean up non-followers"""
        logger.info("Auditing Network: Checking for non-backers...")
        followers = set(f.login for f in self.user.get_followers())
        following = self.user.get_following()
        
        unfollowed_count = 0
        for user in following:
            if user.login not in followers:
                try:
                    self.user.remove_from_following(user)
                    logger.info(f"[-] Unfollowed: {user.login}")
                    unfollowed_count += 1
                    time.sleep(1) # Safety delay
                except Exception as e:
                    logger.error(f"Error unfollowing {user.login}: {e}")
        return unfollowed_count

    def tech_scout(self):
        """Feature 3: Find Trending Repos"""
        logger.info("Scouting GitHub for trending Tech...")
        date_limit = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        query = f"created:>{date_limit} topic:laravel topic:javascript"
        repos = self.gh.search_repositories(query=query, sort="stars", order="desc")
        
        results = []
        for i, repo in enumerate(repos):
            if i >= 5: break
            results.append({
                "name": repo.full_name,
                "stars": repo.stargazers_count,
                "language": repo.language,
                "url": repo.html_url
            })
        return results

class TerminalUI:
    def __init__(self):
        self.console = Console()
        self.banner = """
 [bold green]
  ____ _   _       ____ ____  ___ _____ 
 / ___| | | |     / ___|  _ \|_ _|__  / 
| |  _| |_| |_____| |   | |_) || |  / /  
| |_| |  _  |_____| |___|  _ < | | / /_  
 \____|_| |_|     \____|_| \_\___/____| 
                                        [/bold green]
 [cyan]GH-CRIZ OMNI TOOL v1.0 | PISCES WORKSTATION[/cyan]
        """

    def get_system_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        stats = Text()
        stats.append(f"CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%", style="bold green")
        return Panel(stats, title="[bold white]System Status[/bold white]", border_style="green")

    def run(self, manager):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.console.print(self.banner)
        
        while True:
            self.console.print(self.get_system_stats())
            self.console.print("\n[1] 🟢 Daily Pulse (Streak)", style="bold white")
            self.console.print("[2] 📡 Network Sync (Follow/Unfollow)", style="bold white")
            self.console.print("[3] 🔍 Tech Scout (Trending)", style="bold white")
            self.console.print("[0] ❌ Exit Terminal", style="bold red")
            
            choice = self.console.input("\n[bold yellow]CRIZ@OMNI:~$ [/bold yellow]")

            if choice == "1":
                manager.pulse_heartbeat()
            elif choice == "2":
                f = manager.follow_users()
                u = manager.unfollow_non_backers()
                self.console.print(f"[bold green]Sync Complete: +{f} follows, -{u} unfollows.[/bold green]")
            elif choice == "3":
                repos = manager.tech_scout()
                table = Table(title="Trending Repos", border_style="green")
                table.add_column("Repo", style="cyan")
                table.add_column("Stars", style="magenta")
                table.add_row(repos[0]['name'], str(repos[0]['stars'])) # Sample row
                self.console.print(table)
            elif choice == "0":
                break
            time.sleep(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true")
    args = parser.parse_args()

    token = os.getenv("GH_TOKEN")
    if not token:
        print("ERROR: GH_TOKEN missing in .env or Environment Variables.")
        sys.exit(1)

    manager = GitHubManager(token)

    if args.auto:
        # Eto ang tatakbo sa GitHub Actions
        manager.pulse_heartbeat()
        manager.follow_users(limit=2) # Safe follow
        manager.unfollow_non_backers()
        sys.exit(0)

    ui = TerminalUI()
    ui.run(manager)

if __name__ == "__main__":
    main()