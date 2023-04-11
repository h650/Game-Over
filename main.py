from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import shutil
import time
import psutil
import pathlib
import os


flag_finish = 0
list_del_apps = []
root = Tk()


def ui():
    def scankey(event):
        val = event.widget.get()

        if val == '':
            data = applist
        else:
            data = []
            for item in applist:
                if val.lower() in item.lower():
                    data.append(item)

        update(data)

    def update(data):
        box.delete(0, 'end')

        # put new data
        for item in data:
            box.insert('end', item)

    def start():
        for ind in range(0, box2.size()):
            item = box2.get(ind)
            list_del_apps.append(item)
        print(list_del_apps)
        with open("notime.txt", 'w') as file:
            file.write('True')
            for app in list_del_apps:
                file.write(app+'\n')
        root.destroy()

    def add_item():
        box.insert(END, entry.get())
        entry.delete(0, END)

    def del_list():
        select = list(box.curselection())
        select.reverse()
        for i in select:
            box.delete(i)

    def plus():
        select = list(box.curselection())
        select.reverse()
        for i in select:
            appname = box.get(select)
            box2.insert(END, appname)
            box.delete(i)

    def minus():
        select = list(box2.curselection())
        select.reverse()
        for i in select:
            appname = box2.get(select)
            box.insert(END, appname)
            box2.delete(i)

    applist = ('Tlauncher', 'Minecraft', 'Roblox', 'WarTunder', 'CS:GO', 'Dota2', 'OSU',
               'Grand Theft Auto', 'Steam', 'EpicGame', 'EA origin', 'Stalker', 'Metro Exodus', 'Cuphead', 'Java(TM)')




    root.title('game over')
    box = Listbox(selectmode=EXTENDED)
    box2 = Listbox(selectmode=EXTENDED)
    box.pack(side=LEFT)
    scroll = Scrollbar(command=box.yview)
    scroll.pack(side=LEFT, fill=Y)
    box.config(yscrollcommand=scroll.set)
    f = Frame()
    f.pack(side=LEFT, padx=10)
    entry = Entry(f)
    entry.pack(anchor=N)
    entry.bind('<KeyRelease>', scankey)
    Button(f, text="Add", command=add_item) \
        .pack(fill=X)
    Button(f, text="Delete", command=del_list) \
        .pack(fill=X)
    Button(f, text=">>>", command=plus) \
        .pack(fill=X)
    Button(f, text="<<<", command=minus)\
        .pack(fill=X)
    Button(f, text="Start", command=start)\
        .pack(fill=X)
    box2.pack(side=LEFT)
    scroll2 = Scrollbar(command=box2)
    scroll2.pack(side=LEFT, fill=Y)
    box2.config(yscrollcommand=scroll2.set)

    for app in applist:
        box.insert(END, app)

    update(applist)
    root.mainloop()


def count_lines(filename, chunk_size=1<<13):
    with open(filename) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


ui()


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def delete_apps(dir, apps):
    filedel_path_list = []
    for file in os.listdir(dir):
        for app in apps:
            if app.lower() in file.lower():
                file_del_path = pathlib.Path(dir, file)
                try:
                    shutil.rmtree(file_del_path)
                    os.rmdir(file_del_path)
                    print(f'delete {file_del_path}')
                except Exception:
                    kill_file_process(apps)


def kill_file_process(apps):
    all_process_pids = psutil.pids()
    for pid in all_process_pids:
        try:
            all_process_info = psutil.Process(pid)
            process_info = all_process_info.as_dict(attrs=['pid', 'name', 'username', 'cwd'])
            for app in list_del_apps:
                if app.lower() in process_info.get('name').lower():
                    need_to_kill_process = psutil.Process(process_info.get('pid'))
                    try:
                        print()
                        print(process_info.get('name'))
                        print(process_info.get('pid'))
                        print()
                        if process_info.get('username') == 'SYSTEM':
                            print('Warning: This process is a system process and cannot be accessed')
                        else:
                            need_to_kill_process.kill()
                            shutil.rmtree(process_info.get('cwd'))
                            os.rmdir(process_info.get('cwd'))
                            print(f'process {process_info.get("name")} was killed')
                    except Exception:
                        print(f'Error: process {process_info.get("name")} not aviable to programm')
                        time.sleep(5)
                        kill_file_process(apps)
        except Exception:
            print('pass')


all_users = psutil.users()


while True:
    for user in all_users:
        user_name = user.name
        appdata_dir = f'C:\\Users\\{user_name}\\AppData'
        appdata_all_dirs = os.listdir(appdata_dir)
        for dir_in_appdata in appdata_all_dirs:
            path_to_dirs_appdata = pathlib.Path(appdata_dir, dir_in_appdata)
            delete_apps(path_to_dirs_appdata, list_del_apps)
        kill_file_process(list_del_apps)
    time.sleep(10)



