{
    'name': 'Meter Reading on Invoice',
    'version': '16.0.1.0.0',
    'summary': 'Adds Previous, New, and Actual meter readings to invoice lines',
    'depends': ['account'],
    'data': [
        'views/invoice_view.xml',
    ],
    'installable': True,
    'application': False,
}