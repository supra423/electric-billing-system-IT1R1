import json

try:
    with open("configs.json") as file:
        data = json.load(file)

except FileNotFoundError:
        print("Error: JSON File not found!")
except json.JSONDecodeError:
    print("Error: Invalid JSON format!")
except Exception as e:
    print(f"An unexpected error occured: {e}")

print("Hi admin!")
print("I am pretty sure why you are here")
print("Do you want to change configurations of the kWh rate and installation fee?")

def showData(data):
    print(f"kWh Rate: {data['kWhRate']}")
    print(f"Installation Fee: {data['installationFee']}")

def inputData():

    kWhRateConfigure = input("Please input new kWh Rate: ").strip()
    installationFeeConfigure = input("Please input new Installation Fee: ").strip()

    return kWhRateConfigure, installationFeeConfigure

def configure():

    while True:
        configurations = inputData()
        kWhRateConfigure, installationFeeConfigure = configurations[0], configurations[1]

        try:
            data['kWhRate'] = float(kWhRateConfigure)
            data['installationFee'] = float(installationFeeConfigure)
            break
        except ValueError:
            print("Invalid input! Please enter a numeric value")

    with open("configs.json", "w") as file:
        json.dump(data, file, indent = 4)

    print("Configurations added!")

while True:
    choice = input("(y) for yes, (n) for no: ").strip().lower()

    if choice == "y":
        showData(data)
        configure()
        break
    elif choice == "n":
        exit()

    else:
        print(f"Invalid input: {choice}")
        print("Please try again!")


