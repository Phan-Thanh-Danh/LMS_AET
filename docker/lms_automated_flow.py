import frappe
import json
import uuid

def run():
    print("--- 🚀 KHỞI CHẠY QUY TRÌNH TỰ ĐỘNG HÓA LMS HACKATHON ---", flush=True)
    frappe.set_user("Administrator")

    # --- BƯỚC 1: GIẢNG VIÊN (Admin) TẠO BÀI TẬP ---
    print("\n[BƯỚC 1] GÓC NHÌN GIẢNG VIÊN / BAN TỔ CHỨC", flush=True)

    # 1.1 Tìm hoặc Tạo Course
    course_name = "tao" # Example course from system or a new one
    if not frappe.db.exists("LMS Course", course_name):
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": "WEB AI HACKATHON 2026",
            "published": 1,
            "short_introduction": "Course dành cho thí sinh Hackathon 2026."
        })
        course.insert(ignore_permissions=True)
        course_name = course.name
        print(f"-> Đã tạo Course mới: {course_name}")
    else:
        course = frappe.get_doc("LMS Course", course_name)
        course.published = 1
        course.save(ignore_permissions=True)
        print(f"-> Sử dụng Course có sẵn: {course_name}")

    # Ensure Chapter
    if not course.chapters:
        ch = frappe.get_doc({
            "doctype": "Course Chapter",
            "title": "Hackathon 2026",
            "course": course_name
        }).insert(ignore_permissions=True)
        course.append("chapters", {"chapter": ch.name})
        course.save(ignore_permissions=True)
        print(f"-> Đã tạo Chapter: {ch.name}")
    
    chapter_name = course.chapters[0].chapter

    # 1.2 Tạo Assignment
    assign_title = "Nộp đề xuất dự án WEB AI HACKATHON 2026"
    assign_id = frappe.db.get_value("LMS Assignment", {"title": assign_title}, "name")
    if not assign_id:
        assign = frappe.get_doc({
            "doctype": "LMS Assignment",
            "title": assign_title,
            "type": "Text",
            "question": "Nhóm dự thi cần nộp tài liệu đề xuất dự án bao gồm: (1) Tên dự án và mô tả bài toán AI muốn giải quyết, (2) Kiến trúc hệ thống tổng thể (sơ đồ), (3) Tech stack sử dụng (Frontend, Backend, AI Model), (4) Link GitHub repository hoặc file slide thuyết trình.",
            "course": course_name
        })
        assign.insert(ignore_permissions=True)
        assign_id = assign.name
        print(f"-> ✅ Đã tạo Assignment: {assign_id}")
    else:
        print(f"-> ✅ Assignment đã tồn tại: {assign_id}")

    # 1.3 Tạo Lesson và gắn Assignment
    lesson_title = "Nộp đề xuất dự án WEB AI HACKATHON 2026"
    lesson_id = frappe.db.get_value("Course Lesson", {"title": lesson_title}, "name")
    if not lesson_id:
        lesson = frappe.get_doc({
            "doctype": "Course Lesson",
            "title": lesson_title,
            "course": course_name,
            "chapter": chapter_name,
            "body": f"Hãy nộp tài liệu dự án của bạn.\n\n{{{{ Assignment('{assign_id}') }}}}"
        })
        lesson.insert(ignore_permissions=True)
        lesson_id = lesson.name
        print(f"-> ✅ Đã tạo Lesson: {lesson_id}")
    else:
        print(f"-> ✅ Lesson đã tồn tại: {lesson_id}")

    frappe.db.commit()

    # --- BƯỚC 2: HỌC VIÊN (Student) ĐĂNG KÝ & NỘP BÀI ---
    print("\n[BƯỚC 2] GÓC NHÌN HỌC VIÊN / THÍ SINH", flush=True)

    student_email = "student_hackathon_test@example.com"
    if not frappe.db.exists("User", student_email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": student_email,
            "first_name": "Nguyen Van A",
            "last_name": "- Team Hackathon",
            "send_welcome_email": 0,
            "enabled": 1,
            "roles": [{"role": "LMS Student"}]
        })
        user.insert(ignore_permissions=True)
        print(f"-> ✅ Đã đăng ký User mới: {student_email}")
    else:
        print(f"-> ✅ User học viên đã tồn tại: {student_email}")

    # Enroll Study
    if not frappe.db.exists("LMS Enrollment", {"course": course_name, "member": student_email}):
        enroll = frappe.get_doc({
            "doctype": "LMS Enrollment",
            "course": course_name,
            "member": student_email
        })
        enroll.insert(ignore_permissions=True)
        print(f"-> ✅ Đã Enroll vào khóa học: {course_name}")
    else:
        print(f"-> ✅ Học viên đã Enroll trước đó.")

    # Submission
    sub_id = frappe.db.get_value("LMS Assignment Submission", {"assignment": assign_id, "member": student_email}, "name")
    if not sub_id:
        sub = frappe.get_doc({
            "doctype": "LMS Assignment Submission",
            "assignment": assign_id,
            "member": student_email,
            "answer": "TÊN DỰ ÁN: AI Resume Screener\n\nMÔ TẢ: Xây dựng hệ thống sàng lọc hồ sơ ứng viên tự động sử dụng RAG.\nGITHUB: https://github.com/team-hackathon/ai-resume-screener",
            "status": "Not Graded"
        })
        sub.insert(ignore_permissions=True)
        sub_id = sub.name
        print(f"-> ✅ Đã nộp bài thành công (Submission ID: {sub_id}). Trạng thái: Under Review.")
    else:
        print(f"-> ✅ Bài nộp đã tồn tại: {sub_id}")

    frappe.db.commit()

    # --- BƯỚC 3: BAN TỔ CHỨC CHẤM ĐIỂM & PHẢN HỒI ---
    print("\n[BƯỚC 3] GÓC NHÌN BAN TỔ CHỨC (Chấm điểm)", flush=True)

    # Re-fetch as Admin to grade
    sub = frappe.get_doc("LMS Assignment Submission", sub_id)
    sub.status = "Pass" # Representing successful evaluation
    sub.comments = "Ý tưởng dự án AI Resume Screener rất thực tiễn và có tiềm năng ứng dụng cao. Điểm mạnh: Tech stack hợp lý, tích hợp RAG với Vector DB là lựa chọn tốt. Điểm số: 85/100."
    sub.evaluator = "Administrator"
    sub.save(ignore_permissions=True)
    frappe.db.commit()

    print(f"-> ✅ Admin đã chấm điểm thành công cho bài nộp {sub_id}")
    print(f"-> Trạng thái cập nhật: {sub.status} (Pass)")
    print(f"-> Phản hồi: Ý tưởng dự án... (85/100)")

    print("\n🎯 QUY TRÌNH ĐẦY ĐỦ: THÀNH CÔNG")

if __name__ == "__main__":
    run()
