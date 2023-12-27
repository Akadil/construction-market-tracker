from django.shortcuts import render

def projects(request):
    view_name = "index"
    parameters = {}  # Index view doesn't have any parameters
    print(f"View Name: {view_name}")
    print(f"Parameters: {parameters}")
    return render(request, 'index.html', {'view_name': view_name, 'parameters': parameters})

def project(request, project_id):
    view_name = "project"
    parameters = {'project_id': project_id}
    print(f"View Name: {view_name}")
    print(f"Parameters: {parameters}")
    return render(request, 'index.html', {'view_name': view_name, 'parameters': parameters})

