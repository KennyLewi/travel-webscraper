import cv2
import easyocr
import os

# Initialize reader with GPU enabled if possible
reader = easyocr.Reader(['en'], gpu=True)


def fast_extract_text(video_path, interval_ms=1000):
    if not os.path.exists(video_path):
        return

    cap = cv2.VideoCapture(video_path)
    total_ms = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) /
                   cap.get(cv2.CAP_PROP_FPS) * 1000)
    unique_text = set()

    print(f"Jumping through {total_ms//1000}s of video...")

    # Strategy: Jump directly to each second
    for current_ms in range(0, total_ms, interval_ms):
        # FAST SEEK: Jump to the timestamp
        cap.set(cv2.CAP_PROP_POS_MSEC, current_ms)
        success, frame = cap.read()

        if not success:
            break

        # Optimization: Downscale frame if it's 4K or 1080p (TikTok is usually 720p)
        # Smaller images process 2-3x faster with almost same accuracy
        height, width = frame.shape[:2]
        if width > 1000:
            frame = cv2.resize(frame, (width//2, height//2))

        # OCR with detail=0 (No bounding boxes = much faster)
        results = reader.readtext(frame, detail=0)

        for text in results:
            if len(text.strip()) > 2:
                unique_text.add(text.strip())

        print(current_ms)

    cap.release()

    final_results = sorted(list(unique_text))
    print("\n".join(final_results))
    return final_results


if __name__ == "__main__":
    filename = "my_tiktok_video.mp4"
    fast_extract_text(filename)
