import tkinter as tk
from tkinter import PhotoImage

class HostelAlertApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Alert")

       
        self.root.geometry("800x600")
        self.root.resizable(False, False)

  
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        try:
          
            bg_image = PhotoImage(file="background_image.png") 
            bg_label = tk.Label(self.main_frame, image=bg_image)
            bg_label.place(relwidth=1, relheight=1)

        except tk.TclError as e:
            print(f"Error loading image: {e}")

       
        welcome_label = tk.Label(self.main_frame, text="Welcome to our Hostel Alert", font=("Helvetica", 24), bg="white")
        welcome_label.pack(pady=50)

    
        continue_button = tk.Button(self.main_frame, text="Continue", command=self.open_main_page, font=("Helvetica", 16))
        continue_button.pack(pady=20)

    def open_main_page(self):
       
        self.main_frame.destroy()

       

if __name__ == "__main__":
    root = tk.Tk()
    app = HostelAlertApp(root)
    root.mainloop()
