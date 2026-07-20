from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone

MigrationRecorder.Migration.objects.get_or_create(app='accounts', name='0001_initial')
print('accounts.0001_initial marked as applied')
