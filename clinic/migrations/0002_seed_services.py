from django.db import migrations


def seed_services(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')

    services = [
        dict(name='Individual Therapy', icon='mind', session_type='individual',
             price=15000, duration=50,
             description='One-on-one sessions using evidence-based approaches like CBT to help you manage thoughts, emotions, and daily challenges.'),
        dict(name='Couples Counseling', icon='heart', session_type='couples',
             price=25000, duration=60,
             description='A safe space for partners to improve communication, rebuild trust, and reconnect.'),
        dict(name='Family Therapy', icon='family', session_type='family',
             price=30000, duration=75,
             description='Guided sessions to help families navigate conflict, transitions, and strengthen relationships.'),
        dict(name='Teen & Adolescent Therapy', icon='teen', session_type='individual',
             price=15000, duration=45,
             description='A supportive space for teens to work through school stress, identity, self-esteem, and relationships.'),
        dict(name='Grief Counseling', icon='grief', session_type='individual',
             price=15000, duration=50,
             description='Compassionate support for processing loss at your own pace, whenever you feel ready.'),
        dict(name='Anxiety & Stress Management', icon='stress', session_type='individual',
             price=15000, duration=50,
             description='Practical, evidence-based tools to help you manage anxiety, overwhelm, and everyday stress.'),
        dict(name='Trauma-Focused Therapy (EMDR)', icon='trauma', session_type='individual',
             price=20000, duration=60,
             description='Specialized trauma-informed care using EMDR techniques to help you process difficult experiences safely.'),
        dict(name='Mindfulness & Meditation Coaching', icon='mindfulness', session_type='individual',
             price=12000, duration=45,
             description='Learn practical mindfulness and meditation techniques to build calm, focus, and resilience.'),
        dict(name='Career & Life Coaching', icon='career', session_type='individual',
             price=18000, duration=50,
             description='Structured coaching to help you gain clarity on career transitions, goals, and life decisions.'),
        dict(name='Group Therapy Sessions', icon='group', session_type='group',
             price=8000, duration=90,
             description='Connect with others facing similar experiences in a supportive, therapist-led group setting.'),
    ]

    for s in services:
        Service.objects.get_or_create(name=s['name'], defaults=s)


def unseed_services(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    Service.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_services, unseed_services),
    ]
