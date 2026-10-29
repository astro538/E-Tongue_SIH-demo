# E-Tongue for Dravya Detection — SIH Demo

A Streamlit prototype that explores herb identification and adulteration screening from four normalized sensor readings. It includes a shared reference table, per-user entries, and a simple admin/user workflow for submitting or removing herb records.

> **Important:** the repository currently contains a demonstration application and small reference CSVs. The similarity score is a hand-written distance calculation, not a validated chemical fingerprinting method. Do not use the output as proof of herb identity, purity, safety, or adulteration.

## How it works

The app accepts four values in the range 0–1:

- Voltammetric sensor
- Conductivity sensor
- Photochemical sensor
- pH sensor

For matching, the app calculates Euclidean distance between the input vector and each herb row, then converts that distance into a percentage-like similarity score. A score of 85% or above is displayed as a match. This threshold and score are heuristic choices in the current code; they need calibration against real, labelled sensor measurements before scientific interpretation.

The “Check Adulteration” screen compares an entered herb name with the corresponding reference row. It does not run laboratory tests or independently identify adulterants.

## Features

- Streamlit interface for a universal reference dataset and a user-specific dataset.
- Herb matching based on four input sensor readings.
- Demo adulteration check against the selected herb reference.
- Submit a new personal herb entry or queue a universal entry for admin review.
- Admin and user views for adding/removing entries.

## Project files

| File | Purpose |
| --- | --- |
| `herb.py` | Streamlit application, matching logic, and user/admin workflow |
| `universal_dataset.csv` | Shared herb reference rows |
| `user1_personal.csv` | Example user-specific CSV file |
| `README.md` | Project documentation |

The app may create `pending_requests.json` at runtime to store pending universal-dataset submissions. CSV and JSON files are read and written in the current working directory.

## Run locally

Requirements: Python 3.9+.

```bash
git clone https://github.com/astro538/E-Tongue_SIH-demo.git
cd E-Tongue_SIH-demo
python -m venv .venv
```

Activate the environment and install dependencies:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
pip install streamlit pandas numpy
streamlit run herb.py
```

**macOS / Linux**
```bash
source .venv/bin/activate
pip install streamlit pandas numpy
streamlit run herb.py
```

Open the local URL printed by Streamlit in your browser.

## Data format

The universal CSV is expected to contain these columns:

```csv
Herb,Voltammetric Sensor,Conductivity Sensor,Photochemical Sensor,pH Sensor
```

Each sensor value should use the same scale and calibration as the values entered in the UI. Matching is meaningful only if reference and unknown samples are measured with consistent procedures and instruments.

## Security and limitations

- The current login credentials are hard-coded in `herb.py` for demonstration. They are not secure authentication and must be replaced before any deployment.
- Do not expose the app publicly with the example credentials or private data files.
- The current score does not account for sensor calibration, uncertainty, measurement variation, or chemical ground truth.
- Persistent edits write to local CSV/JSON files. There is no database-backed multi-user synchronization.
- The provided example values should not be treated as verified experimental measurements.

## Suggested next steps

Collect traceable labelled measurements, define sensor calibration and repeatability protocols, evaluate matching thresholds on a held-out set, report confusion matrices and uncertainty, and add secure authentication and storage.

## License

No explicit license file was identified in the repository when this README was prepared.
