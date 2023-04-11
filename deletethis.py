import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import asyncio
import tracemalloc


tracemalloc.start()


class DataEntryForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        # form variables
        self.name = ttk.StringVar(value="")
        self.address = ttk.StringVar(value="")
        self.phone = ttk.StringVar(value="")

        # form header
        hdr_txt = "Please, enter time to send mails,\nemail and password of sender."
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=10)

        meter_txt = "Time to send"
        meter_time = ttk.Meter(bootstyle="success", subtextstyle="warning")
        meter_time.pack(fill=X, pady=10)

        # form entries
        self.create_form_entry("Time", self.name)
        self.create_form_entry("Address", self.address)
        self.create_form_entry("Password", self.phone)
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="Save",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="Start",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

    async def save_animation(self):
        save_txt1 = "info saved."
        save_txt2 = "info saved.."
        save_txt3 = "info saved..."
        save_txt0 = ""
        save_animate_text = ttk.Label(master=self, text=save_txt0, width=50)
        save_animate_text.pack(fill=X, pady=10)
        save_animate_text.configure(text=save_txt1)
        await asyncio.sleep(0.5)
        save_animate_text.configure(text=save_txt2)
        await asyncio.sleep(0.5)
        save_animate_text.configure(text=save_txt3)
        await asyncio.sleep(0.5)
        save_animate_text.configure(text=save_txt0)

    def on_submit(self):
        print("Time:", self.name.get())
        print("Address:", self.address.get())
        print("Password:", self.phone.get())
        asyncio.run(self.save_animation())

        return self.name.get(), self.address.get(), self.phone.get()

    def on_cancel(self):        self.quit()


if __name__ == "__main__":
    app = ttk.Window("Systemcong - 1.5.1", "superhero", resizable=(False, False))
    DataEntryForm(app)
    app.mainloop()