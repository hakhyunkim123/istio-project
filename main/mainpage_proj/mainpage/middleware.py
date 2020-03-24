class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'id' in request.session:
            request.META['end-user'] = request.session.get('id')
        else: 
            request.META['end-user'] = None

        if 'Authorization' in request.session:
            request.META['Authorization'] = request.session.get('Authorization')
        else: 
            request.META['Authorization'] = None
        response = self.get_response(request)
        return response
