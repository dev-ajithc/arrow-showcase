"""
Integration examples with other libraries.

Demonstrates Arrow usage with pandas, JSON, databases, APIs.
"""

import json
import time

import arrow


def demo_pandas_integration() -> None:
    """Use Arrow with pandas DataFrames."""
    print("\n=== Pandas Integration Demo ===")

    try:
        import pandas as pd

        dates = [
            arrow.get('2024-02-01'),
            arrow.get('2024-02-02'),
            arrow.get('2024-02-03'),
        ]

        data = {
            'date': [d.datetime for d in dates],
            'value': [100, 150, 200],
        }

        df = pd.DataFrame(data)
        print("DataFrame with Arrow dates:")
        print(df)

        print("\nDate operations:")
        print(f"Min date: {arrow.get(df['date'].min())}")
        print(f"Max date: {arrow.get(df['date'].max())}")

    except ImportError:
        print("pandas not installed - skipping pandas examples")


def demo_json_serialization() -> None:
    """Serialize/deserialize dates in JSON."""
    print("\n=== JSON Serialization Demo ===")

    dt = arrow.utcnow()

    data = {
        'event': 'User Login',
        'timestamp': dt.timestamp(),
        'iso_date': dt.isoformat(),
        'formatted': dt.format('YYYY-MM-DD HH:mm:ss'),
    }

    json_str = json.dumps(data, indent=2)
    print("Serialized JSON:")
    print(json_str)

    loaded_data = json.loads(json_str)

    print("\nDeserialized dates:")
    dt_from_ts = arrow.get(loaded_data['timestamp'])
    print(f"From timestamp: {dt_from_ts}")

    dt_from_iso = arrow.get(loaded_data['iso_date'])
    print(f"From ISO: {dt_from_iso}")


def demo_database_timestamps() -> None:
    """Handle database timestamp fields."""
    print("\n=== Database Timestamps Demo ===")

    print("Common database timestamp scenarios:\n")

    created_at = arrow.utcnow()
    updated_at = arrow.utcnow()

    print("Storing in database:")
    print(f"  created_at: {created_at.isoformat()}")
    print(f"  updated_at: {updated_at.isoformat()}")

    print("\nRetrieving from database:")
    db_timestamp = "2024-02-07T14:30:45.123456+00:00"
    retrieved = arrow.get(db_timestamp)
    print(f"  Raw: {db_timestamp}")
    print(f"  Parsed: {retrieved}")
    print(f"  Local: {retrieved.to('local')}")

    print("\nAge calculation:")
    age = arrow.utcnow() - retrieved
    print(f"  Record age: {age.total_seconds():.0f} seconds")


def demo_api_date_parsing() -> None:
    """Parse dates from API responses."""
    print("\n=== API Date Parsing Demo ===")

    api_responses = [
        {
            'format': 'ISO 8601',
            'date': '2024-02-07T14:30:45Z',
        },
        {
            'format': 'Unix timestamp',
            'date': 1707318645,
        },
        {
            'format': 'Custom format',
            'date': '2024-02-07 14:30:45',
        },
    ]

    print("Parsing various API date formats:")
    for response in api_responses:
        print(f"\n{response['format']}:")
        print(f"  Raw: {response['date']}")

        if isinstance(response['date'], int):
            dt = arrow.get(response['date'])
        elif 'T' in str(response['date']):
            dt = arrow.get(response['date'])
        else:
            dt = arrow.get(response['date'], 'YYYY-MM-DD HH:mm:ss')

        print(f"  Parsed: {dt}")
        print(f"  Formatted: {dt.format('MMMM DD, YYYY at HH:mm')}")


def demo_config_date_handling() -> None:
    """Handle dates in configuration files."""
    print("\n=== Config Date Handling Demo ===")

    config = {
        'backup_time': '02:00',
        'retention_days': 7,
        'timezone': 'UTC',
        'start_date': '2024-01-01',
    }

    print("Configuration:")
    print(json.dumps(config, indent=2))

    print("\nProcessed configuration:")

    backup_time = arrow.now(config['timezone']).replace(
        hour=int(config['backup_time'].split(':')[0]),
        minute=int(config['backup_time'].split(':')[1]),
        second=0
    )
    print(f"Backup time: {backup_time.format('YYYY-MM-DD HH:mm:ss ZZ')}")

    start_date = arrow.get(config['start_date'])
    print(f"Start date: {start_date.format('YYYY-MM-DD')}")

    cutoff_date = arrow.now().shift(days=-config['retention_days'])
    print(f"Cutoff date: {cutoff_date.format('YYYY-MM-DD')}")


def demo_csv_date_handling() -> None:
    """Handle dates in CSV data."""
    print("\n=== CSV Date Handling Demo ===")

    csv_data = [
        {'date': '2024-02-01', 'value': 100},
        {'date': '2024-02-02', 'value': 150},
        {'date': '2024-02-03', 'value': 200},
    ]

    print("CSV data with dates:")
    for row in csv_data:
        date_obj = arrow.get(row['date'])
        row['parsed_date'] = date_obj
        row['weekday'] = date_obj.format('dddd')
        print(f"  {row['date']} ({row['weekday']}): {row['value']}")


def demo_logging_timestamps() -> None:
    """Generate timestamps for logging."""
    print("\n=== Logging Timestamps Demo ===")

    log_entries = [
        {'level': 'INFO', 'message': 'Application started'},
        {'level': 'DEBUG', 'message': 'Processing request'},
        {'level': 'WARNING', 'message': 'High memory usage'},
        {'level': 'ERROR', 'message': 'Connection failed'},
    ]

    print("Log entries with timestamps:")
    for entry in log_entries:
        timestamp = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')
        print(f"{timestamp} - {entry['level']:7} - {entry['message']}")
        time.sleep(0.1)


def main() -> None:
    """Run all integration examples."""
    print("=" * 60)
    print("Arrow Integration Examples")
    print("=" * 60)

    demo_pandas_integration()
    time.sleep(0.5)

    demo_json_serialization()
    time.sleep(0.5)

    demo_database_timestamps()
    time.sleep(0.5)

    demo_api_date_parsing()
    time.sleep(0.5)

    demo_config_date_handling()
    time.sleep(0.5)

    demo_csv_date_handling()
    time.sleep(0.5)

    demo_logging_timestamps()

    print("\n" + "=" * 60)
    print("All integration examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
