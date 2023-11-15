from datetime import datetime

from django.db.models import Q

from core.pos.models import Client


def visitFrequency(request):
    try:
        today = datetime.today().strftime('%A')[:3].lower()
        if request.user.is_superuser:
            query = Client.objects.select_related().filter(is_active=True)
        else:
            query = Client.objects.select_related().filter(Q(is_active=True) & Q(user_id=request.user.id))

        if today == 'mon':
            queryFilter = query.filter(Q(frequent=True) | Q(mon=True))
        elif today == 'tue':
            queryFilter = query.filter(Q(frequent=True) | Q(tue=True))
        elif today == 'wed':
            queryFilter = query.filter(Q(frequent=True) | Q(wed=True))
        elif today == 'thu':
            queryFilter = query.filter(Q(frequent=True) | Q(thu=True))
        elif today == 'fri':
            queryFilter = query.filter(Q(frequent=True) | Q(fri=True))
        elif today == 'sat':
            queryFilter = query.filter(Q(frequent=True) | Q(sat=True))
        else:
            queryFilter = query
    except Exception as e:
        data = {'error': str(e)}
        return data
    return queryFilter


# def visitFrequencyWeek(request):
#     try:
#         today = datetime.today().strftime('%A')[:3].lower()
#         if request.user.is_superuser:
#             query = Client.objects.select_related().filter(is_active=True)
#         else:
#             query = Client.objects.select_related().filter(Q(is_active=True) & Q(user_id=request.user.id))
#
#         if today == 'mon':
#             queryFilter = query.filter(Q(frequent=True) | Q(mon=True))
#         elif today == 'tue':
#             queryFilter = query.filter(Q(frequent=True) | Q(tue=True))
#         elif today == 'wed':
#             queryFilter = query.filter(Q(frequent=True) | Q(wed=True))
#         elif today == 'thu':
#             queryFilter = query.filter(Q(frequent=True) | Q(thu=True))
#         elif today == 'fri':
#             queryFilter = query.filter(Q(frequent=True) | Q(fri=True))
#         elif today == 'sat':
#             queryFilter = query.filter(Q(frequent=True) | Q(sat=True))
#         else:
#             queryFilter = query
#     except Exception as e:
#         data = {'error': str(e)}
#         return data
#     return queryFilter
