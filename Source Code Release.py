import json
import urllib.request as urllib2
import webbrowser
from datetime import date
from tkinter import *
import tkinter as tk
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import tkinter.messagebox as mb
from urllib.parse import quote
import requests
import customtkinter
import urllib.request
from time import sleep
import sys
import os
from showinfm import show_in_file_manager
from datetime import datetime

# Set appearance mode and default color theme based on stored config

f = open('Resources/Scripts/Config.json')
data = json.load(f)
buttoncolor = data.get("buttoncolor")
themecolor = data.get("theme")

if str(themecolor) != " ":
    customtkinter.set_appearance_mode(themecolor)
else:
    customtkinter.set_appearance_mode("Dark")

if str(buttoncolor) != " ":
    customtkinter.set_default_color_theme(buttoncolor)
else:
    customtkinter.set_default_color_theme("blue")

# Set default values for variables, these are the values needed for side changing in e.g. the guild members
def_search = index = counter = index2 = counter2 = index3 = 0
index4 = 0
cap, cap2, cap3, cap4 = 18, 18, 6, 8
startpunkt, startpunkt2, startpunkt3, startpunkt4 = 0, 0, 0, 0

# Set up the root window
x, y = 500, 400
root = tk.Tk()
root.title('Oracle\'s Eye')
root.geometry(f"{x}x{y}")
root.iconbitmap(r"Resources/eye-tracking.ico")
frame = customtkinter.CTkFrame(root)
frame.pack(pady=0, padx=0, fill="both", expand=True)

# Center the root window on the screen, make it not resizable
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - 300 / 2)
center_y = int(screen_height / 2 - 318 / 2)
root.geometry(f'{x}x{y}+{center_x}+{center_y}')
root.resizable(False, False)


# callback for side menu (menu1), destroys it if cursour is not in range
def callback(e):
    x = e.x
    y = e.y

    if e.x <= 385:
        frame2.place_forget()
    print("Pointer is currently at %d, %d" % (x, y))


# if hoverlabel is hovered, open menu call
def on_enter(e):
    # pass
    menu1()


frame.bind('<Motion>', callback)

s_index = 0

# static paths to the needed resources stoed as variables
guildicon = PhotoImage(file="Resources/Icons/verein.png")
friendicon = PhotoImage(file="Resources/Icons/wiedervereinigung.png")
zurueck = PhotoImage(file=r"Resources\Icons/zuruck.png")
pho = PhotoImage(file=r"Resources\Icons/ausloggen.png")
pro = PhotoImage(file=r"Resources\Icons/profil.png")
forw = PhotoImage(file="Resources/Icons/forward.png")
backw = PhotoImage(file="Resources/Icons/backward.png")
github = PhotoImage(file="Resources/Icons/github.png")
settings = PhotoImage(file="Resources/Icons/einstellen.png")
copyr = PhotoImage(file="Resources/Icons/copyright.png")
sear = PhotoImage(file="Resources/Icons/glas.png")
markt = PhotoImage(file="Resources/Icons/markt.png")
memID = 0
memgender = ""
memgender2 = ""


# side menu including content
def menu1():
    global frame2
    frame2 = customtkinter.CTkFrame(root, width=120, height=400)
    frame2.place(x=380, y=0)


    page = customtkinter.CTkButton(frame2, text="Jobs", anchor=RIGHT, image=forw, command=page2, width=104, height=40)
    page.place(x=8, y=60)

    Friendbut1 = customtkinter.CTkButton(frame2, text="Logout", anchor=RIGHT, image=zurueck, command=back, width=104,
                                         height=40)
    Friendbut1.place(x=8, y=310)
    # guildmember
    Friendbut2 = customtkinter.CTkButton(frame2, text="Social", anchor=RIGHT, image=friendicon, command=guildmember,
                                         width=104, height=40)
    Friendbut2.place(x=8, y=210)

    Friendbut3 = customtkinter.CTkButton(frame2, text="Guild", anchor=RIGHT, image=guildicon, command=guild, width=104,
                                         height=40)
    Friendbut3.place(x=8, y=160)

    Friendbut3 = customtkinter.CTkButton(frame2, text="Misc.", anchor=RIGHT, image=settings, command=misc, width=104,
                                         height=40)
    Friendbut3.place(x=8, y=260)

    Friendbut4 = customtkinter.CTkButton(frame2, text="Profile", anchor=RIGHT, image=pro, command=Profile, width=104,
                                         height=40)
    Friendbut4.place(x=8, y=10)

    Friendbut4 = customtkinter.CTkButton(frame2, text="Search", anchor=RIGHT, image=sear, command=search_opt, width=104,
                                         height=40)
    Friendbut4.place(x=8, y=110)


# choose search engine. provides 2 buttons, each calls different new window with search field
def search_opt():
    for child in frame.winfo_children():
        child.destroy()

    custom_font = ("Arial", 20, 'bold')

    Label1 = customtkinter.CTkLabel(frame, text="Choose a search engine", font=custom_font, width=200, height=20)
    Label1.place(x=140, y=30)

    Friendbut4 = customtkinter.CTkButton(frame, text="Items", font=custom_font, anchor=RIGHT, image=sear,
                                         command=search, width=200, height=100)  # option 1
    Friendbut4.place(x=25, y=120)

    Friendbut4 = customtkinter.CTkButton(frame, text="Market", font=custom_font, anchor=RIGHT, image=markt,
                                         command=market, width=200, height=100)  # option 2
    Friendbut4.place(x=275, y=120)

    Friendbut4 = customtkinter.CTkButton(frame, text="Player", font=custom_font, anchor=RIGHT, image=friendicon,
                                         command=search_player, width=200, height=100)  # option 3
    Friendbut4.place(x=25, y=235)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    Label2 = customtkinter.CTkLabel(frame,
                                    text="Items search shows Items from the game. Market\n"
                                         "works more like the market board and shows prices.",
                                    width=400, height=20)
    Label2.place(x=50, y=60)

    Bozbut = customtkinter.CTkButton(frame, text="Back", command=Profile, width=100, height=20)
    Bozbut.place(x=375, y=350)


# misc menu. Contains buttons with weblinks or plain text popup and theme change
def misc():
    global radiobutton_2
    if frame2:
        frame2.destroy()
    for child in frame.winfo_children():
        child.destroy()

    def universalis():
        webbrowser.open("https://universalis.app/")

    def projects():
        webbrowser.open("https://github.com/snomsionius?tab=repositories")

    def credits():
        mb.showinfo("Copyright&Info",
                    "Please note that this version of the lodestone is fanmade and fully relies on a fanmade API. If "
                    "it doesnt work somedays, it most likely is because Yoshi P changed something in the game "
                    "files.Please refrain from commenting on GitHub. When I notice somthing is wrong, I will most "
                    "likely make a new version depending on how many people downloaded this tool.\n\n "
                    "Feel free to share the tool on your website or chat etc. if you like it.\n\n"
                    "The download must happen via my GitHub, creating your own download link is forbidden.\n\n"
                    "The authors name (mine) needs to be mentioned.Taking credit for creating this program is "
                    "forbidden.\n\n "
                    "Asking for money to get a download link, from for example your own website, is forbidden.\n\n"
                    "This tool is FREE to use for everyone who wants to and it must stay like this\n\n"
                    "Whats new in version 5.0.0 ? \n\n"
                    "-Player-search implemented\n-Bugfixes")

    # check if a given config exists. if not, create one containing all neccessary values.
    def modus():
        global radiobutton_2, ID, dataserver

        if os.path.isfile('Resources/Scripts/Config.json'):
            f = open('Resources/Scripts/Config.json')
            data = json.load(f)
            if data != "":
                buttoncolor = data.get("buttoncolor")
                themecolor = data.get("theme")
                checkvar = data.get("remember")
                checkname = data.get("name")
                getserver = data.get("server")
        else:
            buttoncolor = ""
            themecolor = ""
            checkvar = 0
            checkname = ID
            sgetserver = dataserver

        # compare existing bg to other possible color. if white -> dark , dark -> white. gets stored in config

        if customtkinter.get_appearance_mode() == "Light":
            customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
            sleep(0.2)
            # radiobutton_2.deselect()
            dictionary = {
                "name": checkname,
                "remember": checkvar,
                "server": getserver,
                "eulacheck": 1, "buttoncolor": buttoncolor, "theme": str("Dark")

            }
            with open("Resources/Scripts/Config.json", "w") as outfile:
                json.dump(dictionary, outfile)

        else:
            customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
            sleep(0.2)

            dictionary = {
                "name": checkname,
                "remember": checkvar,
                "server": getserver,
                "eulacheck": 1, "buttoncolor": buttoncolor, "theme": str("Light")

            }
            with open("Resources/Scripts/Config.json", "w") as outfile:
                json.dump(dictionary, outfile)
            # radiobutton_2.deselect()

    def open_pic():
        show_in_file_manager('Resources/Images')

    def open_files():
        show_in_file_manager('Resources')

    # privacy center shows stored data in text.
    def privacy_set():
        global dataname, parsedate
        for child in frame.winfo_children():
            child.destroy()

        f = open('Resources/Scripts/Config.json')

        # returns JSON object as
        # a dictionary
        data = json.load(f)
        savedid = data.get("name")
        savedserver = data.get("server")

        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

        # print(stuff["Level"])
        my_label = customtkinter.CTkTextbox(frame, font=("Arial", 15, "bold"), width=125, height=20)
        my_label.insert(END, text=f"Privacy Center")
        my_label.place(x=187, y=15)
        my_label.configure(state="disabled")

        my_label = customtkinter.CTkTextbox(frame, wrap=WORD, width=400, height=305)
        my_label.insert(INSERT, text=f"You can always delete your data by logging out.\n"
                                     f"All data entered by the User does NOT get saved until the remember me "
                                     f"login is used. Then the data listed below will get saved to automatically log-in next time."
                                     f"Everything else, Guild data, Jobs, Profile data come from the FFXVI API (Unofficial) through "
                                     f"the App providing your ID, Server and Name. The App does NOT connect to another server besides the API,"
                                     f"so no data gets stored on another server. This data is needed to provide the service.\n"
                                     f"The following data is stored:\n\n"
                                     f"-Name: {dataname}\n"
                                     f"-ID: {ID}\n"
                                     f"Server: {savedserver}\n\n"
                                     f"The following can get stored:\n"
                                     f"-Name\n"
                                     f"-User-ID\n"
                                     f"-Server\n"
                                     f"                                                                    Data from: {dt_string}")

        my_label.configure(state="disabled")
        my_label.place(x=50, y=60)

        exitbut = customtkinter.CTkButton(frame, text="Back", command=misc, width=100, height=20)
        exitbut.place(x=350, y=375)

    # contains all neccessary information, links and buttons to other menus

    def appearance():
        for child in frame.winfo_children():
            child.destroy()
        creds = customtkinter.CTkLabel(frame, text="Made by snomsionius", width=150, height=20)
        creds.place(x=175, y=385)

        marlab = customtkinter.CTkLabel(frame, image=markt, compound=TOP, text="", width=40, height=40)
        marlab.place(x=75, y=100)

        gitlab = customtkinter.CTkLabel(frame, image=github, compound=TOP, text="", width=40, height=40)
        gitlab.place(x=75, y=150)

        coplab = customtkinter.CTkLabel(frame, image=copyr, compound=TOP, text="", width=40, height=40)
        coplab.place(x=265, y=100)

        Button2 = customtkinter.CTkButton(frame, text="FFXIV Universalis", command=universalis, width=100, height=20)
        Button2.place(x=125, y=110)

        Button3 = customtkinter.CTkButton(frame, text="More Projects", command=projects, width=100, height=20)
        Button3.place(x=125, y=160)

        Button4 = customtkinter.CTkButton(frame, text="Copyright&Info", command=credits, width=100, height=20)
        Button4.place(x=315, y=110)

        Button5 = customtkinter.CTkButton(frame, text="Show pictures", command=open_pic, width=100, height=20)
        Button5.place(x=315, y=160)

        Button6 = customtkinter.CTkButton(frame, text="App files", command=open_files, width=100, height=20)
        Button6.place(x=315, y=210)

        Button7 = customtkinter.CTkButton(frame, text="Privacy&Data", command=privacy_set, width=100, height=20)
        Button7.place(x=315, y=260)

        page = customtkinter.CTkButton(frame, text="", image=zurueck, command=Profile, width=30, height=30)
        page.place(x=455, y=350)

        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

        custom_font = ("Arial", 15, 'bold')

        settbut = customtkinter.CTkButton(frame, text="Links", font=custom_font, command=appearance, width=200,
                                          height=20)
        settbut.place(x=50, y=20)

        appbut = customtkinter.CTkButton(frame, text="Appereance", font=custom_font, command=settings, width=200,
                                         height=20)
        appbut.place(x=250, y=20)

    # change color theme of widgets and store the new value

    def settings():
        for child in frame.winfo_children():
            child.destroy()

        f = open('Resources/Scripts/Config.json')
        data = json.load(f)
        buttoncolor = data.get("buttoncolor")
        themecolor = data.get("theme")
        checkvar = data.get("remember")
        checkname = data.get("name")
        getserver = data.get("server")

        def color_theme():
            customtkinter.set_default_color_theme("dark-blue")
            sleep(0.2)
            dictionary = {
                "name": checkname,
                "remember": checkvar,
                "server": getserver,
                "eulacheck": 1, "buttoncolor": "dark-blue", "theme": themecolor

            }
            with open("Resources/Scripts/Config.json", "w") as outfile:
                json.dump(dictionary, outfile)
            radiobutton_4.deselect()
            radiobutton_5.deselect()
            settings()

        def color_theme1():
            customtkinter.set_default_color_theme("green")
            sleep(0.2)
            dictionary = {
                "name": checkname,
                "remember": checkvar,
                "server": getserver,
                "eulacheck": 1, "buttoncolor": "green", "theme": themecolor

            }
            with open("Resources/Scripts/Config.json", "w") as outfile:
                json.dump(dictionary, outfile)
            radiobutton_4.deselect()
            radiobutton_3.deselect()
            settings()

        def color_theme2():
            customtkinter.set_default_color_theme("blue")
            sleep(0.2)
            dictionary = {
                "name": checkname,
                "remember": checkvar,
                "server": getserver,
                "eulacheck": 1, "buttoncolor": "blue", "theme": themecolor

            }
            with open("Resources/Scripts/Config.json", "w") as outfile:
                json.dump(dictionary, outfile)
            radiobutton_3.deselect()
            radiobutton_5.deselect()
            settings()

        radiobutton_var = customtkinter.IntVar()
        radiobutton_var2 = customtkinter.IntVar()
        radiobutton_var3 = customtkinter.IntVar()
        radiobutton_var4 = customtkinter.IntVar()

        radiobutton_2 = customtkinter.CTkSwitch(frame, text="Change Theme", variable=radiobutton_var2, onvalue=1,
                                                offvalue=0,
                                                command=modus, width=130, height=20)
        radiobutton_2.place(x=75, y=100)

        radiobutton_3 = customtkinter.CTkRadioButton(frame, text="Dark_Blue Buttons", command=color_theme,
                                                     variable=radiobutton_var, value=1, width=130, height=20)
        radiobutton_3.place(x=75, y=220)

        radiobutton_4 = customtkinter.CTkRadioButton(frame, text="Blue Buttons", command=color_theme2,
                                                     variable=radiobutton_var3, value=1,
                                                     width=130, height=20)
        radiobutton_4.place(x=75, y=160)

        radiobutton_5 = customtkinter.CTkRadioButton(frame, text="Green Buttons", command=color_theme1,
                                                     variable=radiobutton_var4, value=1,
                                                     width=130, height=20)
        radiobutton_5.place(x=265, y=160)

        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

        creds = customtkinter.CTkLabel(frame, text="Made by snomsionius", width=150, height=20)
        creds.place(x=175, y=385)

        page = customtkinter.CTkButton(frame, text="", image=zurueck, command=Profile, width=30, height=30)
        page.place(x=455, y=350)

        custom_font = ("Arial", 15, 'bold')

        settbut = customtkinter.CTkButton(frame, text="Links", font=custom_font, command=appearance, width=200,
                                          height=20)
        settbut.place(x=50, y=20)

        appbut = customtkinter.CTkButton(frame, text="Appearance", font=custom_font, command=settings, width=200,
                                         height=20)
        appbut.place(x=250, y=20)

    appearance()


