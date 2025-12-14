import flet as ft

class StatusColors:
    PRESENT = "#22C55E"
    ABSENT = "#EF4444"
    LATE = "#F59E0B"
    LEAVE = "#64748B"

def get_light_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#2563EB",
            on_primary="#FFFFFF",
            primary_container="#DBEAFE",
            
            background="#F1F5F9",
            on_background="#0F172A",
            
            surface="#FFFFFF",
            on_surface="#1E293B",
            
            outline="#CBD5E1",
            
            error="#B91C1C",
            on_error="#FFFFFF",
        )
    )

def get_dark_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#60A5FA",
            on_primary="#0F172A",
            primary_container="#1E40AF",
            
            background="#0F172A",
            on_background="#F1F5F9",
            
            surface="#1E293B",
            on_surface="#F8FAFC",
            
            outline="#475569",
            
            error="#EF4444",
            on_error="#000000",
        )
    )