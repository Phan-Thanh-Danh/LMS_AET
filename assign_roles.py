import frappe

# Assign roles

frappe.db.add_roles("ash@ipp.com", "Course Creator")

frappe.db.add_roles("john.doe@example.com", "Evaluator")

print("Roles assigned")
