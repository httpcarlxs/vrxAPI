import os, re, time
from datetime import datetime
from openpyxl.styles import Alignment, Font

def load_configuration():
    api_key = os.getenv('API_KEY_ESPM')
    api_url = os.getenv('API_URL_ESPM')
    description_file_url = os.getenv('DESCRIPTION_FILE_URL')
    description_file_path = os.getenv('DESCRIPTION_FILE_PATH')
    return api_key, api_url, description_file_url, description_file_path


def control_rate(query_limit=50):
    global last_query_time

    elapsed_time = time.time() - last_query_time
    if elapsed_time < (60 / query_limit):
        time.sleep((60 / query_limit) - elapsed_time)

    last_query_time = time.time()
    

def convert_timestamp_to_datetime(timestamp):
    try:
        # Check if the timestamp is likely in milliseconds (large numbers)
        if timestamp > 1e10:  # Adjust threshold as necessary
            timestamp /= 1000.0  # Convert from milliseconds to seconds

        return datetime.fromtimestamp(timestamp)
    except (TypeError, ValueError, OverflowError):
        return timestamp
    

def write_sheet(writer, sheet_name, df, column_widths):
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    worksheet = writer.sheets[sheet_name]
    
    for col_num, col_name in enumerate(df.columns, start=1):
        col_letter = chr(64 + col_num)
        sheet_type = re.match(r"^[^_]+", sheet_name).group()
        width = column_widths[sheet_type].get(col_name, 15)
        worksheet.column_dimensions[col_letter].width = width
        
        title_cell = worksheet[f"{col_letter}1"]
        title_cell.alignment = Alignment(horizontal="center", vertical="center", wrapText=True)
        title_cell.font = Font(bold=True)
        
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=col_num, max_col=col_num):
            for cell in row:
                cell.alignment = Alignment(wrapText=True)
    
    
def split_and_write(writer, base_name, df, prefixes, column_widths):
    df["Prefixo"] = df["Hostname"].str.upper().str[:2]

    for prefix in prefixes:
        df_filtered = df[df["Prefixo"] == prefix]
        if not df_filtered.empty:
            write_sheet(writer, f"{base_name}_{prefix}", df_filtered.drop(columns=["Prefixo"]), column_widths)

    
    df_outros = df[~df["Prefixo"].isin(prefixes)]
    if not df_outros.empty:
        write_sheet(writer, f"{base_name}_Outros", df_outros.drop(columns=["Prefixo"]), column_widths)

last_query_time = 0