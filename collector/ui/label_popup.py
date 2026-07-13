import tkinter as tk


class LabelPopup:

    LABELS = {
        "0": "NO_PUNCH",
        "1": "LEFT_PUNCH",
        "2": "RIGHT_PUNCH",
        "4": "LEFT_MISS",
        "5": "RIGHT_MISS",
    }

    def ask(self, event):

        self.result = None

        root = tk.Tk()
        root.title("Punch Detected")
        root.geometry("320x180")
        root.resizable(False, False)
        root.attributes("-topmost", True)
        root.focus_force()

        tk.Label(
            root,
            text="🥊 Punch Detected",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 5))

        tk.Label(
            root,
            text=f"Event ID : {event['event_id']}",
            font=("Arial", 11)
        ).pack()

        tk.Label(
            root,
            text=f"Hand : {event['hand']}",
            font=("Arial", 11)
        ).pack(pady=(0, 10))

        tk.Label(
            root,
            text="Press a key",
            font=("Arial", 12, "bold")
        ).pack()

        tk.Label(
            root,
            text="""
0 → No Punch
1 → Left Punch
2 → Right Punch
4 → Left Miss
5 → Right Miss
""",
            font=("Consolas", 11),
            justify="left"
        ).pack()

        def on_key(event_obj):

            key = event_obj.keysym

            if key in self.LABELS:
                self.result = self.LABELS[key]
                root.destroy()

        # Bind number keys
        root.bind("<Key>", on_key)

        # Ensure popup receives keyboard focus
        root.after(50, lambda: root.focus_force())

        root.mainloop()

        return self.result