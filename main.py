
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/Users/sharmae/PycharmProjects/FBLA2023/Resources/fbla-2023-firebase-adminsdk-hicji-8387b1c4e7.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Admin Portal that allows admin to access capabilities
def admin_portal():
    print("Welcome to the Admin Portal! You have access to all your admin capabilities here.\n")
    print("1. Create an Event")
    print("2. See Event Information")
    print("3. Add a Prize")
    print("4. Generate Student Report")
    print("5. Pick Random Winner")
    print("6. Pick Top Point Student")
    print("7. Remove Event")
    print("8. Remove Prize")
    print("9. Return Home")
    adminPortalOptionSelected = input("\nPlease select an option from the following list by entering the corresponding number\n--> ")

    # Allows admin to create an event
    if adminPortalOptionSelected == "1":

        event_count = str(len(db.collection(u'Events').get()))
        print("")
        eventName = input("Please enter the event's name --> ")
        eventDate = input("Please enter the event's date (mm/dd/YYYY) --> ")
        eventSporting = input("Is this event a sporting event? (y/n) --> ")
        if eventSporting == "y":
            eventSporting = True
        else:
            eventSporting = False
        eventPoints = input("How many points would you like this event to be worth? --> ")

        event_ref = db.collection(u'Events').document(event_count)
        event_ref.set({"eventName": eventName, "eventDate": eventDate, "points": int(eventPoints), "sportingEvent": eventSporting, "studentsNameAttended" : [""]})
        print("\nSuccessfully created new event! Returning to Admin Portal...")
        admin_portal()

    # Allows admin to see a specific event's information
    elif adminPortalOptionSelected == "2":
        print("")
        events_list = []
        events_count = len(db.collection(u'Events').get())
        for i in range(events_count):

            event_ref = db.collection(u'Events').document(str(i))
            event = event_ref.get()
            event_data = event.to_dict()

            if event.exists:
                events_list.append(event_data)
                eventNameRead = event_data['eventName']
                eventDateRead = event_data['eventDate']
                eventPointsRead = str(event_data['points'])
                sportingEvent = event_data['sportingEvent']

                if sportingEvent == True:
                    sportingEvent = " |**SPORTING EVENT**"
                else:
                    sportingEvent = ""

                print(
                    str(i + 1) + ". " + eventNameRead + " on " + eventDateRead + sportingEvent + "| " + eventPointsRead + " points")

            else:
                print('\nERROR. Returning to Admin Portal...')
                admin_portal()

        adminEventSelection = input(
            "\nPlease select the event you want information about from the following list by entering the corresponding number\n--> ")

        selected_event_ref = db.collection('Events').where('eventName', '==',
                                                           events_list[int(adminEventSelection) - 1][
                                                               'eventName']).get()
        for event in selected_event_ref:
            selected_event_data = event.to_dict()
            print("Event Name: " + selected_event_data['eventName'])
            print("Event Date: " + selected_event_data['eventDate'])
            print("Event Points: " + str(selected_event_data['points']))
            print("Sporting Event? (t/f): " + str(selected_event_data['sportingEvent']))
            selected_event_students_attended = selected_event_data['studentsNameAttended']
            print("Students Attended:")
            if len(selected_event_students_attended) == 1:
                print("None")
            else:
                for i in range(len(selected_event_students_attended)):
                    if i != 0:
                        print(str(i) + ". " + selected_event_students_attended[i])

        print("\nReturning to Admin Portal...")
        admin_portal()

    # Allows admin to add a prize
    elif adminPortalOptionSelected == "3":

        prize_count = str(len(db.collection(u'Prizes').get()))

        prizeName = input("Please enter the name of the prize --> ")
        prizePoints = input("What are the minimum amount of points to win this prize? --> ")
        prizeType = input("What type of prize is it? (school, food, spirit, or other) --> ")

        prize_ref = db.collection(u'Prizes').document(prize_count)
        prize_ref.set({"prizeName": prizeName, "prizePoints": int(prizePoints), "prizeType": prizeType})
        print("\nSuccessfully created new prize! Returning to Admin Portal...")
        admin_portal()

    # Allows admin to generate student report
    elif adminPortalOptionSelected == "4":
        print("\n~~~Student Report~~~\n")

        students_count = len(db.collection(u'StudentReport').get())
        for i in range(students_count):
            if i != 0:

                student_ref = db.collection(u'StudentReport').document(str(i))
                student = student_ref.get()
                student_data = student.to_dict()

                if student.exists:
                    print("----- Student: " + student_data['studentName'] + " ----- Grade: " + student_data['studentGrade'] + " ----- " + str(student_data['studentsPoints']) + " points -----")


                else:
                    print('\nERROR. Returning to Admin Portal...')
                    admin_portal()

        print("\nReturning to Admin Portal...")
        admin_portal()

    # Allows admin to pick random winner from a desired grade or all grades
    elif adminPortalOptionSelected == "5":
        import random
        student_desired_grade = input("\nWhat grade would you like to pick a random winner from (9/10/11/12/all) --> ")

        students_list = []
        if student_desired_grade != "all":

            filtered_student_ref = db.collection('StudentReport').where('studentGrade', '==', student_desired_grade).stream()
            for student in filtered_student_ref:
                if student.id != "0":
                    student_data = student.to_dict()
                    students_list.append(student_data['studentName'])

            print("Randomly chosen student winner from grade " + student_desired_grade + ": " + random.choice(students_list))

            print("\nReturning to Admin Portal...")
            admin_portal()

        elif student_desired_grade == "all":
            students_count = len(db.collection(u'StudentReport').get())
            for i in range(students_count):
                if i != 0:

                    student_ref = db.collection(u'StudentReport').document(str(i))
                    student = student_ref.get()
                    student_data = student.to_dict()

                    if student.exists:

                        students_list.append(student_data['studentName'])

                    else:
                        print('\nERROR. Returning to Admin Portal...')
                        admin_portal()

            print("Randomly chosen student winner from all grades"  + ": " + random.choice(
                students_list))

            print("\nReturning to Admin Portal...")
            admin_portal()

        else:
            print('\nERROR. Returning to Admin Portal...')
            admin_portal()

    # Allows admin to pick top point student from a desired grade or all grades
    elif adminPortalOptionSelected == "6":

        student_desired_grade = input("\nWhat grade would you like to pick the top point accumulator from (9/10/11/12/all) --> ")

        students_points_list = []
        students_names_list = []

        if student_desired_grade != "all":

            filtered_student_ref = db.collection('StudentReport').where('studentGrade', '==', student_desired_grade).stream()
            for student in filtered_student_ref:
                if student.id != "0":
                    student_data = student.to_dict()
                    students_points_list.append(student_data['studentsPoints'])
                    students_names_list.append(student_data['studentName'])

            max_points = max(students_points_list)
            index_val = str([index for index, item in enumerate(students_points_list) if item == max_points])
            index_filtered_val = index_val[1:2]
            print("Student with highest points in grade " + student_desired_grade + ": " + students_names_list[int(index_filtered_val)] + " with " + str(max_points) + " points!")


            print("\nReturning to Admin Portal...")
            admin_portal()


        elif student_desired_grade == "all":

            students_count = len(db.collection(u'StudentReport').get())

            for i in range(students_count):

                if i != 0:

                    student_ref = db.collection(u'StudentReport').document(str(i))

                    student = student_ref.get()

                    student_data = student.to_dict()

                    if student.exists:

                        students_points_list.append(student_data['studentsPoints'])
                        students_names_list.append(student_data['studentName'])


                    else:

                        print('\nERROR. Returning to Admin Portal...')

                        admin_portal()

            max_points = max(students_points_list)
            index_val = str([index for index, item in enumerate(students_points_list) if item == max_points])
            index_filtered_val = index_val[1:2]
            print("Student with highest points: " + students_names_list[int(index_filtered_val)] + " with " + str(max_points) + " points!")

            print("\nReturning to Admin Portal...")

            admin_portal()


        else:

            print('\nERROR. Returning to Admin Portal...')

            admin_portal()

    # Allows admin to remove an event
    elif adminPortalOptionSelected == "7":
        event_count = str(len(db.collection(u'Events').get()))
        print("")
        for i in range(int(event_count)):
            if i != 0:
                event_ref = db.collection(u'Events').document(str(i))
                event_doc = event_ref.get()
                event_name = event_doc.to_dict()["eventName"]
                print(str(i) + ". " + event_name)
        remove_event_option = input("Please select the event you would like to remove by entering the corresponding number \n--> ")
        remove_event_ref = db.collection(u'Events').document(remove_event_option)
        remove_event_ref.delete()

        print("\n Successfully removed! Returning to Admin Portal...")
        admin_portal()

    # Allows admin to remove a prize
    elif adminPortalOptionSelected == "8":
        prize_count = str(len(db.collection(u'Prizes').get()))
        print("")
        for i in range(int(prize_count)):
            if i != 0:
                prize_ref = db.collection(u'Prizes').document(str(i))
                prize_doc = prize_ref.get()
                prize_name = prize_doc.to_dict()["prizeName"]
                print(str(i) + ". " + prize_name)
        remove_prize_option = input("Please select the prize you would like to remove by entering the corresponding number \n--> ")
        remove_prize_ref = db.collection(u'Prizes').document(remove_prize_option)
        remove_prize_ref.delete()

        print("\n Successfully removed! Returning to Admin Portal...")
        admin_portal()

    # Allows admin to go back to home page
    elif adminPortalOptionSelected == "9":
        print("\nReturning to Home Page...")
        home()

    # Admin stays in portal if they input an invalid option
    else:
        admin_portal()


