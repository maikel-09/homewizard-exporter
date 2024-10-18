HomeWizard Energy Prometheus Exporter

This script fetches data from the HomeWizard Energy device and exposes it as Prometheus metrics. The configuration can be set via environment variables or command-line arguments.

Requirements

- Python 3.x
- homewizard-energy library
- prometheus_client library

Installation

Install the required libraries using pip:
```bash
python3 -m pip install -r requirements.txt
```

Usage

You can configure the script using environment variables or command-line arguments.

Environment Variables

- HW_EXPORTER_ENDPOINT: The endpoint of the HomeWizard Energy device.
- HW_EXPORTER_PORT: The port on which to run the Prometheus exporter.
- HW_EXPORTER_INTERVAL: The interval in seconds for fetching data (minimum 5 seconds).
- HW_EXPORTER_LOGLEVEL: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

Command-Line Arguments

- --endpoint: Set the HomeWizard Energy endpoint.
- --port: Set the HomeWizard Exporter port.
- --interval: Set the HomeWizard Exporter interval in seconds (minimum 5 seconds).
- --loglevel: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

Docker

```
docker run -d \
    -p 9002:9002 \
    --name homewizard_exporter \
    maikel09/homewizard-exporter
```

Example Command
```bash
python3 homewizard-exporter.py --endpoint ENDPOINT --port 9002 --interval 5 --loglevel DEBUG
```
Script Details

Environment Variables

- ENDPOINT: HomeWizard Energy device endpoint.
- PORT: Port for the Prometheus exporter.
- INTERVAL: Interval for fetching data.
- LOGLEVEL: Logging level.

Command-Line Arguments

The script accepts the following command-line arguments:

- --endpoint: The HomeWizard Energy endpoint.
- --port: The port for the Prometheus exporter.
- --interval: The interval for fetching data in seconds (default: 5).
- --loglevel: The logging level (default: INFO).

Prometheus Metrics

The script exposes the following Prometheus metrics with the prefix homewizard_:

- homewizard_wifi_ssid
- homewizard_wifi_strength
- homewizard_smr_version
- homewizard_meter_model
- homewizard_unique_meter_id
- homewizard_active_tariff
- homewizard_total_energy_import_kwh
- homewizard_total_energy_import_t1_kwh
- homewizard_total_energy_import_t2_kwh
- homewizard_total_energy_import_t3_kwh
- homewizard_total_energy_import_t4_kwh
- homewizard_total_energy_export_kwh
- homewizard_total_energy_export_t1_kwh
- homewizard_total_energy_export_t2_kwh
- homewizard_total_energy_export_t3_kwh
- homewizard_total_energy_export_t4_kwh
- homewizard_active_power_w
- homewizard_active_power_l1_w
- homewizard_active_power_l2_w
- homewizard_active_power_l3_w
- homewizard_active_voltage_v
- homewizard_active_voltage_l1_v
- homewizard_active_voltage_l2_v
- homewizard_active_voltage_l3_v
- homewizard_active_current_a
- homewizard_active_current_l1_a
- homewizard_active_current_l2_a
- homewizard_active_current_l3_a
- homewizard_voltage_sag_l1_count
- homewizard_voltage_swell_l1_count
- homewizard_any_power_fail_count
- homewizard_long_power_fail_count
- homewizard_total_gas_m3
- homewizard_gas_timestamp
- homewizard_gas_unique_id
- homewizard_active_liter_lpm
- homewizard_total_liter_m3