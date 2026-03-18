import os
import sys
import time
import argparse
import datetime
import psutil
from github import Github
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.logging import RichHandler
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
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
        self.gh = Github(token)
        self.user = self.gh.get_user()

    def pulse_heartbeat(self):
        """Feature 1: Pulse Heartbeat"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - System Health Check\n"
        
        with open(os.path.join(log_dir, "pulse.log"), "a") as f:
            f.write(log_message)
        
        logger.info(f"Pulse Heartbeat logged: {timestamp}")

    def follow_users(self, keyword='Laravel Philippines', limit=5):
        """Feature 2: Network Sync - Follow Users"""
        logger.info(f"Searching for users with keyword: {keyword}")
        users = self.gh.search_users(keyword)
        count = 0
        for user in users:
            if count >= limit:
                break
            try:
                if not self.user.has_in_following(user):
                    self.user.add_to_following(user)
                    logger.info(f"Followed user: {user.login}")
                    count += 1
            except Exception as e:
                logger.error(f"Error following {user.login}: {e}")
        return count

    def unfollow_non_backers(self):
        """Feature 2: Network Sync - Unfollow Non-Backers"""
        logger.info("Syncing network: Unfollowing non-backers...")
        followers = set(f.login for f in self.user.get_followers())
        following = self.user.get_following()
        
        unfollowed_count = 0
        for user in following:
            if user.login not in followers:
                try:
                    self.user.remove_from_following(user)
                    logger.info(f"Unfollowed: {user.login}")
                    unfollowed_count += 1
                except Exception as e:
                    logger.error(f"Error unfollowing {user.login}: {e}")
        return unfollowed_count

    def tech_scout(self):
        """Feature 3: Tech Scout"""
        logger.info("Scouting top repos in Laravel and JavaScript...")
        seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        query = f"created:>{seven_days_ago} topic:laravel topic:javascript"
        repos = self.gh.search_repositories(query=query, sort="stars", order="desc")
        
        results = []
        for i, repo in enumerate(repos):
            if i >= 5:
                break
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
  ____ _   _        ____ ____  ___ _____ 
 / ___| | | |      / ___|  _ \|_ _|__  / 
| |  _| |_| |_____| |   | |_) || |  / /  
| |_| |  _  |_____| |___|  _ < | | / /_  
 \____|_| |_|      \____|_| \_\___/____| 
        """

    def get_system_stats(self):
        """Feature 4: System Monitor"""
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        stats = Text()
        stats.append(f"PISCES Laptop Stats\n", style="bold green")
        stats.append(f"CPU Usage:  [", style="green")
        stats.append(f"{cpu_usage}%", style="bold green")
        stats.append(f"]\n", style="green")
        stats.append(f"RAM Usage:  [", style="green")
        stats.append(f"{ram.percent}%", style="bold green")
        stats.append(f"] ({ram.used//(1024**2)}MB / {ram.total//(1024**2)}MB)\n", style="green")
        stats.append(f"Disk Space: [", style="green")
        stats.append(f"{disk.percent}%", style="bold green")
        stats.append(f"] ({disk.free//(1024**3)}GB free)\n", style="green")
        
        return Panel(stats, title="System Monitor", border_style="green")

    def create_tech_scout_table(self, repos):
        table = Table(title="Tech Scout: Top Trending Repos", border_style="green", header_style="bold green")
        table.add_column("Repository", style="green")
        table.add_column("Stars", justify="right", style="green")
        table.add_column("Language", style="green")
        table.add_column("Link", style="blue")

        for repo in repos:
            table.add_row(repo['name'], str(repo['stars']), str(repo['language']), repo['url'])
        
        return table

    def run(self, manager):
        self.console.print(self.banner, style="bold green")
        
        with Live(self.get_system_stats(), refresh_per_second=2) as live:
            # Perform Tech Scout
            repos = manager.tech_scout()
            table = self.create_tech_scout_table(repos)
            
            # Update display
            live.update(Layout(Panel(table, border_style="green")))
            
            # Simple interaction loop or just display once
            logger.info("GH-CRIZ OMNI TOOL is active.")
            time.sleep(5)  # Keep it alive for a moment to see the stats

def main():
    parser = argparse.ArgumentParser(description="GH-CRIZ OMNI TOOL")
    parser.add_argument("--auto", action="store_true", help="Run Pulse Heartbeat ONLY and exit")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN")
    
    # We allow running without token for --auto if logger/local logic only, 
    # but PyGithub needs it for other features.
    
    manager = GitHubManager(token if token else "MOCK_TOKEN")

    if args.auto:
        manager.pulse_heartbeat()
        sys.exit(0)

    if not token:
        logger.error("Error: GH_TOKEN environment variable not set.")
        sys.exit(1)

    ui = TerminalUI()
    ui.run(manager)

if __name__ == "__main__":
    main()