RADIUS = 10


# download function for getting files of images. uses urllib to get the file and requests it from the api

def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.png'
    with urllib.request.urlopen(url) as response, open(full_path, 'wb') as out_file:
        data = response.read()
        out_file.write(data)


# resize the image and blur the edges
def loadimage2(x):
    # Open an image
    im = Image.open(x)

    # Paste image on white background
    diam = 2 * RADIUS
    back = Image.new('RGB', (im.size[0] + diam, im.size[1] + diam), (255, 255, 255))
    back.paste(im, (RADIUS, RADIUS))

    # Create paste mask
    mask = Image.new('L', back.size, 0)
    draw = ImageDraw.Draw(mask)
    for d in range(diam + RADIUS):
        alpha = 255 if d < RADIUS else int(255 * (diam + RADIUS - d) / diam)
        draw.rectangle([d, d, back.size[0] - d, back.size[1] - d], outline=alpha)

    # Blur image and paste blurred edge according to mask
    blur = back.filter(ImageFilter.GaussianBlur(RADIUS / 2))
    back.paste(blur, mask=mask)

    back.save(x)


# create on png from the 3 parts of the guild icon.
def getgildpic():
    url = guildpics[0]
    url1 = guildpics[1]
    if len(guildpics) > 2:
        url2 = guildpics[2]
        # url = input('Please enter image URL (string):')
        file_name = "pic1"
        filename2 = "pic2"
        filename3 = "pic3"

        # download and store them via download function above

        download_image(url, 'Resources/Images/', file_name)
        download_image(url1, 'Resources/Images/', filename2)
        download_image(url2, 'Resources/Images/', filename3)

        bil1 = Image.open("Resources/Images/pic1.png")
        bil2 = Image.open("Resources/Images/pic2.png")
        bil3 = Image.open("Resources/Images/pic3.png")

        # paste them onto each other and save it for later

        bil1.paste(bil2, (0, 0), bil2)
        # bil2.show()
        bil1.paste(bil3, (0, 0), bil3)
        # bil1.show()
        bil1.save("Resources/Images/gildbild.png")

    else:
        # url = input('Please enter image URL (string):')
        file_name = "pic1"
        filename2 = "pic2"
        filename3 = "pic3"

        download_image(url, 'Resources/Images/', file_name)
        download_image(url1, 'Resources/Images/', filename2)
        # download_image(url2, 'Resources/Images/', filename3)

        bil1 = Image.open("Resources/Images/pic1.png")
        bil2 = Image.open("Resources/Images/pic2.png")
        # bil3 = Image.open("Resources/Images/pic3.png")

        bil1.paste(bil2, (0, 0), bil2)
        # bil2.show()
        # bil1.paste(bil3, (0, 0), bil3)
        # bil1.show()
        bil1.save("Resources/Images/gildbild.png")


def loadimage():
    global bild1
    bild1 = PhotoImage(file="Resources/Images/gildbild.png")

    # load the image from the file


def send():
    '''The big main function responsible for collecting all neccessary data after logging in. Sorry for globals. Gets
    time and checks wheter its remember login or not and coninues from there. It is in bot cases the same procedure.
    After that it collects all data about your character, your profile and the guild. Calls download of Profile picture,
    guild image and loads your profile.'''

    global datapic, dataname, dataserver, dataclub, dataact, datalevact, guildpics, Guildname, GuildServer, Guildslog, Guildtag, data1, data2, memdata, ID, request, Names, Ranks, Entry1, server, dt_string

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    f = open('Resources/Scripts/Config.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    checkvar = data.get("name")
    if str(checkvar) != "":
        ID = str(checkvar)
        print(ID, "send")
        f.close()

    if not checkvar:
        if Entry1.get().isdigit():
            ID = Entry1.get()
            Entry1.delete(0, END)

        else:
            if Entry1.get():
                print(Entry1.get(), "yooo")
                Entry = Entry1.get().replace(" ", "%20")
                link2 = f"https://xivapi.com/character/search?name={Entry}&server={server}"
                response = requests.get(link2, headers={'User-Agent': '<User-Agent>'})
                ID = response.json().get("Results")[0].get("ID")
                # dicti = data4.get("Results")[0]
                # ID = data4.get("ID")

                Entry1.delete(0, END)
                f.close()
    # ID = str(44023757)
    link = f"https://xivapi.com/character/{ID}"
    request = urllib2.Request(link)
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    data = json.loads(urllib2.urlopen(request).read())

    dataact, datalevact, datall, datapic, dataname, dataserver, dataclub = (
        data.get("Character").get("ActiveClassJob").get("UnlockedState").get("Name"),
        data.get("Character").get("ActiveClassJob").get("Level"),
        data.get("Character").get("ClassJobs"),
        data.get("Character").get("Portrait"),
        data.get("Character").get("Name"),
        data.get("Character").get("Server"),
        data.get("Character").get("Nameday")
    )
    num = list(range(0, 31))
    data1, data2 = [], []

    for j in num:
        data1.append(datall[j].get("UnlockedState").get("Name"))
        data2.append(datall[j].get("Level"))

    # link2 = f"https://xivapi.com/character/{ID}?data=FCM"
    request2 = urllib2.Request(f"https://xivapi.com/character/{ID}?data=FCM")
    request2.add_header('User-Agent', '&lt;User-Agent&gt;')
    data5 = json.loads(urllib2.urlopen(request2).read()).get("FreeCompanyMembers")
    # data5 = data4.get("FreeCompanyMembers")

    Names, Ranks, Avatare, IDs = [], [], [], []

    if data5 is not None:
        for member in data5:
            Names.append(member.get("Name"))
            Ranks.append(member.get("Rank"))
            Avatare.append(member.get("Avatar"))
            IDs.append(member.get("ID"))

    memdata, Memderdata, Memderdata2 = dict(zip(Names, IDs)), dict(zip(Names, Ranks)), dict(zip(Avatare, IDs))

    # link3 = f"https://xivapi.com/character/{ID}?data=FC"
    request3 = urllib2.Request(f"https://xivapi.com/character/{ID}?data=FC")
    request3.add_header('User-Agent', '&lt;User-Agent&gt;')
    data6 = json.loads(urllib2.urlopen(request3).read())
    guildpics = data6.get("FreeCompany").get("Crest")

    if data6.get("FreeCompany") is None:
        Guildname, GuildServer, Guildslog, Guildtag = "None", "None", "None", "None"
    else:
        Guildname, GuildServer, Guildslog, Guildtag = (
            data6.get("FreeCompany").get("Name"),
            data6.get("FreeCompany").get("Server"),
            data6.get("FreeCompany").get("Slogan"),
            data6.get("FreeCompany").get("Tag")
        )

    URL = str(datapic)
    download_image(URL, "Resources/Images/", "profpic")
    icon = data6.get("Character").get("Avatar")
    # download_image(icon, "Resources/Images/", "Avatar")

    loadimage2(r"Resources/Images/profpic.png")
    getgildpic()
    loadimage()
    Profile()
    print("ffinished")


def display_info(variable, variable2, variable3):
    '''Uses the information provided in the form of lists to display it in labels via loops.'''
    for child in frame.winfo_children():
        child.destroy()

    x = 100
    y = 245
    x2 = 0
    y2 = 50
    Bindex = 0
    Itemdict = variable

    descdict = variable2

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)
    # print("Itemdict", Itemdict)

    if Itemdict != "None":
        for i in Itemdict:

            my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
            my_label.insert(END, i)
            my_label.place(x=x, y=y)
            my_label.configure(state="disabled")

            display = Itemdict[i]
            # print(display)
            # if display["NQ"] != :
            # display = Itemdict[i]
            my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
            my_label.insert(END, str(display["NQ"]))
            my_label.place(x=x + 170, y=y)
            my_label.configure(state="disabled")

            y += 38  # Increase column to next on Left side
            Bindex += 1
            if (y >= 380):  # Maximum Number of elements in a row reached
                x += 160  # Go to Next row
                y = 50

    if descdict != "None":
        # print(descdict)
        my_label = customtkinter.CTkTextbox(frame, width=230, height=20)
        my_label.insert(END, str(descdict["Name"]))
        my_label.place(x=100, y=25)
        my_label.configure(state="disabled")

        my_label = customtkinter.CTkTextbox(frame, width=90, height=20)
        my_label.insert(END, "EQ-Lev: " + str(descdict["LevelEquip"]))
        my_label.place(x=340, y=25)
        my_label.configure(state="disabled")

        my_label = customtkinter.CTkTextbox(frame, width=330, height=70)
        my_label.insert(END, str(descdict["Description2"]) + "\n\n" + str(descdict["Description"]))
        my_label.place(x=100, y=110)
        my_label.configure(state="disabled")

        my_label = customtkinter.CTkTextbox(frame, width=90, height=20)
        my_label.insert(END, "I-Lev: " + str(descdict["LevelItem"]))
        my_label.place(x=340, y=65)
        my_label.configure(state="disabled")

        my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
        my_label.insert(END, "PriceLow:  " + str(descdict["PriceLow"]) + " Gil")
        my_label.place(x=100, y=200)
        my_label.configure(state="disabled")

        my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
        my_label.insert(END, "PriceMid:  " + str(descdict["PriceMid"]) + " Gil")
        my_label.place(x=270, y=200)
        my_label.configure(state="disabled")
        if descdict["ExName"]:
            my_label = customtkinter.CTkTextbox(frame, width=230, height=20)
            my_label.insert(END, str(descdict["ExName"]))
            my_label.place(x=100, y=65)
            my_label.configure(state="disabled")

    print(variable3)
    if variable3 != "None":
        for i in variable3:
            my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
            my_label.insert(END, i)
            my_label.place(x=x2, y=y2)
            my_label.configure(state="disabled")

            # display = Itemdict[i]
            my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
            my_label.insert(END, str(i[0]))
            my_label.place(x=x2 + 170, y=y2)
            my_label.configure(state="disabled")

            y += 38  # Increase column to next on Left side
            Bindex += 1
            if (y >= 380):  # Maximum Number of elements in a row reached
                x += 160  # Go to Next row
                y = 50


