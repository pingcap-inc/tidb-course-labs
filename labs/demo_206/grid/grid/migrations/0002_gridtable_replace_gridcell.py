# Replace grid_cell with grid_table (schema_design: RID + A-X, 24 rows).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GridTable',
            fields=[
                ('rid', models.AutoField(db_column='RID', primary_key=True, serialize=False)),
                ('a', models.CharField(blank=True, db_column='A', default='', max_length=6)),
                ('b', models.CharField(blank=True, db_column='B', default='', max_length=6)),
                ('c', models.CharField(blank=True, db_column='C', default='', max_length=6)),
                ('d', models.CharField(blank=True, db_column='D', default='', max_length=6)),
                ('e', models.CharField(blank=True, db_column='E', default='', max_length=6)),
                ('f', models.CharField(blank=True, db_column='F', default='', max_length=6)),
                ('g', models.CharField(blank=True, db_column='G', default='', max_length=6)),
                ('h', models.CharField(blank=True, db_column='H', default='', max_length=6)),
                ('i', models.CharField(blank=True, db_column='I', default='', max_length=6)),
                ('j', models.CharField(blank=True, db_column='J', default='', max_length=6)),
                ('k', models.CharField(blank=True, db_column='K', default='', max_length=6)),
                ('l', models.CharField(blank=True, db_column='L', default='', max_length=6)),
                ('m', models.CharField(blank=True, db_column='M', default='', max_length=6)),
                ('n', models.CharField(blank=True, db_column='N', default='', max_length=6)),
                ('o', models.CharField(blank=True, db_column='O', default='', max_length=6)),
                ('p', models.CharField(blank=True, db_column='P', default='', max_length=6)),
                ('q', models.CharField(blank=True, db_column='Q', default='', max_length=6)),
                ('r', models.CharField(blank=True, db_column='R', default='', max_length=6)),
                ('s', models.CharField(blank=True, db_column='S', default='', max_length=6)),
                ('t', models.CharField(blank=True, db_column='T', default='', max_length=6)),
                ('u', models.CharField(blank=True, db_column='U', default='', max_length=6)),
                ('v', models.CharField(blank=True, db_column='V', default='', max_length=6)),
                ('w', models.CharField(blank=True, db_column='W', default='', max_length=6)),
                ('x', models.CharField(blank=True, db_column='X', default='', max_length=6)),
            ],
            options={
                'db_table': 'grid_table',
                'ordering': ['rid'],
            },
        ),
        migrations.DeleteModel(name='GridCell'),
    ]
