import django_filters

from datetime import datetime, timedelta
from django.db.models import Q

from collections import Counter
from django.db.models import Func
from django_filters.rest_framework import FilterSet
from ninetofiver import models
from ninetofiver.utils import merge_dicts
from rest_framework import generics

from django.contrib.auth import models as auth_models
from django.core.exceptions import ValidationError


class IsNull(Func):
    template = '%(expressions)s IS NULL'


class NullLastOrderingFilter(django_filters.OrderingFilter):
    """An ordering filter which places records with fields containing null values last."""

    def filter(self, qs, value):
        """Execute the filter."""
        if value in django_filters.filters.EMPTY_VALUES:
            return qs

        ordering = []
        for param in value:
            if param[0] == '-':
                cleaned_param = param.lstrip('-')
                order = self.param_map[cleaned_param]

                if type(order) is dict:
                    order['order'] = '-%s' % order['order']
                    ordering.append(order)
                    continue

            ordering.append(self.get_ordering_value(param))

        # ordering = [self.get_ordering_value(param) for param in value]
        final_ordering = []

        for order in ordering:
            if type(order) is dict:
                if order.get('annotate', None):
                    qs = qs.annotate(**order['annotate'])

                if order.get('order', None):
                    order = order['order']
                else:
                    continue

            # field = order.lstrip('-')
            # null_field = '%s_isnull' % field
            # params = {null_field: IsNull(field)}
            # qs = qs.annotate(**params)
            #
            # final_ordering.append(null_field)
            final_ordering.append(order)

        qs = qs.order_by(*final_ordering)

        return qs


class UserFilter(FilterSet):    
    
    # Custom method to see if user is active on specific day
    def filter_active_day(self, queryset, name, value):
        fl = 'gt' if value else 'lte'
    
        lookup = '__'.join(['employmentcontract', 'work_schedule', name, fl])
        return queryset.filter(**{lookup: 0})


    employmentcontract_type = django_filters.CharFilter(name='employmentcontract__employment_contract_type__label')
    workschedule_label = django_filters.CharFilter(name='employmentcontract__work_schedule__label')
    workschedule_label__contains = django_filters.CharFilter(name='employmentcontract__work_schedule__label', lookup_expr='contains')
    workschedule_label__icontains = django_filters.CharFilter(name='employmentcontract__work_schedule__label', lookup_expr='icontains')

    active_monday = django_filters.BooleanFilter(name='monday', method='filter_active_day')
    active_tuesday = django_filters.BooleanFilter(name='tuesday', method='filter_active_day')
    active_wednesday = django_filters.BooleanFilter(name='wednesday', method='filter_active_day')
    active_thursday = django_filters.BooleanFilter(name='thursday', method='filter_active_day')
    active_friday = django_filters.BooleanFilter(name='friday', method='filter_active_day')
    active_saturday = django_filters.BooleanFilter(name='saturday', method='filter_active_day')
    active_sunday = django_filters.BooleanFilter(name='sunday', method='filter_active_day')

    order_fields = ('username', 'email', 'first_name', 'last_name', 'groups', 'userrelative__name', 
        'userinfo__gender', 'userinfo__country', 'userinfo__birth_date', 'employmentcontract__started_at',
        'employmentcontract__ended_at', 'employmentcontract__company__name', 'employmentcontract__work_schedule__label',
        'employmentcontract__employment_contract_type__label', 'leave__leavedate__starts_at', 'leave__leavedate__ends_at',
        'active_monday', 'active_tuesday', 'active_wednesday', 'active_thursday', 'active_friday',
        'active_saturday', 'active_sunday', 'userinfo__join_date')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:

        model = auth_models.User
        fields = {
            # Basic user fields
            'username': ['exact', ],
            'email': ['exact', ],
            'first_name': ['exact', 'contains', 'icontains', ],
            'last_name': ['exact', 'contains', 'icontains', ],
            'is_active': ['exact', ],

            # AuthGroups fields
            'groups': ['exact', 'contains', 'icontains', ],

            # Userrelative fields
            'userrelative__name': ['exact', 'contains', 'icontains', ],

            # Userinfo fields
            'userinfo__gender': ['iexact', ],
            'userinfo__country': ['iexact', ],
            'userinfo__birth_date': ['exact', 'year__gt', 'year__gte', 'year__lt', 'year__lte', ],
            'userinfo__join_date': ['exact', 'year__gt', 'year__gte', 'year__lt', 'year__lte', ],

            # Employmentcontract fields
            'employmentcontract__started_at': ['exact', 'year__gt', 'year__gte', 'year__lt', 'year__lte', ],
            'employmentcontract__ended_at': ['exact', 'year__gt', 'year__gte', 'year__lt', 'year__lte'],
            'employmentcontract__company__name': ['exact', 'contains', 'icontains', ],

            # Check if user is on leave
            'leave__leavedate__starts_at': ['lte'],
            'leave__leavedate__ends_at': ['gte'],
        }


