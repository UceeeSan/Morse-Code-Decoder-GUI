import customtkinter
from customtkinter import IntVar,END
import os
from playsound import playsound
from PIL import ImageTk, Image
directory=os.getcwd()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme('green')

#Defining window
root=customtkinter.CTk()
root.title('Morse Code Decoder')
icon_path=directory+"\Resource\morse.ico"
root.iconbitmap(icon_path)
root.geometry("630x450")
root.resizable(0,0)

#Defining Fonts 
button_font=('Roboto',13,"bold")

#Define Functions
def convert():
    output_text.delete(1.0,END)
    if language.get()==1:
        get_morse()
       
    elif language.get()==2:
        get_english()
    
def get_morse():
    '''Convert english to morse'''
    morse=""
    text=input_text.get(1.0,END)
    text=text.lower()

    #Replacing unknown characters with an empty string
    for letter in text:
        if letter not in english_to_morse.keys():
            text=text.replace(letter,"")
    word_list=text.split()
    #Decoding each word
    for letters in word_list:
        for i in letters:
            morse= morse + english_to_morse[i] + " "

        morse+= "|"
    output_text.insert(1.0,morse)

def get_english():
    '''Conver morse code to english'''
    english=""
    text=input_text.get(1.0,END)
    for letter in text:
        if letter not in morse_to_english.keys():
            text=text.replace(letter,"")
    word_list=text.split("|")
    print(word_list)
    for letter in word_list:
        letter=letter.split(" ")
        for i in letter:
            english=english+morse_to_english[i]
        english+=" "
    output_text.insert(1.0,english)

def clear():
    input_text.delete(1.0,END)
    output_text.delete(1.0,END)

def play():
    '''Play tones for corresponding dots and dashes'''
    dash=directory+"\Resource\dash.mp3"
    dot=directory+"\Resource\dot.mp3"
    #Finding out where the morse code is
    if language.get()==1:
        text=output_text.get(1.0,END)
    elif language.get()==2:
        text=input_text.get(1.0,END)
    #play the tones
    for value in text:
        if value=='.':
            playsound(dot)
            root.after(100)
        elif value=='-':
            playsound(dash)
            root.after(200)
        elif value== ' ':
            root.after(300)
        elif value=='|':
            root.after(700)

def show_guide():
    '''Show a morse code guide'''
    guide_button.configure(state="disabled")
    global morse
    global guide
    guide=customtkinter.CTkToplevel()
    guide.title("Morse guide")
    guide.iconbitmap(icon_path)
    guide.geometry("350x350+"+str(root.winfo_x()+650)+ "+" + str(root.winfo_y()))
    guide.resizable(0,0)
    guide.protocol("WM_DELETE_WINDOW", disable_event)
    #Create image label and pack
    morse=ImageTk.PhotoImage(Image.open(directory+"\Resource\morse_chart.jpg"))
    image_label=customtkinter.CTkLabel(guide,image=morse,text="")
    image_label.pack(padx=10,pady=10)

    close_button=customtkinter.CTkButton(guide,text="Close",font=button_font,command=hide_guide)
    close_button.pack(padx=10,ipadx=50)

def hide_guide():
    guide_button.configure(state="normal")
    guide.destroy()

def disable_event():
   pass

#Creating Morse_Code Dictionary
english_to_morse={'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..',
        'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
        'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
        'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
        'q': '--.-', 'r': '.-.', 's': '...', 't': '-',
        'u': '..--', 'v': '...-', 'w': '.--', 'x': '-..-',
        'y': '-.--', 'z': '--..', '1': '.----',
        '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '0': '-----', ' ':' ', '|':'|', "":"" }

morse_to_english=dict([(value,key) for key,value in english_to_morse.items()])

#Define Layout
#Creating Frames
input_frame=customtkinter.CTkFrame(root)
output_frame=customtkinter.CTkFrame(root)
input_frame.pack(padx=16,pady=(16,8))
output_frame.pack(padx=16,pady=(8,16))

#Layout for text Frame
input_text=customtkinter.CTkTextbox(input_frame,font=button_font,height=175,width=320,text_color="white",activate_scrollbars=True)
input_text.grid(row=0,column=1,rowspan=3,padx=5,pady=5)

#Creating Buttons
language=IntVar()
language.set(1)
morse_button=customtkinter.CTkRadioButton(input_frame,text="English --> Morse Code",variable=language,value=1,font=button_font)
english_button=customtkinter.CTkRadioButton(input_frame,text="Morse Code --> English",variable=language,value=2,font=button_font)
guide_button=customtkinter.CTkButton(input_frame,text="GUIDE",font=button_font,command=show_guide)

morse_button.grid(row=0,column=0,pady=(15,0),padx=5)
english_button.grid(row=1,column=0,padx=5)
guide_button.grid(row=2,column=0,sticky="WE",padx=5)

#Output Frame
output_text=customtkinter.CTkTextbox(output_frame,font=button_font,height=175,width=320,text_color="white",activate_scrollbars=True)
output_text.grid(row=0,column=1,rowspan=4,padx=5,pady=5)

convert_button=customtkinter.CTkButton(output_frame,text="Convert",font=button_font,command=convert)
play_button=customtkinter.CTkButton(output_frame,text="Play",font=button_font,command=play)
clear_button=customtkinter.CTkButton(output_frame,text="Clear",font=button_font,command=clear)
quit_button=customtkinter.CTkButton(output_frame,text="Quit",font=button_font,command=root.destroy)

convert_button.grid(row=0,column=0,padx=5,ipadx=22)
play_button.grid(row=1,column=0,padx=5,sticky="WE")
clear_button.grid(row=2,column=0,padx=5,sticky="WE")
quit_button.grid(row=3,column=0,padx=5,sticky="WE")

#Running main loop

root.mainloop()