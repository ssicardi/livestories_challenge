from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

from .models import Events

import io
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib

try:
    matplotlib.use("TKAgg")
except ModuleNotFoundError:
    matplotlib.use('Agg')


@csrf_exempt
def countEvent(request, event, count=1):
    t = timezone.now()
    if count == 1:
        Events.objects.create(event_type=event, date=t)
    else:
        events_list = [Events(event_type=event, date=t) for i in range(count)]
        Events.objects.bulk_create(events_list)


def getUniqueEvents(request):
    try:
        queryResult = list(Events.objects.values('event_type').annotate(count=Count('id')))

        jsonRes = {"result": [{"event": d["event_type"], "count": d["count"]} for d in queryResult]}

        return JsonResponse(jsonRes)
    except Exception as e:
        return JsonResponse({"error": str(e)})


def getEventsFromDates(request):
    try:
        start = datetime.strptime(request.GET['start_date'], "%Y%m%d%H")
        end = datetime.strptime(request.GET['end_date'], "%Y%m%d")

        # we add hours and minutes to END to assure we get the events from the day
        time_added = timedelta(hours=23, minutes=59, seconds=59)
        end += time_added

        querySet = Events.objects.filter(date__range=(start, end))
        queryResult = list(querySet.values('date__date', 'event_type'))

        jsonDict = {"result": [{"date": str(d["date__date"]), "event": d["event_type"], "count": d["count"]} for d in
                               queryResult]}

        return JsonResponse(jsonDict)
    except Exception as e:
        return JsonResponse({"error": str(e)})


def histogramFromDate(request, event, date):
    try:
        start = datetime.strptime(date, "%Y%m%d")
        time_added = timedelta(hours=23, minutes=59, seconds=59)
        end = start + time_added

        querySet = Events.objects.filter(date__range=(start, end), event_type=event).values()
        queryResult = list(querySet.values('date__hour').annotate(count=Count('id')))

        jsonDict = {"hour": [d["date__hour"] for d in queryResult], "count": [d["count"] for d in queryResult]}

        print(jsonDict)

        return generateImage(jsonDict, event, date)
    except Exception as e:
        return JsonResponse({"error": str(e)})


def generateImage(jsonDict, event, date):
    f = plt.figure()

    plt.bar(jsonDict["hour"], [x / sum(jsonDict["count"]) * 100 for x in jsonDict["count"]])

    plt.xlabel("Hour")
    plt.ylabel("Frecuency (%)")
    plt.xlim((0, 24))
    plt.ylim((0, 100))

    plt.title("Event: {} by hour on {}".format(event, date))
    time = [i for i in range(24)]
    plt.xticks(time, time)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    f.clear()
    response['Content-Length'] = str(len(response.content))

    return response