class CompanyFilter(FilterSet):
    order_fields = ('name', 'country', 'vat_identification_number', 'address', 'internal')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.Company
        fields = {
            'name': ['exact', 'contains', 'icontains'],
            'country': ['exact'],
            'vat_identification_number': ['exact', 'contains', 'icontains'],
            'address': ['exact', 'contains', 'icontains'],
            'internal': ['exact'],
        }


class EmploymentContractTypeFilter(FilterSet):
    order_fields = ('label',)
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.EmploymentContractType
        fields = {
            'label': ['exact', 'contains', 'icontains'],
        }


class EmploymentContractFilter(FilterSet):
    order_fields = ('started_at', 'ended_at')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.EmploymentContract
        fields = {
            'started_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'ended_at': ['exact', 'gt', 'gte', 'lt', 'lte', 'isnull'],
            'user': ['exact'],

        }


class WorkScheduleFilter(FilterSet):
    order_fields = ('label',)
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.WorkSchedule
        fields = {
            'label': ['exact', 'contains', 'icontains'],
        }


class UserRelativeFilter(FilterSet):
    order_fields = ('name', 'relation', 'birth_date', 'gender')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.UserRelative
        fields = {
            'name': ['exact', 'contains', 'icontains'],
            'relation': ['exact', 'contains', 'icontains'],
            'birth_date': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'gender': ['exact'],
            'user__username': ['exact', ],
            'user__first_name': ['exact', 'contains', 'icontains', ],
            'user__last_name': ['exact', 'contains', 'icontains', ],
        }


class AttachmentFilter(FilterSet):
    order_fields = ('label', 'description')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.Attachment
        fields = {
            'label': ['exact', 'contains', 'icontains'],
            'description': ['exact', 'contains', 'icontains'],
        }


class HolidayFilter(FilterSet):
    order_fields = ('name', 'date', 'country')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.Holiday
        fields = {
            'name': ['exact', 'contains', 'icontains'],
            'date': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'country': ['exact'],
        }


class LeaveTypeFilter(FilterSet):
    order_fields = ('label',)
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.LeaveType
        fields = {
            'label': ['exact', 'contains', 'icontains'],
        }


