"""Billing — build an invoice total. (Sample file, just here to be explored.)"""
from shared.constants import TAX_LABEL


def line_total(qty, price):
    return qty * price


def invoice_total(lines, tax_rate):
    subtotal = sum(line_total(q, p) for q, p in lines)
    return subtotal + subtotal * tax_rate
