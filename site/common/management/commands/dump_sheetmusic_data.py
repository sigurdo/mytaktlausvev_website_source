from json import dumps

from django.core.management.base import BaseCommand

from sheetmusic.models import InstrumentType, Part, Pdf, Score


class Command(BaseCommand):
    def handle(self, **options):
        scores = [
            {
                "title": score.title,
                "pdfs": [
                    {
                        "url": f"https://taktlaus.no/{pdf.file.url}",
                        "parts": [
                            {
                                "instrument_type_pk": part.instrument_type.pk,
                                "part_number": part.part_number,
                                "note": part.note,
                                "from_page": part.from_page,
                                "to_page": part.to_page,
                            }
                            for part in Part.objects.filter(pdf=pdf)
                        ],
                    }
                    for pdf in Pdf.objects.filter(score=score)
                ],
            }
            for score in Score.objects.all()
        ]
        instrument_types = [
            {
                "pk": instrument_type.pk,
                "name": instrument_type.name,
            }
            for instrument_type in InstrumentType.objects.all()
        ]
        sheetmusic_dump = {
            "scores": scores,
            "instrument_types": instrument_types,
        }
        example = {
            "scores": [
                {
                    "title": "Score title",
                    "pdfs": [
                        {
                            "url": "https://taktlaus.no/path/to.pdf",
                            "parts": [
                                {
                                    "instrument_type_pk": 42,
                                    "part_number": 1,
                                    "note": "Bass Clef",
                                    "from_page": 5,
                                    "to_page": 6,
                                }
                            ],
                        }
                    ],
                }
            ],
            "instrument_types": [
                {
                    "pk": 42,
                    "name": "Instrument name",
                }
            ],
        }
        print("Sheetmusic data dump:")
        print(dumps(sheetmusic_dump))
        print()
        print("Indented example to show data format:")
        print(dumps(example, indent=4))