class LeaveFilter(FilterSet):

    def leavedate_range_distinct(self, queryset, name, value):
        """Filters distinct leavedates between a given range."""
        
        # Validate input.
        try:
            # Split value.
            values = value.split(',')
            start_date = datetime.strptime(values[0], "%Y-%m-%dT%H:%M:%S")
            end_date = datetime.strptime(values[1], "%Y-%m-%dT%H:%M:%S")
        except:
            # Raise validation error.
            raise ValidationError('Datetimes have to be in the correct \'YYYY-MM-DDTHH:mm:ss\' format.')

        # Filter distinct using range.
        return queryset.filter(leavedate__starts_at__range=(start_date, end_date)).distinct()


    def leavedate_upcoming_distinct(self, queryset, name, value):
        """Filters distinct leavedates happening after provided date."""

        #Validate input
        try:
            #Convert input into values
            base_date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            #Raise validationerror
            raise ValidationError('Datetime has to be in the correct \'YYYY-MM-DDTHH:mm:ss\' format.')

        # Filter distinct using range.
        return queryset.filter(leavedate__starts_at__gte=base_date).distinct()


    def leavedate_timesheet(self, queryset, name, value):
        """Filters distinct leavedates linked to the provided timesheet."""

        return queryset.filter(leavedate__timesheet=value).distinct()


    order_fields = ('status', 'description')
    order_by = NullLastOrderingFilter(fields=order_fields)

    leavedate__range = django_filters.CharFilter(method='leavedate_range_distinct')
    leavedate__gte = django_filters.CharFilter(method='leavedate_upcoming_distinct')
    leavedate__timesheet = django_filters.NumberFilter(method='leavedate_timesheet')

    class Meta:
        model = models.Leave
        fields = {
            'status': ['exact'],
            'description': ['exact', 'contains', 'icontains'],
            'user_id': ['exact'],
        }


class LeaveDateFilter(FilterSet):
    order_fields = ('starts_at', 'ends_at')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.LeaveDate
        fields = {
            'starts_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'ends_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }


class PerformanceTypeFilter(FilterSet):
    order_fields = ('label', 'description', 'multiplier')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.PerformanceType
        fields = {
            'label': ['exact', 'contains', 'icontains'],
            'description': ['exact', 'contains', 'icontains'],
            'multiplier': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }


class ContractFilter(FilterSet):
    
    order_fields = ('label', 'description', 'active', 'contractuser__user__username', 'contractuser__user__first_name',
        'contractuser__user__last_name', 'contractuser__user__groups', 'company__vat_identification_number', 'customer__vat_identification_number',
        'company__name', 'customer__name', 'company__country', 'customer_country', 'company__internal', 'customer__internal',
        'contract_groups__label', 'performance_types__label')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:

        model = models.Contract
        fields = {

            # Basic contract fields
            'label': ['exact', 'contains', 'icontains'],
            'description': ['exact', 'contains', 'icontains'],
            'active': ['exact', ],

            # User related fields
            'contractuser__user__username': ['exact', 'contains', 'icontains', ],
            'contractuser__user__id': ['exact', ],
            'contractuser__user__first_name': ['exact', 'contains', 'icontains', ],
            'contractuser__user__last_name': ['exact', 'contains', 'icontains', ],
            'contractuser__user__groups': ['exact', 'contains', 'icontains', ],

            # Companies & Customer fields
            'company__vat_identification_number': ['exact', ],
            'customer__vat_identification_number': ['exact', ],
            'company__name': ['exact', 'contains', 'icontains', ],
            'company': ['exact', ],
            'customer__name': ['exact', 'contains', 'icontains', ],
            'company__country': ['exact', ],
            'customer__country': ['exact', ],
            'company__internal': ['exact', ],
            'customer__internal': ['exact', ],

            # Contractgroup fields
            'contract_groups__label': ['exact', 'contains', 'icontains', ],

            # Performancetype fields
            'performance_types__label': ['exact', 'contains', 'icontains', ],
            'performance_types__id': ['exact', ],
        }


class ProjectContractFilter(ContractFilter):
    order_fields = ContractFilter.order_fields + ('fixed_fee', 'starts_at', 'ends_at')
    order_by = NullLastOrderingFilter(fields = order_fields)
    
    class Meta(ContractFilter.Meta):
        model = models.ProjectContract
        fields = merge_dicts(ContractFilter.Meta.fields, {

            # Basic ProjectContract fields
            'fixed_fee': ['exact', 'contains', ],
            'starts_at': ['exact', 'gt', 'gte', 'lt', 'lte', ],
            'ends_at': ['exact', 'gt', 'gte', 'lt', 'lte', ],
        })