def admin_login():

    # Loads admin credentials
    print("\nRock Canyon High School Admin Login")
    doc_count = len(db.collection(u'AdminCredentials').get())

    if doc_count > 1:

        doc_ref = db.collection(u'AdminCredentials').document(u'1')
        doc = doc_ref.get()
        data = doc.to_dict()

        if doc.exists:
            userRead = data['user']
            schoolCodeRead = data['schoolCode']

        else:
            print('\nERROR. Returning to Admin Page...')
            admin_login()


        print("1. Admin Login")
        print("2. Reset Code")
        print("3. Delete Credentials")
        print("4. Return Home")
        adminOptionSelected = input("\nPlease select an option from the following list by entering the corresponding number\n--> ")

        # Allows admin to login by entering credentials
        if adminOptionSelected == "1":
            print("\nPlease enter your Admin Login Credentials")
            user = input("user: ")
            schoolCode = input("school code: ")

            if user == userRead and schoolCode == schoolCodeRead:
                print("\nAdmin Login Successful! Directing to admin portal...")
                admin_portal()
            else:
                print("\nLogin FAILED. Returning to Admin Page...")
                admin_login()

        # Allows admin to reset school code if it needs to be changed or is forgotten
        elif adminOptionSelected == "2":
            print("\nPlease enter your Admin Login USER Credential")
            userCodeReset = input("user: ")

            if userCodeReset == userRead:
                print("\nUser Credential Verification Successful")
                newSchoolCode = input("Please enter your new school code\n--> ")
                doc_ref.update({"schoolCode": newSchoolCode})
                print("\nReturning to Admin Page...")
                admin_login()
            else:
                print("\nUser Credential Verification FAILED. Returning to Admin Page...")
                admin_login()

        # Admin cannot reset user credential, so this option allows them to delete their credentials if needed
        elif adminOptionSelected == "3":
            print("\nPlease validate your Admin Credentials to delete your account")
            userDelete = input("user: ")
            schoolCodeDelete = input("school code: ")
            if userDelete == userRead and schoolCodeDelete == schoolCodeRead:
                print("\nDeleting Account...")
                doc_ref.delete()
                print("Returning to Home Page")
                home()
            else:
                print("\nCould not validate Admin Credentials. Returning to Admin Page...")
                admin_login()

        # Allows admin to return to home page
        elif adminOptionSelected == "4":
            print("\nReturning to Home Page...")
            home()

        # Admin stays in login page if they input an invalid option
        else:
            admin_login()


    else:

        # If admin has not already created login credentials, they can create it here
        createLogin = input("\nLooks like you don't have login credentials. Would you like to create them? (y/n)\n--> ")
        if createLogin == "y":
            print("Please create an admin account by entering identifying credentials")
            createUser = input("create user: ")
            createSchoolCode = input("create school code: ")
            doc_ref = db.collection(u'AdminCredentials').document(u'1')
            doc_ref.set({"user": createUser, "schoolCode": createSchoolCode})

            print("\nAdmin Account Successfully Created. Directing to Admin Page...")
            admin_login()
        elif createLogin == "n":
            print("Returning to Home Page...")
            home()
        else:
            print("ERROR. Returning to Admin Page...")
            admin_login()

