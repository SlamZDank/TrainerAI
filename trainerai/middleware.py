import logging
import time

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timer
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate execution time
        duration = time.time() - start_time
        
        # Log details
        log_data = {
            'method': request.method,
            'path': request.get_full_path(),
            'status_code': response.status_code,
            'duration': f"{duration:.3f}s",
            'ip': self.get_client_ip(request),
            'user': request.user.id if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        }
        
        message = f"[{log_data['method']}] {log_data['path']} - Status: {log_data['status_code']} - Time: {log_data['duration']} - IP: {log_data['ip']} - User: {log_data['user']}"
        
        if response.status_code >= 500:
            logger.error(message)
        elif response.status_code >= 400:
            logger.warning(message)
        else:
            logger.info(message)
            
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
