MEMBERSHIP_CHOICES = (
        ('None', 'None'),
        ('General', 'General'),
        ('Lifetime', 'Lifetime'),
        ('System', 'System')
    )

CLAIMANT_CHOICES = tuple(choice for choice in MEMBERSHIP_CHOICES if choice[0] not in ['None', 'System'])

ROLE_CHOICES = (
        ('None', 'None'),
        ('GS', 'General Secretary'),
        ('President', 'President'),
        ('EM', 'Executive Member'),
        ('VP', 'Vice President'),
)