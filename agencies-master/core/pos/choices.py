import random

personalized_invoice = {
    'disam': 16,
    'di': 1
}

genders = (
    ('male', 'Masculino'),
    ('female', 'Femenino'),
)

payment = (
    ('cash', 'Efectivo'),
    ('credit', 'Credito'),
    ('transfer', 'Transferencia'),
    ('pos', 'POS'),
)

municipality = (
    ('boaco', 'BOACO'),
    ('carazo', 'CARAZO'),
    ('chinandega', 'CHINANDEGA'),
    ('chontales', 'CHONTALES'),
    ('raccn', 'RACCN'),
    ('raccs', 'RACCS'),
    ('esteli', 'ESTELI'),
    ('granada', 'GRANADA'),
    ('jinotega', 'JINOTEGA'),
    ('leon', 'LEON'),
    ('madriz', 'MADRIZ'),
    ('managua', 'MANAGUA'),
    ('masaya', 'MASAYA'),
    ('matagalpa', 'MATAGALPA'),
    ('nueva segovia', 'NUEVA SEGOVIA'),
    ('rio san juan', 'RIO SAN JUAN'),
    ('rivas', 'RIVAS'),
)


# FUNCTION FOR THE RANDOM CODE FOR THE PRODUCTS
def random_code():
    code = random.randrange(100000, 999999, 6)
    return code
