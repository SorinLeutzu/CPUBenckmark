import tkinter as tk
from tkinter import ttk, messagebox, END
import os
import subprocess
import matplotlib.pyplot as plt
from tkinter.scrolledtext import ScrolledText

score_multiplier = 1_000_000

# calculating pi
# matrix multiplication
# GAME OF LIFE
# encoding decoding

#hashmap operations

def write_threads_to_file(num_threads):
    with open("info.txt", "w") as file:
        file.write(f"{num_threads}\n")



def append_to_benchmark():
    if not os.path.exists("info.txt"):
        messagebox.showerror("Error", "info.txt does not exist. No data to append.")
        return

    with open("info.txt", "r") as infile, open("benchmark.txt", "a") as outfile:
        outfile.write(infile.read())



def view_plot():
    if not os.path.exists("benchmark.txt"):
        messagebox.showerror("Error", "benchmark.txt does not exist. No data to visualize.")
        return


    thread_counts = []
    total_times = []

    try:
        with open("benchmark.txt", "r") as file:
            lines = file.readlines()
            for line in lines:

                if "Number of threads:" in line:
                    thread_count = int(line.split(":")[1].strip())
                    thread_counts.append(thread_count)


                if "Total computation time:" in line:
                    total_time = int(line.split(":")[1].strip().split()[0])
                    total_times.append(total_time)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse benchmark.txt: {e}")
        return

    #
    if not thread_counts or not total_times:
        messagebox.showerror("Error", "No valid data found in benchmark.txt.")
        return


    plt.figure(figsize=(10, 6))
    plt.plot(thread_counts, total_times, marker='o', color='b', label='Total computation time')
    plt.title("Benchmark results: Threads vs total computation time")
    plt.xlabel("Number of threads")
    plt.ylabel("Total computation time (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    #
    plt.show()


def start_specific_test():
    num_threads = thread_spinbox.get()
    selected_test = test_combo.get()

    if not selected_test:
        messagebox.showerror("Error", "Please select a test to run.")
        return

    try:
        num_threads = int(num_threads)
        if num_threads <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of threads.")
        return


    write_threads_to_file(num_threads)


    try:
        result = subprocess.run([f"./{selected_test}"], check=True)
        append_to_benchmark()
        messagebox.showinfo("Test", "Test completed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error running test: {e}")

    display_specific_test_time()


def run_benchmark():
    selected_test = test_combo.get()

    if not selected_test:
        messagebox.showerror("Error", "Please select a test to run.")
        return

    max_threads = os.cpu_count()

    if not max_threads:
        messagebox.showerror("Error", "Unable to determine the maximum number of threads.")
        return


    progress_bar["maximum"] = max_threads
    progress_bar["value"] = 0

    with open("benchmark.txt", "w") as benchmark_file:
        benchmark_file.write("")
        benchmark_file.close()

    with open("score.txt", "w") as score_file:
        score_file.write("")
        score_file.close()

    try:
        for num_threads in range(1, max_threads + 1):
            write_threads_to_file(num_threads)
            subprocess.run([f"./{selected_test}"], check=True)
            append_to_benchmark()


            progress_bar["value"] = num_threads
            root.update_idletasks()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error running test with {num_threads} threads: {e}")
        return

    progress_bar["value"] = max_threads
    messagebox.showinfo("Benchmark", "Benchmark completed successfully!")
    display_score_and_scalability()



def display_score_and_scalability():

    score_display.config(state='normal')
    score_display.delete('1.0', tk.END)

    try:
        with open("score.txt", "r") as f:
            lines = f.readlines()
            single_thread_time = None
            max_thread_time = None


            for line in lines:
                if "1 thread" in line:
                    single_thread_time = int(line.split(":")[1].strip().split()[0])
                elif "maximum number of threads" in line:
                    max_thread_time = int(line.split(":")[1].strip().split()[0])

            if single_thread_time and max_thread_time:

                scalability_factor = single_thread_time / max_thread_time
                cpu_score = score_multiplier / max_thread_time


                score_display.insert(
                    tk.END,
                    f"Computation Time (1 Thread): {single_thread_time} ms\n"
                )
                score_display.insert(
                    tk.END,
                    f"Computation Time (Max Threads): {max_thread_time} ms\n"
                )
                score_display.insert(
                    tk.END,
                    f"Scalability Factor: {scalability_factor:.2f}\n"
                )
                score_display.insert(
                    tk.END,
                    f"CPU Score: {cpu_score:.2f}\n"
                )
            else:
                score_display.insert(tk.END, "Incomplete data in score.txt.\n")

    except FileNotFoundError:
        score_display.insert(tk.END, "Score data not found. Run the benchmark first.\n")


    score_display.config(state='disabled')

def display_specific_test_time():

    score_display.config(state='normal')
    score_display.delete('1.0', tk.END)

    try:
        with open("info.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if "Number of" in line:
                    score_display.insert(tk.END, line)
                if "computation" in line:
                    score_display.insert(tk.END, line)

    except FileNotFoundError:
        score_display.insert(tk.END, "Score data not found. Run the benchmark first.\n")


    score_display.config(state='disabled')



# Application window
root = tk.Tk()
root.title("Multicore Benchmark Application")
root.geometry("800x600")

# Left Panel 
control_frame = tk.Frame(root)
control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Label and spinbox
thread_label = ttk.Label(control_frame, text="Number of threads:")
thread_label.pack(pady=10)

thread_spinbox = ttk.Spinbox(control_frame, from_=1, to=os.cpu_count(), width=10)
thread_spinbox.pack(pady=5)

# Label and dropdown menu 
test_label = ttk.Label(control_frame, text="Select test:")
test_label.pack(pady=10)

test_combo = ttk.Combobox(control_frame, values=["calculatingPi.exe", "matrix_multiplication.exe", "game_of_life.exe", "encoding.exe", "hashmap_operations.exe"], state="readonly")
test_combo.pack(pady=5)


run_button = ttk.Button(control_frame, text="Run Specific Test", command=start_specific_test)
run_button.pack(pady=10)

benchmark_button = ttk.Button(control_frame, text="Run Benchmark", command=run_benchmark)
benchmark_button.pack(pady=10)

# Button for viewing results
view_results_button = ttk.Button(control_frame, text="View Plot", command=view_plot)
view_results_button.pack(pady=10)

# Right panel display
score_frame = tk.Frame(root, width=300, bg="lightgray")
score_frame.pack(side=tk.RIGHT, fill=tk.Y)

score_label = tk.Label(score_frame, text="Benchmark Results", bg="lightgray", font=("Arial", 14, "bold"))
score_label.pack(pady=10)

score_display = ScrolledText(score_frame, wrap=tk.WORD, state='disabled', width=35, height=20)
score_display.pack(pady=10, padx=10)

# Progress bar for the benchmark process
progress_label = ttk.Label(control_frame, text="Progress:")
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(control_frame, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=5)




root.mainloop()
