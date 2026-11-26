
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
import hashlib

# Official RBA foreign exchange dataset
RBA_URL = (
    "https://www.rba.gov.au/statistics/"
    "tables/csv/f11.1-data.csv"
)

# Local output directory in the execution environment
OUTPUT_DIR = Path("downloads")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def download_rba_data():
    print("Starting RBA exchange rate download...")

    request = Request(
        RBA_URL,
        headers={"User-Agent": "RBA-FX-Data-Engineering/1.0"}
    )

    with urlopen(request, timeout=60) as response:
        content = response.read()

    if not content or len(content) < 100:
        raise ValueError("RBA download is empty or unexpectedly small")

    if content.lstrip().lower().startswith(b"<html"):
        raise ValueError("Received HTML instead of RBA data")

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"rba_f11_1_{timestamp}.csv"
    filepath = OUTPUT_DIR / filename

    filepath.write_bytes(content)

    checksum = hashlib.sha256(content).hexdigest()

    print(f"File downloaded: {filepath}")
    print(f"File size: {len(content)} bytes")
    print(f"SHA256: {checksum}")
    print("Download completed successfully!")


if __name__ == "__main__":
    download_rba_data()
