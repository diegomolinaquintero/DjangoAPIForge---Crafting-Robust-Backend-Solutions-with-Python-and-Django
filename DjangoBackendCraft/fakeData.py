import os
import django
import random
from faker import Faker
from django.conf import settings

# Configurar la configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoBackendCraft.settings") 
django.setup()

# Importar tus modelos
from users.models import CustomUser
from users.models import UserProfile
from users.models import UserActivityLog
from users.models import PasswordResetToken
from avatar.models import UserAvatar
from block.models import BlockedUser
from search.models import UserSearchHistory
from stats.models import UserStatistics

fake = Faker()

# Crear 50 usuarios falsos
for _ in range(50):
    user = CustomUser.objects.create(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_active=fake.boolean(),
        is_staff=fake.boolean()
    )
    UserProfile.objects.create(
        user=user,
        avatar=fake.image_url(),
        bio=fake.text()
    )
    UserActivityLog.objects.create(
        user=user,
        timestamp=fake.date_time(),
        action=fake.sentence()
    )
    PasswordResetToken.objects.create(
        user=user,
        token=fake.uuid4(),
        created_at=fake.date_time(),
        is_used=fake.boolean()
    )
    UserAvatar.objects.create(
        user=user,
        avatar=fake.image_url()
    )
    BlockedUser.objects.create(
        user=user,
        is_blocked=fake.boolean()
    )
    UserSearchHistory.objects.create(
        user=user,
        search_query=fake.word(),
        timestamp=fake.date_time()
    )
    UserStatistics.objects.create(
        user=user,
        total_logins=random.randint(1, 100)
    )
