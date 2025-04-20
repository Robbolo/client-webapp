from .notification_rules import (
    notify_clients_not_contacted_weekly,
    notify_clients_not_contacted_monthly,
    notify_clients_low_sessions,
    notify_clients_no_sessions_left,
)

def run_all_notification_checks():
    notify_clients_not_contacted_weekly()
    notify_clients_not_contacted_monthly()
    notify_clients_low_sessions(),
    notify_clients_no_sessions_left(),