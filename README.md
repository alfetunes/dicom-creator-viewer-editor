# Simple DICOM Editor

<p align="center">

A lightweight desktop application for creating, viewing and editing DICOM files.

Built with **Python**, **PySide6**, **pydicom**, **NumPy** and **Pillow**.

Designed primarily for **QA engineers**, **developers**, **researchers**, and anyone who needs to quickly generate or edit DICOM files for testing purposes.

</p>

---

## Features

- Create DICOM files from common image formats
  - PNG
  - JPG / JPEG
  - BMP

- Open existing DICOM files

- Preview DICOM images

- Edit common metadata fields

  - Patient Name
  - Patient ID
  - Patient Birth Date
  - Study Date
  - Study Time
  - Study Instance UID
  - Series Instance UID
  - SOP Instance UID
  - Modality

- Save edited DICOM files

- Simple and lightweight graphical interface

- Fully offline

---

## Technologies

- Python 3
- PySide6
- pydicom
- Pillow
- NumPy

---

## Project Structure

```
simple-dicom-editor/
│
├── src/
│   ├── main.py
├── requirements.txt
├── LICENSE
├── README.md
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/alfetunes/dicom-creator-viewer-editor.git

cd simple-dicom-editor
```

---

## Create a Virtual Environment (Recommended)

Modern Linux distributions such as **Ubuntu 24.04+** and **Debian 12+** implement **PEP 668**, which prevents installing Python packages directly into the system Python environment.

Creating a virtual environment is the recommended and safest approach.

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Windows (Command Prompt)

```cmd
python -m venv .venv

.venv\Scripts\activate.bat
```

### Windows (PowerShell)

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

---

## Install Dependencies

Upgrade pip first.

```bash
python -m pip install --upgrade pip
```

Install the required packages.

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python src/main.py
```

---

# Ubuntu / Debian Notes

If you receive the following error:

```
error: externally-managed-environment
```

your operating system is enforcing **PEP 668**.

This is expected behavior and is intended to protect the system Python installation.

Install the required packages:

```bash
sudo apt update

sudo apt install python3-full python3-venv
```

Then recreate the virtual environment:

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

---

# Alternative Installation (Not Recommended)

If you intentionally want to install the dependencies into your system Python installation, you can use:

```bash
pip install -r requirements.txt --break-system-packages
```

This approach is **not recommended**, as it may interfere with packages managed by your operating system.

---

# Requirements

- Python 3.10 or newer
- NumPy
- Pillow
- pydicom
- PySide6

All dependencies are listed in `requirements.txt`.

---

# Usage

## Create a DICOM

1. Click **Create From Image**
2. Select an image
3. The application creates a valid DICOM object
4. Preview the generated image
5. Edit metadata if necessary
6. Save the DICOM file

---

## Open an Existing DICOM

1. Click **Open DICOM**
2. Select a `.dcm` file
3. Preview the image
4. Edit metadata
5. Save your changes

---

## Edit Metadata

The application currently supports editing:

- Patient Name
- Patient ID
- Patient Birth Date
- Study Date
- Study Time
- Study Instance UID
- Series Instance UID
- SOP Instance UID
- Modality

---

## Save

Click **Save As** to write the modified dataset to disk.

---

# Privacy

This application runs entirely on your computer.

- No internet connection required
- No cloud services
- No telemetry
- No analytics
- No external API calls

All DICOM processing is performed locally.

---

# Known Limitations

Current version limitations include:

- Single-image DICOM creation only
- Limited metadata editor
- No drag & drop support
- No DICOM validation
- No multi-frame support
- No CT/MR series generation

---

# Roadmap

Future improvements may include:

- Drag & Drop

- Multi-frame DICOM

- Batch image conversion

- Complete DICOM tag editor

- DICOM validation

- Window/Level controls

- Zoom and pan

- Multiple image series

- Dark mode

- Export options

- Executable releases for Windows, Linux and macOS

---

# Contributing

Contributions are welcome.

If you find a bug or have an idea for an improvement, feel free to open an Issue or submit a Pull Request.

---

# License

This project is released under the MIT License.

---

# Acknowledgements

- pydicom
- PySide6
- Pillow
- NumPy

These excellent open-source projects make this application possible.
