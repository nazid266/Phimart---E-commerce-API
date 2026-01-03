from django.core.exceptions import ValidationError
def validate_file_size(files):
    """This validator validate if files size is less than 10MB"""
    
    max_size=10
    max_size_in_bytes=max_size*1024
    if files.size>max_size_in_bytes:
        raise ValidationError(f'file can not be larger than {max_size}MB!')