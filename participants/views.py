from django.shortcuts import render

def participants(request):
    view_name = "participants"
    parameters = {}  # Index view doesn't have any parameters
    print(f"View Name: {view_name}")
    print(f"Parameters: {parameters}")
    return render(request, 'index.html', {'view_name': view_name, 'parameters': parameters})

def participant(request, participant_id):
    view_name = "participant"
    parameters = {'participant_id': participant_id}
    print(f"View Name: {view_name}")
    print(f"Parameters: {parameters}")
    return render(request, 'index.html', {'view_name': view_name, 'parameters': parameters})

