# Import Module
from tkinter import *
from tkhtmlview import HTMLLabel

# Create Object
root = Tk()

# Set Geometry
root.geometry("400x400")
list_of_stuff = ['Head <b>east</b> toward <b>E Southern Ave</b><div style="font-size:0.9em">Restricted usage road</div>', 'Turn <b>left</b> onto <b>E Southern Ave</b><div style="font-size:0.9em">Restricted usage road</div>', 'Turn <b>left</b> to stay on <b>E Southern Ave</b>', 'Turn <b>right</b> onto <b>S Rural Rd</b><div style="font-size:0.9em">Pass by Jimmy John\'s (on the left)</div>', 'Turn <b>right</b><div style="font-size:0.9em">Destination will be on the left</div>']
print(list_of_stuff[0])
# Add label
html = ""
for row in list_of_stuff:
    html += f"""<h6>{row}</h6>"""

print(html)
my_label = HTMLLabel(root, html=html)
# my_label = HTMLLabel(root, html=f"""
#         <h6>{list_of_stuff[0]}</h6>
#         <h6>Turn <b>left</b> onto <b>E Southern Ave</b><div style="font-size:0.9em">Restricted usage road</div>/h6>
#         <h6>Head <b>east</b> toward <b>E Southern Ave</b><div style="font-size:0.9em">Restricted usage road</div></h6>
#         <h6>Head <b>east</b> toward <b>E Southern Ave</b><div style="font-size:0.9em">Restricted usage road</div></h6>
#     """)

# Adjust label
my_label.pack(pady=20, padx=20)

# Execute Tkinter
root.mainloop()