import streamlit as st
import pandas as pd
import os
from streamlit_local_storage import LocalStorage

def render_sidebar() -> pd.DataFrame:
    """
    Renders the sidebar components including the dataset selector.
    Returns the selected and loaded pandas DataFrame.
    """
    st.sidebar.header("Dataset Selector")
    
    # Get the list of available datasets
    dataset_folder = "dataset"
    uploaded_dataset_folder = "uploaded_datasets"
    related_uploads_folder = "uploded_file_relateds"
    generated_dataset_folder = "generated_fake_traffic_datasets"
    other_party_uploads_folder = "uploded_file_others"
    
    dataset_options = {}

    # Add datasets from the 'dataset' folder
    if os.path.exists(dataset_folder):
        for filename in os.listdir(dataset_folder):
            if filename.endswith(".csv"):
                dataset_options[f"{filename} [Sample]"] = os.path.join(dataset_folder, filename)

    # Function to scan a directory and add to options
    def scan_and_add_datasets(directory, prefix):
        if os.path.exists(directory):
            # Scan for date-based directories (for generated data)
            if "generated" in directory:
                for date_dir in sorted(os.listdir(directory), reverse=True):
                    full_date_dir = os.path.join(directory, date_dir)
                    if os.path.isdir(full_date_dir):
                        for file_name in sorted(os.listdir(full_date_dir)):
                            if file_name.endswith('.csv'):
                                display_name = f"{file_name} [{prefix} - {date_dir}]"
                                dataset_options[display_name] = os.path.join(full_date_dir, file_name)
            else: # Original logic for other directories
                for file_name in sorted(os.listdir(directory)):
                    if file_name.endswith('.csv'):
                        dataset_options[f"{file_name} [{prefix}]"] = os.path.join(directory, file_name)

    # Scan new directories in the desired order
    scan_and_add_datasets(generated_dataset_folder, "Fake Generated")
    scan_and_add_datasets(related_uploads_folder, "Legacy")
    scan_and_add_datasets(other_party_uploads_folder, "Other CSVs")

    # Add datasets from the 'uploaded_datasets' folder (legacy)
    if os.path.exists(uploaded_dataset_folder):
        for root, dirs, files in os.walk(uploaded_dataset_folder):
            for filename in files:
                if filename.endswith(".csv"):
                    # Get the parent directory name for context
                    parent_dir = os.path.basename(root)
                    dataset_options[f"[Legacy] {parent_dir}/{filename}"] = os.path.join(root, filename)

    # ==========================================================================================================    
    # Persistence with Local Storage
    # ==========================================================================================================    

    localS = LocalStorage()
    
    # distinct key for local storage item
    ls_key = "selected_dataset_name" 
    
    # Get stored value (might be None/null if not set)
    stored_value = localS.getItem(ls_key)
    
    options_list = list(dataset_options.keys())
    default_index = 0
    
    # Try to match stored value to current options
    if stored_value and stored_value in options_list:
        default_index = options_list.index(stored_value)

    # 1. Create Selectbox
    selected_dataset_display_name = st.sidebar.selectbox(
        "Choose a dataset", 
        options_list,
        index=default_index,
        width="stretch"
    )

    # 2. Update Local Storage if changed
    if selected_dataset_display_name and selected_dataset_display_name != stored_value:
        localS.setItem(ls_key, selected_dataset_display_name)

    if not selected_dataset_display_name:
        st.sidebar.warning("Please select a dataset.")
        return None

    # 3. Get Selected Dataset Path  
    selected_dataset_path = dataset_options[selected_dataset_display_name]

    # 4. Load the selected dataset
    @st.cache_data
    def load_data(path):
        df = pd.read_csv(path)
        return df.copy() # Return a copy to prevent mutation of cached data
    df = load_data(selected_dataset_path)
    
    # 4. Display Success Message
    st.sidebar.success(f"Loaded dataset: **{selected_dataset_display_name}**")
    st.session_state.df = df.copy() 

    
    # 5. Return the loaded dataset
    return df.copy()
