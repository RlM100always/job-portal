from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Job, Application, UserProfile
from .forms import UserRegistrationForm, JobForm, ApplicationForm, JobSearchForm

def home(request):
    """Home page with role-based redirection"""
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            if profile.role == 'employer':
                return redirect('jobs:employer_dashboard')
            else:
                return redirect('jobs:applicant_dashboard')
        except UserProfile.DoesNotExist:
            # Handle case where user doesn't have a profile
            return redirect('jobs:job_list')
    
    # Show recent jobs for non-authenticated users
    recent_jobs = Job.objects.all()[:6]
    return render(request, 'jobs/home.html', {'recent_jobs': recent_jobs})

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('jobs:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'jobs/register.html', {'form': form})

def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('jobs:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'jobs/login.html')

def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('jobs:home')

@login_required
def employer_dashboard(request):
    """Employer dashboard"""
    try:
        profile = request.user.userprofile
        if profile.role != 'employer':
            messages.error(request, 'Access denied. Employer account required.')
            return redirect('jobs:home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('jobs:home')
    
    # Get employer's jobs and recent applications
    my_jobs = Job.objects.filter(posted_by=request.user)[:5]
    recent_applications = Application.objects.filter(job__posted_by=request.user)[:5]
    
    context = {
        'my_jobs': my_jobs,
        'recent_applications': recent_applications,
        'total_jobs': Job.objects.filter(posted_by=request.user).count(),
        'total_applications': Application.objects.filter(job__posted_by=request.user).count(),
    }
    return render(request, 'jobs/employer_dashboard.html', context)

@login_required
def applicant_dashboard(request):
    """Applicant dashboard"""
    try:
        profile = request.user.userprofile
        if profile.role != 'applicant':
            messages.error(request, 'Access denied. Applicant account required.')
            return redirect('jobs:home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('jobs:home')
    
    # Get applicant's applications and recommended jobs
    my_applications = Application.objects.filter(applicant=request.user)[:5]
    recommended_jobs = Job.objects.exclude(
        id__in=Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)
    )[:5]
    
    context = {
        'my_applications': my_applications,
        'recommended_jobs': recommended_jobs,
        'total_applications': Application.objects.filter(applicant=request.user).count(),
    }
    return render(request, 'jobs/applicant_dashboard.html', context)

@login_required
def post_job(request):
    """Post a new job (employer only)"""
    try:
        profile = request.user.userprofile
        if profile.role != 'employer':
            messages.error(request, 'Access denied. Employer account required.')
            return redirect('jobs:home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('jobs:home')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:my_jobs')
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def my_jobs(request):
    """View employer's posted jobs"""
    try:
        profile = request.user.userprofile
        if profile.role != 'employer':
            messages.error(request, 'Access denied. Employer account required.')
            return redirect('jobs:home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('jobs:home')
    
    jobs = Job.objects.filter(posted_by=request.user)
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'jobs/my_jobs.html', {'page_obj': page_obj})

@login_required
def job_applicants(request, job_id):
    """View applicants for a specific job (employer only)"""
    try:
        profile = request.user.userprofile
        if profile.role != 'employer':
            messages.error(request, 'Access denied. Employer account required.')
            return redirect('jobs:home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('jobs:home')
    
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = Application.objects.filter(job=job)
    
    return render(request, 'jobs/job_applicants.html', {
        'job': job,
        'applications': applications
    })

def job_list(request):
    """List all jobs with search functionality"""
    form = JobSearchForm(request.GET)
    jobs = Job.objects.all()
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            jobs = jobs.filter(
                Q(title__icontains=search_query) |
                Q(company_name__icontains=search_query) |
                Q(location__icontains=search_query)
            )
    
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'jobs/job_list.html', {
        'page_obj': page_obj,
        'form': form
    })

def job_detail(request, job_id):
    """View job details"""
    job = get_object_or_404(Job, id=job_id)
    user_has_applied = False
    
    if request.user.is_authenticated:
        user_has_applied = Application.objects.filter(
            job=job, applicant=request.user
        ).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'user_has_applied': user_has_applied
    })

@login_required
def apply_job(request, job_id):
    """Apply for a job (applicant only)"""
    try:
        profile = request.user.userprofile
        if profile.role != 'applicant':
            messages.error(request, 'Access denied. Applicant account required.')
            return redirect('jobs:home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('jobs:home')
    
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user has already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('jobs:job_detail', job_id=job_id)
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/apply_job.html', {
        'form': form,
        'job': job
    })

@login_required
def my_applications(request):
    """View applicant's submitted applications"""
    try:
        profile = request.user.userprofile
        if profile.role != 'applicant':
            messages.error(request, 'Access denied. Applicant account required.')
            return redirect('jobs:home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('jobs:home')
    
    applications = Application.objects.filter(applicant=request.user)
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'jobs/my_applications.html', {'page_obj': page_obj})

