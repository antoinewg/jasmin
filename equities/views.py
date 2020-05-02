from django.shortcuts import render
from django.http import HttpResponse

from equities.models import Company


def index(request):
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
        {
            "category": "company news",
            "datetime": 1588446372,
            "headline": "UPDATE 1-Millicom backs out of $570 mln deal for Telefonica's Costa Rica unit",
            "id": 4164242,
            "image": "https://s3.reutersmedia.net/resources/r/?m=02\u0026d=20200502\u0026t=2\u0026i=1517267164\u0026w=1200\u0026r=LYNXMPEG410J5",
            "related": "",
            "source": "Reuters",
            "summary": "Millicom International Cellular\nsaid on Saturday it would back out of a $570\nmillion deal to buy Telefonica's Costa Rican business,\ncreating a headache for the Spanish company as it looks to\nsharpen its focus on core markets in Europe and Brazil.",
            "url": "https://www.reuters.com/article/us-millicom-telefonica-deal/millicom-backs-out-of-570-million-deal-for-telefonicas-costa-rica-unit-idUSKBN22E0NM",
        },
    ]
    return render(request, "index.html", locals())


def stocks(request):
    stocks = Company.objects.all()
    return render(request, "stocks.html", locals())
