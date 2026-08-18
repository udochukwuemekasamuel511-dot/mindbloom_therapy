# MindBloom Therapy — Scheduling App

A Django scheduling app for a therapist's practice, built on the same core logic as
the braiding-salon project: clients browse services, book sessions, view their own
bookings, and cancel them; the therapist manages everything from the Django admin.

Same architecture, different domain, different look — bright and calming instead of
the salon's dark/gold luxury theme, with original illustrated icons instead of photos.

## How to run

```bash
cd mindbloom_therapy
python3 -m venv venv && source venv/bin/activate    # optional but recommended
pip install django
python manage.py migrate      # also seeds 10 therapy services automatically
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## What's included

**Services (seeded automatically via migration):**
Individual Therapy, Couples Counseling, Family Therapy, Teen & Adolescent Therapy,
Grief Counseling, Anxiety & Stress Management, Trauma-Focused Therapy (EMDR),
Mindfulness & Meditation Coaching, Career & Life Coaching, Group Therapy Sessions.
Each has its own price, session length, and an original SVG icon (no external images
or photos used — everything is inline, hand-drawn illustration, so there's nothing to
break or fail to load).

**Client-facing:**
- Home page with a bright hero + 4 featured services
- Full service catalog with live search
- Booking form: phone, session mode (in person / virtual), date, time, notes
- Server-side validation: required fields, no past dates, and **double-booking
  prevention** — two clients can't book the exact same date+time slot. A cancelled
  slot frees back up automatically.
- Dashboard: view all your sessions with status, and **cancel any Pending or
  Confirmed session** (with a confirmation prompt) — cancelling is restricted to the
  session's own owner and only while it's still cancellable.
- Signup/login with field-level error messages.

**Admin (therapist side)** — visit `/admin/`:
- Bookings list with filters (status, mode, date, service), a date-hierarchy for a
  daily-schedule view, inline status editing, and bulk actions to Approve (Confirmed),
  Reject (Cancelled), or mark Completed.
- Services list to add/edit/remove offerings and pricing.

**Design differences from the braiding site (as requested):**
- Bright white/teal/mint palette instead of black/gold
- 'Quicksand' + 'Inter' fonts instead of 'Playfair Display' + 'Great Vibes'
- Original SVG illustrations per service instead of uploaded photos
- Session "mode" (in person / virtual) instead of hair-length price tiers, since that
  maps more naturally to how therapy sessions are actually offered

Everything was tested end-to-end (signup → book → duplicate-slot rejection → dashboard
→ cancel → slot-freed-for-another-client → cross-user permission check → logout)
before packaging, the same way the braiding-site fixes were verified.