def display_search2(info, det, info2):
    '''Filters the data about the item and sorts it for display. and calls display info wile providing the funtion the
     values needed.'''

    print(info2)
    search_string2 = f"https://xivapi.com/item/{info}"
    headers = {'User-Agent': '&lt;User-Agent&gt;'}
    with urllib.request.urlopen(urllib.request.Request(search_string2, headers=headers)) as url:
        search_data2 = json.loads(url.read().decode())
    if det == "Item":
        stats = search_data2.get("Stats")
        if stats:
            display_info(
                stats,
                {
                    "Name": info2,
                    "Description": search_data2["BaseParam0"]["Description_en"],
                    "Description2": search_data2["BaseParam1"]["Description_en"],
                    "ExName": search_data2["GamePatch"]["ExName"],
                    "LevelEquip": search_data2["LevelEquip"],
                    "LevelItem": search_data2["LevelItem"],
                    "PriceLow": search_data2["PriceLow"],
                    "PriceMid": search_data2["PriceMid"],
                },
                "None",
            )
            print(search_data2)
        else:
            usedict = search_data2["BaseParamSpecial0"]
            print(usedict[2])
            print(search_data2["BaseParamSpecial0"]["Description_en"])
            display_info(
                "None",
                "None",
                {"Name": info2, "Description": search_data2["BaseParamSpecial0"]["Description_en"]},
            )
    else:
        mb.showinfo("Sorry", "Thats not an item")


def more_info(info, info2):
    '''If called, the function checks for displayable information for the item. If not compatible it redirects to the
    items web page. If compatible, reloads the window with the display_search command and provides everythig neccessary
    to it.'''

    encoded_info = quote(info)
    search_string2 = f"https://xivapi.com/search?string={encoded_info}"
    request = urllib2.Request(search_string2)
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    search_data2 = json.loads(urllib2.urlopen(request).read())
    search_data3 = search_data2.get("Results")
    search_data4 = search_data3[0]
    search_data5 = search_data4["ID"]
    det = search_data4["UrlType"]

    search_string9 = f"https://xivapi.com/item/{search_data5}"
    request = urllib2.Request(search_string9)
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    search_data9 = json.loads(urllib2.urlopen(request).read())

    if str(det) == "Item":
        if search_data9.get("Stats"):
            display_search2(search_data5, det, info2)
        else:
            x = mb.askyesno("Whoa",
                            "More information works only with Gear at the moment. If you want to, the item can be opened in your browser.\n\n"
                            "Sorry, but the file structure is very complicated.")
            if x:
                encoded_info = quote(info)
                webbrowser.open(f"https://eu.finalfantasyxiv.com/lodestone/playguide/db/search/?q={encoded_info}")


def present(results):
    '''Works exactly the same as list members of guild. Please look it up for more information.'''

    global cap2, index2, limit2, startpunkt2
    for child in frame.winfo_children():
        child.destroy()

    x = 20
    y = 50

    def createbuttons():

        Label1 = customtkinter.CTkLabel(frame, text="Results: (Are clickable)", width=100, height=40)
        Label1.place(x=20, y=5)

        page = customtkinter.CTkButton(frame, text="", image=backw, command=refreshing, width=30, height=30)
        page.place(x=410, y=350)

        page = customtkinter.CTkButton(frame, text="", image=forw, command=refreshing2, width=30, height=30)
        page.place(x=455, y=350)

        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

    def refreshing():
        global index2, startpunkt2, cap2, limit2
        # if index != 0:
        g = index2 - 18
        if g >= 0:
            index2 -= 18
            cap2 -= 18
            startpunkt2 -= 18
            refresh4(index2, cap2, startpunkt2)

    def refreshing2():
        global index2, startpunkt2, cap2, limit2
        h = cap2 + 18
        if h <= len(Names):
            print("kacke")
            index2 += 18
            cap2 += 18
            startpunkt2 += 18
            refresh2(index2, cap2, counter2, startpunkt2)

    def refresh4(index2, cap2, startpunkt2):
        for child in frame.winfo_children():
            child.destroy()

        listresults(x, y, index2, cap2, startpunkt2, counter2)
        # print(cap, index, startpunkt)
        createbuttons()

    def refresh2(index2, cap2, counter2, startpunkt2):
        print(cap2, index2, startpunkt2)
        listresults(x, y, index2, cap2, startpunkt2, counter2)

        createbuttons()

    def onClick(event):
        global info, info2
        info = event.widget.cget("text")
        info2 = event.widget.cget("text")

        more_info(info, info2)
        # get_item_id()

    def listresults(x, y, index2, cap2, startpunkt2, counter2):
        if results:
            print(len(results), results)
            for i in results[startpunkt2:cap2]:
                my_label = customtkinter.CTkLabel(frame, text=str(i), anchor=W, width=220, height=20)
                my_label.place(x=x, y=y)
                my_label.bind('<Button-1>', onClick)
                # my_label = customtkinter.CTkLabel(frame, anchor=E, text=str(results[index2]), width=100, height=20)
                # my_label.place(x=x + 125, y=y)
                y += 35  # Increase column to next on Left side
                if index2 <= cap:
                    index2 += 1

                if y >= 300:  # Maximum Number of elements in a row reached
                    if x <= 500:
                        x += 240  # Go to Next row
                        y = 50
        else:
            my_label = customtkinter.CTkLabel(frame,
                                              text="Sorry,your search wasn't successfull\n maybe your item wasn't eqiuppable",
                                              anchor=W, width=200, height=20)
            my_label.place(x=150, y=150)

    listresults(x, y, index2, cap2, startpunkt2, counter2)
    createbuttons()


def do_search():
    '''Calls the API for anything related or including the term. After that, filters for items and gets their name
    regardless if they can be displayed or not(Normal search)
    Detailed search gets the Name too but filters for items that have information that can be displayed.
    Calls the present function when finished.'''

    global def_search, radiobutton_var
    # print(str(search_entry.get()))
    search_string = "https://xivapi.com/search?string=" + str(search_entry.get().replace(" ", "%20"))

    request = urllib2.Request(search_string)
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    search_data = json.loads(urllib2.urlopen(request).read())
    stuff = search_data.get("Results")
    # print(stuff)

    results = []
    if radiobutton_var.get() == 0:
        print(radiobutton_var)
        for i in stuff:
            result = i
            if i["UrlType"] == "Item":
                results.append(result["Name"])
                # print(result["Name"])

    if radiobutton_var.get() == 1:

        for i in stuff:
            print(i)
            result = i
            # filter2 = result[i]

            if i["UrlType"] == "Item":
                info = i["Name"].replace(" ", "%20")

                search_string2 = "https://xivapi.com/search?string=" + info
                # search_string2 = "https://xivapi.com/item/"+str(info)
                print(search_string2)
                request2 = urllib2.Request(search_string2)
                request2.add_header('User-Agent', '&lt;User-Agent&gt;')
                search_data2 = json.loads(urllib2.urlopen(request2).read())
                stuff = search_data2.get("Results")
                search_data3 = search_data2.get("Results")
                search_data4 = search_data3[0]
                search_data5 = search_data4["ID"]
                det = search_data4["UrlType"]
                search_string9 = "https://xivapi.com/item/" + str(search_data5)
                print(search_string9)
                import requests
                request3 = urllib2.Request(search_string9)
                request3.add_header('User-Agent', '&lt;User-Agent&gt;')

                search_data9 = json.loads(urllib2.urlopen(request3).read())

                if str(search_data9.get("Stats")) != "None":
                    results.append(result["Name"])
                # print(result["Name"])

    present(results)


def search():
    '''Provides an entry window for entering a search term. When pressing detailed search, it uses another algorithm'''

    for child in frame.winfo_children():
        child.destroy()
    global search_entry

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    Label1 = customtkinter.CTkLabel(frame, text="Search for anything you like", width=200, height=40)
    Label1.place(x=150, y=50)

    search_entry = customtkinter.CTkEntry(frame, width=300, height=20)
    search_entry.place(x=100, y=100)

    Button1 = customtkinter.CTkButton(frame, text="Search", command=do_search, width=100, height=40)
    Button1.place(x=200, y=140)

    global radiobutton_var
    radiobutton_var = customtkinter.IntVar()

    radiobutton_1 = customtkinter.CTkSwitch(master=frame, text="Detailed Search", variable=radiobutton_var, onvalue=1,
                                            width=100, height=20)
    radiobutton_1.place(x=185, y=195)

    Label2 = customtkinter.CTkLabel(frame,
                                    text="Detailed search shows ALL items that can be displayed in App."
                                         "Normal \nsearch shows everything related to the term",
                                    width=400, height=20)
    Label2.place(x=50, y=360)


def market_present(results, PriceLow, PriceMid):
    global cap4, index4, limit4, startpunkt4
    for child in frame.winfo_children():
        child.destroy()

    x = 55
    y = 60

    def createbuttons():

        Label1 = customtkinter.CTkLabel(frame, text="Results: (Are clickable)", width=100, height=40)
        Label1.place(x=40, y=5)
        Label2 = customtkinter.CTkLabel(frame, text="Lowest Price:", width=100, height=40)
        Label2.place(x=240, y=5)
        Label3 = customtkinter.CTkLabel(frame, text="Highest Price:", width=100, height=40)
        Label3.place(x=340, y=5)

        page = customtkinter.CTkButton(frame, text="", image=backw, command=refreshing, width=30, height=30)
        page.place(x=410, y=350)

        page = customtkinter.CTkButton(frame, text="", image=forw, command=refreshing2, width=30, height=30)
        page.place(x=455, y=350)

        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

    def refreshing():
        global index4, startpunkt4, cap4
        # if index != 0:
        g = index4 - 8
        if g >= 0:
            index4 -= 8
            cap4 -= 8
            startpunkt4 -= 8
            refresh4(index4, cap4, startpunkt4)

    def refreshing2():
        global index4, startpunkt4, cap4
        h = cap4 + 8
        if h <= len(results):
            print("kacke")
            index4 += 8
            cap4 += 8
            startpunkt4 += 8
        refresh2(index4, cap4, counter2, startpunkt4)

    def refresh4(index4, cap4, startpunkt4):
        for child in frame.winfo_children():
            child.destroy()

        listresults(x, y, index4, cap4, startpunkt4, counter2)
        # print(cap, index, startpunkt)
        createbuttons()

    def refresh2(index4, cap4, counter2, startpunkt4):
        print(cap4, index4, startpunkt4)
        listresults(x, y, index4, cap4, startpunkt4, counter2)

        createbuttons()

    def onClick(event):
        global info, info2
        info = event.widget.cget("text")
        info2 = event.widget.cget("text")

        more_info(info, info2)
        # get_item_id()

    def listresults(x, y, index4, cap4, startpunkt4, counter2):
        if results:
            print(len(results), results)
            for i in results[startpunkt4:cap4]:
                my_label = customtkinter.CTkLabel(frame, text=str(i), anchor=W, width=220, height=20)
                my_label.place(x=x, y=y)
                my_label.bind('<Button-1>', onClick)
                my_label = customtkinter.CTkLabel(frame, anchor=E, text=str(PriceLow[index4]) + "gil", width=50,
                                                  height=20)
                my_label.place(x=x + 220, y=y)
                my_label = customtkinter.CTkLabel(frame, anchor=E, text=str(PriceMid[index4]) + "gil", width=50,
                                                  height=20)
                my_label.place(x=x + 320, y=y)
                y += 35  # Increase column to next on Left side
                if index4 <= cap4:
                    index4 += 1

                if y >= 310:  # Maximum Number of elements in a row reached
                    if x <= 500:
                        x += 240  # Go to Next row
                        y = 60
        else:
            my_label = customtkinter.CTkLabel(frame,
                                              text="Sorry,your search wasn't successfull\n maybe your item wasn't eqiuppable",
                                              anchor=W, width=200, height=20)
            my_label.place(x=150, y=150)

    listresults(x, y, index4, cap4, startpunkt4, counter2)
    createbuttons()


