import tkinter as tk
from tkinter import ttk, messagebox
import platform
import socket
import psutil
import os
from datetime import datetime


class SystemConfigurationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("System Configuration Comparison Tool")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)

        self.system_a = {}
        self.system_b = {}

        self.create_interface()
        self.refresh_system_info()

    # ---------------------------------------------------------
    # CREATE GUI
    # ---------------------------------------------------------
    def create_interface(self):

        title = tk.Label(
            self.root,
            text="SYSTEM CONFIGURATION COMPARISON TOOL",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            self.root,
            text="Python-Based GUI Application for Retrieving and Comparing System Configurations",
            font=("Arial", 10)
        )
        subtitle.pack(pady=2)

        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Refresh System",
            command=self.refresh_system_info,
            width=18
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Save as System A",
            command=self.save_system_a,
            width=18
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Save as System B",
            command=self.save_system_b,
            width=18
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Compare Systems",
            command=self.compare_systems,
            width=18
        ).grid(row=0, column=3, padx=5)

        # Current system information
        info_frame = tk.LabelFrame(
            self.root,
            text="Current System Configuration",
            font=("Arial", 11, "bold")
        )
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Parameter", "Value")

        self.tree = ttk.Treeview(
            info_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("Parameter", text="Parameter")
        self.tree.heading("Value", text="Value")

        self.tree.column("Parameter", width=250)
        self.tree.column("Value", width=650)

        scrollbar = ttk.Scrollbar(
            info_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Status bar
        self.status = tk.Label(
            self.root,
            text="Ready",
            anchor="w",
            relief="sunken"
        )
        self.status.pack(
            side="bottom",
            fill="x"
        )

    # ---------------------------------------------------------
    # GET SYSTEM INFORMATION
    # ---------------------------------------------------------
    def get_system_info(self):

        info = {}

        # Operating System
        info["Operating System"] = platform.system()
        info["OS Version"] = platform.version()
        info["OS Release"] = platform.release()

        # Computer
        info["Computer Name"] = socket.gethostname()
        info["Architecture"] = platform.machine()
        info["Processor"] = platform.processor()

        # CPU
        info["CPU Cores (Physical)"] = psutil.cpu_count(logical=False)
        info["CPU Threads (Logical)"] = psutil.cpu_count(logical=True)

        cpu_frequency = psutil.cpu_freq()

        if cpu_frequency:
            info["CPU Current Frequency"] = (
                f"{cpu_frequency.current:.2f} MHz"
            )
            info["CPU Max Frequency"] = (
                f"{cpu_frequency.max:.2f} MHz"
            )
        else:
            info["CPU Current Frequency"] = "Not available"
            info["CPU Max Frequency"] = "Not available"

        # RAM
        memory = psutil.virtual_memory()

        info["Total RAM"] = (
            f"{memory.total / (1024 ** 3):.2f} GB"
        )

        info["Available RAM"] = (
            f"{memory.available / (1024 ** 3):.2f} GB"
        )

        info["RAM Usage"] = f"{memory.percent}%"

        # Storage
        disk = psutil.disk_usage(os.path.abspath(os.sep))

        info["Total Storage"] = (
            f"{disk.total / (1024 ** 3):.2f} GB"
        )

        info["Used Storage"] = (
            f"{disk.used / (1024 ** 3):.2f} GB"
        )

        info["Free Storage"] = (
            f"{disk.free / (1024 ** 3):.2f} GB"
        )

        info["Storage Usage"] = f"{disk.percent}%"

        # Boot time
        boot_time = datetime.fromtimestamp(
            psutil.boot_time()
        )

        info["Last Boot Time"] = boot_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Python
        info["Python Version"] = platform.python_version()

        return info

    # ---------------------------------------------------------
    # DISPLAY SYSTEM INFORMATION
    # ---------------------------------------------------------
    def refresh_system_info(self):

        self.tree.delete(*self.tree.get_children())

        info = self.get_system_info()

        for parameter, value in info.items():
            self.tree.insert(
                "",
                "end",
                values=(parameter, value)
            )

        self.status.config(
            text="System information refreshed successfully."
        )

    # ---------------------------------------------------------
    # SAVE SYSTEM A
    # ---------------------------------------------------------
    def save_system_a(self):

        self.system_a = self.get_system_info()

        self.status.config(
            text="Current configuration saved as System A."
        )

        messagebox.showinfo(
            "System A",
            "Current system configuration has been saved as System A."
        )

    # ---------------------------------------------------------
    # SAVE SYSTEM B
    # ---------------------------------------------------------
    def save_system_b(self):

        self.system_b = self.get_system_info()

        self.status.config(
            text="Current configuration saved as System B."
        )

        messagebox.showinfo(
            "System B",
            "Current system configuration has been saved as System B."
        )

    # ---------------------------------------------------------
    # COMPARE SYSTEMS
    # ---------------------------------------------------------
    def compare_systems(self):

        if not self.system_a or not self.system_b:
            messagebox.showwarning(
                "Missing Configuration",
                "Please save both System A and System B first."
            )
            return

        comparison_window = tk.Toplevel(self.root)
        comparison_window.title(
            "System Configuration Comparison"
        )
        comparison_window.geometry("1100x650")

        title = tk.Label(
            comparison_window,
            text="SYSTEM CONFIGURATION COMPARISON",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=15)

        columns = (
            "Parameter",
            "System A",
            "System B",
            "Status"
        )

        tree = ttk.Treeview(
            comparison_window,
            columns=columns,
            show="headings"
        )

        for column in columns:
            tree.heading(column, text=column)

        tree.column("Parameter", width=250)
        tree.column("System A", width=250)
        tree.column("System B", width=250)
        tree.column("Status", width=120)

        tree.tag_configure(
            "different",
            background="#ffcccc"
        )

        tree.tag_configure(
            "same",
            background="#ccffcc"
        )

        all_parameters = set(
            self.system_a.keys()
        ).union(
            self.system_b.keys()
        )

        for parameter in sorted(all_parameters):

            value_a = self.system_a.get(
                parameter,
                "Not Available"
            )

            value_b = self.system_b.get(
                parameter,
                "Not Available"
            )

            if value_a == value_b:
                status = "Same"
                tag = "same"
            else:
                status = "Different"
                tag = "different"

            tree.insert(
                "",
                "end",
                values=(
                    parameter,
                    value_a,
                    value_b,
                    status
                ),
                tags=(tag,)
            )

        scrollbar = ttk.Scrollbar(
            comparison_window,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=10,
            padx=(0, 15)
        )

        self.status.config(
            text="System A and System B comparison completed."
        )


# -------------------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = SystemConfigurationTool(root)

    root.mainloop()