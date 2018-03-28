import csv
from ticket.models import Ticket
from django.contrib.auth.models import User

def export(csv_file):
    with open(csv_file, 'rb') as file:
        reader = csv.reader(file)
        for row in reader:
            print row
            ticket = Ticket.objects.create(
                ticket_type=1,
                title=str(row[1]),
                description=str(row[2]),
                due_date=row[0],
                status=1
            )
            users = row[3].split(",")
            for user in users:
                user.replace(" ", "")
                user, created = User.objects.get_or_create(username=user.lower())
                ticket.assigned_to.add(user)
                ticket.save()