def student_portal(student_name, student_grade):
    print("\nWelcome " + student_name + "!\n")
    print("1. School Event Check-In")
    print("2. View Prizes Earned")
    print("3. View Profile and Points")
    print("4. Return Home")
    studentOptionSelected = input(
        "\nPlease select an option from the following list by entering the corresponding number\n--> ")

    # Allows student to check-in to created school events
    if studentOptionSelected == "1":
        print("")
        events_list = []
        events_count = len(db.collection(u'Events').get())
        for i in range(events_count):

            event_ref = db.collection(u'Events').document(str(i))
            event = event_ref.get()
            event_data = event.to_dict()

            if event.exists:
                events_list.append(event_data)
                eventNameRead = event_data['eventName']
                eventDateRead = event_data['eventDate']
                eventPointsRead = str(event_data['points'])
                sportingEvent = event_data['sportingEvent']

                if sportingEvent == True:
                    sportingEvent = " |**SPORTING EVENT**"
                else:
                    sportingEvent = ""

                print(str(i+1) + ". " + eventNameRead + " on " + eventDateRead + sportingEvent + "| " + eventPointsRead + " points")

            else:
                print('\nERROR. Returning to Student Portal...')
                student_portal(student_name, student_grade)

        studentEventSelection = input("\nPlease select the event you are attending from the following list by entering the corresponding number\n--> ")

        current_student_ref = db.collection('StudentReport').where('studentName', '==', student_name).stream()
        for student in current_student_ref:
            student_doc_id = student.id
            current_student_data = student.to_dict()
            current_student_points = current_student_data['studentsPoints']
            current_student_name = current_student_data['studentName']

        new_point_val = current_student_points + events_list[int(studentEventSelection) - 1]['points']

        db.collection('StudentReport').document(student_doc_id).update({'studentsPoints': new_point_val})


        selected_event_students_attended = []

        selected_event_ref = db.collection('Events').where('eventName', '==', events_list[int(studentEventSelection) - 1]['eventName']).get()
        for event in selected_event_ref:
            event_doc_id = event.id
            selected_event_data = event.to_dict()
            selected_event_students_attended = selected_event_data['studentsNameAttended']

        selected_event_students_attended.append(current_student_name)

        db.collection('Events').document(event_doc_id).update({'studentsNameAttended': selected_event_students_attended})

        print("Successfully checked-in! Returning to Student Portal...")
        student_portal(student_name, student_grade)

    # Allows student to view the prizes they have earned from their points
    elif studentOptionSelected == "2":
        print("\nPrizes you have won for your points:")
        current_student_ref = db.collection('StudentReport').where('studentName', '==', student_name).stream()
        for student in current_student_ref:
            current_student_data = student.to_dict()
            current_student_points = current_student_data['studentsPoints']

        prizes_list = []
        prizes_count = len(db.collection(u'Prizes').get())
        for i in range(prizes_count):

            prize_ref = db.collection(u'Prizes').document(str(i))
            prize = prize_ref.get()
            prize_data = prize.to_dict()

            if prize.exists:
                prizePointsRead = prize_data['prizePoints']
                if int(current_student_points) >= int(prizePointsRead):
                    prizeNameRead = prize_data['prizeName']
                    prizeTypeRead = prize_data['prizeType']
                    prizes_list.append(prizeNameRead + " (Prize Type: " + prizeTypeRead + ")")

            else:
                print('\nERROR. Returning to Student Portal...')
                student_portal(student_name, student_grade)

        if len(prizes_list) == 0:
            print("No prizes yet. Get more points to get prizes!")
        else:
            for i in range (len(prizes_list)):
                print(prizes_list[i])

        print("\n Returning to Student Portal...")
        student_portal(student_name, student_grade)

    # Allows student to view their profile information and the points they have received
    elif studentOptionSelected == "3":
        current_student_ref = db.collection('StudentReport').where('studentName', '==', student_name).stream()
        for student in current_student_ref:
            current_student_data = student.to_dict()
            current_student_name = current_student_data['studentName']
            current_student_grade = current_student_data['studentGrade']
            current_student_points = current_student_data['studentsPoints']

        print("\nYour Name: " + current_student_name)
        print("Your Grade: " + str(current_student_grade))
        print("Your Points: " + str(current_student_points))

        print("\n Returning to Student Portal...")
        student_portal(student_name, student_grade)

    # Allows student to return to the Home Page
    elif studentOptionSelected == "4":
        print("Returning to Home Page...")
        home()

    # Student stays in student portal if they input an invalid option
    else:
        print('\nERROR. Returning to Student Portal...')
        student_portal(student_name, student_grade)


