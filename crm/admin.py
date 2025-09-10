from django.contrib import admin
from crm.models import Customer, Product, Deal, Pipeline, DealStage, Task, TaskType


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    search_fields = ('first_name', 'last_name', 'national_code', 'phone_number')
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'stage')
    search_fields = ('title',)
    list_filter = ('stage',)


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DealStage)
class DealStageAdmin(admin.ModelAdmin):
    list_display = ('name', 'pipeline', 'order')
    search_fields = ('name',)
    list_filter = ('pipeline',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'due_date', 'assigned_to')
    search_fields = ('title',)
    list_filter = ('completed', 'due_date')


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


