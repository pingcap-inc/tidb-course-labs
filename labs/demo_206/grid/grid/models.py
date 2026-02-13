"""
24x24 grid stored as grid_table: 24 rows, columns A-X (CHAR(6) each).
One table row = one grid row; columns A..X = grid columns 0..23.
"""
from django.db import models

# Column names A-X for grid_table (match schema_design.sql)
GRID_COLUMNS = [chr(ord('A') + i) for i in range(24)]  # A..X


class GridTable(models.Model):
    """One row of the 24x24 grid. RID = row id, A-X = cell colors (6-char hex)."""
    rid = models.AutoField(primary_key=True, db_column='RID')
    a = models.CharField(max_length=6, blank=True, default='', db_column='A')
    b = models.CharField(max_length=6, blank=True, default='', db_column='B')
    c = models.CharField(max_length=6, blank=True, default='', db_column='C')
    d = models.CharField(max_length=6, blank=True, default='', db_column='D')
    e = models.CharField(max_length=6, blank=True, default='', db_column='E')
    f = models.CharField(max_length=6, blank=True, default='', db_column='F')
    g = models.CharField(max_length=6, blank=True, default='', db_column='G')
    h = models.CharField(max_length=6, blank=True, default='', db_column='H')
    i = models.CharField(max_length=6, blank=True, default='', db_column='I')
    j = models.CharField(max_length=6, blank=True, default='', db_column='J')
    k = models.CharField(max_length=6, blank=True, default='', db_column='K')
    l = models.CharField(max_length=6, blank=True, default='', db_column='L')
    m = models.CharField(max_length=6, blank=True, default='', db_column='M')
    n = models.CharField(max_length=6, blank=True, default='', db_column='N')
    o = models.CharField(max_length=6, blank=True, default='', db_column='O')
    p = models.CharField(max_length=6, blank=True, default='', db_column='P')
    q = models.CharField(max_length=6, blank=True, default='', db_column='Q')
    r = models.CharField(max_length=6, blank=True, default='', db_column='R')
    s = models.CharField(max_length=6, blank=True, default='', db_column='S')
    t = models.CharField(max_length=6, blank=True, default='', db_column='T')
    u = models.CharField(max_length=6, blank=True, default='', db_column='U')
    v = models.CharField(max_length=6, blank=True, default='', db_column='V')
    w = models.CharField(max_length=6, blank=True, default='', db_column='W')
    x = models.CharField(max_length=6, blank=True, default='', db_column='X')

    class Meta:
        app_label = 'grid'
        db_table = 'grid_table'
        ordering = ['rid']

    def get_row_colors(self):
        """Return list of 24 color hex strings (with #) for this grid row."""
        return [_to_css_hex(getattr(self, col.lower(), '') or '') for col in GRID_COLUMNS]


def _to_css_hex(val):
    """Normalize to #rrggbb for CSS. val may be 6-char hex or 7-char with #."""
    val = (val or '').strip()
    if not val:
        return '#1a1a2e'
    if val.startswith('#'):
        return val if len(val) >= 7 else '#1a1a2e'
    return '#' + val if len(val) == 6 else '#1a1a2e'
