from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Access dictionary items safely in templates"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def get_summary(summaries, student):
    """
    Returns the GradeSummary for a specific student.
    Works with either a dict or a queryset.
    """
    # If dict with student IDs
    if isinstance(summaries, dict):
        return summaries.get(student.id)
    
    # If queryset
    try:
        return summaries.filter(student=student).first()
    except Exception:
        return None
    
@register.filter
def dict_get(d, key):
    return d.get(key)