from django.db import migrations, models
import django.db.models.deletion
import ckeditor.fields

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('subtitle', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
                ('sort_order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='CateringInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=50)),
                ('event_date', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Catering Inquiries',
            },
        ),
        migrations.CreateModel(
            name='ContactInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Contact Inquiries',
            },
        ),
        migrations.CreateModel(
            name='HeroSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kicker', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('button_text', models.CharField(default='Shop Now', max_length=50)),
                ('button_link', models.CharField(default='#products-section', max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='hero_slides/')),
                ('graphic_type', models.CharField(choices=[('star', 'Star Emblem'), ('jar_red', 'Red Jar (Khlii)'), ('pot_gold', 'Gold Pot (Amlou)'), ('jar_green', 'Green Jar (Tagine Spice)')], default='star', max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_percentage', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SiteContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_key', models.CharField(help_text='Type exact key like: about_us', max_length=100, unique=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('body_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='site_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('subtitle', models.CharField(max_length=200)),
                ('description', ckeditor.fields.RichTextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('inventory_stock', models.PositiveIntegerField(default=10)),
                ('is_bestseller', models.BooleanField(default=False)),
                ('image_placeholder_tag', models.CharField(choices=[('khlii', 'Moroccan Khlii Jar (Maroon Confit)'), ('smen', 'Moroccan Smen Pot (Cultured Butter)'), ('lemon', 'Preserved Lemon Jar (Salt-Cured)'), ('orange_jam', 'Moroccan Orange Jam (Bright Orange)'), ('lemon_jam', 'Moroccan Lemon Jam (Light Citrus)'), ('spice_ras', 'Ras el Hanout Spice Jar (Deep Red)'), ('spice_tagine', 'Tagine Spice Blend Jar (Deep Green)'), ('spice_chermoula', 'Chermoula Spice Jar (Golden Mustard)'), ('spice_couscous', 'Couscous Spice Jar (Warm Brown)'), ('amlou_orig', 'Amlou Original Pot (Amber Honey)'), ('amlou_dxb', 'Amlou DXB Style Pot (Rich Cocoa)'), ('amlou_dates', 'Amlou Dates & Nuts Pot (Deep Rust)')], default='khlii', max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_gallery/')),
                ('alt_text', models.CharField(blank=True, max_length=100, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='store.product')),
            ],
        ),
    ]
