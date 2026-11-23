from django.contrib import admin, messages
from django.utils import timezone

from .models import (
    AdmissionCycle,
    Course,
    CourseRequirement,
    Faculty,
    Institution,
    Origin,
    Source,
    Subject,
    VerificationStatus,
)


class ProvenanceAdmin(admin.ModelAdmin):
    """Base comum: mostra a proveniência e mantém a verificação coerente."""

    list_filter = ("origin", "verification_status")
    readonly_fields = ("verified_on",)
    actions = ("mark_verified", "mark_unverified")

    def save_model(self, request, obj, form, change):
        if obj.verification_status == VerificationStatus.VERIFIED:
            obj.verified_on = obj.verified_on or timezone.localdate()
        else:
            obj.verified_on = None
        super().save_model(request, obj, form, change)

    @admin.action(description="Marcar como verificado")
    def mark_verified(self, request, queryset):
        selected = queryset.count()
        updated = queryset.filter(origin=Origin.OFFICIAL, source__isnull=False).update(
            verification_status=VerificationStatus.VERIFIED, verified_on=timezone.localdate()
        )
        ignored = selected - updated
        if updated:
            self.message_user(
                request, f"{updated} registo(s) marcado(s) como verificado(s).", messages.SUCCESS
            )
        if ignored:
            self.message_user(
                request,
                f"{ignored} registo(s) ignorado(s): só os dados oficiais com fonte "
                "podem ser verificados.",
                messages.WARNING,
            )

    @admin.action(description="Marcar como por verificar")
    def mark_unverified(self, request, queryset):
        updated = queryset.update(
            verification_status=VerificationStatus.UNVERIFIED, verified_on=None
        )
        self.message_user(
            request, f"{updated} registo(s) marcado(s) como por verificar.", messages.SUCCESS
        )


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "published_on", "retrieved_on")
    list_filter = ("kind",)
    search_fields = ("title",)


@admin.register(Institution)
class InstitutionAdmin(ProvenanceAdmin):
    list_display = ("name", "acronym", "origin", "verification_status")
    search_fields = ("name", "acronym")


@admin.register(Faculty)
class FacultyAdmin(ProvenanceAdmin):
    list_display = ("name", "institution", "origin", "verification_status")
    list_filter = (*ProvenanceAdmin.list_filter, "institution")
    list_select_related = ("institution",)
    search_fields = ("name", "institution__name")


@admin.register(Course)
class CourseAdmin(ProvenanceAdmin):
    list_display = ("name", "faculty", "origin", "verification_status")
    list_select_related = ("faculty",)
    search_fields = ("name", "faculty__name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(AdmissionCycle)
class AdmissionCycleAdmin(ProvenanceAdmin):
    list_display = ("institution", "academic_year", "origin", "verification_status")
    list_filter = (*ProvenanceAdmin.list_filter, "academic_year")
    list_select_related = ("institution",)
    search_fields = ("institution__name", "academic_year")


@admin.register(CourseRequirement)
class CourseRequirementAdmin(ProvenanceAdmin):
    list_display = (
        "admission_cycle",
        "course",
        "subject",
        "weight",
        "origin",
        "verification_status",
    )
    list_filter = (*ProvenanceAdmin.list_filter, "subject")
    list_select_related = ("admission_cycle__institution", "course", "subject")
    autocomplete_fields = ("admission_cycle", "course", "subject")
