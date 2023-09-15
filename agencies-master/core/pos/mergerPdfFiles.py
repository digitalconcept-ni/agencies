import os
from datetime import datetime, timedelta
from PyPDF2 import PdfMerger, PdfReader
from config import settings


def mergerPdf(directorySchema):
    try:
        data = {}
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        dirname = directorySchema
        # dirname = os.path.join(settings.MEDIA_ROOT, 'merger')
        invoice = dirname + '/invoices.pdf'
        guide = dirname + '/guide.pdf'
        finalName = 'guia-facturas-' + str(today) + '.pdf'
        beforeGuide = dirname + '/guia-facturas-' + str(yesterday) + '.pdf'

        # REMOVE GUIDE AND INVOICES FROM THE PREVIOUS DAY
        if os.path.exists(beforeGuide): os.remove(beforeGuide)

        readerGuide = PdfReader(guide)
        readerInvoice = PdfReader(invoice)

        merger = PdfMerger()
        merger.append(readerGuide)
        merger.append(readerInvoice)
        with open(os.path.join(dirname, finalName), 'wb') as f:
            merger.write(f)
            merger.close()
        # FINAL PATH WHERE THE FILE IS STORAGE
        data['path'] = os.path.join(dirname, finalName)
    except Exception as e:
        data['error'] = str(e)
    return data
