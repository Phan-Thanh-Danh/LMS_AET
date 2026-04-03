from frappe.utils.password import set_password

users = frappe.get_all('User', filters={'name': ['not in', ['Administrator', 'Guest']]}, pluck='name')

for u in users:

    set_password(u, 'password123')

print('Passwords set')
