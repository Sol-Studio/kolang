import tkinter as tk
import threading, time
import uuid


code = ""
components = []
functions = {}
c_id = 0
root = None
app = None

class App(threading.Thread):
    def __init__(self, code):
        self.code = code
        threading.Thread.__init__(self)
        self.start()

    def quit(self):
        root.quit()

    def run(self):
        global root
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", self.quit)

        exec(self.code)

        root.mainloop()





def create_component(유형, 텍스트=None, 커맨드=None):
    global c_id
    component = None
    if 유형 == "버튼":
        uid = uuid.uuid4()
        functions[str(uid)] = 커맨드
        component = tk.Button(root, text=텍스트, command=functions[str(uid)])
    elif 유형 == "텍스트":
        component = tk.Label(root, text=텍스트)
    component.pack()
    components.append(component)
    c_id += 1
    return c_id-1

def edit_label(id, text):
    components[id]['text'] = text

def delete_component(id):
    components[id].destroy()

def create_window():
    global app
    if app != None:
        raise Exception("이미 창이 실행중입니다.")
    app = App(code)
    time.sleep(0.1)

def set_window_geometry(너비, 높이, 가로, 세로):
    root.geometry("%dx%d-%d+%d" % (너비, 높이, 가로, 세로))

def change_window_title(text):
    root.title(text)
    root.update()
