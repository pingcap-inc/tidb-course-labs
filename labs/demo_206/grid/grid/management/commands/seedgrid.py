"""
Seed the 24x24 grid in grid_table. Idempotent: clears existing rows then inserts 24 rows (A-X each).
"""
import random
from django.core.management.base import BaseCommand
from grid.models import GridTable

GRID_COLS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x']


def random_hex6():
    """Return 6-char hex color (no #) for CHAR(6) column."""
    r = random.randint(40, 255)
    g = random.randint(40, 255)
    b = random.randint(40, 255)
    return f'{r:02x}{g:02x}{b:02x}'


class Command(BaseCommand):
    help = 'Seed grid_table with 24 rows and random colors in A-X (run once after migrate).'

    def handle(self, *args, **options):
        GridTable.objects.all().delete()
        for _ in range(24):
            row_data = {col: random_hex6() for col in GRID_COLS}
            GridTable.objects.create(**row_data)
        self.stdout.write(self.style.SUCCESS('Seeded grid_table with 24 rows (columns A-X).'))
