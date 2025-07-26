from django.contrib import admin
from .models import UserProfile, Job, Application

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'get_full_name', 'get_email']
    list_filter = ['role']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'location', 'posted_by', 'created_at', 'get_applications_count']
    list_filter = ['created_at', 'location', 'company_name']
    search_fields = ['title', 'company_name', 'location', 'posted_by__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def get_applications_count(self, obj):
        return obj.applications.count()
    get_applications_count.short_description = 'Applications'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_applicant_name', 'get_job_title', 'get_company_name', 'applied_at', 'get_applicant_email']
    list_filter = ['applied_at', 'job__company_name']
    search_fields = ['applicant__username', 'applicant__first_name', 'applicant__last_name', 
                    'job__title', 'job__company_name']
    date_hierarchy = 'applied_at'
    ordering = ['-applied_at']
    
    def get_applicant_name(self, obj):
        return f"{obj.applicant.first_name} {obj.applicant.last_name}"
    get_applicant_name.short_description = 'Applicant'
    
    def get_job_title(self, obj):
        return obj.job.title
    get_job_title.short_description = 'Job Title'
    
    def get_company_name(self, obj):
        return obj.job.company_name
    get_company_name.short_description = 'Company'
    
    def get_applicant_email(self, obj):
        return obj.applicant.email
    get_applicant_email.short_description = 'Email'

# Customize admin site header and title
admin.site.site_header = "Job Portal Administration"
admin.site.site_title = "Job Portal Admin"
admin.site.index_title = "Welcome to Job Portal Administration"

