import json
import os
from github import Github
from dotenv import load_dotenv
from model import TeamModel

class DatabaseManager:
    def __init__(self):
        """Initialize JSON file and GitHub connection."""
        self.json_file = "teams.json"
        self.model = TeamModel()
        load_dotenv()
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_owner = os.getenv("GITHUB_REPO_OWNER")
        self.repo_name = os.getenv("GITHUB_REPO_NAME")
        self.github = Github(self.github_token)
        self.repo = self.github.get_repo(f"{self.repo_owner}/{self.repo_name}")
        self.initialize_json_file()

    def initialize_json_file(self):
        """Create teams.json if it doesn't exist."""
        if not os.path.exists(self.json_file):
            data = {category: [] for category in self.model.categories}
            with open(self.json_file, "w") as f:
                json.dump(data, f, indent=4)
            self.commit_to_github("Initialize teams.json")

    def read_json(self):
        """Read data from teams.json."""
        try:
            with open(self.json_file, "r") as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to read JSON file: {e}")

    def write_json(self, data):
        """Write data to teams.json and commit to GitHub."""
        try:
            with open(self.json_file, "w") as f:
                json.dump(data, f, indent=4)
            self.commit_to_github("Update teams.json")
        except Exception as e:
            raise Exception(f"Failed to write JSON file: {e}")

    def commit_to_github(self, commit_message):
        """Commit and push teams.json to GitHub."""
        try:
            with open(self.json_file, "r") as f:
                content = f.read()
            try:
                # Get the file from the repository
                file = self.repo.get_contents(self.json_file)
                # Update the file
                self.repo.update_file(
                    path=self.json_file,
                    message=commit_message,
                    content=content,
                    sha=file.sha
                )
            except:
                # Create the file if it doesn't exist
                self.repo.create_file(
                    path=self.json_file,
                    message=commit_message,
                    content=content
                )
        except Exception as e:
            raise Exception(f"Failed to commit to GitHub: {e}")

    def get_teams(self, category, sort_col="REF_NO"):
        """Retrieve teams for a given category."""
        try:
            data = self.read_json()
            teams = data.get(category, [])
            if sort_col in self.model.columns:
                teams = sorted(teams, key=lambda x: x.get(sort_col, ""))
            return teams
        except Exception as e:
            raise Exception(f"Failed to retrieve teams: {e}")

    def add_team(self, category, team_data):
        """Add a new team to the JSON file."""
        try:
            data = self.read_json()
            teams = data.get(category, [])
            max_ref = max([team["REF_NO"] for team in teams], default=0)
            ref_no = max_ref + 1
            team_data["REF_NO"] = ref_no
            teams.append(team_data)
            data[category] = teams
            self.write_json(data)
        except Exception as e:
            raise Exception(f"Failed to add team: {e}")

    def update_team(self, category, ref_no, team_data):
        """Update an existing team in the JSON file."""
        try:
            data = self.read_json()
            teams = data.get(category, [])
            for team in teams:
                if team["REF_NO"] == ref_no:
                    team.update(team_data)
                    break
            else:
                raise Exception(f"Team with REF_NO {ref_no} not found in category {category}")
            data[category] = teams
            self.write_json(data)
        except Exception as e:
            raise Exception(f"Failed to update team: {e}")

    def delete_team(self, category, ref_no):
        """Delete a team from the JSON file."""
        try:
            data = self.read_json()
            teams = data.get(category, [])
            teams = [team for team in teams if team["REF_NO"] != ref_no]
            data[category] = teams
            self.write_json(data)
        except Exception as e:
            raise Exception(f"Failed to delete team: {e}")