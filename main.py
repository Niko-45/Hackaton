import sqlite3
import face_recognition
import cv2
import datetime
import numpy as np

# SQLite bağlantısı
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Öğrencileri veritabanından al
cursor.execute("SELECT id, name, face_encoding, course_id FROM myapp_student")
students = cursor.fetchall()

# Bilinen yüzler ve kurslar hazırlanır
known_face_encodings = []
known_face_names = []
student_courses = {}

for student in students:
    student_id, name, encoding_data, course_id = student
    encoding = np.frombuffer(encoding_data, dtype=np.float64)
    known_face_encodings.append(encoding)
    known_face_names.append(name)
    student_courses[student_id] = course_id

# Kamerayı başlat
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Camera failed to initialize!")

# Yoklama kontrolü
while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        student_id = None

        if True in matches:
            matched_index = matches.index(True)
            student_id = students[matched_index][0]
            name = known_face_names[matched_index]
            course_id = student_courses[student_id]
            
            # Kurs başlangıç saati kontrolü
            cursor.execute("SELECT start_time FROM myapp_course WHERE id = ?", (course_id,))
            course_start_time = cursor.fetchone()[0]
            attendance_time = datetime.datetime.now()
            attendance_date = attendance_time.date()

            # Kurs başlangıç tarihi ve saati
            course_start_datetime = datetime.datetime.combine(attendance_date, datetime.datetime.strptime(course_start_time, "%H:%M:%S").time())

            # Yalnızca kurs başlangıç saatiyle kayıt al
            if attendance_time >= course_start_datetime:
                cursor.execute(
                    "SELECT 1 FROM myapp_attendance WHERE student_id = ? AND attendance_date = ?",
                    (student_id, attendance_date)
                )
                existing_record = cursor.fetchone()

                if not existing_record:
                    # Geç kalma hesaplama
                    late_minutes = max((attendance_time - course_start_datetime).seconds // 60, 0)
                    
                    cursor.execute(
                        "INSERT INTO myapp_attendance (student_id, course_id, attendance_time, attendance_date, late_minutes, is_active) VALUES (?, ?, ?, ?, ?, ?)",
                        (student_id, course_id, attendance_time.strftime("%H:%M:%S"), attendance_date, late_minutes, True)
                    )
                    conn.commit()
                    print(f"{name}'s attendance recorded. Late by {late_minutes} minutes." if late_minutes else f"{name}'s attendance recorded on time.")
                else:
                    print(f"{name} already has an attendance record for today.")  # Kayıt var uyarısı
            else:
                print(f"{name}'s attendance not recorded. Class has not started yet.")  # Kurs başlamadı uyarısı

        # Yüz kutusunu çiz ve adı göster
        if student_id is not None:  # Sadece tanınan yüzler için kutu çiz
            top, right, bottom, left = top * 2, right * 2, bottom * 2, left * 2
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()
