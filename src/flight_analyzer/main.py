import argparse
import logging

import pandas as pd

from flight_analyzer.loader import load_data
from flight_analyzer.validator import validate_dataframe
from flight_analyzer.charts import create_charts
from flight_analyzer.flight_path import create_flight_path


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Flight telemetry analyzer"
    )

    parser.add_argument(
        "file",
        help="Telemetry JSON filename located in the data folder",
    )

    return parser.parse_args()


def main() -> int:
    """
    Run analysis, returning 1 for input errors and 0 for success.
    """

    args = parse_arguments()

    try:
        logging.info("Loading telemetry data...")

        data = load_data(args.file)

        logging.info(
            "Loaded %s telemetry records",
            len(data),
        )

        df = pd.DataFrame(data)

        logging.info("Validating telemetry format...")
        validate_dataframe(df)

    except (OSError, ValueError) as error:
        logging.error("%s", error)
        return 1

    logging.info("Generating 3D flight path...")
    create_flight_path(df)

    logging.info("Generating telemetry charts...")
    create_charts(df)

    logging.info("Analysis complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
