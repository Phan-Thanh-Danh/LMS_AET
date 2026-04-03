import os

os.environ["FRAPPE_SITE"] = "lms.localhost"

import frappe

frappe.init("")

frappe.connect()

exec(open("set_password.py").read())
