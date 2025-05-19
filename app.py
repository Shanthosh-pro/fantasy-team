from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Role constraints
constraints = {
    "WK": (1, 4),
    "Bat": (3, 6),
    "AR": (1, 4),
    "Bowl": (3, 6)
}

def filter_by_team(players):
    team_count = {}
    filtered_players = []
    for player in players:
        team = player["team"]
        if team_count.get(team, 0) < 7:
            filtered_players.append(player)
            team_count[team] = team_count.get(team, 0) + 1
    return filtered_players

def select_captain_vc(team):
    sorted_team = sorted(team, key=lambda p: constraints[p["role"]][1], reverse=True)
    return sorted_team[0], sorted_team[1]  # Best two players for captain & vice-captain

@app.route("/select_team", methods=["POST"])
def select_team():
    player_data = request.json.get("players", [])
    if len(player_data) < 15:
        return jsonify({"error": "Please provide 15 players"}), 400

    random.shuffle(player_data)
    filtered_players = filter_by_team(player_data)
    teams = [filtered_players[i * 11: (i + 1) * 11] for i in range(3)]

    response = []
    for i, team in enumerate(teams):
        captain, vice_captain = select_captain_vc(team)
        response.append({
            "team_number": i + 1,
            "players": team,
            "captain": captain,
            "vice_captain": vice_captain
        })

    return jsonify({"teams": response})

if __name__ == "__main__":
    app.run(debug=True)
