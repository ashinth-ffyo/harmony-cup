class TeamModel:
    def __init__(self):
        """Initialize the data model for Harmony Cup."""
        self.categories = ["F1", "F2", "F3", "F4", "AS"]
        self.columns = [
            "REF_NO", "Name_1", "Name_2", "Name_3", "Name_4", "Name_5",
            "Class_1", "Class_2", "Class_3", "Class_4", "Class_5",
            "Type", "Round1", "Round2", "Round3", "Round4", "Final"
        ]
        self.team_fields = [
            "Name_1", "Name_2", "Name_3", "Name_4", "Name_5",
            "Class_1", "Class_2", "Class_3", "Class_4", "Class_5", "Type"
        ]
        self.round_fields = ["Round1", "Round2", "Round3", "Round4", "Final"]
        self.status_options = ["Not Yet", "Passed", "Failed"]