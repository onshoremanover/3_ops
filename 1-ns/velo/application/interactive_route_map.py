import streamlit as st
from streamlit_folium import st_folium
import folium
import networkx as nx
import pandas as pd
from shapely.geometry import LineString

# Inject Umami tracking script
umami_script = """
<script defer src="https://umami.publio.online/script.js" data-website-id="acfdace2-c355-4c3d-9d15-102959a15e44"></script>
"""

# Use `st.markdown()` to insert the script
st.markdown(umami_script, unsafe_allow_html=True)

# Load data and create the graph
@st.cache_resource
def load_data_and_graph():
    df = pd.DataFrame({
        'geometry': [LineString([(0, 0), (1, 1), (2, 2)]), LineString([(2, 2), (3, 3)])],
        'weight': [1, 2]
    })
    
    # Create graph
    graph = nx.Graph()
    for _, row in df.iterrows():
        coords = list(row['geometry'].coords)
        for i in range(len(coords) - 1):
            graph.add_edge(coords[i], coords[i + 1], weight=row['weight'])
    return graph, df

# Create a Streamlit app
st.title("Interactive Route Map")

st.write("Click on the map to select two points. The shortest route will be calculated based on the data.")

# Load graph and data
graph, df = load_data_and_graph()

# Create the Folium map
m = folium.Map(location=[46.8, 8.3], zoom_start=8)

# Add map to Streamlit
map_data = st_folium(m, width=700, height=500)

# Check if user clicked on the map
if map_data and 'last_clicked' in map_data:
    st.session_state.points = st.session_state.get('points', [])

    # Get the clicked coordinates
    clicked_coords = map_data['last_clicked']
    st.session_state.points.append((clicked_coords['lng'], clicked_coords['lat']))

    # Limit to 2 points
    if len(st.session_state.points) > 2:
        st.session_state.points = st.session_state.points[-2:]

# Show selected points
if 'points' in st.session_state and len(st.session_state.points) == 2:
    st.write("Selected points:", st.session_state.points)

    # Calculate shortest path
    shortest_path = nx.shortest_path(graph, source=st.session_state.points[0], target=st.session_state.points[1], weight="weight")

    # Add path to the map
    for coord1, coord2 in zip(shortest_path[:-1], shortest_path[1:]):
        folium.PolyLine([coord1, coord2], color="blue", weight=5).add_to(m)

    # Update the map with the path
    st_folium(m, width=700, height=500)

