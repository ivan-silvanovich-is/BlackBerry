from django_filters import rest_framework as filters


__all__ = (
    'CustomFilterBackend',
    'TimeStampFilter',
    'DateOrderFilter',
)


class CustomFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        if view.action != 'list':
            return None

        default_filterset_class = getattr(view, 'filterset_class', None)
        staff_filterset_class = getattr(view, 'staff_filterset_class', None)
        admin_filterset_class = getattr(view, 'admin_filterset_class', None)

        if view.request.user.is_superuser:
            filterset_class = admin_filterset_class or staff_filterset_class or default_filterset_class
        elif view.request.user.is_staff:
            filterset_class = staff_filterset_class or default_filterset_class
        else:
            filterset_class = default_filterset_class

        if filterset_class:
            filterset_model = filterset_class._meta.model

            if filterset_model and queryset is not None:
                assert issubclass(
                    queryset.model, filterset_model
                ), "FilterSet model %s does not match queryset model %s" % (
                    filterset_model,
                    queryset.model,
                )

            return filterset_class

        return None


class TimeStampFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()


class DateOrderFilter(filters.FilterSet):
    order = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': 'Дата создания',
            'updated_at': 'Дата обновления',
        }
    )