class ConsultancyContractFilter(ContractFilter):
    order_fields = ContractFilter.order_fields + ('day_rate', 'starts_at', 'ends_at', 'duration')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta(ContractFilter.Meta):
        model = models.ConsultancyContract
        fields = merge_dicts(ContractFilter.Meta.fields, {
            'day_rate': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'starts_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'ends_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'duration': ['exact', 'gt', 'gte', 'lt', 'lte'],
        })


class SupportContractFilter(ContractFilter):
    order_fields = ContractFilter.order_fields + ('day_rate', 'starts_at', 'ends_at', 'fixed_fee', 'fixed_fee_period')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta(ContractFilter.Meta):
        model = models.SupportContract
        fields = merge_dicts(ContractFilter.Meta.fields, {
            'day_rate': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'starts_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'ends_at': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'fixed_fee': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'fixed_fee_period': ['exact'],
        })


class ContractGroupFilter(FilterSet):
    order_fields = ('label', )
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.ContractGroup
        fields = {
            'label': ['exact', 'contains', 'icontains'],
            'contract__label': ['exact', 'contains', 'icontains', ],
        }


class ContractRoleFilter(FilterSet):
    order_fields = ('label', 'description')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.ContractRole
        fields = {
            'label': ['exact', 'contains', 'icontains'],
            'description': ['exact', 'contains', 'icontains'],
        }


class ContractUserFilter(FilterSet):
    order_fields = ('contract')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.ContractUser
        fields = {
            'contract': ['exact',]
        }


class ProjectEstimateFilter(FilterSet):
    order_fields = ( 'hours_estimated', 'role__label', 'project__label', 'project__description', )
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.ProjectEstimate
        fields = {            
            'hours_estimated': ['exact', 'gt', 'gte', 'lt', 'lte', ],
            'role__label': ['exact', 'contains', 'icontains', ],
            'project__label': ['exact', 'contains', 'icontains', ],
            'project__description': ['contains', 'icontains', ],
        }


class TimesheetFilter(FilterSet):
    order_fields = ('year', 'month', 'status')
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.Timesheet
        fields = {
            'year': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'month': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'status': ['exact'],
        }


class WhereaboutFilter(FilterSet):
    order_fields = ('location', 'day', 'timesheet__month', 'timesheet__year', )
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.Whereabout
        fields = {
            'location': ['exact', 'contains', 'icontains'],
            'day': ['exact', 'gt', 'gte', 'lt', 'lte', ],
            'timesheet': ['exact', ],
            'timesheet__month': ['exact', 'gte', 'lte', ],
            'timesheet__year': ['exact', 'gte', 'lte', ],
            'timesheet__user_id': ['exact'],
        }


class PerformanceFilter(FilterSet):
    order_fields = ('day', 'timesheet__month', 'timesheet__year', 'contract', )
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta:
        model = models.Performance
        fields = {
            'day': ['exact', 'gt', 'gte', 'lt', 'lte', ],
            'timesheet': ['exact', ],
            'timesheet__month': ['exact', 'gte', 'lte', ],
            'timesheet__year': ['exact', 'gte', 'lte', ],
            'timesheet__user_id': ['exact'],
            'contract': ['exact'],
        }


class ActivityPerformanceFilter(PerformanceFilter):
    order_fields = PerformanceFilter.order_fields + ('duration', 'description', )
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta(PerformanceFilter.Meta):
        model = models.ActivityPerformance
        fields = merge_dicts(PerformanceFilter.Meta.fields, {
            'duration': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'description': ['exact', 'contains', 'icontains'],
        })


class StandbyPerformanceFilter(PerformanceFilter):
    order_fields = PerformanceFilter.order_fields
    order_by = NullLastOrderingFilter(fields=order_fields)

    class Meta(PerformanceFilter.Meta):
        model = models.StandbyPerformance
        fields = PerformanceFilter.Meta.fields