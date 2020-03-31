from django import template

register = template.Library()

@register.filter(name = "replace")
def replace(value, repstring):
    return value.replace(repstring[0], repstring[1])

@register.filter(name = "divide")
def divide(value, divider):
    return value/divider

@register.filter(name = "fulldivide")
def fulldivide(value, divider):
    return value//divider

@register.filter(name = "SmoothWeekTest")
def SmoothWeekTest(value, profit):
    return (value+profit)/7

@register.filter(name = "RawWeekTest")
def RawWeekTest(value, profit):
    return (value+profit)//7