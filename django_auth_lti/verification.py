from django.core.exceptions import ImproperlyConfigured, PermissionDenied


def is_allowed(request, allowed_roles, raise_exception):
    # allowed_roles can either be a string (for just one)
    # or a tuple or list (for several)
    if not isinstance(allowed_roles, (list, tuple)):
        allowed = (allowed_roles, )
    else:
        allowed = allowed_roles
    
    if not hasattr(request, 'lti_launch_params'):
        # If this is raised, then likely the project doesn't have
        # the correct settings or is being run outside of an lti context
        raise ImproperlyConfigured("No LTI_LAUNCH value found in session")
    lti_launch = request.lti_launch_params
    print "lti_launch params are %s" % lti_launch
    user_roles = lti_launch.get('roles', [])
    print "user roles are %s" % user_roles
    is_user_allowed = set(allowed) & set(user_roles)
    
    if not is_user_allowed and raise_exception:
        raise PermissionDenied
    
    return is_user_allowed
