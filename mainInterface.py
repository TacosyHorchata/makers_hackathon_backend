import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
import time
from storageFirebase import uploadFileFirebase
from azureRead import analyze_read
from gptToExcel import convertToExcel
from openAI import chatgpt_req

def convertToExcelFake(data):
    time.sleep(5)

def reset_gui():
    status_label.config(text="")
    progress_bar["value"] = 0
    upload_button["state"] = "normal"
    try_again_button.pack_forget()  # Hide the "Try Again" button if it's visible
    error_label.config(text="")

def process_file():
    try: 
        file_path = filedialog.askopenfilename(title="Selecciona un PDF", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            fileUrl = uploadFileFirebase(file_path)
            progress_bar["value"] = 0
            status_label.config(text="Subiendo Archivo...")
            root.update()

            def thread_function():
                print(fileUrl)
                progress_bar["value"] = 33
                status_label.config(text="Analizando PDF...")
                root.update()
                analizedPDF = analyze_read(fileUrl)
                progress_bar["value"] = 66
                status_label.config(text="Analizando con IA...")
                root.update()
                gpt_response = chatgpt_req(analizedPDF)
                progress_bar["value"] = 100
                status_label.config(text="Excel Listo")
                root.update()
                convertToExcel(gpt_response)
                upload_button["state"] = "normal"

            upload_button["state"] = "disabled"
            thread = threading.Thread(target=thread_function)
            thread.start()
    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")
        reset_gui()

root = tk.Tk()
root.title("PDF a Excel - Camtom Tools")
root.geometry("600x400") 
root.configure(bg="#f0f0f0")
style = ttk.Style()
style.theme_use("clam")

# Button styling
style.configure("TButton", font=("Arial", 12), background="#00b894", foreground="#f0f0f0")
style.map("TButton",
          background=[('disabled', '#b2bec3'), ('pressed', '#6c5ce7'), ('active', '#74b9ff')],
          foreground=[('disabled', '#2d3436')])

# Progressbar styling
style.configure("TProgressbar", thickness=25, troughcolor='#1e2124', bordercolor='#00b894', background='#00b894', )

# Label styling
style.configure("TLabel", background="#f0f0f0", foreground="#2f3640", font=("Arial", 14))

upload_button = ttk.Button(root, text="Subir archivo PDF", command=process_file)
upload_button.pack(pady=20)

try_again_button = ttk.Button(root, text="Try Again", command=reset_gui)
error_label = ttk.Label(root, text="", foreground="red")
error_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

status_label = ttk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()