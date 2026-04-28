import os
from google.cloud import storage, bigquery
from google.oauth2 import service_account

# ==============================
# CONFIG
# ==============================

PROJECT_ID = "cdmxmobility"
BUCKET_NAME = "cdmx_mobility_insight2024"
DATASET_ID = "cyclistic2024"
TABLE_ID = "cleaned_trips_2024"

KEY_PATH = r"C:\Users\LENOVO\OneDrive - Conocimiento en Tecnología de Información, SC\Desktop\cyclistic_pipeline\cdmxmobility-663c243fa692.json"

WRITE_MODE = "WRITE_TRUNCATE"  # or WRITE_APPEND

# ==============================
# AUTHENTICATION
# ==============================

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

storage_client = storage.Client(project=PROJECT_ID, credentials=credentials)
bq_client = bigquery.Client(project=PROJECT_ID, credentials=credentials)

# ==============================
# GET ALL CSV FILES
# ==============================

def get_all_csv_files(folder_path="."):
    return [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# ==============================
# UPLOAD FUNCTION
# ==============================

def upload_to_gcs(source_file, destination_blob):
    try:
        print(f"Uploading {source_file} to Cloud Storage...")
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(destination_blob)

        blob.upload_from_filename(source_file)

        print("✅ File uploaded to Cloud Storage")
        return True

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

# ==============================
# LOAD FUNCTION
# ==============================

def load_to_bigquery(destination_blob):
    try:
        print("Loading data into BigQuery...")

        uri = f"gs://{BUCKET_NAME}/{destination_blob}"
        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=WRITE_MODE
        )

        load_job = bq_client.load_table_from_uri(uri, table_ref, job_config=job_config)
        load_job.result()

        print("✅ Data loaded into BigQuery successfully")
        return True

    except Exception as e:
        print(f"❌ BigQuery load failed: {e}")
        return False

# ==============================
# MAIN PIPELINE
# ==============================

def run_pipeline():
    print("🚀 Pipeline started")

    files = get_all_csv_files()

    if not files:
        print("❌ No CSV files found")
        return

    for file in files:
        print(f"\nProcessing file: {file}")

        destination_blob = f"data/{file}"

        if not upload_to_gcs(file, destination_blob):
            continue

        if not load_to_bigquery(destination_blob):
            continue

    print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY")

# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    run_pipeline()