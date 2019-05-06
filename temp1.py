from tkinter import *
root = Tk()
List_of_sites = Listbox(root, selectbackground='blue', selectforeground='yellow', text="List of sites", selectmode=SINGLE)

config = open('synonyms.yml', 'r')
for site in config:
    line = config.readline()
    line = re.search("https://.+", line).group(0)
    #print (line.group(0))
    List_of_sites.insert(END, line)

Site = List_of_sites.get(ACTIVE)

config.close()
List_of_sites.pack(side=LEFT, fill=BOTH, expand=1)

Select_button = Button(root, text="Select a site", command=lambda tagcounter(Site))
Select_button.pack()
root.mainloop()

