from django.contrib.auth import get_user_model

User = get_user_model()

if User.objects.filter(username='admin').exists():
    print('admin exists')
else:
    User.objects.create_superuser('admin', 'admin@example.com', 'AdminPass123!')
    print('admin created')

if User.objects.filter(username='hr').exists():
    print('hr exists')
else:
    User.objects.create_user('hr', 'hr@example.com', 'HrPass123!', is_staff=True)
    print('hr created')
