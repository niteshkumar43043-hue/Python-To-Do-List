import json
from datetime import datetime
to_do_list={}

def add_task():
    task=input("Add Your Task :").strip()
    if not task:
        print("Task cannot be empty")
        return
    if task in to_do_list:
        print("Task already exists")
    else:
        to_do_list[task]={"status":False}
        while True:
            priority = input("Enter the priority of the task (High/Medium/Low): ").strip().capitalize()
            if priority in ["High", "Medium", "Low"]:
                break
            else:
                print("Invalid priority. Please enter High, Medium, or Low.")
        to_do_list[task]["priority"] = priority
        to_do_list[task]["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        save_task()
        print("Task Added :",task)

def view_task():
    index=1
    print("")
    print("-"*20,"Your Task List :","-"*20)
    for task in  to_do_list:
        if to_do_list[task]["status"]==False:
            print(f"{index}. {task} -[ status - Pending , Priority: {to_do_list[task]['priority']} , Created: {to_do_list[task]['created_at']}]")
            index=index+1
        else:
            print(f"{index}. {task} -[ status - Completed , Priority: {to_do_list[task]['priority']} , Created: {to_do_list[task]['created_at']}]")
            index=index+1
    print("-"*60)
def delete_task(n):
    task = list(to_do_list.keys())[n]
    print(f"{task} will be removed")
    to_do_list.pop(task)
    print("Task Deleted ")
    save_task()
def mark_task_completed(n):
    task = list(to_do_list.keys())[n]
    if to_do_list[task]["status"]:
        print(f"{task} is already completed")
    else:
        to_do_list[task]["status"]=True
        save_task()
        print(f"{task} marked as completed")

def mark_task_pending(n):
    task = list(to_do_list.keys())[n]
    if not to_do_list[task]["status"]:
        print(f"{task} is already pending")
    else:
        to_do_list[task]["status"]=False
        save_task()
        print(f"{task} marked as pending")
def search_task():
    search_term=input("Enter the task to search: ").strip()
    
    if not search_term:
        print("Search term cannot be empty")
        return
    found_tasks = [task for task in to_do_list if search_term.lower() in task.lower()]
    if found_tasks:
        print("Found Tasks:")
        for task in found_tasks:
            status = "Completed" if to_do_list[task]["status"] else "Pending"
            print(f"- {task} [ status: {status} , Priority: {to_do_list[task]['priority']}, Created: {to_do_list[task]['created_at']}]")
    else:
        print("No tasks found matching your search.")
def save_task():
    with open("task.json","w")as file:
        json.dump(to_do_list,file)
def load_task():
    try:
        with open("task.json","r")as file:
            global to_do_list
            to_do_list=json.load(file)
    except FileNotFoundError:
        print("No previous task found, starting fresh.")
    except json.JSONDecodeError:
        print("Error reading task file, starting fresh.")
        to_do_list = {}

def task_statistics():
    total_tasks = len(to_do_list)
    completed_tasks = sum(1 for status in to_do_list.values() if status["status"])
    pending_tasks = total_tasks - completed_tasks
    complete_rate= (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    print(f"Total Tasks: {total_tasks}")
    print(f"Completed Tasks: {completed_tasks}")
    print(f"Pending Tasks: {pending_tasks}")
    print(f"Completion Rate: {complete_rate:.2f}%")
def edit_task(n):
    task = list(to_do_list.keys())[n]
    while True:
        print(f"Editing Task: {task}")
        print("1. Edit Task Name")
        print("2. Edit Task Priority")
        print("3. Exit Editing")
        choice = input("Choose an option : ").strip()
        if choice == "1":
            new_task_name = input(f"Enter the new name for the task '{task}': ").strip()
            if not new_task_name:
                print("Task name cannot be empty.")
                continue
            if new_task_name != task and new_task_name in to_do_list:
                print("Task with this name already exists.")
                continue
            to_do_list[new_task_name] = to_do_list.pop(task)
            to_do_list[new_task_name]["edited_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Task name changed from '{task}' to '{new_task_name}'")
            task=new_task_name
            save_task()
        elif choice == "2":

            while True:
                new_priority = input(f"Enter the new priority for the task '{task}' (High/Medium/Low): ").strip().capitalize()
                if new_priority in ["High", "Medium", "Low"]:
                    to_do_list[task]["priority"] = new_priority
                    break
                else:
                    print("Invalid priority. Please enter High, Medium, or Low.")
            to_do_list[task]["edited_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_task()
            print(f"Task priority updated to '{new_priority}' for task '{task}'")
        elif choice == "3":
            print("Exiting editing mode.")
            return
        else:
            print("Invalid choice. Please choose a valid option.")
    
load_task()
while True :
    print("-"*15,"To-Do List",15*"-")
    print("1. Add Task  ")
    print("2. view Task  ")
    print("3. Delete Task  ")
    print("4. Mark Task as Completed ")
    print("5. Mark Task as pending ")
    print("6. Search Task ")
    print("7. Task Statistics ")
    print("8. Edit Task ")
    print("9. Exit ")
    choice=input("choose the number:")
    if choice=="1":
        add_task()
    elif choice=="2":
        if len(to_do_list)==0:
            print("Task List is empty")
        else:
            view_task()
    elif choice=="3":

        if len(to_do_list)<=0:
            print("list is empty")
        else:
            while True:
                try :
                    n=int(input("Enter the task no delete it :"))
                    if 0>=n or n>len(to_do_list):
                        raise ValueError("invalid task no")
                    else:
                        delete_task(n-1)
                        break
                except ValueError as error :
                    print("error",error)
    elif choice=="4":
        if len(to_do_list)<=0:
            print("list is empty")
        else:
            while True:
                try :
                    n=int(input("Enter the task no to mark it as completed :"))
                    if 0>=n or n>len(to_do_list):
                        raise ValueError("invalid task no")
                    else:
                        mark_task_completed(n-1)
                        break
                except ValueError as error :
                    print("error",error)
    elif choice=="5":
        if len(to_do_list)<=0:
            print("list is empty")
        else:
            while True:
                try :
                    n=int(input("Enter the task no to mark it as pending :"))
                    if 0>=n or n>len(to_do_list):
                        raise ValueError("invalid task no")
                    else:
                        mark_task_pending(n-1)
                        break
                except ValueError as error :
                    print("error",error)
    elif choice=="6":
        if len(to_do_list)<=0:
            print("list is empty")
        else:
            search_task()
    elif choice=="7":
        if len(to_do_list)<=0:
            print("list is empty")
        else:   
            task_statistics()
    elif choice=="8":
        if len(to_do_list)<=0:
            print("list is empty")
        else:
            while True:
                try:
                    n = int(input("Enter the task number to edit: "))
                    if 0 >= n or n > len(to_do_list):
                        raise ValueError("Invalid task number")
                    else:
                        edit_task(n - 1)
                        break
                except ValueError as error:
                    print("Error:", error)
    elif choice=="9":
        print("-"*15,"Program Ended","-"*15)
        save_task()
        break
    else :
        print("invalid input choos the correct no")



