import frappe

from frappe.utils.password import set_password

# Set password for all users

users = frappe.get_all("User", filters={"name": ["not in", ["Administrator", "Guest"]]}, pluck="name")

for user in users:

    set_password(user, "password123")

print("Passwords set to password123")
