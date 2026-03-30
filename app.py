from rich.console import Console
from rich.table import Table
import argparse
import json
import os

FILE="tasks.json"

class Task:


    def __init__(self, title, status="todo"):
        self.title=title
        self.status=status
    def to_dict(self):
        return{
            "title":self.title,
            "status":self.status
        }
    @staticmethod
    def from_dict(data):
        return Task(title=data["title"],status=data.get("status","todo"))



def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            data = json.load(f)

            tasks = []
            for item in data:
                if isinstance(item, dict):
                    tasks.append(Task.from_dict(item))
                else:
                    # old format (string)
                    tasks.append(Task(item))

            return tasks
    except json.JSONDecodeError:
        return []
def save_tasks(tasks):
    with open(FILE,"w") as f:
        json.dump([task.to_dict() for task in tasks],f,indent=4)

def add_task(args):
    tasks=load_tasks()
    tasks.append(Task(args.task))
    save_tasks(tasks)
    print("Task Added")

console= Console()

def list_tasks(args):
    tasks = load_tasks()

    if args.filter:
        tasks = [t for t in tasks if t.status == args.filter]
    elif args.filter=="not-done":
        tasks=[t for t in tasks if t.status!="done"]
    if not tasks:
        console.print("[bold red]No tasks found[/bold red]")
        return

    table = Table(title="Task List")

    table.add_column("ID", width=4)
    table.add_column("Status", width=12)
    table.add_column("Task", width=50)

    for i, task in enumerate(tasks, 1):
        color = {
            "todo": "red",
            "in-progress": "yellow",
            "done": "green"
        }[task.status]

        table.add_row(
            str(i),
            f"[{color}]{task.status}[/{color}]",
            task.title[:50]
        )

    console.print(table)

def done_task(args):
    tasks=load_tasks()
    if args.index<1 or args.index>len(tasks):
        print("invalid index")
        return
    tasks[args.index-1].status="done"
    save_tasks(tasks)
    print("Task marked as done")

def delete_task(args):
    tasks = load_tasks()
    if args.index<1 or args.index> len(tasks):
        print("Invalid index")
        return
    removed = tasks.pop(args.index-1)
    save_tasks(tasks)
    print(f"deleted: {removed}")

def in_progress_task(args):
    tasks=load_tasks()
    if args.index < 1 or args.index > len(tasks):
        print("Invalid index")
        return
    tasks[args.index-1].status="in-progress"
    save_tasks(tasks)
    print("Task marked as in progress")

def update_task(args):
    tasks=load_tasks()
    if args.index < 1 or args.index > len(tasks):
        print("Invalid index")
        return
    tasks[args.index-1].title=args.title
    save_tasks(tasks)
    print("task updated")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="add tasks")
    add_parser.add_argument("task", help="task description")
    add_parser.set_defaults(func=add_task)
    
    list_parser = subparsers.add_parser("list",help="list tasks")
    list_parser.set_defaults(func=list_tasks)

    done_parser=subparsers.add_parser("done",help="mark task as done")
    done_parser.add_argument("index",type=int,help="task number")
    done_parser.set_defaults(func=done_task)

    delete_parser = subparsers.add_parser("delete", help="delete a task")
    delete_parser.add_argument("index",type=int,help="task number")
    delete_parser.set_defaults(func=delete_task)

    # update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("index", type=int)
    update_parser.add_argument("title")
    update_parser.set_defaults(func=update_task)

    # in-progress
    progress_parser = subparsers.add_parser("progress")
    progress_parser.add_argument("index", type=int)
    progress_parser.set_defaults(func=in_progress_task)

    # filter
    list_parser.add_argument(
        "--filter",
        choices=["todo", "in-progress", "done","not-done"],
        help="Filter tasks"
    )

    args = parser.parse_args()

    if hasattr(args,"func"): # built-in utility used to check if an object has a specified named attribute or method
        args.func(args)
    else:
        parser.print_help()
   
if __name__=="__main__":
    main()