import cv2
from ocr_inference import extract_text_from_image

def extract_text_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "", None

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    mid = frame_count // 2

    cap.set(cv2.CAP_PROP_POS_FRAMES, mid)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "", None

    text = extract_text_from_image(frame)
    return text, frame
