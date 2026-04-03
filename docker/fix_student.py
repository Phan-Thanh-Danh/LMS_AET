import frappe
from frappe.utils.password import set_password

def run():
    email = "student_hackathon_test@example.com"
    pwd = "StrongPass@2026"
    
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": "Nguyen Van A",
            "last_name": "- Team Hackathon",
            "send_welcome_email": 0
        })
        user.insert(ignore_permissions=True)
        print(f"Created user {email}")
    else:
        user = frappe.get_doc("User", email)
        print(f"User {email} already exists")

    # Force enable and set password
    user.enabled = 1
    user.save(ignore_permissions=True)
    
    set_password(email, pwd)
    
    # Ensure role
    if not any(r.role == "LMS Student" for r in user.roles):
        user.add_roles("LMS Student")
        print("Added LMS Student role")
    
    frappe.db.commit()
    print(f"✅ Đã cấu hình lại tài khoản: {email} / {pwd}")

if __name__ == "__main__":
    run()