def display_market_search(results):
    import requests

    PriceLow = []
    PriceMid = []

    def search_price(results):
        if len(results) == 0:
            return
        i = results[0]
        encoded_info = i.replace(" ", "%20")
        search_string2 = f"https://xivapi.com/search?string={encoded_info}"
        headers = {'User-Agent': '<User-Agent>'}
        search_data2 = requests.get(search_string2, headers=headers).json()
        search_data3 = search_data2.get("Results")
        search_data4 = search_data3[0]
        search_data5 = search_data4["ID"]
        search_string9 = f"https://xivapi.com/item/{search_data5}"
        search_data9 = requests.get(search_string9, headers=headers).json()
        PriceLow.append(search_data9["PriceLow"])
        PriceMid.append(search_data9["PriceMid"])
        search_price(results[1:])

    search_price(results)

    market_present(results, PriceLow, PriceMid)


def do_market_search():
    global def_search, radiobutton_var
    # print(str(search_entry.get()))
    search_string = "https://xivapi.com/search?string=" + str(search_entry.get().replace(" ", "%20"))

    request = urllib2.Request(search_string)
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    search_data = json.loads(urllib2.urlopen(request).read())
    # print(search_data)
    stuff = search_data.get("Results")

    results = []
    if radiobutton_var.get() == 0:
        # print(radiobutton_var)
        for i in stuff:
            result = i
            if i["UrlType"] == "Item":
                results.append(result["Name"])
                # print(result["Name"])
        display_market_search(results)

    if radiobutton_var.get() == 1:

        for i in stuff:
            print(i)
            result = i
            # filter2 = result[i]

            if i["UrlType"] == "Item":
                info = i["Name"].replace(" ", "%20")

                search_string2 = "https://xivapi.com/search?string=" + info
                # search_string2 = "https://xivapi.com/item/"+str(info)
                print(search_string2)
                request2 = urllib2.Request(search_string2)
                request2.add_header('User-Agent', '&lt;User-Agent&gt;')
                search_data2 = json.loads(urllib2.urlopen(request2).read())
                stuff = search_data2.get("Results")
                search_data3 = search_data2.get("Results")
                search_data4 = search_data3[0]
                search_data5 = search_data4["ID"]
                det = search_data4["UrlType"]
                search_string9 = "https://xivapi.com/item/" + str(search_data5)
                print(search_string9)
                import requests
                request3 = urllib2.Request(search_string9)
                request3.add_header('User-Agent', '&lt;User-Agent&gt;')

                search_data9 = json.loads(urllib2.urlopen(request3).read())

                if str(search_data9.get("Stats")) != "None":
                    results.append(result["Name"])
                # print(result["Name"])

        display_market_search(results)
    # market_present(results)


def market():
    for child in frame.winfo_children():
        child.destroy()
    global search_entry, radiobutton_var

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    Label1 = customtkinter.CTkLabel(frame, text="What are you looking for?", width=200, height=40)
    Label1.place(x=150, y=50)

    search_entry = customtkinter.CTkEntry(frame, width=300, height=20)
    search_entry.place(x=100, y=100)

    Button1 = customtkinter.CTkButton(frame, text="Get prices", command=do_market_search, width=100, height=40)
    Button1.place(x=200, y=140)

    Label2 = customtkinter.CTkLabel(frame,
                                    text="This section works like the market board. Prices may vary from server"
                                         " \n to server. Use FFXIV Universalis for more info.",
                                    width=400, height=20)
    Label2.place(x=50, y=360)

    radiobutton_var = customtkinter.IntVar()

    radiobutton_1 = customtkinter.CTkSwitch(master=frame, text="Detailed Search", variable=radiobutton_var, onvalue=1,
                                            width=100, height=20)
    radiobutton_1.place(x=185, y=195)


def owngear():
    global startpunkt3, cap3

    startpunkt3 = startpunkt3
    cap3 = cap3

    for child in frame.winfo_children():
        child.destroy()
    link4 = "https://xivapi.com/character/" + str(ID) + "/data= FR"
    request4 = urllib2.Request(link4)
    request4.add_header('User-Agent', '&lt;User-Agent&gt;')
    data7 = json.loads(urllib2.urlopen(request).read())
    # print(data7)
    Elemdict = data7.get("Character").get("GearSet").get("Gear")
    Keylist = []
    for i in Elemdict.keys():
        Keylist.append(i)
    print(Elemdict)
    # print(Elemdict)
    x = 125
    y = 80

    def onClick(event):
        global info, info2
        info = event.widget.cget("text")
        info2 = event.widget.cget("text")

        more_info(info, info2)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    def createbuttons():

        Label1 = customtkinter.CTkTextbox(frame, width=200, height=20)
        Label1.insert(END, "Your current gear (Click it)")
        Label1.place(x=150, y=15)

        page = customtkinter.CTkButton(frame, text="", image=backw, command=refreshing, width=30, height=30)
        page.place(x=410, y=350)

        page = customtkinter.CTkButton(frame, text="", image=forw, command=refreshing2, width=30, height=30)
        page.place(x=455, y=350)

        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

    def refreshing():
        global index3, startpunkt3, cap3
        # if index != 0:
        g = index3 - 6
        if g >= 0:
            index3 -= 6
            cap3 -= 6
            startpunkt3 -= 6
            refresh4(index3, cap3, startpunkt3)

    def refreshing2():
        global index3, startpunkt3, cap3

        h = cap3 + 6
        if h <= len(Keylist):
            print("kacke", y)
            index3 += 6
            cap3 += 6
            startpunkt3 += 6
            refresh2(index3, cap3, startpunkt3, counter2)

    def refresh4(index3, cap3, startpunkt3):
        for child in frame.winfo_children():
            child.destroy()
        print(cap3, startpunkt3, index3)
        listresults(x, y, index3, cap3, startpunkt3, counter2)
        # print(cap, index, startpunkt)
        createbuttons()

    def refresh2(index3, cap3, counter3, startpunkt3):
        for child in frame.winfo_children():
            child.destroy()
        startpunkt3 += 6
        print(cap3, index3, startpunkt3)
        listresults(x, y, index3, cap3, startpunkt3, counter3)
        createbuttons()

    def listresults(x, y, index3, cap3, startpunkt3, counter2):
        # print(len(results), results)
        for i in Keylist[startpunkt3:cap3]:
            my_label55 = customtkinter.CTkLabel(frame, text=str(i), anchor=W, width=50, height=20)
            my_label55.place(x=x, y=y)
            display = Elemdict[i]
            getval = Elemdict[str(i)]

            # print(search_string9)
            import requests

            with requests.session() as session:
                search_string9 = "https://xivapi.com/item/" + str(getval["ID"])
                request3 = session.get(search_string9).json().get("Name")
                # request3.add_header('User-Agent', '&lt;User-Agent&gt;')

                # search_data9 = json.loads(urllib2.urlopen(request3.json()).read())
            # print(request3)
            # print(search_data9.get("Name"))

            my_label2 = customtkinter.CTkLabel(frame, text=str(request3), anchor=W, width=100, height=20)
            my_label2.place(x=x + 75, y=y)
            my_label2.bind('<Button-1>', onClick)

            y += 45  # Increase column to next on Left side
            if index3 <= cap3:
                index3 += 1

            if y >= 316:  # Maximum Number of elements in a row reached
                if x <= 355:
                    x += 240  # Go to Next row
                    y = 80

    listresults(x, y, index3, cap3, startpunkt3, counter2)
    createbuttons()


def Profile():
    '''Works exatly like memprofile except using the Information about yourself. Provides buttons to anvigate too.'''
    global state, function1, function2
    today = date.today()

    # Textual month, day and year
    d1 = today.strftime("%d.%m.%Y")
    for child in frame.winfo_children():
        child.destroy()

    # update delay in milliseconds
    UpdateDelay = 153

    def update():
        """Update customtkinter.CTkLabel text every whenever."""

        # the text to display
        s = "Hello" + " " + dataname + "" + "." + "How was your Day until now ? Today is the " + " " + d1 + ". How about you go and have a look at my GitHub ? There are more tools avaiable for you to try.                                    "

        global s_index

        double = s + '  ' + s + '  ' + s  # double string so slicing wraps around
        display = double[s_index:s_index + 60]  # get display slice
        label2.configure(text=display)  # show in customtkinter.CTkLabel

        s_index += 1  # shift next display one left
        if s_index >= len(double) // 2:  # reset index if near end of text
            s_index = 0

        frame.after(UpdateDelay, update)  # reschedule function

    frame.after(UpdateDelay, update)  # start the update mechanism

    im = Image.open("Resources/Images/profpic.png")
    im = im.resize((200, 260), Image.Resampling.BOX)
    photo = ImageTk.PhotoImage(im)
    phot = tk.Label(frame, image=photo, compound=TOP)
    phot.bind('<Motion>', callback)
    phot.image = photo
    phot.place(x=285, y=50, width=200, height=260)

    namelabel = customtkinter.CTkTextbox(frame, width=170, height=20)
    namelabel.place(x=25, y=40)
    namelabel.insert(END, dataname)
    namelabel.configure(state=DISABLED)

    label2 = customtkinter.CTkLabel(frame, text="", width=450, height=20)
    label2.place(x=25, y=15)

    daylabel = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel.place(x=25, y=75)
    daylabel.insert(END, "Your Nameday :")
    daylabel.configure(state=DISABLED)

    daylabel2 = customtkinter.CTkTextbox(frame, width=250, height=20)
    daylabel2.place(x=25, y=110)
    daylabel2.insert(END, dataclub)
    daylabel2.configure(state=DISABLED)

    daylabel3 = customtkinter.CTkTextbox(frame, width=190, height=20)
    daylabel3.place(x=25, y=145)
    daylabel3.insert(END, "You currently play on:")
    daylabel3.configure(state=DISABLED)

    daylabel4 = customtkinter.CTkTextbox(frame, width=100, height=20)
    daylabel4.place(x=25, y=180)
    daylabel4.insert(END, dataserver)
    daylabel4.configure(state=DISABLED)

    daylabel5 = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel5.place(x=25, y=215)
    daylabel5.insert(END, "Your ActiveClass :")
    daylabel5.configure(state=DISABLED)

    daylabel6 = customtkinter.CTkTextbox(frame, width=250, height=20)
    daylabel6.place(x=25, y=250)
    daylabel6.insert(END, dataact + "  " + "at level" + " " + str(datalevact))
    daylabel6.configure(state=DISABLED)

    daylabel7 = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel7.place(x=25, y=285)
    daylabel7.insert(END, "Your Free Company :")
    daylabel7.configure(state=DISABLED)

    daylabel8 = customtkinter.CTkTextbox(frame, width=150, height=20)
    daylabel8.place(x=25, y=320)
    daylabel8.insert(END, Guildname)
    daylabel8.configure(state=DISABLED)

    # page = customtkinter.CTkButton(frame,text = "Menu",command=menu1, width=100, height=32)
    # page.place(x=400, y=0)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    Bozbut = customtkinter.CTkButton(frame, text="Bozja", command=Bozjan, width=100, height=20)
    Bozbut.place(x=282, y=320)

    Elmbut = customtkinter.CTkButton(frame, text="Eureka", command=Elemental, width=100, height=20)
    Elmbut.place(x=384, y=320)

    Friendbut = customtkinter.CTkButton(frame, text="Exit", image=pho, command=logout, width=100, height=40)
    Friendbut.place(x=384, y=345)

    Friendbut = customtkinter.CTkButton(frame, text="Gear", command=owngear, width=100, height=40)
    Friendbut.place(x=282, y=345)


