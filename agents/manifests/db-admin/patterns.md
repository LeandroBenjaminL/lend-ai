# DB Admin — Patterns

### PostgreSQL tuning
```
shared_buffers = 25% of RAM
effective_cache_size = 75% of RAM
work_mem = 4-8MB (por query, cuidado con OOM)
maintenance_work_mem = 256MB
random_page_cost = 1.1 (si SSD)
```

### Migration pattern
```python
"""add user email index"""
from alembic import op

def upgrade():
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email')
```

### Backup command
```bash
pg_dump -Fc -Z 9 --file=db_$(date +%Y%m%d).dump mydb
```
