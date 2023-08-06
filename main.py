from __init__ import *
import asyncio
import os
import customtkinter
from tkinter import *
import asyncio
from threading import Thread
# Intial datas
FONT = "Helvetica"
Number = 0 

class ChatApplication:
    
    def __init__(self):
        self.window = customtkinter.CTk() 
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        customtkinter.set_appearance_mode("dark")
        self.window.title("LUCY CHAT BOT")
        self.window.iconbitmap("images/icon.ico")
        self.window.geometry("1000x550")
        
        # Head label
        head_label = customtkinter.CTkLabel(self.window,text="LUCY CHAT BOT",font=customtkinter.CTkFont(FONT,size=15,weight="bold")) 
        head_label.place(relwidth=1.8,rely=0.010)

        # Language menu
        self.language_label = customtkinter.CTkLabel(head_label,text="Language: ")
        self.language_label.place(relx=0.01)
        self.language = customtkinter.CTkComboBox(head_label,values=["አማርኛ", "English"])
        self.language.place(relx=0.05)

        # TTS menu
        self.synthesis_lable = customtkinter.CTkLabel(head_label,text="Speech Synthesis: ")
        self.synthesis_lable.place(relx=0.15)
        self.synthesis = customtkinter.CTkComboBox(head_label, values=["Enable", "Disable"])
        self.synthesis.place(relx=0.22)

        # Text widget
        self.text_widget = customtkinter.CTkTextbox(self.window, width=20, height=2, padx=5, pady=5,corner_radius=0,state=DISABLED)
        self.text_widget.place(relheight=0.8, relwidth=1,rely=0.08)
        self.text_widget.configure(cursor="arrow")
        
        
        # Bottom label
        bottom_label = customtkinter.CTkLabel(self.window,height=800,text="",)
        bottom_label.place(relwidth=1, rely=0.9)
        
        # Message entry box
        self.msg_entry = customtkinter.CTkEntry(bottom_label,placeholder_text="Write your message")
        self.msg_entry.place(relwidth=0.75, relheight=0.05, relx=0.030)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
         
        # Send button
        send_button = customtkinter.CTkButton(master=bottom_label, fg_color="transparent",text="send", border_width=2, text_color=("gray10", "#DCE4EE"),command=self._on_enter_pressed,hover_color="#6D6D6D",hover=True)
        send_button.place(relx=0.83, relheight=0.05, relwidth=0.13)
     
    def _on_enter_pressed(self,*args):
        # Button callback handler
        msg = self.msg_entry.get()
        thread = Thread(target=self._insert_message, args=[msg])
        thread.start()

    def response(self, msg):
        # Send request and get response
        eng_trans = Translate(msg).ToEnglish() if self.language.get() != "English" else msg
        bard_resp = chat(eng_trans)
        amh_trans = Translate(bard_resp).ToAmharic() if self.language.get() != "English" else bard_resp
	
        return amh_trans

    def _insert_message(self, msg):
        global Number
        if not msg:
            return
        
        # Get user input and display it
        msg1 = f"አንተ: {msg}\n\n" if self.language.get() != "English" else f"You: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        self.msg_entry.delete(0,"end")

        eng_trans = Translate(msg).ToEnglish() if self.language.get() != "English" else msg
        bard_resp = chat(eng_trans)
        amh_trans = Translate(bard_resp).ToAmharic() if self.language.get() != "English" else bard_resp

        # Display response data
        msg2 = f"ሉሲ: {amh_trans}\n\n" if self.language.get() != "English" else f"Lucy: {amh_trans}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        # Generate synthesis sound of response and play it
        if self.synthesis.get() == "Enable":
            tts = TextToSpeech(amh_trans,self.language.get(),f"cache/output{Number}.mp3")
            tts.synthesis()
            tts.play()
            Number = 1 if Number == 0 else 0
            try: os.remove(f"cache/output{Number}.mp3")
            except Exception: pass

if __name__ == "__main__":
    app = ChatApplication()
    app.run()