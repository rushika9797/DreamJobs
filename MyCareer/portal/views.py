from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Job, Profile
from .forms import UserRegisterForm, JobForm, ApplicationForm
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Job, Application

def home(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'portal/home.html', {'jobs': jobs})
    
def register(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = form.cleaned_data["role"]
            profile.save()

            login(request, user)
            return redirect("dashboard")

    else:
        form = UserRegisterForm()

    return render(request, "portal/register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "portal/login.html", {"error": "Invalid credentials"})

    return render(request, "portal/login.html")

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user

    if user.profile.role == "employer":
        jobs = Job.objects.filter(employer=user)
        applied_jobs = {}
    else:
        jobs = Job.objects.all()
        user_applications = Application.objects.filter(applicant=user)
        applied_jobs = {app.job.id: app.status for app in user_applications}

    print("ROLE:", user.profile.role)
    print("APPLICATIONS:", applied_jobs)

    return render(request, "portal/dashboard.html", {
        "jobs": jobs,
        "applied_jobs": applied_jobs,
    })

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('dashboard')
    else:
        form = JobForm()

    return render(request, 'portal/post_job.html', {'form': form})



def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'portal/job_detail.html', {'job': job})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            print("APPLICATION SAVED ✅")
            return redirect('dashboard')
        else:
            print("FORM ERRORS ❌:", form.errors)  

    else:
        form = ApplicationForm()

    return render(request, 'portal/apply_job.html', {
        'form': form,
        'job': job
    })



@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)

    applicants = job.application_set.all()   # all applications

    return render(request, "portal/applicants.html",{
        'job': job,
        'applicants': applicants
    })

def approve_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    application.status = "approved"
    application.save()

    send_mail(
        subject="Application Approved 🎉",
        message=f"Congratulations! You are selected for {application.job.title}.",
        from_email=None,
        recipient_list=[application.applicant.email],
    )

    messages.success(request, "Applicant approved and email sent.")
    return redirect("view_applicants", application.job.id)

def reject_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    application.status = "rejected"
    application.save()

    send_mail(
        subject="Application Update",
        message=f"Sorry, you were not selected for {application.job.title}.",
        from_email=None,
        recipient_list=[application.applicant.email],
    )

    messages.info(request, "Applicant rejected and email sent.")
    return redirect("view_applicants", application.job.id)