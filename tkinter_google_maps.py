import tkinter
from tkintermapview import TkinterMapView


def embed_google_maps(og_lat, og_lon, lat, lon, name):
    window3 = tkinter.Tk()
    window3.geometry(f"{1200}x{600}")
    window3.title("map_view_simple_example.py")

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


if __name__ == '__main__':
    from geocoding_api import get_lat_lon
    og_lat, og_lon = get_lat_lon("85282", "US")
    embed_google_maps(float(og_lat), float(og_lon), 33.421101, -111.925018, "D.P.Dough")