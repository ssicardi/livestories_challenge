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
    matplotlib.use('Agg')
except ModuleNotFoundError:
    matplotlib.use("TKAgg")


@csrf_exempt
def countEvent(request, event, count=1):
    t = timezone.now()
    if count == 1:
        Events.objects.create(event_type=event, date=t)
    else:
        events_list = [Events(event_type=event, date=t) for i in range(count)]
        Events.objects.bulk_create(events_list)
    return HttpResponse('')


def getUniqueEvents(request):
    queryResult = list(Events.objects.values('event_type').annotate(count=Count('id')))

    jsonRes = {"result": [{"event": d["event_type"], "count": d["count"]} for d in queryResult]}

    return JsonResponse(jsonRes)


def getEventsFromDates(request):
    start, error_start = parseDate(request.GET['start_date'], "%Y%m%d%H")

    if (error_start):
        return JsonResponse(error_start)

    end, error_end = parseDate(request.GET['end_date'], "%Y%m%d")

    if (error_end):
        return JsonResponse(error_end)

    # we add hours and minutes to END to assure we get the events from the day
    time_added = timedelta(hours=23, minutes=59, seconds=59)
    end += time_added

    querySet = Events.objects.filter(date__range=(start, end))
    queryResult = list(querySet.values('date__date', 'event_type').annotate(count=Count('id')))

    jsonDict = {"result": [{"date": str(d["date__date"]), "event": d["event_type"], "count": d["count"]} for d in
                           queryResult]}

    return JsonResponse(jsonDict)


def histogramFromDate(request, event, date):
    start, error = parseDate(date, "%Y%m%d")

    if (error):
        return JsonResponse(error)

    time_added = timedelta(hours=23, minutes=59, seconds=59)
    end = start + time_added

    querySet = Events.objects.filter(date__range=(start, end), event_type=event).values()
    queryResult = list(querySet.values('date__hour').annotate(count=Count('id')))

    jsonDict = {"hour": [d["date__hour"] for d in queryResult], "count": [d["count"] for d in queryResult]}

    print(jsonDict)

    return generateImage(jsonDict, event, date)


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

def parseDate(date_string, date_format):
    try:
        return datetime.strptime(date_string, date_format), {}
    except Exception as e:
        return None, {"Error": "Incorrect date format"}