def createmem(memID):
    '''Main function for grabbing data about the member like server or name before calling his profile or downloading
        his pictures'''

    print(memID)
    global memdata1, memdata2, memGuildname, memdatapic, memdataname, memdataserver, memdataclub, memdataact, memdatalevact, memguildpics, memGuildname, memdata1, memdata2, memgender, memgender2

    # ID = str(Entry1.get())

    # input = input("CharacterID pls")
    # ID = 44023757
    # memlink = "https://xivapi.com/character/" + str(memID)

    # session = requests.session()
    memrequest = urllib2.Request(f"https://xivapi.com/character/{str(memID)}")
    # memrequest = session.get(memlink)
    memrequest.add_header('User-Agent', '&lt;User-Agent&gt;')
    memdata = json.loads(urllib2.urlopen(memrequest).read())

    memdataact = memdata.get("Character").get("ActiveClassJob").get("UnlockedState").get("Name")
    memdatalevact = memdata.get("Character").get("ActiveClassJob").get("Level")
    memdatall = memdata.get("Character").get("ClassJobs")
    memdatapic = memdata.get("Character").get("Portrait")
    memdataname = memdata.get("Character").get("Name")
    memdataserver = memdata.get("Character").get("Server")
    memdataclub = memdata.get("Character").get("Nameday")
    memgen = memdata.get("Character").get("Gender")
    if int(memgen) == 1:
        memgender = "His"
        memgender2 = "He"
    else:
        memgender = "Her"
        memgender2 = "She"

    # print(data)
    # Character Data
    # print(dataname,dataserver,dataclub,datapic)
    # data1 = data.get("Character").get("ActiveClassJob").get("Level")
    # webbrowser.open(datapic)

    num = []
    for i in range(0, 31):
        num.append(i)

    memdata1 = []
    memdata2 = []
    for j in num:
        d = memdatall[j].get("UnlockedState").get("Name")
        da = memdatall[j].get("Level")
        memdata1.append(d)
        memdata2.append(da)

    # Guild data
    memlink3 = "https://xivapi.com/character/" + str(memID) + "?data=FC"
    memrequest3 = urllib2.Request(memlink3)
    memrequest3.add_header('User-Agent', '&lt;User-Agent&gt;')
    memdata6 = json.loads(urllib2.urlopen(memrequest3).read())

    if memdata6.get("FreeCompany") is None:
        memGuildname = "None"

    else:
        memGuildname = memdata6.get("FreeCompany").get("Name")

    URL = str(memdatapic)
    download_image(URL, "Resources/Images/", "memprofpic")
    loadimage2("Resources/Images/memprofpic.png")
    getgildpic()
    loadimage()

    memProfile()


def memProfile():
    '''Member profile. Gets time and date and feeds it to label2. Displays all information about the member in labels.
       Provides Buttons to navigate around the members profile. They call functions defined below.'''
    today = date.today()

    # Textual month, day and year
    d1 = today.strftime("%d.%m.%Y")
    for child in frame.winfo_children():
        child.destroy()

    # update delay in milliseconds
    UpdateDelay = 153

    def update():
        """Update customtkinter.CTkLabel text every whenever."""

        # the text to display
        s = "You are currently seeing the profile of :" + " " + memdataname

        global s_index

        double = s + '  ' + s + '  ' + s  # double string so slicing wraps around
        display = double[s_index:s_index + 50]  # get display slice
        label2.configure(text=display)  # show in customtkinter.CTkLabel

        s_index += 1  # shift next display one left
        if s_index >= len(double) // 2:  # reset index if near end of text
            s_index = 0

        frame.after(UpdateDelay, update)  # reschedule function

    frame.after(UpdateDelay, update)  # start the update mechanism

    im = Image.open("Resources/Images/memprofpic.png")
    im = im.resize((200, 260), Image.Resampling.BOX)
    photo = ImageTk.PhotoImage(im)
    phot = tk.Label(frame, image=photo, compound=TOP)
    phot.image = photo
    phot.place(x=285, y=50, width=200, height=260)

    namelabel = customtkinter.CTkTextbox(frame, width=170, height=20)
    namelabel.place(x=25, y=40)
    namelabel.insert(END, memdataname)
    namelabel.configure(state=DISABLED)

    label2 = customtkinter.CTkLabel(frame, text="", width=450, height=20)
    label2.place(x=25, y=15)

    daylabel = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel.place(x=25, y=75)
    daylabel.insert(END, memgender + " Nameday :")
    daylabel.configure(state=DISABLED)

    daylabel2 = customtkinter.CTkTextbox(frame, width=250, height=20)
    daylabel2.place(x=25, y=110)
    daylabel2.insert(END, memdataclub)
    daylabel2.configure(state=DISABLED)

    daylabel3 = customtkinter.CTkTextbox(frame, width=190, height=20)
    daylabel3.place(x=25, y=145)
    daylabel3.insert(END, memgender2 + " currently play on:")
    daylabel3.configure(state=DISABLED)

    daylabel4 = customtkinter.CTkTextbox(frame, width=100, height=20)
    daylabel4.place(x=25, y=180)
    daylabel4.insert(END, memdataserver)
    daylabel4.configure(state=DISABLED)

    daylabel5 = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel5.place(x=25, y=215)
    daylabel5.insert(END, memgender + " ActiveClass :")
    daylabel5.configure(state=DISABLED)

    daylabel6 = customtkinter.CTkTextbox(frame, width=250, height=20)
    daylabel6.place(x=25, y=250)
    daylabel6.insert(END, memdataact + "  " + "at level" + " " + str(memdatalevact))
    daylabel6.configure(state=DISABLED)

    daylabel7 = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel7.place(x=25, y=285)
    daylabel7.insert(END, "Member of :")
    daylabel7.configure(state=DISABLED)

    daylabel8 = customtkinter.CTkTextbox(frame, width=150, height=20)
    daylabel8.place(x=25, y=320)
    daylabel8.insert(END, memGuildname)
    daylabel8.configure(state=DISABLED)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    jobbut = customtkinter.CTkButton(frame, text="Jobs", command=mempage2, width=100, height=20)
    jobbut.place(x=384, y=350)

    Bozbut = customtkinter.CTkButton(frame, text="Back", command=guildmember, width=100, height=20)
    Bozbut.place(x=282, y=350)

    Bozbut = customtkinter.CTkButton(frame, text="Bozja", command=memBozjan, width=100, height=20)
    Bozbut.place(x=282, y=320)

    Elmbut = customtkinter.CTkButton(frame, text="Eureka", command=memElemental, width=100, height=20)
    Elmbut.place(x=384, y=320)


def memjobsite(h2):
    '''For more info, look at "jobsite" it is nearly the same functionbut with changing ID and pronouns based on gender
    of the character'''

    for child in frame.winfo_children():
        child.destroy()

    print(h2)
    spaces = 0
    for i in h2:
        if i == " ":
            spaces += 1

    print(spaces)

    if spaces >= 3:
        h2 = str(h2.split(" ")[0]) + " " + str(h2.split(" ")[1])
        print("h1", h2)
        spaces = 0

    else:
        h2 = h2.split(" ")[0]
        print("h2", h2)
        spaces = 0
    print(memID)
    link = f"https://xivapi.com/character/{memdata.get(memID)}"
    request = urllib2.Request(link)
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    data = json.loads(urllib2.urlopen(request).read()).get("Character").get("ClassJobs")
    stuff = ""
    # print(stuff)
    # h = "Botanist"
    for i in data:
        if str(h2) == i.get("UnlockedState").get("Name"):
            print(h2, i)
            stuff = i

    # print(stuff)
    custom_font = ("Arial", 15, 'bold')

    my_label = customtkinter.CTkLabel(frame,
                                      text=f"About {memgender} {h2}", font=custom_font,
                                      width=150, height=20)
    my_label.place(x=175, y=15)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    # print(stuff["Level"])
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"Level: {stuff['Level']}")
    my_label.place(x=75, y=80)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"About the current level:")
    my_label.place(x=75, y=115)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"{memgender2} has {stuff['ExpLevel']} exp out of {stuff['ExpLevelMax']}" if int(
        stuff['Level'] + 1) <= 90 and int(stuff['Level'] + 1) >= 0 else "Max xp")

    my_label.place(x=75, y=150)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END,
                    text=f"{memgender2} needs: {stuff['ExpLevelTogo']} exp for level {int(stuff['Level'] + 1) if not int(stuff['Level'] + 1) >= 90 else 'Max Level'}" if int(
                        stuff['Level'] + 1) <= 90 else "Max Level, no xp needed")
    my_label.place(x=75, y=185)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"Specialised: {stuff['IsSpecialised']}")
    my_label.place(x=75, y=235)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"ClassID: {stuff['ClassID']}")
    my_label.place(x=75, y=270)
    my_label.configure(state="disabled")
    exitbut = customtkinter.CTkButton(frame, text="Back", command=mempage2, width=100, height=20)
    exitbut.place(x=384, y=350)


def mempage2():
    '''Works like your own page2 function but uses guild member ID and cahnges you/r to she/her or he/his'''

    for child in frame.winfo_children():
        child.destroy()

    x = 15
    y = 50
    hindex = 0

    def onClick(event):
        h2 = event.widget.cget("text")
        memjobsite(h2)

    for data in memdata1:
        my_label = customtkinter.CTkLabel(frame, text=data + " lv. " + str(memdata2[hindex]), width=160, height=20)
        my_label.place(x=x, y=y)
        my_label.bind('<Button-1>', onClick)
        y += 30  # Increase column to next on Left side
        hindex += 1
        if (y >= 380):  # Maximum Number of elements in a row reached
            x += 160  # Go to Next row
            y = 50

    custom_font = ("Arial", 15, 'bold')

    my_label = customtkinter.CTkLabel(frame,
                                      text="His/Her Jobs + Level", font=custom_font,
                                      width=150, height=20)
    my_label.place(x=175, y=15)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    jobbut = customtkinter.CTkButton(frame, text="Profile", command=memProfile, width=100, height=20)
    jobbut.place(x=384, y=320)

    Bozbut = customtkinter.CTkButton(frame, text="Back", command=guildmember, width=100, height=20)
    Bozbut.place(x=384, y=350)

    Label2 = customtkinter.CTkLabel(frame, text="*Click name for more information", width=390,
                                    height=40)
    Label2.place(x=55, y=370)

def createplayer(memID):
    '''Main function for grabbing data about the member like server or name before calling his profile or downloading
        his pictures'''

    print(memID)
    global memdata1, memdata2, memGuildname, memdatapic, memdataname, memdataserver, memdataclub, memdataact, memdatalevact, memguildpics, memGuildname, memdata1, memdata2, memgender, memgender2

    # ID = str(Entry1.get())

    # input = input("CharacterID pls")
    # ID = 44023757
    # memlink = "https://xivapi.com/character/" + str(memID)

    # session = requests.session()
    memrequest = urllib2.Request(f"https://xivapi.com/character/{str(memID)}")
    # memrequest = session.get(memlink)
    memrequest.add_header('User-Agent', '&lt;User-Agent&gt;')
    memdata = json.loads(urllib2.urlopen(memrequest).read())

    memdataact = memdata.get("Character").get("ActiveClassJob").get("UnlockedState").get("Name")
    memdatalevact = memdata.get("Character").get("ActiveClassJob").get("Level")
    memdatall = memdata.get("Character").get("ClassJobs")
    memdatapic = memdata.get("Character").get("Portrait")
    memdataname = memdata.get("Character").get("Name")
    memdataserver = memdata.get("Character").get("Server")
    memdataclub = memdata.get("Character").get("Nameday")
    memgen = memdata.get("Character").get("Gender")
    if int(memgen) == 1:
        memgender = "His"
        memgender2 = "He"
    else:
        memgender = "Her"
        memgender2 = "She"

    # print(data)
    # Character Data
    # print(dataname,dataserver,dataclub,datapic)
    # data1 = data.get("Character").get("ActiveClassJob").get("Level")
    # webbrowser.open(datapic)

    num = []
    for i in range(0, 31):
        num.append(i)

    memdata1 = []
    memdata2 = []
    for j in num:
        d = memdatall[j].get("UnlockedState").get("Name")
        da = memdatall[j].get("Level")
        memdata1.append(d)
        memdata2.append(da)

    # Guild data
    memlink3 = "https://xivapi.com/character/" + str(memID) + "?data=FC"
    memrequest3 = urllib2.Request(memlink3)
    memrequest3.add_header('User-Agent', '&lt;User-Agent&gt;')
    memdata6 = json.loads(urllib2.urlopen(memrequest3).read())

    if memdata6.get("FreeCompany") is None:
        memGuildname = "None"

    else:
        memGuildname = memdata6.get("FreeCompany").get("Name")

    URL = str(memdatapic)
    download_image(URL, "Resources/Images/", "memprofpic")
    loadimage2("Resources/Images/memprofpic.png")
    getgildpic()
    loadimage()

    playerProfile()


