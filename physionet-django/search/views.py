import pdb

from django.shortcuts import render, redirect, reverse

from . import forms
from project.models import PublishedProject, PublishedTopic


def google_custom_search(request):
    """
    Page for performing google custom search on the site
    """
    return render(request, 'search/google_custom_search.html')


def redirect_google_custom_search(request):
    """
    Used to redirect queries from the navbar search to the main google
    search page

    """
    return redirect(reverse('google_custom_search') + '?q={}'.format(request.GET['query']))


def topic_search(request):
    """
    Search published projects by topic keyword

    Search with form submission or direct url
    """
    topic, valid_search, projects = '', False, None
    # If we get a form submission, redirect to generate the querystring
    # in the url
    if 'topic' in request.GET:
        form = forms.TopicSearchForm(request.GET)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            valid_search = True
        projects = PublishedProject.objects.filter(topics__description=topic)
    else:
        form = forms.TopicSearchForm()

    return render(request, 'search/topic_search.html', {'topic':topic,
        'projects':projects, 'form':form, 'valid_search':valid_search})


def all_topics(request):
    """
    Show all topics contained in PhysioNet

    """
    topics = PublishedTopic.objects.all().order_by('-project_count')

    return render(request, 'search/all_topics.html', {'topics':topics})


def get_content(resource_type, orderby, direction):
    """
    Helper function to get content shown on a resource listing page
    """
    if resource_type is None:
        published_projects = PublishedProject.objects.all()
    else:
        published_projects = PublishedProject.objects.filter(
            resource_type=resource_type)

    direction = '-' if direction == 'desc' else ''

    order_string = '{}{}'.format(direction, orderby)
    published_projects = published_projects.order_by(order_string)

    authors = [p.authors.all() for p in published_projects]
    topics = [p.topics.all() for p in published_projects]
    projects_authors_topics = zip(published_projects, authors, topics)

    return projects_authors_topics


def content_index(request, resource_type=None):
    """
    List of all published resources
    """
    LABELS = {None:['Content', 'projects'], 0:['Database', 'databases'],
        1:['Software', 'software']}
    main_label, plural_label = LABELS[resource_type]

    orderby, direction = 'publish_datetime', 'desc'
    form = forms.ProjectOrderForm()

    if 'orderby' in request.GET or 'direction' in request.GET:
        form = forms.ProjectOrderForm(request.GET)
        if form.is_valid():
            orderby, direction = [form.cleaned_data[item] for item in ['orderby', 'direction']]
        projects_authors_topics = get_content(resource_type=resource_type,
            orderby=orderby, direction=direction)
    else:
        projects_authors_topics = get_content(resource_type=resource_type,
            orderby=orderby, direction=direction)

    return render(request, 'search/content_index.html', {'form':form,
        'projects_authors_topics':projects_authors_topics,
        'main_label':main_label, 'plural_label':plural_label})


def database_index(request):
    """
    List of published databases
    """
    return content_index(request, resource_type=0)


def software_index(request):
    """
    List of published software
    """
    return content_index(request, resource_type=1)


def charts(request):
    """
    Chart statistics about published projects
    """
    resource_type = None

    if 'resource_type' in request.GET and request.GET['resource_type'] in ['0', '1']:
        resource_type = int(request.GET['resource_type'])

    LABELS = {None:['Content', 'Projects'], 0:['Database', 'Databases'],
        1:['Software', 'Software Projects']}

    main_label, plural_label = LABELS[resource_type]
    return render(request, 'search/charts.html', {
        'resource_type':resource_type,
        'main_label':main_label, 'plural_label':plural_label})