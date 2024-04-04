import cv2
import requests
import time

# Endpoint to send scanned data
SERVER_URL = 'http://localhost:3000/'

# Time to wait after successful scan (in seconds)
WAIT_TIME_AFTER_SCAN = 3600  # 60 minutes

# Dictionary to store last scan time of each QR code
last_scan_times = {}

def send_data_to_server(name):
    try:
        response = requests.post('http://localhost:3000/', json={'name': name})
        if response.status_code == 200:
            print('Scanned data sent to server successfully')
            return True
        else:
            print('Failed to send scanned data to server:', response.status_code)
            return False
    except Exception as e:
        print('Error sending data to server:', e)
        return False

def main():
    # Open camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read frame from camera
        ret, frame = cap.read()

        # Initialize QR code scanner
        scanner = cv2.QRCodeDetector()

        # Detect QR code in the frame
        data, bbox, _ = scanner.detectAndDecode(frame)

        if bbox is not None:
            # Convert bbox coordinates to integers
            bbox = bbox.astype(int)

            # Draw bounding box around the QR code
            for i in range(len(bbox)):
                cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)

            if data:
                # Check if QR code has been scanned within the last 60 minutes
                if data in last_scan_times and time.time() - last_scan_times[data] < WAIT_TIME_AFTER_SCAN:
                    # Display message on camera feed
                    cv2.putText(frame, 'Your Turn Is Done', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    # Send scanned data to server
                    print('Scanned data:', data)
                    if send_data_to_server(data):
                        # Update last scan time for the QR code
                        last_scan_times[data] = time.time()

        # Display the frame
        cv2.imshow('QR Code Scanner', frame)

        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera
    cap.release()

    # Close OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
