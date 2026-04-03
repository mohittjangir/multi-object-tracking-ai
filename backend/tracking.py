import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=30)

def process_video(input_path, output_path="output.mp4"):

    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)[0]

        detections = []

        for r in results.boxes.data.tolist():

            x1,y1,x2,y2,conf,cls = r

            if int(cls) == 0:
                detections.append(([x1,y1,x2-x1,y2-y1], conf, "person"))

        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:

            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l,t,w,h = track.to_ltrb()

            x1,y1,x2,y2 = int(l),int(t),int(w),int(h)

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

            cv2.putText(
                frame,
                f"ID {track_id}",
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

        out.write(frame)

    cap.release()
    out.release()

    return output_path


if __name__ == "__main__":

    process_video("input.mp4")