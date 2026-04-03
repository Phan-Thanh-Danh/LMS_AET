import frappe

# Course Creator
if not frappe.db.exists("User", "creator@example.com"):
    user = frappe.new_doc("User")
    user.first_name = "Creator"
    user.last_name = "User"
    user.email = "creator@example.com"
    user.send_welcome_email = False
    user.add_roles("Course Creator")
    user.save()

# Evaluator
if not frappe.db.exists("User", "evaluator@example.com"):
    user = frappe.new_doc("User")
    user.first_name = "Evaluator"
    user.last_name = "User"
    user.email = "evaluator@example.com"
    user.send_welcome_email = False
    user.add_roles("Evaluator")
    user.save()

print("Users created")
