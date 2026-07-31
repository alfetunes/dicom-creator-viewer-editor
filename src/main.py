import sys
import numpy as np
import pydicom
from PIL import Image
from datetime import datetime

from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import generate_uid

from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog,
    QMessageBox, QVBoxLayout, QHBoxLayout,
    QFormLayout, QDialog, QLineEdit,
    QLabel, QDialogButtonBox
)

from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class MetadataDialog(QDialog):

    def __init__(self, ds):
        super().__init__()

        self.ds = ds

        self.setWindowTitle("Edit Metadata")
        self.resize(800, 500)

        layout = QFormLayout()

        self.fields = {}

        tags = [
            "PatientName",
            "PatientID",
            "PatientBirthDate",
            "StudyDate",
            "StudyTime",
            "StudyInstanceUID",
            "SeriesInstanceUID",
            "SOPInstanceUID",
            "Modality"
        ]

        for tag in tags:

            value = str(getattr(ds, tag, ""))

            edit = QLineEdit(value)

            self.fields[tag] = edit

            layout.addRow(tag, edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

        self.setLayout(layout)

    def apply(self):

        for tag, widget in self.fields.items():

            setattr(
                self.ds,
                tag,
                widget.text()
            )


class DicomEditor(QWidget):

    def __init__(self):
        super().__init__()

        self.ds = None

        self.setWindowTitle("Simple DICOM Editor")
        self.resize(900, 700)

        layout = QVBoxLayout()

        buttons = QHBoxLayout()

        create_btn = QPushButton("Create From Image")
        create_btn.clicked.connect(
            self.create_from_image
        )

        open_btn = QPushButton("Open DICOM")
        open_btn.clicked.connect(
            self.open_dicom
        )

        edit_btn = QPushButton("Edit Metadata")
        edit_btn.clicked.connect(
            self.edit_metadata
        )

        save_btn = QPushButton("Save As")
        save_btn.clicked.connect(
            self.save_dicom
        )

        buttons.addWidget(create_btn)
        buttons.addWidget(open_btn)
        buttons.addWidget(edit_btn)
        buttons.addWidget(save_btn)

        self.preview = QLabel(
            "No image loaded"
        )

        self.preview.setAlignment(
            Qt.AlignCenter
        )

        layout.addLayout(buttons)
        layout.addWidget(self.preview)

        self.setLayout(layout)

    def create_from_image(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not path:
            return

        try:

            img = Image.open(path)

            if img.mode == "RGBA":
                img = img.convert("RGB")

            arr = np.array(img)

            ds = Dataset()

            meta = FileMetaDataset()

            meta.TransferSyntaxUID = (
                pydicom.uid.ExplicitVRLittleEndian
            )

            sop_class = (
                pydicom.uid.SecondaryCaptureImageStorage
            )

            sop_uid = generate_uid()

            meta.MediaStorageSOPClassUID = sop_class
            meta.MediaStorageSOPInstanceUID = sop_uid

            ds.file_meta = meta

            ds.is_little_endian = True
            ds.is_implicit_VR = False

            now = datetime.now()

            ds.PatientName = "ANON"
            ds.PatientID = "000001"

            ds.PatientBirthDate = ""

            ds.StudyDate = now.strftime("%Y%m%d")
            ds.StudyTime = now.strftime("%H%M%S")

            ds.StudyInstanceUID = generate_uid()
            ds.SeriesInstanceUID = generate_uid()

            ds.SOPClassUID = sop_class
            ds.SOPInstanceUID = sop_uid

            ds.Modality = "OT"

            if img.mode == "L":

                ds.Rows, ds.Columns = arr.shape

                ds.SamplesPerPixel = 1

                ds.PhotometricInterpretation = (
                    "MONOCHROME2"
                )

            else:

                ds.Rows = arr.shape[0]
                ds.Columns = arr.shape[1]

                ds.SamplesPerPixel = 3

                ds.PhotometricInterpretation = (
                    "RGB"
                )

                ds.PlanarConfiguration = 0

            ds.BitsAllocated = 8
            ds.BitsStored = 8
            ds.HighBit = 7
            ds.PixelRepresentation = 0

            ds.PixelData = arr.tobytes()

            self.ds = ds

            self.show_preview()

            QMessageBox.information(
                self,
                "Done",
                "DICOM created."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def open_dicom(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open DICOM",
            "",
            "DICOM (*.dcm)"
        )

        if not path:
            return

        try:

            self.ds = pydicom.dcmread(path)

            self.show_preview()

            QMessageBox.information(
                self,
                "Loaded",
                "DICOM opened."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def edit_metadata(self):

        if self.ds is None:

            QMessageBox.warning(
                self,
                "No dataset",
                "Load or create a DICOM first."
            )

            return

        dialog = MetadataDialog(
            self.ds
        )

        if dialog.exec():

            dialog.apply()

    def save_dicom(self):

        if self.ds is None:

            QMessageBox.warning(
                self,
                "No dataset",
                "Nothing to save."
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save DICOM",
            "edited.dcm",
            "DICOM (*.dcm)"
        )

        if not path:
            return

        try:

            self.ds.save_as(
                path,
                write_like_original=False
            )

            QMessageBox.information(
                self,
                "Saved",
                f"Saved:\n{path}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def show_preview(self):

        if self.ds is None:
            return

        if "PixelData" not in self.ds:

            self.preview.setText(
                "No PixelData"
            )

            return

        try:

            arr = self.ds.pixel_array

            if arr.dtype != np.uint8:

                arr = arr.astype(float)

                arr = (
                    arr / arr.max() * 255
                ).astype(np.uint8)

            if arr.ndim == 2:

                h, w = arr.shape

                qimg = QImage(
                    arr.data,
                    w,
                    h,
                    w,
                    QImage.Format_Grayscale8
                )

            else:

                h, w, c = arr.shape

                qimg = QImage(
                    arr.data,
                    w,
                    h,
                    3 * w,
                    QImage.Format_RGB888
                )

            pix = QPixmap.fromImage(
                qimg.copy()
            )

            pix = pix.scaled(
                700,
                500,
                Qt.KeepAspectRatio
            )

            self.preview.setPixmap(
                pix
            )

        except Exception as e:

            self.preview.setText(
                f"Preview failed:\n{e}"
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = DicomEditor()

    window.show()

    sys.exit(
        app.exec()
    )