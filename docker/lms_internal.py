import frappe
from lms.lms.doctype.lms_enrollment.lms_enrollment import enroll_in_course

def run():
    print("--- STARTING LMS AUTOMATION ---\n")
    frappe.set_user("Administrator")
    
    # 1. BƯỚC 1: TẠO LESSON & ASSIGNMENT
    course_name = "tao" 
    if not frappe.db.exists("LMS Course", course_name):
        courses = frappe.get_all("LMS Course", limit=1)
        if not courses:
            print("ERROR: No courses found.")
            return
        course_name = courses[0].name
    
    course = frappe.get_doc("LMS Course", course_name)
    course.published = 1
    
    # Ensure a chapter exists
    if not course.chapters:
        ch_name = "CH-Hackathon"
        if not frappe.db.exists("Course Chapter", ch_name):
            ch = frappe.get_doc({
                "doctype": "Course Chapter",
                "title": "Hackathon 2026",
                "course": course_name
            }).insert(ignore_permissions=True)
            ch_name = ch.name
        course.append("chapters", {"chapter": ch_name})
    
    course.save(ignore_permissions=True)
    frappe.db.commit()

    # Create Assignment
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
        print(f"✅ BƯỚC 1: Đã tạo Assignment {assign_id}")
    else:
        print(f"✅ BƯỚC 1: Assignment {assign_id} đã tồn tại.")

    # Create Lesson
    lesson_title = "Nộp đề xuất dự án WEB AI HACKATHON 2026"
    lesson_id = frappe.db.get_value("Course Lesson", {"title": lesson_title}, "name")
    if not lesson_id:
        lesson = frappe.get_doc({
            "doctype": "Course Lesson",
            "title": lesson_title,
            "course": course_name,
            "chapter": course.chapters[0].chapter,
            "body": f"Yêu cầu:\n- Nêu tên dự án\n- Mô tả bài toán\n- Tech stack\n- Link GitHub\n\n{{{{ Assignment('{assign_id}') }}}}"
        })
        lesson.insert(ignore_permissions=True)
        lesson_id = lesson.name
        print(f"✅ BƯỚC 1: Đã tạo Lesson {lesson_id}")
    else:
        print(f"✅ BƯỚC 1: Lesson {lesson_id} đã tồn tại.")

    # 2. BƯỚC 2: HỌC VIÊN NỘP BÀI
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
        print(f"✅ BƯỚC 2: Đã tạo User {student_email}")
    
    # Enroll
    enroll_in_course(course_name, student_email)
    
    # Submission
    # Check if already submitted
    sub_id = frappe.db.get_value("LMS Assignment Submission", {"assignment": assign_id, "member": student_email}, "name")
    if not sub_id:
        sub = frappe.get_doc({
            "doctype": "LMS Assignment Submission",
            "assignment": assign_id,
            "member": student_email,
            "answer": "TÊN DỰ ÁN: AI Resume Screener\nMÔ TẢ: Hệ thống sàng lọc CV tự động.\nTECH STACK: React, FastAPI, GPT-4o.\nGITHUB: https://github.com/team-hackathon/ai-resume-screener",
            "status": "Not Graded"
        })
        sub.insert(ignore_permissions=True)
        sub_id = sub.name
        print(f"✅ BƯỚC 2: Đã nộp bài. Submission ID: {sub_id}")
    else:
        print(f"✅ BƯỚC 2: Bài nộp đã tồn tại: {sub_id}")

    # 3. BƯỚC 3: CHẤM ĐIỂM
    sub = frappe.get_doc("LMS Assignment Submission", sub_id)
    sub.status = "Pass"
    sub.comments = "Ý tưởng dự án AI Resume Screener rất thực tiễn và có tiềm năng ứng dụng cao. Điểm mạnh: Tech stack hợp lý, tích hợp RAG với Vector DB là lựa chọn tốt."
    sub.evaluator = "Administrator"
    sub.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"✅ BƯỚC 3: Đã chấm điểm PASS (Evaluated) và ghi Feedback thành công.")
    
    print("\n🎯 QUY TRÌNH ĐẦY ĐỦ: THÀNH CÔNG")

if __name__ == "__main__":
    run()
