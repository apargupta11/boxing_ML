
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"

CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

DEVICE_NAME = "ESP32_RIGHT_RELAY"

BUFFER_SECONDS = 3

SAMPLING_RATE = 60      # your current BLE rate

SAVE_DIRECTORY = "../data/raw"

WINDOW_BEFORE =10
WINDOW_AFTER = 10


# ==========================
# Activity Labels
# ==========================

LABEL_MAP = {
    "NONE": 0,
    "LEFT": 1,
    "RIGHT": 2,
    "BOTH": 3,
}
RAW_DATA_DIR = "data/raw"

METADATA_DIR = "data/metadata"

TRAINING_DIR = "data/training"
WINDOW_BEFORE = 13
WINDOW_AFTER = 13
WINDOW_STRIDE = 5

WINDOW_SIZE = WINDOW_BEFORE + WINDOW_AFTER + 1

MASTER_DATA_DIR = "data/master"
MODEL_DIR = "models"