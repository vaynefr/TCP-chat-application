import tkinter as tk
from tkinter import messagebox
import customtkinter
import socket
import threading

client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

window = customtkinter.CTk()
window.title("Chatbox")

def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="Error!", message="Please enter your Name")
    else:
        username = entName.get()
        connect_to_server(username)

def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # set up TCP socket 
        client.connect((HOST_ADDR, HOST_PORT)) 
        client.send(name.encode("utf-8")) # sends username to the server

        entName.configure(state=tk.DISABLED)
        connectButton.configure(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        #start thread to receive messages from server
        threading._start_new_thread(recv_msg, (client,))

    except socket.error as e:
        print(e)

def recv_msg(sock):
    while True:
        data = sock.recv(4096) # data/msg from server 
        if not data:break
        # enable display area and insert text
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, data)
        else:
            tkDisplay.insert(tk.END, "\n\n" + data.decode("utf-8"))

        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)
        print("Recieved from server: "+data.decode("utf-8"))
    sock.close()
    window.destroy()

def getChatMessage(msg):
    # get message the client typed 
    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()
    #insert message typed, into display area
    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message")
    else:
        tkDisplay.insert(tk.END, "\n\n"+"You->"+msg, "tag_your_message")
    tkDisplay.config(state=tk.DISABLED)
    send_message_to_server(msg) # TODO

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)

def send_message_to_server(msg):
    client.send(msg.encode("utf-8"))
    if msg == "exit":
        client.close() # close/end connection
        window.destroy()
    print("Sent message.")



topFrame = tk.Frame(window)
nameLabel = customtkinter.CTkLabel(topFrame, text="User Name:",fg_color="black").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
connectButton = customtkinter.CTkButton(topFrame, text="Connect to chat", command=connect)
connectButton.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
headingLine = customtkinter.CTkLabel(displayFrame, text="*********************",fg_color="black").pack()
scrollBar = customtkinter.CTkScrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5,0))
scrollBar.configure(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#FFFFFF", highlightbackground="black", state="disabled")
displayFrame.pack(side=tk.TOP)

bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="black", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)


window.mainloop()