def playerProfile():
    '''Member profile. Gets time and date and feeds it to label2. Displays all information about the member in labels.
       Provides Buttons to navigate around the members profile. They call functions defined below.'''
    today = date.today()

    # Textual month, day and year
    d1 = today.strftime("%d.%m.%Y")
    for child in frame.winfo_children():
        child.destroy()


    # update delay in milliseconds
    UpdateDelay = 153

    def update():
        """Update customtkinter.CTkLabel text every whenever."""

        # the text to display
        s = "You are currently seeing the profile of :" + " " + memdataname

        global s_index,playerID

        double = s + '  ' + s + '  ' + s  # double string so slicing wraps around
        display = double[s_index:s_index + 50]  # get display slice
        label2.configure(text=display)  # show in customtkinter.CTkLabel

        s_index += 1  # shift next display one left
        if s_index >= len(double) // 2:  # reset index if near end of text
            s_index = 0

        frame.after(UpdateDelay, update)  # reschedule function

    print(playerID)
    frame.after(UpdateDelay, update)  # start the update mechanism

    im = Image.open("Resources/Images/memprofpic.png")
    im = im.resize((200, 260), Image.Resampling.BOX)
    photo = ImageTk.PhotoImage(im)
    phot = tk.Label(frame, image=photo, compound=TOP)
    phot.image = photo
    phot.place(x=285, y=50, width=200, height=260)

    namelabel = customtkinter.CTkTextbox(frame, width=170, height=20)
    namelabel.place(x=25, y=40)
    namelabel.insert(END, memdataname)
    namelabel.configure(state=DISABLED)

    label2 = customtkinter.CTkLabel(frame, text="", width=450, height=20)
    label2.place(x=25, y=15)

    daylabel = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel.place(x=25, y=75)
    daylabel.insert(END, memgender + " Nameday :")
    daylabel.configure(state=DISABLED)

    daylabel2 = customtkinter.CTkTextbox(frame, width=250, height=20)
    daylabel2.place(x=25, y=110)
    daylabel2.insert(END, memdataclub)
    daylabel2.configure(state=DISABLED)

    daylabel3 = customtkinter.CTkTextbox(frame, width=190, height=20)
    daylabel3.place(x=25, y=145)
    daylabel3.insert(END, memgender2 + " currently play on:")
    daylabel3.configure(state=DISABLED)

    daylabel4 = customtkinter.CTkTextbox(frame, width=100, height=20)
    daylabel4.place(x=25, y=180)
    daylabel4.insert(END, memdataserver)
    daylabel4.configure(state=DISABLED)

    daylabel5 = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel5.place(x=25, y=215)
    daylabel5.insert(END, memgender + " ActiveClass :")
    daylabel5.configure(state=DISABLED)

    daylabel6 = customtkinter.CTkTextbox(frame, width=250, height=20)
    daylabel6.place(x=25, y=250)
    daylabel6.insert(END, memdataact + "  " + "at level" + " " + str(memdatalevact))
    daylabel6.configure(state=DISABLED)

    daylabel7 = customtkinter.CTkTextbox(frame, width=170, height=20)
    daylabel7.place(x=25, y=285)
    daylabel7.insert(END, "Member of :")
    daylabel7.configure(state=DISABLED)

    daylabel8 = customtkinter.CTkTextbox(frame, width=150, height=20)
    daylabel8.place(x=25, y=320)
    daylabel8.insert(END, memGuildname)
    daylabel8.configure(state=DISABLED)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    jobbut = customtkinter.CTkButton(frame, text="Jobs", command=playerpage2, width=100, height=20)
    jobbut.place(x=384, y=350)

    Bozbut = customtkinter.CTkButton(frame, text="Back", command=search_player, width=100, height=20)
    Bozbut.place(x=282, y=350)

    Bozbut = customtkinter.CTkButton(frame, text="Bozja", command=memBozjan, width=100, height=20)
    Bozbut.place(x=282, y=320)

    Elmbut = customtkinter.CTkButton(frame, text="Eureka", command=memElemental, width=100, height=20)
    Elmbut.place(x=384, y=320)


def playerjobsite(h2):
    global playerID
    '''For more info, look at "jobsite" it is nearly the same functionbut with changing ID and pronouns based on gender
    of the character'''

    for child in frame.winfo_children():
        child.destroy()

   # print(h2)
    spaces = 0
    for i in h2:
        if i == " ":
            spaces += 1

    #print(spaces)

    if spaces >= 3:
        h2 = str(h2.split(" ")[0]) + " " + str(h2.split(" ")[1])
        #print("h1", h2)
        spaces = 0

    else:
        h2 = h2.split(" ")[0]
        print("h2", h2)
        spaces = 0
   # print(playerID)
    link = f"https://xivapi.com/character/{playerID}"
    print(link)
    request = urllib2.Request(link)
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    data = json.loads(urllib2.urlopen(request).read()).get("Character").get("ClassJobs")
    stuff = ""
    # print(stuff)
    # h = "Botanist"
    for i in data:
        if str(h2) == i.get("UnlockedState").get("Name"):
            print(h2, i)
            stuff = i

    # print(stuff)
    custom_font = ("Arial", 15, 'bold')

    my_label = customtkinter.CTkLabel(frame,
                                      text=f"About {memgender} {h2}", font=custom_font,
                                      width=150, height=20)
    my_label.place(x=175, y=15)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    # print(stuff["Level"])
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"Level: {stuff['Level']}")
    my_label.place(x=75, y=80)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"About the current level:")
    my_label.place(x=75, y=115)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"{memgender2} has {stuff['ExpLevel']} exp out of {stuff['ExpLevelMax']}" if int(
        stuff['Level'] + 1) <= 90 and int(stuff['Level'] + 1) >= 0 else "Max xp")

    my_label.place(x=75, y=150)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END,
                    text=f"{memgender2} needs: {stuff['ExpLevelTogo']} exp for level {int(stuff['Level'] + 1) if not int(stuff['Level'] + 1) >= 90 else 'Max Level'}" if int(
                        stuff['Level'] + 1) <= 90 else "Max Level, no xp needed")
    my_label.place(x=75, y=185)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"Specialised: {stuff['IsSpecialised']}")
    my_label.place(x=75, y=235)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"ClassID: {stuff['ClassID']}")
    my_label.place(x=75, y=270)
    my_label.configure(state="disabled")
    exitbut = customtkinter.CTkButton(frame, text="Back", command=playerpage2, width=100, height=20)
    exitbut.place(x=384, y=350)


def playerpage2():
    '''Works like your own page2 function but uses guild member ID and cahnges you/r to she/her or he/his'''
    for child in frame.winfo_children():
        child.destroy()


    x = 15
    y = 50
    hindex = 0

    def onClick(event):
        h2 = event.widget.cget("text")
        playerjobsite(h2)

    for data in memdata1:
        global playerID
        print(playerID)
        my_label = customtkinter.CTkLabel(frame, text=data + " lv. " + str(memdata2[hindex]), width=160, height=20)
        my_label.place(x=x, y=y)
        my_label.bind('<Button-1>', onClick)
        y += 30  # Increase column to next on Left side
        hindex += 1
        if (y >= 380):  # Maximum Number of elements in a row reached
            x += 160  # Go to Next row
            y = 50

    custom_font = ("Arial", 15, 'bold')

    my_label = customtkinter.CTkLabel(frame,
                                      text="His/Her Jobs + Level", font=custom_font,
                                      width=150, height=20)
    my_label.place(x=175, y=15)


    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    jobbut = customtkinter.CTkButton(frame, text="Profile", command=playerProfile, width=100, height=20)
    jobbut.place(x=384, y=320)

    Bozbut = customtkinter.CTkButton(frame, text="Back", command=search_player, width=100, height=20)
    Bozbut.place(x=384, y=350)

    Label2 = customtkinter.CTkLabel(frame, text="*Click name for more information", width=390,
                                    height=40)
    Label2.place(x=55, y=370)



def search_player():
    '''This function provides an Entry widget where the user can enter a desired player name.
        It then gets send to do_player_search to process the player name and look it up as well as present it.'''

    for child in frame.winfo_children():
        child.destroy()
    global player_entry

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    Label1 = customtkinter.CTkLabel(frame, text="Who are you looking for?", width=200, height=40)
    Label1.place(x=150, y=50)

    player_entry = customtkinter.CTkEntry(frame, width=300, height=20)
    player_entry.place(x=100, y=100)

    Button1 = customtkinter.CTkButton(frame, text="Search", command=do_player_search, width=100, height=40)
    Button1.place(x=200, y=140)

    Label2 = customtkinter.CTkLabel(frame,
                                    text="Search for the name and then select the right result"
                                         "\n for more information",
                                    width=400, height=20)
    Label2.place(x=50, y=360)

def do_player_search():
    global player_entry


    def onClick(event):
        global playerID
        # get event widget content aka player name and server
        h = event.widget.get(1.0,END)

        # Split the string at the first occurrence of multiple consecutive spaces
        split_string = h.split("  ", 1)

        # Remove leading and trailing whitespace from each split part
        split_string = [part.strip() for part in split_string]

        coolerstring = f"{str(split_string[1].replace(' ', '%20'))}&server={split_string[0]}"
        print(coolerstring)

        request2 = urllib2.Request(
        "https://xivapi.com/character/search?name="+str(coolerstring))
        request2.add_header('User-Agent', '&lt;User-Agent&gt;')

        playerID = json.loads(urllib2.urlopen(request2).read()).get("Results")[0].get("ID")

        # Create the player page
        createplayer(playerID)


    request2 = urllib2.Request("https://xivapi.com/character/search?name="+(str(player_entry.get().replace(' ', '%20'))))
    request2.add_header('User-Agent', '&lt;User-Agent&gt;')
    server = json.loads(urllib2.urlopen(request2).read()).get("Results")

    servers = []
    Names = []

    for i in server:
        servers.append(i.get("Server"))
        Names.append(i.get("Name"))

    for child in frame.winfo_children():
        child.destroy()
    #print(servers)


    scrollable_frame = customtkinter.CTkScrollableFrame(frame, width=400, height=300)
    scrollable_frame.place(x=50,y=70)
    scrollable_frame.bind('<Motion>', callback)
    xi = 0
    x = 50
    y = 25
    Bindex = 0

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    my_label3 = customtkinter.CTkTextbox(frame, width=160, height=20)
    my_label3.insert(END, text="Server")
    my_label3.place(x=90, y=30)
    my_label3.configure(state="disabled")

    my_label3 = customtkinter.CTkTextbox(frame, width=160, height=20)
    my_label3.insert(END, text="Name")
    my_label3.place(x=260, y=30)
    my_label3.configure(state="disabled")



    if server != "None":
        for i in Names:
            '''Place the names and servers on the frame and connect them to the onClick function'''

            my_label = customtkinter.CTkTextbox(scrollable_frame,font=("Courier New",14), cursor="left_ptr", width=330, height=20)
            my_label.insert(END, text=str(servers[Bindex]).ljust(18)+str(i))
            my_label.grid(row=xi, column=0, padx=35, pady=5)
            my_label.configure(state="disabled")
            my_label.bind('<Button-1>', onClick)

            xi += 1
            y += 38  # Increase column to next on Left side
            Bindex += 1


def memBozjan():
    '''Look at Member Eureka.'''

    link4 = "https://xivapi.com/character/" + str(memID) + "/data= FR"
    request4 = urllib2.Request(link4)
    request4.add_header('User-Agent', '&lt;User-Agent&gt;')
    data7 = json.loads(urllib2.urlopen(request).read())
    Elemdict = data7.get("Character").get("ClassJobsBozjan")
    print(data7)
    # check = (str(Elemdict["Level"]))
    # if check == "None":
    #   mb.showinfo("Bozja", "It seems like the API didn't get the request right. Please come back later")

    for child in frame.winfo_children():
        child.destroy()

    x = 85
    y = 100
    Bindex = 0

    Elemdict = data7.get("Character").get("ClassJobsBozjan")
    print(Elemdict)

    my_label = customtkinter.CTkTextbox(frame, width=320, height=20)
    my_label.insert(END, f"Here you can have a look at some of {memgender} Bozja stats")
    my_label.place(x=90, y=10)
    my_label.configure(state="disabled")
    my_label1 = customtkinter.CTkLabel(frame,
                                       text=f"Bozja api response is weird, it could happen\n that the stats are useless",
                                       width=320, height=20)
    my_label1.place(x=90, y=315)

    for i in Elemdict:
        my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
        my_label.insert(END, i)
        my_label.place(x=x, y=y)
        my_label.configure(state="disabled")
        my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
        my_label.insert(END, str(Elemdict[i]))
        my_label.place(x=x + 170, y=y)
        my_label.configure(state="disabled")
        y += 38  # Increase column to next on Left side
        Bindex += 1
        if (y >= 380):  # Maximum Number of elements in a row reached
            x += 160  # Go to Next row
            y = 50

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    Bozbut = customtkinter.CTkButton(frame, text="Back", command=memProfile, width=100, height=20)
    Bozbut.place(x=384, y=350)


