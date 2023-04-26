import os, json, logging, time, re

from logging.handlers import TimedRotatingFileHandler

log_directory = "data/logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_filename = os.path.join(log_directory, time.strftime("%d-%m-%y-%I-%M-%S")+".log")
handler = TimedRotatingFileHandler(log_filename, when="midnight", backupCount=7)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log(message):
    '''Logs a specified message'''
    logging.info(message)

def get_answer(question):
    # A custom "input" to prevent exceptions on CTRL + thing
    try:
        answer = input(question)
        return answer
    except KeyboardInterrupt:
        application.exit()

from data.datatable.new_project_dt import new_project_dt
log("new_project_dt imported from data.datatable.new_project_dt")
from data.datatable.appdata import appdata as appdata_dt
log("appdata imported from data.datatable.appdata")
from data.datatable.highestprojtrack import highest_project_tracker_dt
log("highest_project_tracker_dt imported from data.datatable.highestprojtrack")

class application:
    def exit():
        '''A Custom exit program. Handles all of our intricacies.'''
        try:
            os.system("cls" if os.name == "nt" else "clear")
        except KeyboardInterrupt:
            print("Wow, you're quick! You entered CTRL + C again before we could even clear the console!")
        try:
            if application.preferences.get_askexit() == True:
                handling = get_answer("Are you sure you want to exit this program? Y/N: ")
                if handling.lower() == "n":
                    print("Got it, sending you back")
                    pass
                elif handling.lower() == "y":
                    print("Understood, Exiting program...")
                    exit()
                else:
                    print("Invalid input. Please try again.")
            else:
                exit()
        except KeyboardInterrupt:
            exit()

    def Action_Handler(request):
        log("Raw Request: " + request)
        request = str(request).lower()
        current_projects = application.json.getvalue(key="managed_projects", json_dir="data/appdata.json", default=None, dt=appdata_dt)        

        # Clears the console upon request (Done)
        if any(request.startswith(s) for s in ["cls", "clear this shit", "clear"]):
            log("Received 'cls' request")
            print("CLS in request. Clearing console.")
            application.sleep(0.3)
            os.system("cls" if os.name == "nt" else "clear")
            return True

        # Handles exiting (Done)
        elif any(request.startswith(s) for s in ["-exit", "-quit"]) or request in ["exit", "quit"]:
            log("Received 'exit' or 'quit' request")
            application.exit()

        # Handles view/select requests (Done)
        elif any(request.startswith(s) for s in ["-view", "--view", "-select", "--select", "-display", "--display", "-v", "--v", "-d", "--d", "-s", "--s"]):
            log("Received 'view' request")
            current_projects = application.json.getvalue(key="managed_projects", json_dir="data/appdata.json", default=None, dt=appdata_dt)

            # if request is == to any of the above checks, it will ask for a project name
            if any(request.startswith(s) and request.endswith(s) for s in ["-view", "--view", "-select", "--select", "-display", "--display", "-v", "--v", "-d", "--d", "-s", "--s"]):
                while True:
                    application.projects.print_all()
                    request = get_answer("Which project would you like to view? (name or number) : ")
                    if request != " " or "" or None:
                        break

            arg_result_1 = application.arguments.get_arg(arg="name", request=request)
            arg_result_2 = application.arguments.get_arg(arg="id", request=request)
            arg_result_3 = application.arguments.get_arg(arg="project", request=request)

            if arg_result_1 != False:
                for project in current_projects:
                    project = str(project)
                    if project.lower() in arg_result_1.lower():
                        application.projects.select(project_id=project)
                        return True
            elif arg_result_2 != False:
                for project in current_projects:
                    project = str(project)
                    if project.lower() in arg_result_2.lower():
                        application.projects.select(project_id=project)
                        return True
            elif arg_result_3 != False:
                for project in current_projects:
                    project = str(project)
                    if project.lower() in arg_result_3.lower():
                        application.projects.select(project_id=project)
                        return True


            # checks if the request is for a specific project without an arg
            for project in current_projects:
                if project.lower() in request.lower():
                    application.projects.select(project_id=project)
                    return True
            # End of handling

        # Handles new project requests (Done)
        elif any(request.startswith(s) for s in ["-new", "--new", "-n", "--n", "-create", "--create", "-c", "--c"]):
            # Prepares for checking if the project already exists
            current_projects = application.json.getvalue(key="managed_projects", json_dir="data/appdata.json", default=None, dt=appdata_dt)
            # actually checks it
            for project in current_projects:
                if str(project).lower() in request[7:]:
                    print("Sorry, that project already exists!")
                    return False

            # Prepares for checking if the project name is banned
            banned_names = application.json.getvalue("banned_names", json_dir="data/appdata.json", default=None, dt=appdata_dt)
            if banned_names == None:
                banned_names = [" ", ""]

            # Handles finding the name arg. Always runs
            if True:
                name = application.arguments.get_arg(arg="name", request=request)
                description = application.arguments.get_arg(arg="description", request=request)


            application.projects.create(name, description)



        else:
            del current_projects
            return False
        del current_projects

    def runsetup():
        # welcomes the new user
        print("Hello! Welcome new user to "+name_of_app+"! Lets go through the basic setup!\n")
        application.sleep(5)

        # Handles "Impatience" Mode
        impatience = get_answer("Would you like to enable impatience mode?\nThis mode disables all unneeded delays\nbut can make the app a bit harder to confront in my opinion\nYou can always toggle this by typing 'darin-settings' then 'impatience (on/off)'\n\nWould you like impatience 'On' or 'Off'? : ")

        # F in impatience for "oFF"
        if "f" in impatience:
            impatience = True
        # N in impatience for "oN"
        elif "n" in impatience:
            impatience = False

        application.json.setvalue(
            json_dir="data/appdata.json",
            value=impatience,
            dt=appdata_dt,
            key="preferences.impatience"
        )

        del impatience
        print("Thanks! I'll remember that.\n")
        application.sleep(2)
        print("Now, lets setup if you want us to ask if you want to exit!\n")
        askexit = input("Normally, when you want to exit, you'd enter CTRL + C or type exit or quit and then we'd ask if you actually wanted to exit.\nThis setting bypasses that and just exits the program.\n\nWould you like us to ask first? (Y/N): ")

        askexit = askexit.lower()
        if "n" in askexit:
            askexit = False
        elif "y" in askexit:
            askexit = True

        application.json.setvalue(
            json_dir="data/appdata.json",
            value=askexit,
            dt=appdata_dt,
            key="preferences.askexit"
        )

        application.sleep(2)
        # Updates the fact that the user is no longer a first start
        application.json.setvalue(
            json_dir="data/appdata.json",
            value=False,
            dt=appdata_dt,
            key="first_start"
        )
        print("Great! Everything is setup! However, before we start we should go over a piece of important information.\nWithout knowing this, you may not be able to use the app properly.\n")
        while True:
            answer = get_answer("Tell me the information! (Yes/No) : ")
            answer = answer.lower()
            if answer == "yes":
                print("\n\nOk! So the app uses something called 'args' to perform certain tasks.")
                print('For example, if you wanted to create a new project, you would want to type\n``-create name:"Fanceh Calculator" description:"A calculator that can do fancy things"``')
                get_answer("\nPress enter to continue...\n")
                print("The args are the things after the command. In this case, the args are 'name:\"Fanceh Calculator\"' and 'description:\"A calculator that can do fancy things\"'.")
                print("The command is the thing that tells the app what to do. In this case, the command is 'create' with a \"-\" at the start to signify that it is a Command.")
                get_answer("Press enter to continue...")
                print("Ok, That's about it. Have fun!")
                application.sleep(3)
                break
            elif answer == "no":
                print("Here be dragons!")
                application.sleep(5)
                os.system("cls" if os.name == "nt" else "clear")
                break
            else:
                print("Please answer with either 'Yes' or 'No'.")
    # End of new user handling  

    def sleep(length):
        impatience = application.json.getvalue(
            key="preferences.impatience",
            json_dir="data/appdata.json",
            default=False,
            dt=appdata_dt
        )
        if impatience == True:
            time.sleep(float(length))
        else:
            return False

    class preferences:
        def get_askexit():
            askexit = application.json.getvalue(
                key="preferences.askexit",
                json_dir="data/appdata.json",
                default=True,
                dt=appdata_dt
            )
            return askexit

    class arguments:
        def get_arg(arg, request):
            """
            Extracts the value of an argument with the specified name from a request string.
            
            Arguments:
            - arg: str, the name of the argument to extract
            - request: str, the request string containing the argument
            
            Returns:
            - str or False, the value of the argument if it is found in the request string, 
              or False if the argument is not found
            """
            # Search for the argument pattern in the request string
            match = re.search(f'{arg}:[\'"]([^\'"]*)[\'"]', request)
            
            # If the pattern is found, return the argument value
            if match:
                return match.group(1)
            
            if arg+'"' in request or arg+"'" in request:
                print("You may have forgotten a : after the argument name.")
            if arg+":" in request:
                print("You may have forgotten to put the argument value in quotes.")
            
            # If the pattern is not found, return False
            return False

    class projects:
        def print_all():
            current_projects = application.json.getvalue(key="managed_projects", json_dir="data/appdata.json", default=None, dt=appdata_dt)
            iterance = 1
            try:
                proj = current_projects[0]
                for i in proj:
                    del i
                else:
                    empty = False
            except:
                empty = True
            
            if empty == False:
                print("/   /   /   /   /   /   /   /")
                for project in current_projects:
                    print(f"Project {str(iterance)}: " + project+"\n/   /   /   /   /   /   /   /")
                    iterance = int(iterance) + 1
            else:
                print("No projects found!")

        def select(project_id):
            application.sleep(1.5)
            print("Project selected. What would you like to do?")
            print("1. Select ToDo List")
            print("2. Select reminders")
            print("3. Select notes")
            print("Please select the number of the option you would like to select.")
            while True:
                choice = get_answer("Enter choice: ")
                for i in choice:
                    # Can't use try-except because it causes problems T.T
                    # And if I can, I can't be fucked figuring it out.
                    if i not in ["1", "2", "3"]:
                        print("Invalid input.")
                else:
                    # If it gets to here, then its a valid input.
                    break
            # Handles TodoList
            if choice == "1":
                todo_list = application.projects.todo.get_todo(project_name=project_id)
                print("Got it, selected to-do list!")
                while True:
                    print("\nWhat would you like to do with the list?")
                    print("1. View list")
                    print("2. Add item to list")
                    print("3. Remove item from list")
                    print("4. Clear list")
                    print("5. Exit selection")
                    print("Please select the number of the option you would like to select.\n")

                    while True:
                        choice = get_answer("Enter choice: ")
                        for i in choice:
                            # Can't use try-except because it causes problems T.T
                            # And if I can, I can't be fucked figuring it out.
                            if i not in ["1", "2", "3", "4", "5"]:
                                print("Invalid input.")
                        else:
                            # If it gets to here, then its a valid input.
                            break
                            
                    # View List
                    if choice == '1':
                        if len(todo_list) == 0:
                            print("No items in list.")
                            get_answer("Press enter to continue...")
                        elif len(todo_list) >= 1:
                            iterance = 1
                            for item in todo_list:
                                print("/   /   /   /   /   /   /   /")
                                print(f"Task/Todo {str(iterance)}: " + str(item) + "\n/   /   /   /   /   /   /   /")
                                iterance = int(iterance) + 1
                            print("\nThat's all the items in the list.")
                            get_answer("Press enter to continue...")
                    # Add Item
                    elif choice == '2':
                        if len(todo_list) == 0:
                            print("No items in list.")
                        elif len(todo_list) >= 0:
                            iterance = 1
                            for item in todo_list:
                                print("To Do List\n/   /   /   /   /   /   /   /")
                                print(f"Task/Todo {str(iterance)}: " + str(item) + "\n/   /   /   /   /   /   /   /")
                                iterance = int(iterance) + 1                    
                        print("What would you like to add to the list?")
                        item = str(get_answer("Enter Item: "))
                        application.projects.todo.add_todo(
                            project_name=project_id,
                            todo_task=item
                        )
                        get_answer("Press enter to continue...")
                    # Remove Item
                    elif choice == '3':
                        if len(todo_list) == 0:
                            print("No items in list.")
                        elif len(todo_list) > 0:
                            iterance = 0
                            for item in todo_list:
                                print("To Do List\n/   /   /   /   /   /   /   /")
                                print(f"Task/Todo {str(iterance)}: " + str(item) + "\n/   /   /   /   /   /   /   /")
                                iterance = int(iterance) + 1                    
                        print("What would you like to remove from the list? (counting starts at 0 or enter the specific task)")
                        item = get_answer("Enter Item: ")
                        if str(item).isnumeric() == False:
                            item = str(item)
                        else:
                            item = int(item)
                            
                            application.projects.todo.remove_todo(
                                project_name=project_id,
                                todo_task=item
                            )
                        get_answer("Press enter to continue...")
                    # Clear List
                    elif choice == '4':
                    
                        try:
                            while True:
                                confirmation = get_answer("Are you sure you want to clear the list?\nThis action cannot be undone (Yes/No)")
                                confirmation = confirmation.lower()
                                if confirmation != "yes" and confirmation != "no":
                                    print("Invalid input. Please try again.")
                                # if confirmation is no, break the second loop
                                else:
                                    print("Got it, clearing list... You have 3 seconds to cancel")
                                    time.sleep(3)
                                    break
                        except KeyboardInterrupt:
                            print("\nCancelled.")
                            get_answer("Press enter to continue...")
                            break    
                            
                        # if confirmation is yes, clear the list
                        if confirmation == "yes":
                            current_projects = application.json.getvalue(key="managed_projects", json_dir="data/appdata.json", default=None, dt=appdata_dt)
                            for project in current_projects:
                                application.json.remvalue(
                                    key="managed_projects",
                                    json_dir="data/appdata.json",
                                    value=project,
                                )
                            application.projects.delete_missing_projects(print=False)
                            print("\nCleared list.")
                            get_answer("Press enter to continue...")
                    # Exit Selection
                    elif choice == '5':
                        print("Exiting selection of "+project_id+"...")
                        return True 
            
            # Handles the reminders
            elif choice == 2:
                raise NotImplementedError
            
        class todo:
            def get_todo(project_name):
                todo = application.json.getvalue(
                    key="todo",
                    json_dir="data/projects/"+project_name+".json",
                    default=None,
                    dt=appdata_dt
                )
                return todo
            
            def add_todo(project_name, todo_task):
                todo = application.json.addvalue(
                    key="todo",
                    json_dir="data/projects/"+project_name+".json",
                    value=todo_task,
                    dt=appdata_dt
                )
                log("Added todo task: " + todo_task)
                print("Finished adding the to-do task :)")
                return todo
            
            def remove_todo(project_name, todo_task):
                if type(todo_task) == int:
                    todolist = application.json.getvalue(
                        key="todo",
                        json_dir="data/projects/"+project_name+".json",
                        default=None,
                        dt=appdata_dt
                    )

                    todo = application.json.remvalue(
                        key="todo",
                        json_dir="data/projects/"+project_name+".json",
                        value=todolist[todo_task],
                    )
                    msg = "Removed todo task: \"" + str(todolist[todo_task])+'"'
                    log(msg)
                    print(msg)
                    return todo
                elif type(todo_task) == str:
                    todolist = application.json.getvalue(
                        key="todo",
                        json_dir="data/projects/"+project_name+".json",
                        default=None,
                        dt=appdata_dt
                    )

                    todo = application.json.remvalue(
                        key="todo",
                        json_dir="data/projects/"+project_name+".json",
                        value=todo_task,
                    )
                    msg = "Removed todo task: \"" + todo_task+'"'
                    log(msg)
                    print(msg)
                    return todo
                

        def create(name="un-named project", description="Undescribed project"):

            if name == False:
                name = get_answer("What would you like to call the project? : ")
            if description == False:
                description = get_answer("How would you describe the project? : ")

            # Creates the project using getvalue's "create file if not exist"
            application.json.getvalue(
                key="Not_actually_checking_for_this",
                json_dir="data/projects/"+name+".json",
                default=None,
                dt=new_project_dt
            )

            # Adds the project to the list of managed projects
            application.json.addvalue(
                key="managed_projects",
                json_dir="data/appdata.json",
                value=name,
                dt=appdata_dt,
            )

            # Sets the name of the project
            application.json.setvalue(
                key="project.name",
                json_dir="data/projects/"+name+".json",
                value=name,
                dt=new_project_dt
            )

            # Sets the description of the project
            application.json.setvalue(
                key="project.description",
                json_dir="data/projects/"+name+".json",
                value=description,
                dt=new_project_dt
            )

            # Gets the highest current ID
            highest_id = application.json.getvalue(
                key="highest",
                json_dir="data/projects/.highest_tracker.json",
                dt=highest_project_tracker_dt
            )


            highest_id = int(highest_id)
            # Adds 1 to the highest ID
            highest_id = highest_id + 1

            # Sets the ID of the project
            application.json.setvalue(
                key="project.id",
                json_dir="data/projects/"+name+".json",
                value=highest_id,
                dt=new_project_dt
            )
            
            # Updates the highest ID
            application.json.setvalue(
                key="highest",
                json_dir="data/projects/.highest_tracker.json",
                value=highest_id,
                dt=highest_project_tracker_dt
            )

            print("Project created! You can now select/view it when desired\n")

        def delete_missing_projects(print=True):
            # Get the current list of managed projects from the appdata JSON file
            current_projects = application.json.getvalue(key="managed_projects", json_dir="data/appdata.json", default=None, dt=appdata_dt)

            # Create a copy of the list
            managed_projects = current_projects
            managed_projects = list(managed_projects)

            # Iterate over each project in the list
            for project in current_projects:
                # Get the path to the project's JSON file
                project_json_path = os.path.join("data/projects/"+project+".json")

                # If the JSON file doesn't exist, remove the project from the managed projects list
                if not os.path.exists(project_json_path):
                    managed_projects.remove(project)
                    if print == True:
                        print("Removed project from managed projects as it did not exist anymore: " + project)
                    log("Removed project from managed projects as it did not exist anymore: " + project)

            # Update the "managed_projects" key in the appdata JSON file with the updated list
            application.json.setvalue(
                key="managed_projects",
                json_dir="data/appdata.json",
                value=managed_projects,
                dt=appdata_dt
            )


    class json:
        def checkjson(obj, json_dir="data/projects/example.json", dt=new_project_dt):
            '''Checks a json file for a certain object and returns its value. Call it as so, checkjson(obj, (optional) json_dir, (optional) data)'''

            # Create directory if it doesn't exist
            if not os.path.exists(json_dir):
                os.makedirs(os.path.dirname(json_dir), exist_ok=True)
                with open(json_dir, "w") as f:
                    json.dump(dt, f, indent=4, separators=(",", ": "))

            # Fetches the data from the json and its object
            with open(f'{json_dir}', 'r') as f:
                data = json.load(f)
            fetcheddata = data.get(obj, [])
            return fetcheddata
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   
        def updatejson(newdata, obj, action, json_dir="data/projects/example.json", data=new_project_dt):
            '''
            Adds or removes data from a JSON file.
    
            Parameters:
            * `newdata`: The data to add or remove
            * `obj`: The object to add or remove the data to
            * `action`: The action to perform. Either "add" or "remove"
            `json_dir` (optional): The directory of the JSON file to add the data to. Default is "data"
            `data` (optional): The data table to add to the JSON file if it doesn't exist. Must be a dictionary.
    
            Usage:
            GameLib.updatejson(*newdata, *obj, *action, json_name, data)
            Items with * are required.
    
            Raises:
            * `Exception` if action is None.
    
            Returns:
            * None.
            '''
    
            # Make sure an action is specified
            if action is None:
                raise Exception("You must specify an action to perform. Either 'add' or 'remove'.")
    
            # Create directory if it doesn't exist
            if not os.path.exists(f"{json_dir}"):
                os.makedirs(os.path.dirname(f"{json_dir}"), exist_ok=True)
                with open(f"{json_dir}", "w") as f:
                    json.dump(data, f, indent=4, separators=(",", ": "))
    
            # Add data to object
            if action == "add" or action == "append":
                # Load the JSON file and select the specified object
                with open(f"{json_dir}", "r") as f:
                    data = json.load(f)
                    fetcheddata = data.get(obj, [])
    
                # Ensure fetcheddata is a list
                if not isinstance(fetcheddata, list):
                    fetcheddata = [fetcheddata]
    
                # Add the new value to the specified object
                fetcheddata.append(newdata)
                data[obj] = fetcheddata
    
                # Update the JSON file with the new data
                with open(f"{json_dir}", "w") as f:
                    json.dump(data, f, indent=4, separators=(",", ": "))
    
            # Remove data from object
            elif action == "remove" or action == "delete":
                # Load the JSON file and select the specified object
                with open(f"{json_dir}", "r") as f:
                    data = json.load(f)
                    fetcheddata = data.get(obj, [])
    
                # Ensure fetcheddata is a list
                if not isinstance(fetcheddata, list):
                    fetcheddata = [fetcheddata]
    
                # Remove the specified value from the specified object
                fetcheddata.remove(newdata)
                data[obj] = fetcheddata
    
                # Update the JSON file with the new data
                with open(f"{json_dir}", "w") as f:
                    json.dump(data, f, indent=4, separators=(",", ": "))
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   
        def clear_json_obj(newdata, obj, json_dir):
            '''
            Clears the data in a specific object in a JSON file.
            Call it as so: ``clear_json_obj(newdata, obj, json_dir)``

            Parameters:
            * `newdata`: The data to add or remove
            * `obj`: The object to add or remove the data to
            * `json_dir`: The directory of the JSON file to add the data to. Default is "data"
            '''
            # Open the JSON file
            with open(json_dir, 'r') as f:
                data = json.load(f)

            # Clear the data in a specific object
            data[obj].clear()

            # Write the updated object to the file
            with open(json_dir, 'w') as f:
                json.dump(data, f, indent=4, separators=(",", ": "))
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   
        def replace_obj(newdata, obj, json_dir="data/projects/example.json", data=new_project_dt, settype=list):

            '''
            Replaces the data in a specific object in a JSON file.
            Call it as so: ``replace_obj(newdata, obj, json_dir)``

            Parameters:
            * `newdata`: The data to add or remove. Not the old data
            * `obj`: The object to add or remove the data to
            * `json_dir`: The directory of the JSON file to add the data to. Default is "data/BotData.json"
            `data`: The data table to add to the JSON file if it doesn't exist. Must be a dictionary.
            `settype`: Declare if you want the data added to be added as a variable or list.
            '''

            # Create directory if it doesn't exist
            if not os.path.exists(f"{json_dir}"):
                os.makedirs(os.path.dirname(f"{json_dir}"), exist_ok=True)
                with open(f"{json_dir}", "w") as f:
                    json.dump(data, f, indent=4, separators=(",", ": "))



            if settype == list:
                olddata = application.json.checkjson(obj=obj, json_dir=json_dir)
                application.json.clear_json_obj(obj=obj, json_dir=json_dir, newdata=olddata)
                application.json.updatejson(newdata=newdata, obj=obj, json_dir=json_dir, action="append", data=data)
                return
            
            elif settype == int or settype == str or settype == bool:
                # Replaces the object with the new data as a STR or INT without a list declaration
                with open(json_dir, "r") as f:
                    data = json.load(f)
                    data[obj] = newdata
                with open(json_dir, "w") as f:
                    json.dump(data, f, indent=4)
            elif settype == tuple:
                raise TypeError("Tuples are not supported. Use lists, ints, strings or bools instead.")

        def getvalue(key, json_dir, default=None, dt=None):
            """
            Retrieve the value of a nested key from a JSON file or dictionary.

            Args:
                key (str): The key to retrieve in the format "parent.child1.child2[0].child3".
                json_dir (str): The file path of the JSON file to read from or write to.
                default: The default value to return if the key is not found (default=None).
                dt (dict): The dictionary to write to the JSON file if it does not exist (default=None).

            Returns:
                The value of the key if found, or the default value if not found.
            """

            # Split the key into parts (assuming key is in the format "parent.child1.child2[0].child3")
            parts = key.split('.')

            # Check if the JSON file exists
            if not os.path.exists(json_dir):
                try:
                    # If not, create the parent directory if it doesn't exist
                    os.makedirs(os.path.dirname(json_dir), exist_ok=True)

                    if dt is not None:
                        # If dt is provided, write it to the JSON file
                        with open(json_dir, 'w') as f:
                            json.dump(dt, f, indent=4, separators=(',', ': '))
                    else:
                        # Otherwise, create an empty JSON file
                        with open(json_dir, 'w') as f:
                            json.dump({}, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    print(f"Error creating JSON file: {str(e)}")
                    return default

            # Load the JSON file
            try:
                with open(json_dir, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error loading JSON file: {str(e)}")
                return default

            # Check if the JSON data is empty
            if not data:
                # If empty, fill it with an empty dictionary or the provided dt
                data = dt or {}
                try:
                    with open(json_dir, 'w') as f:
                        json.dump(data, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    print(f"Error writing to JSON file: {str(e)}")
                    return default

            # Traverse the nested dictionaries/lists in the JSON data to get the value
            value = data
            for part in parts:
                if part.endswith(']'):  # Check if part is an array index
                    index = int(part[part.index('[') + 1:part.index(']')])  # Extract the array index
                    value = value[index]
                else:
                    if part in value:
                        value = value[part]
                    else:
                        # If the key doesn't exist, return the default value (default=None)
                        return default

            return value

        def setvalue(key, json_dir, value, default=None, dt=None):
            """
            Set the value of a nested key in a JSON file or dictionary.

            Args:
                key (str): The key to set in the format "parent.child1.child2[0].child3".
                json_dir (str): The file path of the JSON file to read from or write to.
                value: The value to set.
                default: The default value to return if the key is not found (default=None).
                dt (dict): The dictionary to write to the JSON file if it does not exist (default=None).

            Returns:
                The updated value of the key if set successfully, or the default value if not found.
            """

            # Split the key into parts (assuming key is in the format "parent.child1.child2[0].child3")
            parts = key.split('.')

            # Check if the JSON file exists
            if not os.path.exists(json_dir):
                try:
                    # If not, create the parent directory if it doesn't exist
                    os.makedirs(os.path.dirname(json_dir), exist_ok=True)

                    if dt is not None:
                        # If dt is provided, write it to the JSON file
                        with open(json_dir, 'w') as f:
                            json.dump(dt, f, indent=4, separators=(',', ': '))
                    else:
                        # Otherwise, create an empty JSON file
                        with open(json_dir, 'w') as f:
                            json.dump({}, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    print(f"Error creating JSON file: {str(e)}")
                    return default

            # Load the JSON file
            try:
                with open(json_dir, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error loading JSON file: {str(e)}")
                return default

            # Check if the JSON data is empty
            if not data:
                # If empty, fill it with an empty dictionary or the provided dt
                data = dt or {}
                try:
                    with open(json_dir, 'w') as f:
                        json.dump(data, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    print(f"Error writing to JSON file: {str(e)}")
                    return default

            # Define a recursive function to traverse the nested dictionaries/lists in the JSON data
            def _setvalue(parts, value, data):
                if len(parts) == 1:
                    # If last part, set the value in the dictionary/list
                    key = parts[0]
                    if key.endswith(']'):  # Check if part is an array index
                        index = int(key[key.index('[') + 1:key.index(']')])  # Extract the array index
                        data[index] = value
                    else:
                        data[key] = value
                else:
                    # Traverse to the next level in the nested dictionary/list
                    key = parts[0]
                    if key.endswith(']'):  # Check if part is an array index
                        index = int(key[key.index('[') + 1:key.index(']')])  # Extract the array index
                        _setvalue(parts[1:], value, data[index])
                    else:
                        _setvalue(parts[1:], value, data[key])

            # Call the recursive function to set the value
            try:
                _setvalue(parts, value, data)
            except KeyError:
                print(f"Key not found: {key}")
                return default
            except IndexError:
                # If array index out of range
                print(f"Array index out of range: {key}")
                return default
            except Exception as e:
                print(f"Error setting value in JSON file: {str(e)}")
                return default

            # Write the updated JSON data back to the file
            try:
                with open(json_dir, 'w') as f:
                    json.dump(data, f, indent=4, separators=(',', ': '))
            except Exception as e:
                print(f"Error writing to JSON file: {str(e)}")
                return default

            return value

        def addvalue(key, json_dir, value, default=None, dt=None):
            """
            Add a value to a list in a nested key of a JSON file or dictionary.

            Args:
                key (str): The key to add to in the format "parent.child1.child2[0].child3".
                json_dir (str): The file path of the JSON file to read from or write to.
                value: The value to add to the list.
                default: The default value to return if the key is not found (default=None).
                dt (dict): The dictionary to write to the JSON file if it does not exist (default=None).

            Returns:
                The updated value of the key if added successfully, or the default value if not found.
            """

            # Split the key into parts (assuming key is in the format "parent.child1.child2[0].child3")
            parts = key.split('.')

            # Check if the JSON file exists
            if not os.path.exists(json_dir):
                try:
                    # If not, create the parent directory if it doesn't exist
                    os.makedirs(os.path.dirname(json_dir), exist_ok=True)

                    if dt is not None:
                        # If dt is provided, write it to the JSON file
                        with open(json_dir, 'w') as f:
                            json.dump(dt, f, indent=4, separators=(',', ': '))
                    else:
                        # Otherwise, create an empty JSON file
                        with open(json_dir, 'w') as f:
                            json.dump({}, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    print(f"Error creating JSON file: {str(e)}")
                    return default

            # Load the JSON file
            try:
                with open(json_dir, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error loading JSON file: {str(e)}")
                return default

            # Check if the JSON data is empty
            if not data:
                # If empty, fill it with an empty dictionary or the provided dt
                data = dt or {}
                try:
                    with open(json_dir, 'w') as f:
                        json.dump(data, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    print(f"Error writing to JSON file: {str(e)}")
                    return default

            # Define a recursive function to traverse the nested dictionaries/lists in the JSON data
            def _addvalue(parts, value, data):
                if len(parts) == 1:
                    # If last part, add the value to the list
                    key = parts[0]
                    if key.endswith(']'):  # Check if part is an array index
                        index = int(key[key.index('[') + 1:key.index(']')])  # Extract the array index
                        if not isinstance(data[index], list):
                            # Create a new list if the existing value is not a list
                            data[index] = [data[index]]
                        data[index].append(value)
                    else:
                        if not isinstance(data[key], list):
                            # Create a new list if the existing value is not a list
                            data[key] = [data[key]]
                        data[key].append(value)
                else:
                    # Traverse to the next level in the nested dictionary/list
                    key = parts[0]
                    if key.endswith(']'):  # Check if part is an array index
                        index = int(key[key.index('[') + 1:key.index(']')])
                        # Extract the array index
                        if not isinstance(data[index], list):
                            # Create a new list if the existing value is not a list
                            data[index] = [data[index]]
                        _addvalue(parts[1:], value, data[index])
                    else:
                        if key not in data:
                            # Create a new dictionary if the key doesn't exist
                            data[key] = {}
                        _addvalue(parts[1:], value, data[key])

            # Call the recursive function with the split key parts and JSON data
            try:
                _addvalue(parts, value, data)
            except Exception as e:
                print(f"Error adding value to JSON file: {str(e)}")
                return default

            # Write the updated JSON data back to the file
            try:
                with open(json_dir, 'w') as f:
                    json.dump(data, f, indent=4, separators=(',', ': '))
            except Exception as e:
                print(f"Error writing to JSON file: {str(e)}")
                return default

            # Return the updated value of the key
            return data.get(parts[-1], default)

        def remvalue(key, json_dir, value, default=None):
            """
            Remove a value from a list in a nested key of a JSON file or dictionary.

            Args:
                key (str): The key to remove from in the format "parent.child1.child2[0].child3".
                json_dir (str): The file path of the JSON file to read from or write to.
                value: The value to remove from the list.
                default: The default value to return if the key is not found (default=None).

            Returns:
                The updated value of the key if removed successfully, or the default value if not found.
            """

            # Split the key into parts (assuming key is in the format "parent.child1.child2[0].child3")
            parts = key.split('.')

            # Check if the JSON file exists
            if not os.path.exists(json_dir):
                print(f"Error: JSON file does not exist at {json_dir}")
                return default

            # Load the JSON file
            try:
                with open(json_dir, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error loading JSON file: {str(e)}")
                return default

            # Define a recursive function to traverse the nested dictionaries/lists in the JSON data
            def _remvalue(parts, value, data):
                if len(parts) == 1:
                    # If last part, remove the value from the list
                    key = parts[0]
                    if key.endswith(']'):  # Check if part is an array index
                        index = int(key[key.index('[') + 1:key.index(']')])  # Extract the array index
                        if isinstance(data[index], list) and value in data[index]:
                            data[index].remove(value)
                    else:
                        if isinstance(data[key], list) and value in data[key]:
                            data[key].remove(value)
                else:
                    # Traverse to the next level in the nested dictionary/list
                    key = parts[0]
                    if key.endswith(']'):  # Check if part is an array index
                        index = int(key[key.index('[') + 1:key.index(']')])
                        # Extract the array index
                        if not isinstance(data[index], list):
                            # Create a new list if the existing value is not a list
                            data[index] = [data[index]]
                        _remvalue(parts[1:], value, data[index])
                    else:
                        if key not in data:
                            # Create a new dictionary if the key doesn't exist
                            data[key] = {}
                        _remvalue(parts[1:], value, data[key])

            # Call the recursive function with the split key parts and JSON data
            try:
                _remvalue(parts, value, data)
            except Exception as e:
                print(f"Error removing value from JSON file: {str(e)}")
                return default

            # Write the updated JSON data back to the file
            try:
                with open(json_dir, 'w') as f:
                    json.dump(data, f, indent=4, separators=(',', ': '))
            except Exception as e:
                print(f"Error writing to JSON file: {str(e)}")
                return default

            # Return the updated value of the key
            return data.get(parts[-1], default)

name_of_app = application.json.getvalue(json_dir="data/appdata.json", key="project_name", dt=appdata_dt)
copyright = f"Copyright © Unreality Team 2023-{time.strftime('%Y')}. Apache License"
first_start = application.json.getvalue(json_dir="data/appdata.json", key="first_start", dt=appdata_dt)

# Create's appdata if it does not exist
if not os.path.exists("data/appdata.json"):
    with open("data/appdata.json", "w") as f:
        json.dump(appdata_dt, f, indent=4, separators=(',', ': '))
    log("Created appdata.json as it did not exist")
else:
    log("appdata.json exists! doing nothing")

# If the First start is false, it will not be True.
if first_start == False:
    pass
# Handles new user setup
else:
    application.runsetup()

hint_or_help_msg = 'If you need help, type "darin-help" or "darin-hint"\nRemember: to enter an arg, type arg_name:"arg_answer"\n'

application.projects.delete_missing_projects()

# Handles the actions of the user
action_handler_response = True
while True:
    try:
        if action_handler_response == True:
            print(hint_or_help_msg)
        question_response = get_answer("Hello! "+name_of_app+" is here, How can I help you today?\n- ")
        action_handler_response = application.Action_Handler(question_response)
        application.projects.delete_missing_projects()
    except KeyboardInterrupt:
        application.exit()