import argparse
import json
import os

FILE="tasks.json"

def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE,"r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
    
def save_tasks(tasks):
    with open(FILE,"w") as f:
        json.dump(tasks,f,indent=4)

def add_task(args):
    tasks=load_tasks()
    tasks.append(args.task)
    save_tasks(tasks)
    print("Task Added")

def list_tasks(args):
    tasks=load_tasks()
    if not tasks:
        print("No tasks found")
        return
    for i,task in enumerate(tasks,1):
        print(f"{i}. {task}")

def delete_task(args):
    tasks = load_tasks()
    if args.index<1 or args.index> len(tasks):
        print("Invalid index")
        return
    removed = tasks.pop(args.index-1)
    save_tasks(tasks)
    print(f"deleted: {removed}")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="add tasks")
    add_parser.add_argument("task", help="task description")
    add_parser.set_defaults(func=add_task)
    
    list_parser = subparsers.add_parser("list",help="list tasks")
    list_parser.set_defaults(func=list_tasks)

    delete_parser = subparsers.add_parser("delete", help="delete a task")
    delete_parser.add_argument("index",type=int,help="task number")
    delete_parser.set_defaults(func=delete_task)

    args = parser.parse_args()

    if hasattr(args,"func"):#keyword
        args.func(args)
    else:
        parser.print_help()
   
if __name__=="__main__":
    main()