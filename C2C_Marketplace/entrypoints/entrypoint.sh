#!/bin/sh

set -e

echo "Applying migrations..."
python manage.py migrate

echo "Loading fixtures..."

python manage.py loaddata seed/users.json
python manage.py loaddata seed/categories.json
python manage.py loaddata seed/locations.json
python manage.py loaddata seed/contact_infos.json
python manage.py loaddata seed/category_attributes.json
python manage.py loaddata seed/category_attribute_options.json
python manage.py loaddata seed/products.json
python manage.py loaddata seed/product_images.json
python manage.py loaddata seed/product_attribute_values.json

# echo "Copying media..."

mkdir -p media
# cp -r seed/media/products .

echo "Database seeded successfully!"

exec "$@"