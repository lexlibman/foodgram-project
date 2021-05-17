from .models import Tag


class Tags:
    def __init__(self, get_response):
        self.get_response = get_response
        self.tags = [{'object': x} for x in Tag.objects.all()]

    def __call__(self, request):
        existing_filters = request.GET.getlist('filter')
        existing_tags = Tag.objects.filter(title__in=existing_filters)
        for tag in self.tags:
            filters = existing_filters.copy()
            tag_obj = tag['object']
            if (tag_obj.title in existing_filters
                    and len(existing_filters) > 1):
                tag['active'] = True
                filters.remove(tag_obj.title)
            elif (tag_obj.title in existing_filters
                    and len(existing_filters) == 1):
                tag['active'] = True
            else:
                tag['active'] = False
                filters.append(tag['object'].title)
        request.current_filter = f"?filter={'&filter='.join(existing_filters)}"
        request.existing_tags = existing_tags
        request.tags = self.tags
        response = self.get_response(request)
        return response
