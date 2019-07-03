import argparse
import csv
import os
import sys
import getch
import subprocess


def pos(x, y):
    print("\x1b[%d;%dH" % (y, x))


def clear():
    print("\x1b[2J")


def save_exit(data):
    for row in data:
        if(len(row) < 4):
            row.append("N/A")
    
    with open("grades.csv", "w") as csvfile:
        fields = ["学号", "姓名", "Github", "白盒成绩"]
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        writer.writerows(data)
    
    exit()


parser = argparse.ArgumentParser(prog="whitebox-helper")
parser.add_argument(
    "-w", "--workspace", help="workspace directory", default="workspace")
parser.add_argument(
    "-s", "--students", help="students.csv path", default="students.csv")
parser.add_argument(
    "-p", "--prefix", help="assignment repo prefix", default="self-intro")
parser.add_argument(
    "-f", "--file", help="students' file to check", default="introduction.txt")
parser.add_argument(
    "-t", "--template", help="template repo path", default="tpl_self-introduction")

args = parser.parse_args()

with open(args.students, 'r') as csvfile:
    next(csvfile, None)
    students = [x for x in csv.reader(csvfile)]

for index, [stuid, name, github] in enumerate(students):
    clear()
    pos(0, 0)
    repo = os.path.join(
        args.workspace, "-".join([args.prefix, github]))

    if(not os.path.exists(repo)):
        print("Repo {} not exists, no points".format(repo))
        grade = None
        continue

    while True:
        clear()
        pos(0, 0)
        print("[{}/{}] Benchmarking {}, name {}, student ID {}"
              .format(index + 1, len(students), github, name, stuid))
        print()
        print("[C] Cat student file")
        print("[D] Diff with template")
        print("[S] Show git history")
        print("[G] Give Grade")
        print("[N] Next student (skip grading)")
        print("[Q] Save and exit")
        print()

        c = getch.getch()
        if c == "n":
            grade = None
            break
        elif c == "q":
            grade = None
            save_exit(students)
        elif c == "c":
            pos(0, 1)
            subprocess.Popen(["cat", os.path.join(repo, args.file)])
        elif c == "s":
            subprocess.Popen(["git", "--no-pager", "-C", repo,
                              "log", "--pretty=format:'%h %cd %an %ae %s'"])
        elif c == "d":
            subprocess.Popen(
                ["diff", "-r", "--exclude=\".git\"", repo, args.template])
        elif c == "g":
            while True:
                print("Give grade here (max 20 points): ")
                grade = int(input())
                if(grade >= 0 and grade <= 20):
                    break
            break
        
    students[index].append(grade if grade != None else "N/A")

save_exit(students)