def memElemental():
    '''Works like own Elemental, but changes you to she/he and uses the member ID to get the data.'''

    link4 = "https://xivapi.com/character/" + str(memID) + "/data= FR"
    request4 = urllib2.Request(link4)
    request4.add_header('User-Agent', '&lt;User-Agent&gt;')
    data7 = json.loads(urllib2.urlopen(request).read())
    Elemdict = data7.get("Character").get("ClassJobsElemental")
    check = (str(Elemdict["Level"]))
    if check == "None":
        mb.showinfo("Eureka", "It seems like he/she hasnt played Eureka. Come back when he/she tried it.")
    else:

        for child in frame.winfo_children():
            child.destroy()

        x = 85
        y = 100
        Bindex = 0

        my_label = customtkinter.CTkTextbox(frame, width=340, height=20)
        my_label.insert(END, f"Here you can have a look at some of {memgender} Eureka stats")
        my_label.place(x=70, y=10)
        my_label.configure(state="disabled")
        for i in Elemdict:
            my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
            my_label.insert(END, i)
            my_label.place(x=x, y=y)
            my_label.configure(state="disabled")
            my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
            my_label.insert(END, str(Elemdict[i]))
            my_label.place(x=x + 170, y=y)
            my_label.configure(state="disabled")
            y += 38  # Increase column to next on Left side
            Bindex += 1
            if (y >= 380):  # Maximum Number of elements in a row reached
                x += 160  # Go to Next row
                y = 50
        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

        Bozbut = customtkinter.CTkButton(frame, text="Back", command=memProfile, width=100, height=20)
        Bozbut.place(x=384, y=350)


def Bozjan():
    '''Look at Eureka for more information. Works the same.'''

    link4 = "https://xivapi.com/character/" + str(ID) + "?data=FR"
    request4 = urllib2.Request(link4)
    request4.add_header('User-Agent', '&lt;User-Agent&gt;')
    data7 = json.loads(urllib2.urlopen(request).read())
    print(data7)
    Elemdict = data7.get("Character").get("ClassJobsBozjan")
    check = (str(Elemdict["Level"]))

    for child in frame.winfo_children():
        child.destroy()

    x = 85
    y = 100
    Bindex = 0

    Elemdict = data7.get("Character").get("ClassJobsBozjan")
    print(Elemdict)

    my_label = customtkinter.CTkTextbox(frame, width=320, height=20)
    my_label.insert(END, "Here you can have a look at some of your Bozja stats")
    my_label.place(x=90, y=10)
    my_label.configure(state="disabled")
    my_label1 = customtkinter.CTkLabel(frame,
                                       text=f"Bozja api response is weird, it could happen\n that the stats are useless",
                                       width=320, height=20)
    my_label1.place(x=90, y=315)

    for i in Elemdict:
        my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
        my_label.insert(END, i)
        my_label.place(x=x, y=y)
        my_label.configure(state="disabled")
        my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
        my_label.insert(END, str(Elemdict[i]))
        my_label.place(x=x + 170, y=y)
        my_label.configure(state="disabled")
        y += 38  # Increase column to next on Left side
        Bindex += 1
        if (y >= 380):  # Maximum Number of elements in a row reached
            x += 160  # Go to Next row
            y = 50
    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    Bozbut = customtkinter.CTkButton(frame, text="Back", command=Profile, width=100, height=20)
    Bozbut.place(x=384, y=350)


def Elemental():
    '''Calls the api with your ID to get the Eureka stats. Displays them in Labels.'''

    link4 = "https://xivapi.com/character/" + str(ID) + "/data= FR"
    request4 = urllib2.Request(link4)
    request4.add_header('User-Agent', '&lt;User-Agent&gt;')
    data7 = json.loads(urllib2.urlopen(request).read())
    Elemdict = data7.get("Character").get("ClassJobsElemental")
    check = (str(Elemdict["Level"]))
    if check == "None":
        mb.showinfo("Eureka", "It seems like you havent played Eureka. Come back when you tried it.")
    else:

        for child in frame.winfo_children():
            child.destroy()

        x = 85
        y = 100
        Bindex = 0

        my_label = customtkinter.CTkTextbox(frame, width=320, height=20)
        my_label.insert(END, "Here you can have a look at some of you Eureka stats")
        my_label.place(x=90, y=10)
        my_label.configure(state="disabled")
        for i in Elemdict:
            my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
            my_label.insert(END, i)
            my_label.place(x=x, y=y)
            my_label.configure(state="disabled")
            my_label = customtkinter.CTkTextbox(frame, width=160, height=20)
            my_label.insert(END, str(Elemdict[i]))
            my_label.place(x=x + 170, y=y)
            my_label.configure(state="disabled")
            y += 38  # Increase column to next on Left side
            Bindex += 1
            if (y >= 380):  # Maximum Number of elements in a row reached
                x += 160  # Go to Next row
                y = 50
        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

        Bozbut = customtkinter.CTkButton(frame, text="Back", command=Profile, width=100, height=20)
        Bozbut.place(x=384, y=350)


def jobsite(h):
    ''' Information about the selected job. Calls the api for the job to get information about its xp progress,
        Level, evolved or not. Lists it in labels'''

    for child in frame.winfo_children():
        child.destroy()

    print(h)
    spaces = 0
    for i in h:
        if i == " ":
            spaces += 1

    print(spaces)

    if spaces >= 3:
        h = str(h.split(" ")[0]) + " " + str(h.split(" ")[1])
        print("h1", h)
        spaces = 0

    else:
        h = h.split(" ")[0]
        print("h2", h)
        spaces = 0

    link = f"https://xivapi.com/character/{ID}"
    request = urllib2.Request(link)
    request.add_header('User-Agent', '&lt;User-Agent&gt;')
    data = json.loads(urllib2.urlopen(request).read()).get("Character").get("ClassJobs")
    stuff = ""
    # print(stuff)
    # h = "Botanist"
    for i in data:
        if str(h) == i.get("UnlockedState").get("Name"):
            print(h, i)
            stuff = i

    # print(stuff)
    custom_font = ("Arial", 15, 'bold')

    my_label = customtkinter.CTkLabel(frame,
                                      text=f"About your {h}", font=custom_font,
                                      width=150, height=20)
    my_label.place(x=175, y=15)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    # print(stuff["Level"])
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"Level: {stuff['Level']}")
    my_label.place(x=75, y=80)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"About the current level:")
    my_label.place(x=75, y=115)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"You have {stuff['ExpLevel']} exp out of {stuff['ExpLevelMax']}" if int(
        stuff['Level'] + 1) <= 90 and int(stuff['Level'] + 1) >= 0 else "Max xp")

    my_label.place(x=75, y=150)
    my_label.configure(state="disabled")

    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END,
                    text=f"You need: {stuff['ExpLevelTogo']} exp for level {int(stuff['Level'] + 1) if not int(stuff['Level'] + 1) >= 90 else 'Max Level'}" if int(
                        stuff['Level'] + 1) <= 90 else "Max Level, no xp needed")
    my_label.place(x=75, y=185)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"Specialised: {stuff['IsSpecialised']}")
    my_label.place(x=75, y=235)
    my_label.configure(state="disabled")
    my_label = customtkinter.CTkTextbox(frame, width=350, height=20)
    my_label.insert(END, text=f"ClassID: {stuff['ClassID']}")
    my_label.place(x=75, y=270)
    my_label.configure(state="disabled")
    exitbut = customtkinter.CTkButton(frame, text="Back", command=page2, width=100, height=20)
    exitbut.place(x=384, y=350)


def page2():
    ''' Works like guildmember functions except using the Job names and level info provided by the main function.
        Clickable, calls jobsite to display more information about the job.'''
    if frame2:
        frame2.destroy()

    for child in frame.winfo_children():
        child.destroy()

    def onClick(event):
        h = event.widget.cget("text")
        jobsite(h)

    # print(data2)

    x, y = 15, 50
    kindex = 0

    # Create all labels before placing them to improve performance
    labels = []
    for data in data1:
        label_text = f"{data} lv. {data2[kindex]}"
        label = customtkinter.CTkLabel(frame, text=label_text, width=160, height=20)
        labels.append(label)
        kindex += 1
    # Place all labels
    for label in labels:
        label.place(x=x, y=y)
        label.bind('<Button-1>', onClick)
        y += 30  # Increase column to next on Left side
        if y >= 380:  # Maximum Number of elements in a row reached
            x += 160  # Go to Next row
            y = 50

    custom_font = ("Arial", 15, 'bold')

    my_label = customtkinter.CTkLabel(frame,
                                      text="Your Jobs + Level", font=custom_font,
                                      width=150, height=20)
    my_label.place(x=175, y=15)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)

    Label2 = customtkinter.CTkLabel(frame, text="*Click name for more information", width=390,
                                    height=40)
    Label2.place(x=55, y=370)


def guildmember():
    '''List of guild members. 2 Buttons refresh the list of members based on index calculation by using the variables
    from the beginning of the code'''

    if frame2:
        frame2.destroy()
    global data1, data2, Guildname

    for child in frame.winfo_children():
        child.destroy()

    x = 15
    y = 50

    def createbuttons():

        custom_font = ("Arial", 15, 'bold')

        Label1 = customtkinter.CTkLabel(frame, text="Members of " + str(Guildname), font=custom_font, width=390,
                                        height=40)
        Label1.place(x=55, y=5)

        Label2 = customtkinter.CTkLabel(frame, text="*Click name for more information", width=390,
                                        height=40)
        Label2.place(x=55, y=370)

        page = customtkinter.CTkButton(frame, text="", image=backw, command=refreshing, width=30, height=30)
        page.place(x=410, y=350)

        page = customtkinter.CTkButton(frame, text="", image=forw, command=refreshing2, width=30, height=30)
        page.place(x=455, y=350)

        Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
        Hoverlabel.place(x=490, y=100)
        Hoverlabel.bind('<Enter>', on_enter)

    b = 18 - (len(data2) % 18)
    # print(data2)
    data1 += [""] * b
    data2 += [""] * b

    # calculate the list index by adding or substracting the number of elements on one page

    def refreshing():
        global index, startpunkt, cap, limit
        # if index != 0:
        g = index - 18
        if g >= 0:
            index -= 18
            cap -= 18
            startpunkt -= 18
            refresh4(index, cap, startpunkt)

    def refreshing2():
        global index, startpunkt, cap, limit
        h = cap + 18
        if h <= len(Names):
            print("kacke")
            index += 18
            cap += 18
            startpunkt += 18
            refresh2(index, cap, counter, startpunkt)

    def refresh4(index, cap, startpunkt):
        for child in frame.winfo_children():
            child.destroy()
        listmember(x, y, index, cap, startpunkt, counter)
        createbuttons()

    def refresh2(index, cap, counter, startpunkt):
        print(cap, index, startpunkt)
        listmember(x, y, index, cap, startpunkt, counter)

        createbuttons()

    # get the name in the label and call the create member function which loads and manages their profile

    def onClick(event):
        h = event.widget.cget("text")
        global memID
        memID = h
        createmem(memdata.get(memID))

    # list the members from a list via a loop.
    # Adding up the y values and x values to place them in a pleasing way

    def listmember(x, y, index, cap, startpunkt, counter):
        # if counter <= cap:
        print(cap, index, startpunkt)
        for data in Names[startpunkt:cap]:
            my_label = customtkinter.CTkLabel(frame, anchor=W, text=str(data), width=125, height=20)
            my_label.place(x=x, y=y)
            my_label.bind('<Button-1>', onClick)
            my_label = customtkinter.CTkLabel(frame, anchor=E, text=str(Ranks[index]), width=100, height=20)
            my_label.place(x=x + 125, y=y)
            y += 30  # Increase column to next on Left side
            if index <= cap:
                index += 1

            if y >= 300:  # Maximum Number of elements in a row reached
                if x <= 475:
                    x += 235  # Go to Next row
                    y = 50

    listmember(x, y, index, cap, startpunkt, counter)
    createbuttons()
    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)


