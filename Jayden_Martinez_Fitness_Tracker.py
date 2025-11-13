# 1. Required libraries to properly function
import json
import os

USER_DATA_FILE = "user_data.json"

if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "r") as f:
        Username_Bank = json.load(f)
else:
    Username_Bank = {}

# Saves repeated user data using a JSON file for future sessions
def save_user_data():
    with open(USER_DATA_FILE, "w") as f:
        json.dump(Username_Bank, f)

# Manager for logging weights and goal tracking updates
def daily_log():
    print("\n--- Daily Log ---")
    Username = input("Username: ")
    is_new_user = False

    if Username in Username_Bank:
        print(f"Welcome back, {Username}!")
        user = Username_Bank[Username]
        Current_Weight = float(input("Enter your current weight (lbs): "))
        user["Weight_Log"].append(Current_Weight)

        Starting_Weight = user["Starting_Weight"]
        Goal_Weight = user["Goal_Weight"]
        Timeframe_Weeks = user["Timeframe_Weeks"]
        Current_Week = user["Current_Week"]

        Total_Weight_Change = Goal_Weight - Starting_Weight
        Weekly_Target_Change = Total_Weight_Change / Timeframe_Weeks
        Expected_Weight = Starting_Weight + (Weekly_Target_Change * Current_Week)

        # FIX: read last item instead of pop()/append() so the list isn't mutated
        weight_difference = user["Weight_Log"][-1] - Starting_Weight
        Protein_Target = round(Starting_Weight + weight_difference)

        print(f"Week {Current_Week} check-in:")
        print(f"Your target weight this week was {Expected_Weight:.2f} lbs.")
        print(f"You should aim to gain/lose {Weekly_Target_Change:.2f} lbs this week.")
        print(f"Your protein intake goal is {Protein_Target}g per day.")

        if (Total_Weight_Change > 0 and Current_Weight >= Goal_Weight) or (Total_Weight_Change < 0 and Current_Weight <= Goal_Weight):
            print("Congratulations! You reached your goal weight! Do you want to make a new goal?")
            reset = input("Enter Y to create a new goal or any other key to keep your current data: ").strip().lower()
            if reset == 'y':
                Starting_Weight = Current_Weight
                Goal_Weight = float(input("Enter your new goal weight (lbs): "))
                Timeframe_Weeks = int(input("Enter your new timeframe in weeks: "))
                Current_Week = 1
                Weight_Log = [Current_Weight]

                user["Starting_Weight"] = Starting_Weight
                user["Goal_Weight"] = Goal_Weight
                user["Timeframe_Weeks"] = Timeframe_Weeks
                user["Current_Week"] = Current_Week
                user["Weight_Log"] = Weight_Log

                print("Your new goal has been set!")

        elif Total_Weight_Change > 0 and Current_Weight >= Expected_Weight:
            print("Excellent job this week! Keep going!")
        elif Total_Weight_Change < 0 and Current_Weight <= Expected_Weight:
            print("Excellent job this week! Keep going!")
        elif abs(Current_Weight - Expected_Weight) <= 1:
            print("You’re on track! Don’t stop!")
        elif Total_Weight_Change > 0:
            print("You need to increase your calorie intake.")
        else:
            print("You need to reduce or supplement your calorie intake with healthier alternatives.")

        user["Current_Week"] += 1
        save_user_data()
        print(f"Daily log for week {user['Current_Week'] - 1} complete.\n")

    else:
        print(f"Greetings, {Username}!")
        Starting_Weight = float(input("Enter your weight (lbs): "))
        Goal_Weight = float(input("Enter your goal weight (lbs): "))
        Timeframe_Weeks = int(input("Enter your timeframe in weeks (e.g. 26 = 6 months, 52 = 12 months): "))
        Current_Week = 1
        Weight_Log = []

        Current_Weight = Starting_Weight
        Weight_Log.append(Current_Weight)

        user = {
            "Starting_Weight": Starting_Weight,
            "Goal_Weight": Goal_Weight,
            "Timeframe_Weeks": Timeframe_Weeks,
            "Current_Week": Current_Week,
            "Weight_Log": Weight_Log
        }
        Username_Bank[Username] = user
        save_user_data()
        is_new_user = True

        Total_Weight_Change = Goal_Weight - Starting_Weight
        Weekly_Target_Change = Total_Weight_Change / Timeframe_Weeks
        Expected_Weight = Starting_Weight + (Weekly_Target_Change * Current_Week)
        Protein_Target = round(Expected_Weight * 1)

        print(f"To reach your goal of {Goal_Weight} lbs in {Timeframe_Weeks} weeks, you should aim to gain/lose {Weekly_Target_Change:.2f} lbs per week.")
        print(f"For Week {Current_Week}, your target weight is {Expected_Weight:.2f} lbs.")
        print(f"Your protein target is about {Protein_Target}g per day.")
        print("Come back next week to check your progress!")

        user["Current_Week"] += 1
        save_user_data()
        print(f"Daily log for week {user['Current_Week'] - 1} complete.\n")

# Calculate weight gain or loss each week to reach desired goal
def weekly_weight_change_calculator():
    print("\n--- Weekly Weight Change Calculator ---")
    Current_Weight = float(input("Enter your current weight (lbs): "))
    Goal_Weight = float(input("Enter your goal weight (lbs): "))
    Weeks = int(input("Enter your timeframe in weeks: "))

    Weight_Change = Goal_Weight - Current_Weight
    Weekly_Change = Weight_Change / Weeks

    print(f"You need to gain or lose {Weekly_Change:.2f} lbs per week to reach your goal.\n")

# Calculate protein intake for each week to reach desired goal
def weekly_protein_intake_calculator():
    print("\n--- Weekly Protein Intake Calculator ---")
    Current_Weight = float(input("Enter your current weight (lbs): "))
    Goal_Weight = float(input("Enter your goal weight (lbs): "))
    Weeks = int(input("Enter your timeframe in weeks (e.g. 26 = 6 months, 52 = 12 months): "))

    Weekly_Weight_Change = (Goal_Weight - Current_Weight) / Weeks

    for week in range(1, Weeks + 1):
        Projected_Weight = Current_Weight + (Weekly_Weight_Change * week)
        Protein_Target = round(Projected_Weight * 1)
        print(f"Week {week}: Target weight = {Projected_Weight:.2f} lbs, Target protein intake = {Protein_Target}g per day")
    print()

# Main menu loop (logging data, calculators, or exit)
while True:
    print("\nFitness Tracker: Select an option")
    print("1 = Daily Log")
    print("2 = Weekly Weight Change Calculator")
    print("3 = Weekly Protein Intake Calculator")
    print("4 = Exit")

    Menu_input = input("Enter choice (1, 2, 3, or 4): ")

    if Menu_input == "1":
        daily_log()
    elif Menu_input == "2":
        weekly_weight_change_calculator()
    elif Menu_input == "3":
        weekly_protein_intake_calculator()
    elif Menu_input == "4":
        print("Goodbye!")
        break
    else:
        print("Try again. Choose 1, 2, 3, or 4.\n")