def student_login():

    # Students can sign-in to their existing account by inputting their name and grade. They will have an account
    # automatically created for them if they do not have one
    students_list = []
    student_grades_list = []
    print("\n~~Sign in to your student account~~")
    studentName = input("What is your name? --> ")
    studentGrade = input("What grade are you in? --> ")

    student_count = len(db.collection(u'StudentReport').get())
    for i in range(student_count):
        student_ref = db.collection(u'StudentReport').document(str(i))
        student = student_ref.get()
        data = student.to_dict()

        if student.exists:
            studentNameRead = data['studentName']
            studentGradeRead = data['studentGrade']
            students_list.append(studentNameRead)
            student_grades_list.append(studentGradeRead)


        else:
            print('\nERROR. Returning to Home Page...')
            home()

    if studentName not in students_list:
        students_ref = db.collection(u'StudentReport').document(str(student_count))
        students_ref.set({"studentName": studentName, "studentsPoints": 0, "studentGrade": studentGrade})
        print("\nCreating your account... Redirecting you to Student Portal...")
        student_portal(studentName, studentGrade)
    else:
        if studentGrade in student_grades_list:
            print("\nSigning you in... Redirecting you to Student Portal...")
            student_portal(studentName, studentGrade)
        else:
            print('\nERROR. Returning to Home Page...')
            home()

def select_option():

    # Allows user to select options from the Home Page, and navigates to respective pages
    userHomeSelection = input(
        "\nPlease select an option from the following list by entering the corresponding number\n--> ")

    if userHomeSelection == "1":
        student_login()
    elif userHomeSelection == "2":
        admin_login()
    elif userHomeSelection == "3":
        print("Thank you for using Rock Canyon High School Event Tracker!")
    else:
        print("Error - Invalid option selected")
        select_option()


def home():

    # Main Home Page with options for pages
    print("")
    print("                 ~~~Welcome to the Rock Canyon High School Event Tracker!~~~")
    print("1. Student Page")
    print("2. Admin Page")
    print("3. Quit Program")

    select_option()

# Run Program
home()



