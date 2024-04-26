import random
import string
import database
import pyperclip
import hashlib
import os.path


#hashing the master password via SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def isPasswordStrong(password):
    return len(password) >= 8

def createMasterPass():
    while True:
        masterPass = input("Please enter a master password (REMEMBER THIS PASSWORD AS IT WILL BE USED TO ACCESS THIS APPLICATION): ")
        if not isPasswordStrong(masterPass):
            print("The password must be at 8 characters or greater in length")
            continue
        hashed_password = hash_password(masterPass)
        file_path = "masterpassword.txt"
        with open (file_path, "w") as f:
            f.write(hashed_password)
        print("Master Password has been created, hashed and saved")
        print("")
        break

def verifyMasterPass():
    stored_hash = ""
    with open("masterpassword.txt", "r") as f:
        stored_hash = f.read().strip()
    while True:
        entered_password = input("Please enter the master password: ")
        if hash_password(entered_password) == stored_hash:
            print("Authentication successful!")
            return True  # Return True if authentication is successful
        else:
            break  # Break out of the loop if authentication fails




def options():
    print("Here are the options to choose from: ")
    print("1. Create a password")
    print("2. Add a new password")
    print("3. Update a password")
    print("4. Retrieve a password")
    print("5. Delete a password")
    print("6. Exit")

    choice = input("What would you like to do (select an option from 1-6): ")

    return choice

def createPassword(minLength, numbers = True, specialCharacters = True):

    letters = string.ascii_letters #using all upper and lower case letters
    digits = string.digits         #convert to string
    special = string.punctuation   #speical characters

    characters = letters
    if numbers:
        characters += digits
    if specialCharacters:
        characters += special

    password = ""
    meetsCriteria = False
    hasNumber = False
    hasSpeical = False

    while not meetsCriteria or len(password) < minLength :
        newCharacter = random.choice(characters)
        password += newCharacter

        if newCharacter in digits:
            hasNumber = True
        elif newCharacter in special:
            hasSpeical = True

        meetsCriteria = True
        if numbers:
            meetsCriteria = hasNumber
        if specialCharacters:
            meetsCriteria = meetsCriteria and hasSpeical
    #filename = "passwords.txt"
    #with open(filename, 'a') as file:  # Use 'a' mode for append
        #file.write(password + '\n')  # Append the new password and a newline character
    #print("Password saved to", filename)
    print("")
    print("You password is: ", password)
    print("")
    pyperclip.copy(password)
    print("Password copied to clipboard!")
    print("")
    return password



def addNewPassword():

    application = input("What is the name of the application?: ")
    username = input("What is your username for " + application + "?: ")
    password = input("What is password for " + application + "? ")

    return application, username, password

def updatePassword(conn):
    while True:
        # Retrieve the list of applications from the database
        applications = database.get_all_applications(conn)

        # Show the list of applications
        print("Applications currently stored in the database:")
        for idx, app in enumerate(applications, start=1):
            print(f"{idx}. {app}")

        # Prompt the user to select an application to update
        selected_app = input("Enter the number of the application you want to update: ")
        selected_app = int(selected_app) - 1  # Adjust for 0-based index
        if selected_app < 0 or selected_app >= len(applications):
            print("Invalid selection. Please enter a valid number.")
            continue

        application = applications[selected_app]

        newPass = input("What would you like to change your password to?: ")
        return application, newPass

def retrievePassword(conn):

    while True:
        # Retrieve the list of applications from the database
        applications = database.get_all_applications(conn)

        # Show the list of applications
        print("Applications currently stored in the database:")
        for idx, app in enumerate(applications, start=1):
            print(f"{idx}. {app}")

        # Prompt the user to select an application to update
        selected_app = input("Enter the number of the application which you would like to retrieve the password for: ")
        selected_app = int(selected_app) - 1  # Adjust for 0-based index
        if selected_app < 0 or selected_app >= len(applications):
            print("Invalid selection. Please enter a valid number.")
            continue

        application = applications[selected_app]
        
        return application


def deletePassword(conn):

    while True:
        applications = database.get_all_applications(conn)
    
    # Show the list of applications
        print("Applications currently stored in the database:")
        for idx, app in enumerate(applications, start=1):
            print(f"{idx}. {app}")

        # Prompt the user to select an application to update
        selected_app = input("Enter the number of the application which you would like to delete the password for: ")
        selected_app = int(selected_app) - 1  # Adjust for 0-based index
        if selected_app < 0 or selected_app >= len(applications):
            print("Invalid selection. Please enter a valid number.")
            continue

        application = applications[selected_app]
        
        return application

#function to display the current applications that are stored in the database
def show_applications(conn):
    """
    Display the list of applications stored in the database.
    """
    applications = database.get_all_applications(conn)

    print("Applications currently stored in the database:")
    for idx, app in enumerate(applications, start=1):
        print(f"{idx}. {app}")
def main():
    # Check if the master password file exists
    if not os.path.exists("masterpassword.txt"):
        createMasterPass()

    # Continue asking for authentication until successful
    while True:
        if verifyMasterPass():
            print("Master password verified.")
            break  # Break out of the loop if authentication is successful
        else:
            print("Authentication failed. Please try again.")

    #database connection
    db_file = "passwords.db"
    conn = database.create_connection(db_file)
    if conn is not None:
        database.create_table(conn)
    else:
        print("Error! Cannot create the database connection.")
        return
        
    #Welcome message
    print("")
    print("Hello! Welcome to the password manager.")
    print("")
    
    while True:
        choice = options()
        if choice =='1':

            minLength = int(input("What is the minimum desired length for your password?: "))
            if (minLength < 0):
                print("Password length must be greater than 0")
                minLength = int(input("What is the minimum desired length for your password?: "))
                
            hasNumber = input("Would you like to have numbers in your password? (y/n): ").lower() == "y"
            hasSpecial = input("Would you like to have special characters in your password? (y/n): ").lower() == "y"
            password = createPassword(minLength, hasNumber, hasSpecial)
            saveToDB = input("Do you want to save the password to the database? (y/n): ").lower() == "y"
            if saveToDB:
            # Insert the password into the database
                application = input("Enter the application name: ")
                username = input("Enter your username: ")
                database.insert_password(conn, username, application, password)

                print("")
                print("Your password for", application, "has been saved.")
            else:
                print("Password not saved to the database.")
                print("")
                continue

        if choice =='2':
            application, username, password = addNewPassword()
            applicationUserName = username
            applicationName = application
            applicationPassword = password

            database.add_password(conn, applicationUserName, applicationName, applicationPassword)
            print("Your password for", applicationName, "has been added.")
            print("")

        if choice =='3':
            updatedApp, updatedPass = updatePassword(conn)
            if updatedApp is not None:  # Check if updatedApp is not None
                database.update_password(conn, updatedApp, updatedPass)
                print("Your password for", updatedApp, "has been saved.")
                print("")
            else:
                print("Update password operation canceled.")

        if choice =='4':
            retApplication = retrievePassword(conn)
            retPass = database.get_password(conn,retApplication)

            print("The password for", retApplication, "is", retPass,".")
            print("")


        if choice =='5':
            delApp = deletePassword(conn)
            database.delete_password(conn,delApp)

            print("The password for", delApp, "has been deleted.")
            print("")

        if choice =='6':
            conn.close()
            print("You have exited this application. Thank you for using the password manager")
            print("")
            break

    


if __name__ == "__main__":
    main()