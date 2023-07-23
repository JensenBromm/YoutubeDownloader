import array
from tkinter import *
from tkinter import filedialog
import urllib.request
import customtkinter 
from pytube import *
from PIL import Image, ImageTk

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
    global youtubeObject 
    youtubeObject= YouTube(url)
    #Get the Thumbnail from the video to show to user
    thumbnailUrl=youtubeObject.thumbnail_url
    title=youtubeObject.title
    uploader=youtubeObject.author
    urllib.request.urlretrieve(thumbnailUrl,"thumbnail.png")
    img=ImageTk.PhotoImage(Image.open("thumbnail.png").resize((600,400)))
    

    #Pop Up a Extra Window
    top=Toplevel(root)
    top.geometry("1280x720")

    #Create a frame for the left and right
    frameLeft=Frame(top)
    frameLeft.grid(row=0,column=0)
    #frameLeft.pack()
    frameRight=Frame(top)
    frameRight.grid(row=0,column=1)
    #frameRight.pack()
    #Display the thumbnail in the frame
    panel=Label(frameLeft,image=img)
    panel.image=img
    panel.pack()
    #Make the download button and put it under the thumbnail
    downloadButton=customtkinter.CTkButton(frameLeft, font=("Arial",20), text="Download" , command=download, fg_color="red" , hover_color=("#DB3E39", "#821D1A"))
    downloadButton.pack()

    #Add the Title and uploader to the right frame
    titleLabel=Label(frameRight, text=title, font=("Arial" ,20))
    titleLabel.pack()
    uploaderLabel=Label(frameRight, text="By "+uploader,  font=("Arial" ,15))
    uploaderLabel.pack()

    #get all avalible streams
    global arr
    arr=youtubeObject.streams.filter(file_extension="mp4", progressive=True) #Progessive streams only so audio and video are combined
    global options
    options=['Highest']
    for i in arr:
         options.append(i.resolution)

    #Create Dropdown menu
    global clicked
    clicked=StringVar()
    drop= OptionMenu(frameLeft,clicked,*options)
    clicked.set( "Highest" )
    drop.pack()
    #Download the highest Resolution
    #I want to change this so you can pick the resolution you download
    
    
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
    global youtubeObject
    #filter the quality based on the drop down menu
    try:
        #Select Filtered Object
        if(clicked.get().__eq__("Highest")):
            youtubeObject=youtubeObject.streams.get_highest_resolution()
        else:
            #loop through the array of valid videos and get the correct resolution
            for i in arr:
                if(i.resolution.__eq__(clicked.get())):
                    youtubeObject=i
                    break

        #Get user to choose where to save the file
        fn=filedialog.askdirectory()
        #Filter returns an array so download the first one in the array
        youtubeObject.download(fn)
        #Everything Worked
        errorPopUp("Download Completed successfully")
    except:
        errorPopUp("An Error has occured")


#Start the GUI program
root.mainloop()