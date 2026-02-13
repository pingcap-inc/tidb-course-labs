from django.shortcuts import render
from django.views import View
from .models import GridTable

DEFAULT_CELL = '#1a1a2e'


class GridView(View):
    """Single page: 24x24 color grid from grid_table (24 rows, columns A-X)."""
    def get(self, request):
        rows = list(GridTable.objects.order_by('rid')[:24])
        grid = []
        for row in rows:
            grid.append(row.get_row_colors())
        # Pad to exactly 24 rows
        while len(grid) < 24:
            grid.append([DEFAULT_CELL] * 24)
        return render(request, 'grid/index.html', {'grid': grid})
