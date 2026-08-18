from .models import People


def people_navigation(request):
    people = People.objects.all()

    return {
        "has_people": people.exists(),

        "has_principal_consultants": people.filter(
            rank__iexact="principal_consultants"
        ).exists(),

        "has_senior_consultants": people.filter(
            rank__iexact="senior_consultants"
        ).exists(),

        "has_consultants": people.filter(
            rank__iexact="consultant"
        ).exists(),

        "has_senior_professionals": people.filter(
            rank__iexact="senior_professionals"
        ).exists(),

        "has_professionals": people.filter(
            rank__iexact="professional"
        ).exists(),

        "has_assistant_professionals": people.filter(
            rank__iexact="assistant_professionals"
        ).exists(),

        "has_support_team": people.filter(
            rank__iexact="support_team"
        ).exists(),

        "has_service_personnel": people.filter(
            rank__iexact="service_personnel"
        ).exists(),
    }
