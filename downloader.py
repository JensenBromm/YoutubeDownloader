from tkinter import *
from tkinter import filedialog
from pytube import *

#create the frame for the GUI
root = Tk()
#Change the title of the frame
root.title("Youtube Video Downloader")
root.geometry("1280x720")
frame = Frame(root)
frame.pack()

#Open an Error Message Frame
def errorPopUp(message):
    #Add ERROR MESSAGE Pop up
    top=Toplevel(root)
    top.geometry("850x200")
    Label(top , text=str(message) , font=("Arial 20")).pack()

#Add a title to the frame
titleLabel= Label(frame,text="Youtube Downloader" , font=("Arial",30))
titleLabel.pack()

#Add Text Area for URL
urlArea=Text(frame, height=1, width=52)
urlArea.insert(INSERT,"Enter Youtube Link:")
urlArea.pack()

#Download Method for when the Download Button is clicked
def download():
    link=urlArea.get("1.0","end")

    #Remove any leading text before URL
    if(link.__contains__("www.youtube.com")):
        index=link.find("www.")
        link=link[index: link.__len__()]
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        try:
            
            fn=filedialog.askdirectory()

            youtubeObject.download(fn)
        except:
            errorPopUp("An Error has occured")

        errorPopUp("Download Completed successfully")

    else:
        errorPopUp("Link is not from Youtube. Make sure it contains 'www.youtube.com' ")
    
    print(link)

#add the button to download the video
downloadButton=Button(frame, font=("Arial",20), text="Download" , command=download)
downloadButton.pack()

#Start the GUI program
root.mainloop()