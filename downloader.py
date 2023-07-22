from tkinter import *
from tkinter import filedialog
import urllib.request
import customtkinter 
from pytube import *
from PIL import Image, ImageTk

youtubeObject=None

#Setup Window
root = customtkinter.CTk() 
#Configure GUI defaults
customtkinter.set_appearance_mode("dark") 
#Change the title of the frame
root.title("Youtube Video Downloader")
#Make the window
root.geometry("1280x720")
frame = Frame(root)
frame.pack() # .pack() puts things into the the gui window

#Add a title to the frame
titleLabel= Label(frame, text="Youtube Downloader", font=("Arial" ,25) ,background="gray",foreground="white")
titleLabel.pack()

#Add Text Area for URL
urlArea=Text(frame, height=1, width=52)
urlArea.insert(INSERT,"Enter Youtube Link:")
urlArea.pack()

#creat the button
findButton=customtkinter.CTkButton(frame, font=("Arial",20), text="Find Video", fg_color="red" , hover_color=("#DB3E39", "#821D1A"))
findButton.pack()


    
#Open an Error Message Frame
def errorPopUp(message):
    #Add ERROR MESSAGE Pop up
    top=Toplevel(root)
    top.geometry("850x200")
    Label(top , text=str(message) , font=("Arial 20")).pack()

def downloadPopUp(url):
    #Connect to youtube to verify link and get the video
    youtubeObject = YouTube(url)
    #Get the Thumbnail from the video to show to user
    thumbnailUrl=youtubeObject.thumbnail_url
    urllib.request.urlretrieve(thumbnailUrl,"thumbnail.png")
    img=ImageTk.PhotoImage(Image.open("thumbnail.png"))

    #Pop Up a Extra Window
    top=Toplevel(root)
    top.geometry("1280x720")

    #Create a frame for the left and right
    frameLeft=Frame(top)
    frameLeft.grid(row=0,column=0)
    frameRight=Frame(top)
    frameRight.grid(row=0,column=1)
    #Display the thumbnail in the frame
    panel=Label(frameLeft,image=img)
    panel.image=img
    panel.pack()

    downloadButton=customtkinter.CTkButton(frameLeft, font=("Arial",20), text="Download" , command=download, fg_color="red" , hover_color=("#DB3E39", "#821D1A"))
    downloadButton.pack()

    #Add the Title and uploader to the right frame

    #Add menu to select Quality that you want to download

    #Download the highest Resolution
    #I want to change this so you can pick the resolution you download
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    
#Add a button to confirm that the video can be found
def find():
    url=urlArea.get("1.0","end")
    #Remove any leading text before URL
    if(url.__contains__("www.youtube.com")):
        index=url.find("www.") #get index of the first w in www.
        url=url[index: url.__len__()] #remove everything before the www. to extract just the link
        downloadPopUp(url)
    else:
         errorPopUp("Link Is Not From Youtube")
#On click the find button will call the find method
findButton._command=find
def download():

        try:
            #Get user to choose where to save the file
            fn=filedialog.askdirectory()
            youtubeObject.download(fn)
            #Everything Worked
            errorPopUp("Download Completed successfully")
        except:
            errorPopUp("An Error has occured")


#Start the GUI program
root.mainloop()