def guild():
    '''Guild window. Shows all Information about the guild in labels. Provides buttons to go back to profile or guild
    member list'''

    for child in frame.winfo_children():
        child.destroy()
    if frame2:
        frame2.destroy()

    if Guildname == "NONE":
        mb.showinfo("Error", "You are not a member of a guild. Join a guild and try again later")
        Profile()

    # print(Guildname,GuildServer,Guildslog,Guildtag)
    label1 = customtkinter.CTkLabel(frame, image=bild1, compound=TOP, text="", width=128, height=128)
    label1.place(x=360, y=70)

    # Create textboxes with labels
    label2 = customtkinter.CTkTextbox(frame, width=230, height=20)
    label2.insert(END, "Here you can have a look at your guild")
    label2.place(x=135, y=5)

    label3 = customtkinter.CTkTextbox(frame, width=80, height=20)
    label3.place(x=25, y=50)
    label3.insert(END, "Name")
    label3.configure(state=DISABLED)

    label4 = customtkinter.CTkTextbox(frame, width=250, height=20)
    label4.place(x=25, y=85)
    label4.insert(END, Guildname)
    label4.configure(state=DISABLED)

    label5 = customtkinter.CTkTextbox(frame, width=80, height=20)
    label5.place(x=25, y=120)
    label5.insert(END, "Server")
    label5.configure(state=DISABLED)

    label6 = customtkinter.CTkTextbox(frame, width=250, height=20)
    label6.place(x=25, y=155)
    label6.insert(END, GuildServer)
    label6.configure(state=DISABLED)

    label7 = customtkinter.CTkTextbox(frame, width=80, height=20)
    label7.place(x=25, y=190)
    label7.insert(END, "Slogan")
    label7.configure(state=DISABLED)

    label8 = customtkinter.CTkTextbox(frame, width=400, height=60)
    label8.place(x=25, y=225)
    label8.insert(END, Guildslog)
    label8.configure(wrap=WORD, state=DISABLED)

    label9 = customtkinter.CTkTextbox(frame, width=80, height=20)
    label9.place(x=25, y=290)
    label9.insert(END, "Tag")
    label9.configure(state=DISABLED)

    label10 = customtkinter.CTkTextbox(frame, width=250, height=20)
    label10.place(x=25, y=325)
    label10.insert(END, Guildtag)
    label10.configure(state=DISABLED)

    page = customtkinter.CTkButton(frame, text="", image=forw, command=guildmember, width=30, height=30)
    page.place(x=455, y=350)

    Hoverlabel = customtkinter.CTkButton(frame, text="", width=10, height=200)
    Hoverlabel.place(x=490, y=100)
    Hoverlabel.bind('<Enter>', on_enter)


def back():
    '''Log out. Delete contents of .ini and restart from login.'''
    f = open('Resources/Scripts/Config.json')
    data = json.load(f)
    checkvar = data.get("eulacheck")
    buttoncolor = data.get("buttoncolor")
    themecolor = data.get("theme")
    if mb.askyesno("Info", "Do you want to re-login ?"):
        dictionary = {
            "name": "",
            "remember": "0",
            "server": "",
            "eulacheck": checkvar, "buttoncolor": buttoncolor, "theme": themecolor

        }
        with open("Resources/Scripts/Config.json", "w") as outfile:
            json.dump(dictionary, outfile)
        print(dictionary)
        frame2.place_forget()
        startwindow()
    else:
        pass


def logout():
    answer = mb.askyesno("Leave", "Do you really want to quit?")
    if answer:
        sys.exit()


def callback2(e):
    webbrowser.open("https://eu.finalfantasyxiv.com/lodestone/")


def remember_login():
    '''Remember login uses the given Data e.g. ID to grab the name, server and eula and ID and saves it in the .ini.
    Old entries get deleted. After saving, it provides the main function with the ID and your Profile gets loaded.'''

    global server
    # Data to be written

    f = open('Resources/Scripts/Config.json')
    data = json.load(f)
    checkvar = data.get("eulacheck")
    buttoncolor = data.get("buttoncolor")
    themecolor = data.get("theme")

    if Entry1.get().isdigit():
        print(Entry1.get())
        dictionary = {
            "name": str(Entry1.get()),
            "remember": "1",
            "eulacheck": checkvar, "buttoncolor": buttoncolor, "theme": themecolor
        }
        with open("Resources/Scripts/Config.json", "w") as outfile:
            json.dump(dictionary, outfile)

        send()
    # call the API to get the ID from Name login and start the main function. Saves the data too.
    if not Entry1.get().isdigit():
        if Entry1.get() != "":
            request2 = urllib2.Request(
                f"https://xivapi.com/character/search?name={str(Entry1.get().replace(' ', '%20'))}&server={server}")
            request2.add_header('User-Agent', '&lt;User-Agent&gt;')
            ID = json.loads(urllib2.urlopen(request2).read()).get("Results")[0].get("ID")
            dictionary = {
                "name": str(ID),
                "remember": "1",
                "server": server,
                "eulacheck": checkvar, "buttoncolor": buttoncolor, "theme": themecolor

            }
            with open("Resources/Scripts/Config.json", "w") as outfile:
                json.dump(dictionary, outfile)
            send()

    if Entry1.get() == "":
        mb.showerror("Login", "Please enter your ID first")
        radiobutton_4.deselect()


def startwindow():
    ''' Login window. Choose ID login and it gets straight to the main function above. Name login needs a bit more.
    Provide your Name in the field and select server and datacenter.'''

    for child in frame.winfo_children():
        child.destroy()
    global Entry1, radiobutton_4

    request2 = urllib2.Request("https://xivapi.com/servers/dc")
    request2.add_header('User-Agent', '&lt;User-Agent&gt;')
    servers = json.loads(urllib2.urlopen(request2).read())
    keys = [x for x in servers.keys()]
    # for key in servers.keys():
    #   keys.append(key)

    # frame.configure(bg="#3d3d3d")
    Label1 = customtkinter.CTkLabel(frame, text="Welcome,please log in with your\nCharacter ID or Name", width=200,
                                    height=40)
    Label1.place(x=150, y=40)

    Label2 = customtkinter.CTkLabel(frame,
                                    text="LogIn via name NEEDS DATACENTER and SERVER.\nYour ID is visible in the link to your lodestone profile. Please copy it.",
                                    width=400, height=20)
    Label2.place(x=50, y=350)

    Label5 = customtkinter.CTkLabel(frame,
                                    text="Or press",
                                    width=25, height=20)
    Label5.place(x=220, y=380)

    Label6 = customtkinter.CTkLabel(frame,
                                    text="here", text_color="#0287c3", cursor="Hand2",
                                    width=10, height=20)
    Label6.place(x=270, y=380)
    Label6.bind("<Button-1>", callback2)

    Label3 = customtkinter.CTkLabel(frame, text="Ver 5.0.0", width=50, height=20)
    Label3.place(x=450, y=385)

    Entry1 = customtkinter.CTkEntry(frame, width=100, height=20)
    Entry1.place(x=125, y=100)

    def optionmenu_callback(choice):
        '''Calls the function to fill the Widget. Same with callback2'''
        print("optionmenu dropdown clicked:", choice)
        optionmenu_2.configure(values=servers.get(choice))

    def optionmenu_callback2(choice):
        global server
        server = choice

    optionmenu_1 = customtkinter.CTkOptionMenu(frame, values=keys, command=optionmenu_callback, width=100, height=20)
    optionmenu_1.place(x=275, y=100)
    optionmenu_1.set("DataCenter")

    optionmenu_2 = customtkinter.CTkOptionMenu(frame, values=[], command=optionmenu_callback2, width=100, height=20)
    optionmenu_2.place(x=275, y=135)
    optionmenu_2.set("Server")

    Button1 = customtkinter.CTkButton(frame, text="Sign in", command=send, width=100, height=20)
    Button1.place(x=200, y=200)

    radiobutton_4 = customtkinter.CTkSwitch(frame, text="Remember me", onvalue=1,
                                            offvalue=0,
                                            command=remember_login, width=130, height=20)
    radiobutton_4.place(x=185, y=250)


def open_settings():
    os.system('start ms-settings:network-status')


def eula():
    ''' Checks if eula is agreed or not. If not, opens agreement window. Disagree results in shutting down, agree
    results in login window. The Choice gets stored in .ini in form 0 or 1'''

    f = open('Resources/Scripts/Config.json')
    data = json.load(f)
    checkvar = data.get("eulacheck")
    buttoncolor = data.get("buttoncolor")
    themecolor = data.get("theme")

    def agree_eula():
        dictionary = {
            "name": "",
            "remember": "",
            "server": "",
            "eulacheck": 1, "buttoncolor": buttoncolor, "theme": themecolor

        }
        with open("Resources/Scripts/Config.json", "w") as outfile:
            json.dump(dictionary, outfile)
        internet_on()

    def disagree_eula():
        dictionary = {
            "name": "",
            "remember": "",
            "server": "",
            "eulacheck": 0, "buttoncolor": buttoncolor, "theme": themecolor

        }
        with open("Resources/Scripts/Config.json", "w") as outfile:
            json.dump(dictionary, outfile)

        sys.exit()

    if checkvar == 1:
        send()

    else:
        for child in frame.winfo_children():
            child.destroy()

        my_label = customtkinter.CTkTextbox(frame, font=("Arial", 15, "bold"), width=140, height=20)
        my_label.insert(END, text=f"Terms of service")
        my_label.place(x=180, y=15)
        my_label.configure(state="disabled")

        my_label = customtkinter.CTkTextbox(frame, wrap=WORD, width=400, height=200)
        my_label.insert(INSERT,
                        text="LICENSE AGREEMENT\n\n"
                             "THIS IS A SUMMARY OF THE FULL LICENSE WHICH CAN BE READ ON GitHub\n\n"
                             "1. YOU shall refer to the user of this software.\n\n"
                             "2. I or ME/MY refers to the author of the software.\n\n"
                             "3. By using this software, you agree to the ways this application uses the data provided by you. More info stated below or under Settings->Privacy.\n\n"
                             "4. FREE FOR EVERYONE\n\n"
                             "This software is FREE to use for everyone. You are allowed to share it or link it on your website or elsewhere."
                             " Selling the software or access to download it, is forbidden.\n\n"
                             "5. DISTRIBUTION\n\nWhen you want to create a download link, please keep in mind that the download must happen via my GitHub.\n\n "
                             "ALWAYS mention the original author of the software.\n\n"
                             "6. OPEN SOURCE\n\n"
                             "This software shall be OpenSource. You can use the sourcecode from GitHub to your liking and make tools with it."
                             "HOWEVER all projects derived from it must be OpenSource and distributed free of charge."
                             "ALWAYS mention the author of the code. E.g. if someone made a project from my code and you base your prgram on it, credit both authors."
                             "I want this so it is evident who made what and noone takes credit for another mans work.\n\n"
                             "7. WARRANTY\n\n"
                             "This software comes AS IS and is not covered by any warranty from my side. If something goes wrong, i am not responsible in any way for any damage that may occur.\n\n"
                             "8. DATA COLLECTION & USAGE\n\n"
                             f"All data entered by the User does NOT get saved until the remember me "
                             f"login is used. Then the data listed below will get saved to automatically log-in next time."
                             f"Everything else, Guild data, Jobs, Profile data come from the FFXVI API (Unofficial) through "
                             f"the App providing your ID, Server and Name. The App does NOT connect to another server besides the API,"
                             f"so no data gets stored on another server. This data is needed to provide the service.\n\n"
                             f"9. HOW TO DELETE YOUR DATA\n\n"
                             f"You can always delete your data by logging out.\n\n"
                             f"The following can get stored:\n"
                             f"-Name\n"
                             f"-User-ID\n"
                             f"-Server\n\n\n\n"
                             "Copyright 2023 snomsionius")
        my_label.configure(state="disabled")
        my_label.place(x=50, y=60)

        checkbox_1 = customtkinter.CTkCheckBox(master=frame, text="I agree to the Terms of service.",
                                               command=agree_eula, width=120, height=20)
        checkbox_1.place(x=50, y=280)

        checkbox_1 = customtkinter.CTkCheckBox(master=frame, text="I do not accept the Terms of service",
                                               command=disagree_eula, width=120, height=20)
        checkbox_1.place(x=50, y=320)


def internet_on():
    ''' Pings google server for internet check. After that compares the values of eula agreement, remember login and
    name. Decides what happens after that. Negative results end in the app calling the neccessary window, e.g. eula not
    agreed or manually changed the value after logging in to disagree : App starts with eula checkbox and does NOT start
    without. If no Network detected, it can redirect the user to Windows network settings or try to reconnect and start
    over.'''

    try:
        requests.get("https://www.google.com", timeout=1)
        f = open('Resources/Scripts/Config.json')

        # returns JSON object as
        # a dictionary
        data = json.load(f)
        checkvar = data.get("remember")
        checkname = data.get("name")
        eulacheck = data.get("eulacheck")
        if str(checkvar) == "1":
            if str(checkname) != "":

                f.close()

                if eulacheck == 0:
                    eula()

                else:
                    send()
        else:
            if eulacheck == 1:
                startwindow()
            else:
                eula()

    except requests.exceptions.RequestException:

        custom_font = ("Arial", 15, 'bold')
        Label = customtkinter.CTkLabel(frame,
                                       text="Something went wrong...", font=custom_font,
                                       width=250, height=50)
        Label.place(x=125, y=15)

        Label1 = customtkinter.CTkLabel(frame,
                                        text="It seems like your pc isn't connected to \n the Internet. Please check and retry.",
                                        width=250, height=50)
        Label1.place(x=125, y=100)

        Button1 = customtkinter.CTkButton(frame, text="Retry", command=internet_on, width=100, height=20)
        Button1.place(x=200, y=190)

        Button1 = customtkinter.CTkButton(frame, text="Network settings", command=open_settings, width=100, height=20)
        Button1.place(x=192, y=230)


# start the program by checking for internet connection and initialise mainloop + login

internet_on()
# market()
# search_opt()
mainloop()
