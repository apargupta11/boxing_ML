import tkinter as tk


class LabelPopup:

    def ask(self, event):

        self.result = None

        root = tk.Tk()

        root.title("Punch Detected")
        root.geometry("350x220")
        root.resizable(False, False)

        tk.Label(
            root,
            text="🥊 Punch Detected",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Label(
            root,
            text=f"Event ID : {event['event_id']}",
            font=("Arial", 12)
        ).pack()

        tk.Label(
            root,
            text=f"Hand : {event['hand']}",
            font=("Arial", 12)
        ).pack(pady=5)

        tk.Label(
            root,
            text="Was this a real punch?",
            font=("Arial", 12)
        ).pack(pady=10)

        def punch():
            self.result = "PUNCH"
            root.destroy()

        def no_punch():
            self.result = "NO_PUNCH"
            root.destroy()

        tk.Button(
            root,
            text="PUNCH",
            width=15,
            height=2,
            command=punch
        ).pack(pady=5)

        tk.Button(
            root,
            text="NO PUNCH",
            width=15,
            height=2,
            command=no_punch
        ).pack()

        root.mainloop()

        return self.result