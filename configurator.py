import json #derulo

# Try to open the JSON file that contains system configuration settings
try:
    with open("configs.json") as file:
        data = json.load(file) # Load the data into a dictionary

except FileNotFoundError: # Handle error if the config file doesn't exist
        print("Error: JSON File not found!")
except json.JSONDecodeError: # Handle error if the file has invalid JSON formatting
    print("Error: Invalid JSON format!")
except Exception as e: # Handle any other unexpected errors
    print(f"An unexpected error occured: {e}")

# Greet the admin and explain the purpose of the script
print("Hi admin!")
print("I am pretty sure why you are here")
print("Do you want to change configurations of the kWh rate and installation fee?")

# Function to display current configuration settings
def showData(data):
    print(f"kWh Rate: {data['kWhRate']}")
    print(f"Installation Fee: {data['installationFee']}")

# Function to get new values from the admin
def inputData():

    kWhRateConfigure = input("Please input new kWh Rate: ").strip()
    installationFeeConfigure = input("Please input new Installation Fee: ").strip()

    return kWhRateConfigure, installationFeeConfigure

# Function to validate and save the new configurations
def configure():

    while True:
        configurations = inputData()
        kWhRateConfigure, installationFeeConfigure = configurations[0], configurations[1]

        try:
            data['kWhRate'] = float(kWhRateConfigure)
            data['installationFee'] = float(installationFeeConfigure)
            break # Exit loop once valid inputs are given
        except ValueError:
            print("Invalid input! Please enter a numeric value")

    # Save the updated data back to the JSON file
    with open("configs.json", "w") as file:
        json.dump(data, file, indent = 4)

    print("Configurations added!")

while True:
    choice = input("(y) for yes, (n) for no: ").strip().lower()

    if choice == "y":
        showData(data) # Show current values
        configure()    # Allow admin to change values
        break          # Exit loop after configuration
    elif choice == "n":
        exit()         # Exit script if admin doesn't want to configure

    else:              # Handle invalid input (not 'y' or 'n')
        print(f"Invalid input: {choice}")
        print("Please try again!")


