import asyncio
from homewizard_energy import HomeWizardEnergy
import logging
from prometheus_client import start_http_server, Gauge, Info, Counter
from datetime import datetime
import os
import argparse

# Try to get the environment variables
ENDPOINT = os.getenv("HW_EXPORTER_ENDPOINT")
PORT     = os.getenv("HW_EXPORTER_PORT")
INTERVAL = os.getenv("HW_EXPORTER_INTERVAL")
LOGLEVEL = os.getenv("HW_EXPORTER_LOGLEVEL")

# Define command line arguments
parser = argparse.ArgumentParser(description="HomeWizard Energy Prometheus Exporter")
parser.add_argument('--endpoint', help="Set the HomeWizard Energy endpoint")
parser.add_argument('--port', help="Set the HomeWizard Exporter port",type=int)
parser.add_argument('--interval', help="Set the HomeWizard Exporter interval in seconds (min 5 seconds)",type=int,default=5)
parser.add_argument('--loglevel', help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)", default="INFO")
args = parser.parse_args()

# Check if set in environment variables or via argparse
ENDPOINT = ENDPOINT if ENDPOINT else args.endpoint
PORT     = PORT     if PORT     else args.port
INTERVAL = INTERVAL if INTERVAL else args.interval
LOGLEVEL = LOGLEVEL if LOGLEVEL else args.loglevel

if not ENDPOINT:
    parser.error("The ENDPOINT must be set via environment variable HW_EXPORTER_ENDPOINT or --endpoint argument")
if not PORT:
    parser.error("The PORT must be set via environment variable HW_EXPORTER_PORT or --port argument")
if not INTERVAL:
    parser.error("The INTERVAL must be set via environment variable HW_EXPORTER_INTERVAL or --interval argument")
if int(INTERVAL) < 5:
    parser.error("The INTERVAL must be equal to or greater than 5 seconds")
if not LOGLEVEL:
    parser.error("The LOGLEVEL must be set via environment variable HW_EXPORTER_LOGLEVEL or --loglevel argument")

numeric_level = getattr(logging, LOGLEVEL.upper(), None)
if not isinstance(numeric_level, int):
    parser.error(f"Invalid log level: {LOGLEVEL}")




# Initialize the Prometheus metrics with 'homewizard_' prefix
metrics = {
    'wifi_ssid': Info('homewizard_wifi_ssid', 'WiFi SSID'),
    'wifi_strength': Gauge('homewizard_wifi_strength', 'WiFi Strength'),
    'smr_version': Gauge('homewizard_smr_version', 'SMR Version'),
    'meter_model': Info('homewizard_meter_model', 'Meter Model'),
    'unique_meter_id': Info('homewizard_unique_meter_id', 'Unique Meter ID'),
    'active_tariff': Gauge('homewizard_active_tariff', 'Active Tariff'),
    'total_energy_import_kwh': Gauge('homewizard_total_energy_import_kwh', 'Total Energy Import in kWh'),
    'total_energy_import_t1_kwh': Gauge('homewizard_total_energy_import_t1_kwh', 'Total Energy Import T1 in kWh'),
    'total_energy_import_t2_kwh': Gauge('homewizard_total_energy_import_t2_kwh', 'Total Energy Import T2 in kWh'),
    'total_energy_import_t3_kwh': Gauge('homewizard_total_energy_import_t3_kwh', 'Total Energy Import T3 in kWh'),
    'total_energy_import_t4_kwh': Gauge('homewizard_total_energy_import_t4_kwh', 'Total Energy Import T4 in kWh'),
    'total_energy_export_kwh': Gauge('homewizard_total_energy_export_kwh', 'Total Energy Export in kWh'),
    'total_energy_export_t1_kwh': Gauge('homewizard_total_energy_export_t1_kwh', 'Total Energy Export T1 in kWh'),
    'total_energy_export_t2_kwh': Gauge('homewizard_total_energy_export_t2_kwh', 'Total Energy Export T2 in kWh'),
    'total_energy_export_t3_kwh': Gauge('homewizard_total_energy_export_t3_kwh', 'Total Energy Export T3 in kWh'),
    'total_energy_export_t4_kwh': Gauge('homewizard_total_energy_export_t4_kwh', 'Total Energy Export T4 in kWh'),
    'active_power_w': Gauge('homewizard_active_power_w', 'Active Power in W'),
    'active_power_l1_w': Gauge('homewizard_active_power_l1_w', 'Active Power L1 in W'),
    'active_power_l2_w': Gauge('homewizard_active_power_l2_w', 'Active Power L2 in W'),
    'active_power_l3_w': Gauge('homewizard_active_power_l3_w', 'Active Power L3 in W'),
    'active_voltage_v': Gauge('homewizard_active_voltage_v', 'Active Voltage in V'),
    'active_voltage_l1_v': Gauge('homewizard_active_voltage_l1_v', 'Active Voltage L1 in V'),
    'active_voltage_l2_v': Gauge('homewizard_active_voltage_l2_v', 'Active Voltage L2 in V'),
    'active_voltage_l3_v': Gauge('homewizard_active_voltage_l3_v', 'Active Voltage L3 in V'),
    'active_current_a': Gauge('homewizard_active_current_a', 'Active Current in A'),
    'active_current_l1_a': Gauge('homewizard_active_current_l1_a', 'Active Current L1 in A'),
    'active_current_l2_a': Gauge('homewizard_active_current_l2_a', 'Active Current L2 in A'),
    'active_current_l3_a': Gauge('homewizard_active_current_l3_a', 'Active Current L3 in A'),
    'voltage_sag_l1_count': Gauge('homewizard_voltage_sag_l1_count', 'Voltage Sag L1 Count'),
    'voltage_swell_l1_count': Gauge('homewizard_voltage_swell_l1_count', 'Voltage Swell L1 Count'),
    'any_power_fail_count': Gauge('homewizard_any_power_fail_count', 'Any Power Fail Count'),
    'long_power_fail_count': Gauge('homewizard_long_power_fail_count', 'Long Power Fail Count'),
    'total_gas_m3': Gauge('homewizard_total_gas_m3', 'Total Gas in m3'),
    'gas_timestamp': Info('homewizard_gas_timestamp', 'Gas Timestamp'),
    'gas_unique_id': Info('homewizard_gas_unique_id', 'Gas Unique ID'),
    'active_liter_lpm': Gauge('homewizard_active_liter_lpm', 'Active Liter LPM'),
    'total_liter_m3': Gauge('homewizard_total_liter_m3', 'Total Liter in m3')
}

async def fetch_data():
    async with HomeWizardEnergy(host=ENDPOINT) as api:
        data = await api.data()
        return data.__dict__

async def main():
    start_http_server(int(PORT))
    logging.info(f"Started Prometheus exporter on port {PORT}")
        
    while True:
        logging.debug("updating data")
        try:
            data = await fetch_data()
            if data:
                for key, value in data.items():
                    if value is not None:
                        if isinstance(value, (int, float)):
                            metrics[key].set(value)
                        elif isinstance(value, str):
                            metrics[key].info({'value': value})
                        elif isinstance(value, datetime):
                            metrics[key].info({'value': value.isoformat()})
            await asyncio.sleep(int(INTERVAL))
        except Exception as e:
            logging.error(f"Error fetching data: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=numeric_level, format='level=%(levelname)s msg="%(message)s"')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Prometheus exporter stopped by user")
        os.sys.exit()