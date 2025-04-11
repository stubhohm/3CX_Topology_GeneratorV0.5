from ...ConfigDict import config_dict
from ...Modules import tk, ttk

class ConfigDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Run Configuration")
        self.geometry("300x600")
        self.configs = config_dict

        
        for idx, (label, var) in enumerate(self.configs.items()):
            frame = ttk.LabelFrame(self, text=label)
            frame.pack(fill='x', padx=10, pady=5)

            if isinstance(var, str):
                ttk.Entry(frame, textvariable=var).pack(fill='x', padx=5)
            else:
                ttk.Radiobutton(frame, text="Yes", variable=tk.BooleanVar(value = var), value=True).pack(side="left", padx=5)
                ttk.Radiobutton(frame, text="No", variable=tk.BooleanVar(value = var), value=False).pack(side="left")

        ttk.Button(self, text="Start Program", command=self.submit).pack(pady=10)


    def submit(self):
        result = {k: v for k, v in self.configs.items()}
        print(result)
        self.configs = result
        self.master.quit()
        self.destroy()