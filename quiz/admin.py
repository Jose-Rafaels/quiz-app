# # Register your models here.
# from django.contrib.auth.models import Group, Permission, User
# from django.contrib.contenttypes.models import ContentType
# from .models import Quiz

# # Membuat Group Admin
# admin_group, created = Group.objects.get_or_create(name='Admin')

# # Menambahkan permission pada group Admin
# content_type = ContentType.objects.get_for_model(Quiz)
# permission = Permission.objects.create(codename='can_add_quiz',
#                                        name='Can Add Quiz',
#                                        content_type=content_type)
# admin_group.permissions.add(permission)

# # Membuat Group User
# user_group, created = Group.objects.get_or_create(name='User')

# # Menambahkan permission pada group User
# permission = Permission.objects.create(codename='can_take_quiz',
#                                        name='Can Take Quiz',
#                                        content_type=content_type)
# user_group.permissions.add(permission)


# # Mengassign User ke dalam group Admin
# user = User.objects.get(username='admin_user')
# admin_group = Group.objects.get(name='Admin')
# user.groups.add(admin_group)

# # Mengassign User ke dalam group User
# user = User.objects.get(username='regular_user')
# user_group = Group.objects.get(name='User')
# user.groups.add(user_group)
