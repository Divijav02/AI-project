import pandas as pd
import core.dashboard_plot as dashboard_plot

# =================================================================================
def get_violations_summary_of_last_n_days(df_last_n_days: pd.DataFrame) -> dict:
    # 1. calculate the no of violations in last n days
    total_no_of_violations = df_last_n_days.shape[0]

    # 2. Generate a figure of pie chart for violation types
    fig = dashboard_plot.plot_violation_type_percentage_pie(df_last_n_days)
    
    return {
        'total_no_of_violations': total_no_of_violations,
        'fig': fig
    }

# =================================================================================
def get_total_fines_generated(df_last_n_days: pd.DataFrame) -> dict:
    # 1. calculate total fines in last n days
    total_fines = df_last_n_days['Fine_Amount'].sum()
    avg_fine_per_violation = total_fines / df_last_n_days.shape[0] if df_last_n_days.shape[0] > 0 else 0
    # ==============================================================================
    # 2. Prepare data for fines based on violation type
    df_last_n_days['Fine_Amount'] = pd.to_numeric(df_last_n_days['Fine_Amount'], errors='coerce').fillna(0)
    df_last_n_days['Fine_Paid'] = df_last_n_days['Fine_Paid'].astype(str).str.upper().str.strip()
    summary = (df_last_n_days.groupby(['Violation_Type', 'Fine_Paid'])['Fine_Amount'].sum().unstack(fill_value=0))
    summary = summary.rename(columns={'YES': 'Paid', 'NO': 'Unpaid'})
    
    # 3. Generate a figure of fines based on violation type
    fig = dashboard_plot.plot_fines_based_on_violation_type(summary)
    
    return {
        'total_fines': total_fines,
        'avg_fine_per_violation': avg_fine_per_violation,
        'fig': fig
    }

# =================================================================================
def get_violations_by_location(df_last_n_days: pd.DataFrame) -> dict:
    # 1. No Of Violations for the location
    location_based_violations = df_last_n_days['Location'].value_counts().reset_index()
    location_based_violations.columns = ['Location', 'No of Violations']

    # 2. Total No Of Violations
    total_locations = location_based_violations.shape[0]
    
    # 3. Top Violations Zone
    most_violated_location = location_based_violations.iloc[0]['Location']

    # 4. Prepare data for plotting (Top 9 + Others)
    if total_locations > 10:
        top_9 = location_based_violations.iloc[:9]
        others_count = location_based_violations.iloc[9:]['No of Violations'].sum()
        others_df = pd.DataFrame({'Location': ['Others'], 'No of Violations': [others_count]})
        plot_data = pd.concat([top_9, others_df], ignore_index=True)
    else:
        plot_data = location_based_violations

    # 5. Plot pie chart for location based violations
    fig = dashboard_plot.plot_violations_by_location(plot_data)
    
    return {
        'total_locations': total_locations,
        'most_violated_location': most_violated_location,
        'fig': fig
    }

# =================================================================================
def get_license_insights(df_last_n_days: pd.DataFrame) -> dict:
    """
    Calculates insights related to License validity and type.
    """
    if df_last_n_days.empty:
        return {}
        
    # 1. Top License Type
    if 'License_Type' in df_last_n_days.columns:
        most_common_license_type = df_last_n_days['License_Type'].mode()[0]
    else:
        most_common_license_type = "N/A"
        
    # 2. Percentage of License Validity Expired
    expired_percentage = 0.0
    if 'License_Validity' in df_last_n_days.columns:
        total_licenses = len(df_last_n_days)
        expired_count = df_last_n_days[df_last_n_days['License_Validity'] == 'Expired'].shape[0]
        expired_percentage = (expired_count / total_licenses) * 100 if total_licenses > 0 else 0

    # 3. Generate License Validity Pie Chart
    validity_fig = dashboard_plot.plot_license_validity_by_gender(df_last_n_days)
    
    return {
        'most_common_license_type': most_common_license_type,
        'expired_percentage': round(expired_percentage, 2),
        'validity_fig': validity_fig
    }


# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================
# =======================================================================================================================
def get_global_overview_metrics(df: pd.DataFrame) -> dict:
    """
    Generates summary statistics for the Global Data Overview.
    """
    metrics = {}
    metrics['total_violations'] = len(df)
    
    if 'Violation_Type' in df.columns:
        metrics['most_common_violation'] = df['Violation_Type'].mode()[0] if not df['Violation_Type'].mode().empty else "N/A"
    else:
        metrics['most_common_violation'] = "N/A"
    
    if 'Fine_Amount' in df.columns:
        metrics['avg_fine'] = df['Fine_Amount'].mean()
        metrics['max_fine'] = df['Fine_Amount'].max()
        metrics['min_fine'] = df['Fine_Amount'].min()
    else:
        metrics['avg_fine'] = 0
        metrics['max_fine'] = 0
        metrics['min_fine'] = 0
    
    if 'Location' in df.columns:
        metrics['top_location'] = df['Location'].mode()[0] if not df['Location'].mode().empty else "N/A"
    else:
        metrics['top_location'] = "N/A"
            
    if 'Issuing_Agency' in df.columns:
        metrics['top_agency'] = df['Issuing_Agency'].mode()[0] if not df['Issuing_Agency'].mode().empty else "N/A"
    else:
        metrics['top_agency'] = "N/A"

    if 'Payment_Method' in df.columns:
        metrics['common_payment'] = df['Payment_Method'].mode()[0] if not df['Payment_Method'].mode().empty else "N/A"
    else:
        metrics['common_payment'] = "N/A"
             
    return metrics


# =======================================================================================================================
def get_behavioral_analysis(df: pd.DataFrame) -> dict:
    """
    Computes flags and returns aggregate counts/percentages for:
    - Over Speeding
    - High Fine (>90th percentile)
    - Repeat Offenders (>2 violations)
    - Bad Weather Risk
    """
    total_records = len(df)
    analysis_results = {
        'total_count': total_records,
        'over_speeding_stats': (0, 0.0),
        'court_appearance_stats': (0, 0.0),
        'repeat_offender_stats': (0, 0.0),
        'bad_weather_stats': (0, 0.0),
        'most_frequent_weather_stats': ("N/A", 0, 0.0)
    }

    if total_records == 0:
        return analysis_results

    # Helper to calculate count and percentage
    def calculate_stats(boolean_mask):
        count = boolean_mask.sum()
        percentage = (count / total_records) * 100
        return (count, percentage)

    # 1. Over Speeding
    analysis_results['over_speeding_stats'] = calculate_stats(df['Recorded_Speed'] > df['Speed_Limit'])

    # 2. Court Appearance Required
    if 'Court_Appearance_Required' in df.columns:
        analysis_results['court_appearance_stats'] = calculate_stats(df['Court_Appearance_Required'] == 'Yes')

    # 3. Repeat Offenders (Based on Comments == 'Repeat Offender')
    if 'Comments' in df.columns:
        repeat_offender_counts = df[df['Comments'] == 'Repeat Offender'].value_counts().sum()
        if len(df) > 0:
            repeat_offender_pct = (repeat_offender_counts / len(df)) * 100

        analysis_results['repeat_offender_stats'] = (repeat_offender_counts, repeat_offender_pct)

    if 'Weather_Condition' in df.columns:
        adverse_weather_conditions = {'fog', 'rain', 'snow', 'thunderstorm', 'hail', 'mist'}
        # Case-insensitive check
        is_adverse_weather = df['Weather_Condition'].astype(str).str.lower().isin(adverse_weather_conditions)
        analysis_results['bad_weather_stats'] = calculate_stats(is_adverse_weather)
        
        # Top Weather
        if not df['Weather_Condition'].empty:
            weather_mode_result = df['Weather_Condition'].mode()
            if not weather_mode_result.empty:
                tps_weather_name = weather_mode_result[0]
                tps_weather_count = (df['Weather_Condition'] == tps_weather_name).sum()
                analysis_results['most_frequent_weather_stats'] = (tps_weather_name, tps_weather_count, (tps_weather_count / total_records) * 100)
    return analysis_results


# =======================================================================================================================