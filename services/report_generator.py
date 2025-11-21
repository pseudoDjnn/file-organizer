import csv
import logging

logger = logging.getLogger(__name__)


def generate_CSV_report(report_data, csv_filename="report.csv"):
    
    # Check is there is any data to report
    
    if not report_data:
        logger.info("No data to report")
        return
    
    # Extract header keys form the first report record.
    # This will serve as the header of our CSV
    
    keys = report_data[0].keys()
    
    # try/except opening a file to create the .csv
    
    try:
        with open(csv_filename, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            
            # Write the header row ot CSV.
        
            writer.writeheader()

            # Write all report records (all dicts) as CSV rows.
        
            writer.writerows(report_data)
        
        logger.info(f"CSV report generated: {csv_filename}")
        
    except Exception as e:
        logger.error(f"Error generating CSV reports: {e}")