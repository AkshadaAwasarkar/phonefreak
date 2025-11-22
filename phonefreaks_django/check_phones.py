from core.models import Phone

# List all phones
phones = Phone.objects.all()
print(f'\nTotal phones: {phones.count()}\n')

for p in phones:
    print(f'ID: "{p.id}" | Brand: {p.brand} | Model: {p.model}')

# Find phones with empty or problematic IDs
empty_id_phones = Phone.objects.filter(id='')
print(f'\n\nPhones with empty IDs: {empty_id_phones.count()}')

# Also check for None IDs
for p in phones:
    if not p.id or p.id.strip() == '':
        print(f'Found problematic phone: {p.brand} {p.model}')
