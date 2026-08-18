from django.contrib import admin

from .models import Booking, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'session_type', 'duration', 'price')
    list_filter = ('session_type',)
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'date', 'time', 'mode', 'phone', 'price', 'status')
    list_filter = ('status', 'mode', 'date', 'service')
    search_fields = ('user__username', 'phone', 'service__name')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    list_editable = ('status',)
    actions = ['approve_bookings', 'reject_bookings', 'mark_completed']

    @admin.action(description='Approve selected sessions (set to Confirmed)')
    def approve_bookings(self, request, queryset):
        updated = queryset.update(status='Confirmed')
        self.message_user(request, f'{updated} session(s) confirmed.')

    @admin.action(description='Reject selected sessions (set to Cancelled)')
    def reject_bookings(self, request, queryset):
        updated = queryset.update(status='Cancelled')
        self.message_user(request, f'{updated} session(s) cancelled.')

    @admin.action(description='Mark selected sessions as Completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='Completed')
        self.message_user(request, f'{updated} session(s) marked completed.')
