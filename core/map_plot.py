import streamlit as st
import json
import folium

@st.cache_data
def load_geojson(file_path="map_data/01_INDIA_STATES.geojson"):
    """
    Loads GeoJSON data from a file and returns the data along with the property name for state names.
    Returns:
        tuple: (geojson_data, state_prop_name)
    """
    try:
        with open(file_path, "r") as f:
            geojson_data = json.load(f)
        # In a more advanced version, we could auto-detect this, but for now we return the known key.
        
        state_prop_name = "STNAME_SH"
        return geojson_data, state_prop_name

    except Exception as e:
        print(f"Error loading GeoJSON file: {e}")
        return None, None

def plot_choropleth_map(map_data, geojson_data, location_col, value_col, state_prop_name="STNAME_SH", color_theme="YlGnBu"):
    """
    Generates a Folium Choropleth map.
    """
    
    # Normalize location names for matching FIRST
    map_data[location_col] = map_data[location_col].astype(str).str.lower()
    
    # Create simple lookup dictionary for values
    val_dict = map_data.set_index(location_col)[value_col].to_dict()

    # Inject value into GeoJSON properties for Tooltip
    for feature in geojson_data['features']:
        # Create a lower-case property for matching if it doesn't exist
        st_name_lower = feature['properties'][state_prop_name].lower()
        feature['properties']['st_nm_lower'] = st_name_lower
        
        # safely get value or 0/N/A
        val = val_dict.get(st_name_lower, 0)
        feature['properties'][value_col] = val
    
    m = folium.Map(location=[22, 82], zoom_start=4, tiles="CartoDB positron")

    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        data=map_data,
        columns=[location_col, value_col],
        key_on="feature.properties.st_nm_lower",
        fill_color=color_theme,
        fill_opacity=0.7,
        line_opacity=0.5,
        nan_fill_color="gray", # Explicitly set no data color to gray
        nan_fill_opacity=0.4,
        legend_name=f"{value_col}",
    ).add_to(m)

    folium.features.GeoJsonTooltip(
        fields=[state_prop_name, value_col],
        aliases=['State:', f'{value_col}:'],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0F0F0;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px 3px 3px 0px rgba(0,0,0,0.2);
        """,
        max_width=800,
    ).add_to(choropleth.geojson)

    return m
