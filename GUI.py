import csv
import json
from tkinter import *
from geocoding_api import get_lat_lon
import tkinter
from tkintermapview import TkinterMapView
from tkinter import ttk
import os
from tkhtmlview import HTMLLabel


def ceil(a, b):
    """ performs a ceiling divide"""
    return -1 * (-a // b)


def send_data_request(og_lat, og_lon, lat, lon):
    """ sends the data request"""
    # send data request
    with open('input2.txt', 'w') as f:
        json.dump([og_lat, og_lon, lat, lon], f)


# the two status checks must be separate in case they are running at the same time.
def check_if_status_exists():
    """ checks if the file exists"""
    while True:
        try:
            with open("status.txt", 'r'):
                break
        except FileNotFoundError:
            continue
    if os.path.exists("status.txt"):
        os.remove("status.txt")


def check_if_status2_exists():
    """ checks if the file exists"""
    while True:
        try:
            with open("status2.txt", 'r'):
                break
        except FileNotFoundError:
            continue
    if os.path.exists("status2.txt"):
        os.remove("status2.txt")


def call_maps_api(og_lat, og_lon, lat, lon):
    """ calls maps api and returns information"""
    send_data_request(og_lat, og_lon, lat, lon)
    check_if_status2_exists()
    # load data
    with open('directions.txt', 'r') as f:
        data = json.load(f)
        # basic starting information:
        distance = data["routes"][0]['legs'][0]['distance']['text']
        duration = data["routes"][0]['legs'][0]['duration']['text']
        end_address = data["routes"][0]['legs'][0]['end_address']
        start_address = data["routes"][0]['legs'][0]['start_address']
        # directions information
        distances_list, durations_list, start_locations, end_locations, html_instructions = [], [], [], [], []
        # parse JSON
        for i in range(len(data["routes"][0]['legs'][0]["steps"])):
            distances_list.append(data["routes"][0]['legs'][0]["steps"][i]['distance']['text'])
            durations_list.append(data["routes"][0]['legs'][0]["steps"][i]['duration']['text'])
            start_locations.append((data["routes"][0]['legs'][0]["steps"][i]['start_location']['lat'], data["routes"][0]['legs'][0]["steps"][i]['start_location']['lng']))
            end_locations.append((data["routes"][0]['legs'][0]["steps"][i]['end_location']['lat'], data["routes"][0]['legs'][0]["steps"][i]['end_location']['lng']))
            html_instructions.append(data["routes"][0]['legs'][0]["steps"][i]['html_instructions'])
    # return data
    return distance, duration, end_address, start_address, distances_list, durations_list, start_locations, end_locations, html_instructions


def directions_html(distance, duration, end_address, start_address, distances_list, durations_list, html_instructions, tab3):
    """ creates the directions portion of the google maps """
    # Directions HTML
    frame2 = Frame(tab3)
    frame2.place(anchor=NW, x=800, width=400, height=750)
    html = ""
    html += f"""<h6>{start_address}</h6>"""
    html += f"""<p>Total: {distance}: ({duration})</p>"""
    for i in range(len(html_instructions)):
        html += f"""<h6>{html_instructions[i]}</h6>"""
        html += f"""<p>{distances_list[i]}: ({durations_list[i]})</p>"""
    html += f"""<h6>{end_address}</h6>"""
    my_label = HTMLLabel(frame2, html=html, height=750, width=400)
    my_label.pack(pady=20, padx=20)


def embed_google_maps(og_lat, og_lon, lat, lon, name, tab3, tabControl):
    """ embed google maps in tkinter"""
    # get data
    distance, duration, end_address, start_address, distances_list, durations_list, start_locations, end_locations, html_instructions = call_maps_api(og_lat, og_lon, lat, lon)
    # destroy old directions
    for widgets in tab3.winfo_children():
        widgets.destroy()
    # create map widget
    frame = Frame(tab3)
    frame.place(anchor=NW, width=800, height=750)
    map_widget = TkinterMapView(frame)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_position(og_lat, og_lon)
    map_widget.set_zoom(12)
    for i in range(len(start_locations)):
        if i == 0:
            map_widget.set_path([map_widget.set_marker(start_locations[i][0], start_locations[i][1], text=f"Starting Location").position, (end_locations[i][0], end_locations[i][1])])
        elif i < len(start_locations)-1:
            map_widget.set_path([(start_locations[i][0], start_locations[i][1]), (end_locations[i][0], end_locations[i][1])])
        else:
            map_widget.set_path([(start_locations[i][0], start_locations[i][1]), map_widget.set_marker(end_locations[i][0], end_locations[i][1], text=f"{name}").position])
    # google normal tile server
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    tabControl.select(tab3)
    # create html directions
    directions_html(distance, duration, end_address, start_address, distances_list, durations_list, html_instructions, tab3)


def get_directions(tab3, tabControl, lat, lon, name, zipcode):
    """ used to get latitude and longitude, and to call the embedded google maps widget"""
    og_lat, og_lon = get_lat_lon(zipcode, "US")
    embed_google_maps(float(og_lat), float(og_lon), lat, lon, name, tab3, tabControl)


def output_results(tab2, tab3, tabControl, zip_code):
    """ helper function for main"""
    title3 = ttk.Label(tab2, text="Here are Your Results! ")
    title3.config(font=("Courier", 16))
    title3.place(x=450, y=40, width=461, height=41)
    title4 = ttk.Label(tab2, text="Note: if you run the search again you\nwill lose your previous results. ")
    title4.config(font=("Courier", 12))
    title4.place(x=450, y=90, width=461, height=41)
    frame_2 = ttk.Frame(tab2)
    frame_2.place(anchor=NW, y=150, height=700, width=1200)
    filename = 'output.csv'
    with open(filename, 'r') as file:
        i = 0
        width = 10
        csv_reader = csv.reader(file)
        for row in csv_reader:  # Rows
            for j in range(width):  # Columns
                if j == 6 or j == 7 or j == 8:
                    continue
                if i == 0:
                    if j == 9:
                        b = Label(frame_2, text='Directions')
                        b.grid(row=i, column=j)
                    else:
                        b = Label(frame_2, text=f'{row[j]}')
                        b.grid(row=i, column=j)
                elif j != width - 1:
                    b = Entry(frame_2)
                    b.grid(row=i, column=j)
                    b.insert(0, row[j])
                else:
                    Button(frame_2, text="Get Directions",
                           command=lambda row=row, j=j: get_directions(tab3, tabControl, float(row[j - 3]), float(row[j - 2]), str(row[j - 9]), str(zip_code.get()))).grid(row=i, column=j)
            i += 1
    tabControl.select(tab2)


def main():
    """ This is the main portion of the widget where most of the stuff is set up"""
    # set up the widget
    root = tkinter.Tk()
    root.title("Place Finder")
    tabControl = ttk.Notebook(root)

    # set up tabs
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)

    tabControl.add(tab1, text='Search')
    tabControl.add(tab2, text='Search Results')
    tabControl.add(tab3, text='Directions')
    tabControl.pack(expand=1, fill="both")
    root.geometry("1200x800")  # this is how one would set up a standard widget size.

    # set up overall frame
    overall_frame = ttk.Frame(tab1)
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
    title.place(x=400, y=40, width=461, height=41)
    title2 = ttk.Label(overall_frame,
                       text="Ethan's Place finder is for those looking for good date ideas,\nfor those looking for something to do, and for anyone interested\n                       in trying new things!")
    title2.config(font=("Courier", 8))
    title2.place(x=400, y=80, width=461, height=61)
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

    def run():
        # query the checkboxes
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
        # dump data
        with open('input.txt', 'w') as f:
            json.dump([str(zip_code.get()), 'US', int(search_radius.get()), str(ceil(int(num_results.get()), len(kinds))), kinds], f)
        # open new window with results
        check_if_status_exists()
        # put out the results
        output_results(tab2, tab3, tabControl, zip_code)

    run_search = Button(tab1, text='Run Search', command=run)
    run_search.place(x=535, y=290, width=151, height=71)

    root.mainloop()


if __name__ == '__main__':
    main()
