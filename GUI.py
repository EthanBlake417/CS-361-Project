import csv
import multiprocessing
from tkinter import *
from tkinter import ttk
from place_finder_api import multiple_kinds
from geocoding_api import get_lat_lon
import tkinter
from tkintermapview import TkinterMapView


def ceil(a, b):
    return -1 * (-a // b)


def embed_google_maps(og_lat, og_lon, lat, lon, name, root):
    window3 = tkinter.Toplevel(root)
    window3.geometry(f"{1200}x{600}")
    window3.title("Directions.py")

    # create map widget
    map_widget = TkinterMapView(window3, width=600, height=400, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_position(og_lat, og_lon)
    map_widget.set_zoom(12)
    marker_2 = map_widget.set_marker(og_lat, og_lon, text="Home")
    marker_3 = map_widget.set_marker(lat, lon, text=name)
    path_1 = map_widget.set_path([marker_2.position, marker_3.position])

    # google normal tile server
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    window3.mainloop()


def get_directions(root):
    og_lat, og_lon = get_lat_lon("85282", "US")
    embed_google_maps(float(og_lat), float(og_lon), 33.421101, -111.925018, "D.P.Dough", root)


def main():
    # set up the widget
    root = tkinter.Tk()
    # print(root.themes)
    root.title("Activity Finder")
    # root.attributes('-fullscreen', True)
    root.geometry("900x750")                  # this is how one would set up a standard widget size.

    overall_frame = ttk.Frame(root)
    overall_frame.place(anchor=NW, height=775, width=858)

    # set up checkboxes
    label1 = ttk.Label(overall_frame, text="Choose what kind of\n  places you are\n  interested in: ")
    label1.config(font=("Courier", 10))
    label1.place(x=50, y=100, width=201, height=50)
    frame1 = ttk.Frame(overall_frame)
    frame1.place(x=50, y=170, width=201, height=180)
    restaurants = IntVar()
    c1 = Checkbutton(frame1, text="Restaurants", variable=restaurants)
    c1.select()
    c1.grid(row=0, sticky=W)
    accommodations = IntVar()
    c2 = Checkbutton(frame1, text="Accomodations", variable=accommodations)
    c2.select()
    c2.grid(row=1, sticky=W)
    interesting_places = IntVar()
    c3 = Checkbutton(frame1, text="Interesting Places", variable=interesting_places)
    c3.select()
    c3.grid(row=2, sticky=W)
    sports = IntVar()
    c4 = Checkbutton(frame1, text="Sports", variable=sports)
    c4.select()
    c4.grid(row=3, sticky=W)
    foods = IntVar()
    c5 = Checkbutton(frame1, text="Foods", variable=foods)
    c5.select()
    c5.grid(row=4, sticky=W)
    shops = IntVar()
    c6 = Checkbutton(frame1, text="Shops", variable=shops)
    c6.select()
    c6.grid(row=5, sticky=W)
    transport = IntVar()
    c7 = Checkbutton(frame1, text="Transport", variable=transport)
    c7.select()
    c7.grid(row=6, sticky=W)
    # This next section is the title
    title = ttk.Label(overall_frame, text="Welcome to Ethan's Place Finder! ")
    title.config(font=("Courier", 16))
    title.place(x=250, y=40, width=461, height=41)
    title2 = ttk.Label(overall_frame, text="Ethan's Place finder is for those looking for good date ideas,\nfor those looking for something to do, and for anyone interested\n                       in trying new things!")
    title2.config(font=("Courier", 8))
    title2.place(x=250, y=80, width=461, height=61)
    # Next frame which has zip code and Search Radius
    frame2 = ttk.Frame(overall_frame)
    frame2.place(x=50, y=370, width=201, height=200)

    label2 = ttk.Label(frame2, text="Zip Code: ")
    label2.config(font=("Courier", 10))
    label2.grid(row=0, column=0, sticky=W)

    zip_code = ttk.Entry(frame2, width=10)
    zip_code.grid(row=1, column=0, sticky=W)
    zip_code.insert(0, "85282")

    label3 = ttk.Label(frame2, text="Search Radius\n(in miles): ")
    label3.config(font=("Courier", 10))
    label3.grid(row=2, column=0, sticky=W)

    search_radius = ttk.Entry(frame2, width=10)
    search_radius.grid(row=3, column=0, sticky=W)
    search_radius.insert(0, "10")

    label4 = ttk.Label(frame2, text="Number of Results: ")
    label4.config(font=("Courier", 10))
    label4.grid(row=4, column=0, sticky=W)

    num_results = ttk.Spinbox(frame2, from_=1, to=25, width=10)
    num_results.grid(row=5, column=0, sticky=W)
    num_results.insert(0, "1")

    # label5 = ttk.Label(frame2, text="Maximum Cost: USD$: ")
    # label5.config(font=("Courier", 10))
    # label5.grid(row=6, column=0, sticky=W)
    #
    # max_cost = ttk.Entry(frame2, width=10)
    # max_cost.grid(row=7, column=0, sticky=W)
    # max_cost.insert(0, "25")

    def run():
        # if Restaurants checked
        kinds = []
        if restaurants.get() == 1:
            kinds.append('restaurants')
        if accommodations.get() == 1:
            kinds.append('accomodations')
        if interesting_places.get() == 1:
            kinds.append('interesting_places')
        if sports.get() == 1:
            kinds.append('sport')
        if foods.get() == 1:
            kinds.append('foods')
        if shops.get() == 1:
            kinds.append('shops')
        if transport.get() == 1:
            kinds.append('transport')
        #    run restaurant api. these things are to be decided in the future
        status = multiple_kinds(zip_code=zip_code.get(), country_code='US', mile_radius=int(search_radius.get()), num_results=ceil(int(num_results.get()), len(kinds)), kinds=kinds)
        if status == "Done":

            # open new window with results
            new_window = tkinter.Toplevel(root)
            new_window.title("Results")
            # root.attributes('-fullscreen', True)
            new_window.geometry("1200x700")
            title3 = ttk.Label(new_window, text="Here are Your Results! ")
            title3.config(font=("Courier", 16))
            title3.place(x=450, y=40, width=461, height=41)
            title4 = ttk.Label(new_window, text="Note: if you run the search again you\nwill lose your previous results. ")
            title4.config(font=("Courier", 12))
            title4.place(x=450, y=90, width=461, height=41)
            treeview_frame = ttk.Frame(new_window)
            treeview_frame.place(anchor=NW, y=150, height=700, width=1200)
            filename = 'output.csv'
            with open(filename, 'r') as file:
                i = 0
                width = 10
                csv_reader = csv.reader(file)
                for row in csv_reader:  # Rows
                    for j in range(width):  # Columns
                        if i == 0:
                            b = Label(treeview_frame, text=f'{row[j]}')
                            b.grid(row=i, column=j)
                        elif j != width-1:
                            b = Entry(treeview_frame)
                            b.grid(row=i, column=j)
                            b.insert(0, row[j])
                        else:
                            b = Button(treeview_frame, text="Get Directions", command=lambda: get_directions(root))
                            b.grid(row=i, column=j)
                    i += 1
            new_window.mainloop()

    run_search = Button(root, text='Run Search', command=run)
    run_search.place(x=390, y=290, width=151, height=71)

    root.mainloop()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
