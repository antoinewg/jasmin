from django.shortcuts import render
from django.http import HttpResponse

from equities import models
from equities.api import endpoints


def gaps(request):
    gaps = models.Gap.objects.all().order_by("-percent")
    return render(request, "pages/gaps.html", locals())


def index(request):
    gaps = models.Gap.objects.all()
    alerts = models.Alert.objects.all()
    newslist = [
        {
            "category": "top news",
            "datetime": 1588450920,
            "headline": "Tara Reade did not say sexual harassment or assault in complaint supposedly filed against Biden",
            "id": 4169188,
            "image": "https://image.cnbcfm.com/api/v1/image/106446200-1584374507008gettyimages-1206480761.jpeg?v=1584374553",
            "related": "",
            "source": "CNBC",
            "summary": "Tara Reade, the former Senate staffer who alleges Joe Biden sexually assaulted her 27 years ago, says she filed a limited report with a congressional personnel office that did not explicitly accuse him of sexual assault or harassment.",
            "url": "https://www.cnbc.com/2020/05/02/tara-reade-did-not-mention-sexual-harassment-or-assault-in-biden-complaint.html",
        },
        {
            "category": "top news",
            "datetime": 1588450236,
            "headline": "Berkshire Hathaway annual meeting live updates: Warren Buffett to address coronavirus, stock losses",
            "id": 4167848,
            "image": "https://image.cnbcfm.com/api/v1/image/105758393-15511059379711u8a9300.jpg?v=1557141979",
            "related": "",
            "source": "CNBC",
            "summary": "Follow the highlights of Berkshire Hathaway's annual meeting here. Warren Buffett is set to comment on the coronavirus, the state of the American economy and whether he sees any value in the sell-off.",
            "url": "https://www.cnbc.com/2020/05/02/warren-buffett-berkshire-hathaway-annual-meeting-live-updates.html",
        },
        {
            "category": "company news",
            "datetime": 1588449855,
            "headline": "Tesla applies to become UK electricity provider - The Telegraph",
            "id": 4172069,
            "image": "https://s4.reutersmedia.net/resources_v2/images/rcom-default.png",
            "related": "",
            "source": "Reuters",
            "summary": "U.S. electric carmaker Tesla Inc\nhas applied for a licence to supply electricity in the United\nKingdom, The Telegraph reported on Saturday.",
            "url": "https://www.reuters.com/article/tesla-licence/tesla-applies-to-become-uk-electricity-provider-the-telegraph-idUSL8N2CK0J8",
        },
        {
            "category": "company news",
            "datetime": 1588449855,
            "headline": "Tesla applies to become UK electricity provider - The Telegraph",
            "id": 4167847,
            "image": "https://s2.reutersmedia.net/resources/r/?m=02\u0026d=20200502\u0026t=2\u0026i=1517269540\u0026w=1200\u0026r=LYNXMPEG410K4",
            "related": "",
            "source": "Reuters",
            "summary": "U.S. electric carmaker Tesla Inc\nhas applied for a licence to supply electricity in the United\nKingdom, The Telegraph reported on Saturday.",
            "url": "https://www.reuters.com/article/us-tesla-licence/tesla-applies-to-become-uk-electricity-provider-the-telegraph-idUSKBN22E0SL",
        },
    ]
    return render(request, "pages/index.html", locals())


def alerts(request):
    alerts = models.Alert.objects.all()
    return render(request, "pages/alerts.html", locals())


def news(request):
    newslist = endpoints.fetch_news()
    return render(request, "pages/news.html", locals())
