import gc
import sys
import uuid
from datetime import datetime, timedelta
from decimal import Decimal, DivisionByZero

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db.transaction import atomic

from ticket.models import Ticket


class Command(BaseCommand):
    help = "Re-Generate ticket token"

    PROGRESS_BAR_LENTH = 30
    CHUNKSIZE = 50
    HASH = '#'
    SPACE = ' '

    def add_arguments(self, parser):
        ""
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        ""
        start_time = datetime.now()
        total_tickets = Ticket.objects.filter(is_regenerate=False).count()
        self.update_progress(0, total_tickets, start_time)
        for i in range(20000):
            tickets = Ticket.objects.filter(is_regenerate=False).order_by("-id")[: self.CHUNKSIZE]

            for index, ticket in enumerate(tickets):
                with atomic():
                    try:
                        _uuid = self._get_random_uuid4()
                        ticket.token = _uuid
                        ticket.is_regenerate = True
                        ticket.save()
                    except IntegrityError:
                        _uuid = self._get_random_uuid4()
                        while Ticket.objects.filter(token=_uuid).exists():
                            _uuid = self._get_random_uuid4()
                        ticket.token = _uuid
                        ticket.is_regenerate = True
                        ticket.save()

                gc.collect()
                self.update_progress(i * 50 + index + 1, total_tickets, start_time)

    def _get_random_uuid4(self):
        return uuid.uuid4()

    def update_progress(self, current_value, target_value, start_time):
        ""
        percent = Decimal(current_value) / Decimal(target_value)
        hashes = self.HASH * int(round(percent * self.PROGRESS_BAR_LENTH))
        spaces = self.SPACE * (self.PROGRESS_BAR_LENTH - len(hashes))

        elapsed_time = datetime.now() - start_time
        try:
            total_seconds = Decimal(elapsed_time.total_seconds() or 1) / percent
            remaining_time = timedelta(
                seconds=max(int(total_seconds) - elapsed_time.total_seconds(), 0)
            )
        except DivisionByZero:
            remaining_time = '--'
        sys.stdout.write(
            f'\rProgress: [{hashes + spaces}] {int(round(percent * 100))}% {current_value}/{target_value} remaining: {remaining_time} elapsed_time: {elapsed_time}     '
        )
        sys.stdout.flush()
