
# TODO add original licensing for this, don't remember where it came from

import re
import random
import math

from itertools import ifilter
from functools import wraps
from twisted.web.resource import Resource
from twisted.web.resource import NoResource
# DFW: I think this is old: from twisted.web.error import NoResource
from zope.interface.advice import addClassAdvisor
from twisted.web.server import NOT_DONE_YET

from paradrop.shared.output import out
from paradrop.shared.pdutils import str2json, explode
from paradrop.lib import settings


def method_factory_factory(method):
    def factory(regex):
        _f = {}

        def decorator(f):
            _f[f.__name__] = f
            return f

        def advisor(cls):
            def wrapped(f):
                def __init__(self, *args, **kwargs):
                    f(self, *args, **kwargs)
                    for func_name in _f:
                        orig = _f[func_name]
                        func = getattr(self, func_name)
                    if func.im_func == orig:
                        self.register(method, regex, func)
                return __init__
            cls.__init__ = wrapped(cls.__init__)
            return cls
        addClassAdvisor(advisor)
        return decorator
    return factory

ALL = method_factory_factory('ALL')
GET = method_factory_factory('GET')
POST = method_factory_factory('POST')
PUT = method_factory_factory('PUT')
DELETE = method_factory_factory('DELETE')


class _FakeResource(Resource):
    _result = ''
    isLeaf = True

    def __init__(self, result):
        Resource.__init__(self)
        self._result = result

    def render(self, request):
        return self._result


def maybeResource(f):
    @wraps(f)
    def inner(*args, **kwargs):
        result = f(*args, **kwargs)
        if not isinstance(result, Resource):
            result = _FakeResource(result)
        return result
    return inner


class APIResource(Resource):

    _registry = None

    def __init__(self, *args, **kwargs):
        Resource.__init__(self, *args, **kwargs)
        self._registry = []

    def _get_callback(self, request):
        filterf = lambda t: t[0] in (request.method, 'ALL')
        for m, r, cb in ifilter(filterf, self._registry):
            result = r.search(request.path)
            if result:
                return cb, result.groupdict()
        return None, None

    def register(self, method, regex, callback):
        self._registry.append((method, re.compile(regex), callback))

    def unregister(self, method=None, regex=None, callback=None):
        if regex is not None:
            regex = re.compile(regex)
        for m, r, cb in self._registry[:]:
            if not method or (method and m == method):
                if not regex or (regex and r == regex):
                    if not callback or (callback and cb == callback):
                        self._registry.remove((m, r, cb))

    def getChild(self, name, request):
        r = self.children.get(name, None)
        if r is None:
            # Go into the thing
            callback, args = self._get_callback(request)
            if callback is None:
                return NoResource()
            else:
                return maybeResource(callback)(request, **args)
        else:
            return r


class APIPackage():

    """
    This is a class that wrap up the input and return value of API
    The input arguments will be in the inputArgs as a dict
    Result is True means the API return success
    Result is False means the API return failure
    Result is None means the API return NOT_YET_DONE
    """

    def __init__(self, request):
        self.request = request
        # input values to the API
        self.inputArgs = {}
        # Return values from API
        self.result = True
        # On success
        self.returnVal = None
        # On failure
        self.errType = None
        self.errMsg = None
        self.countFailure = True
        # On NOT_YET_DONE

    def setSuccess(self, returnVal):
        self.result = True
        self.returnVal = returnVal

    def setFailure(self, errType, errMsg=None, countFailure=True):
        self.result = False
        self.errType = errType
        self.errMsg = errMsg
        self.countFailure = countFailure

    def setNotDoneYet(self):
        self.result = None


def APIDecorator(admin=False, permission=None, requiredArgs=[], optionalArgs=[]):
    """
        The decorator for the API functions to make the API functions focus on their job.
        This decorator do the following things:
            * Set HTTP header
            * Get some common values like ip, tictoc
            * Do the preprocess
            * Extract arguments from HTTP body and put them into APIPackage
            * Get devid if token is shown and put devid into APIPackage
            * Check admin authorization if devid is shown and admin argument is set to be true
            * Do the failprocess if fails. Do the postProcess if success
        This decorator will pass an APIPackage to an API function and the API function is supposed to put return value into the API package
        Arguments:
            * admin: if the function needs admin authority to call
            * requiredArgs: the required arguments for this API, this wrapper will parse the required args from HTTP body and check if they exist in the body.
            * optionalArgs: the optional arguments for this API, the args will be parsed from HTTP body
            * permission: choose from None, "AP Owner", "Chute Owner"
        TODO: 
            1.Permission
                * multiple permission/multiple level of permission??
                * More permissions: such as Vnet Owner, Group Owner
    """
    def realDecorator(func):
        def wrapper(theSelf, request, *args, **kwargs):
            tictoc = 0  # theSelf.perf.tic()
            ip = '0.0.0.0'  # TODO getIP(request)
            out.verbose('HTTP request from IP %s\n' % (ip))
            request.setHeader('Access-Control-Allow-Origin', settings.PDFCD_HEADER_VALUE)

            apiPackage = APIPackage(request)
            # Extract required arguments
            if(requiredArgs or optionalArgs):
                body = str2json(request.content.read())
            if(requiredArgs):
                required = explode(body, *requiredArgs)
                for idx, arg in enumerate(requiredArgs):
                    # Check if required arg exist
                    if(required[idx] is None):
                        return theSelf.rest.failprocess(ip, request, (ip, theSelf.rest.clientFailures), "Malformed Body: %s", (tictoc, None), ERR_BADPARAM)
                    # If exist put it into the apiPackage
                    apiPackage.inputArgs[arg] = required[idx]

            # Extract optional arguments
            if(optionalArgs):
                optional = explode(body, *optionalArgs)
                for idx, arg in enumerate(optionalArgs):
                    if(optional[idx]):
                        apiPackage.inputArgs[arg] = optional[idx]

            #######################################################################################
            # Make the real function call
            #######################################################################################
            func(theSelf, apiPackage, *args, **kwargs)

            # NOT_DONE_YET
            if(apiPackage.result is None):
                return NOT_DONE_YET
            # SUCCESS
            elif(apiPackage.result is True):
                theSelf.rest.postprocess(request, failureKey, failureDict, (tictoc, ip, devid))
                return apiPackage.returnVal
            # FAILURE
            else:
                errMsg = apiPackage.errMsg
                errType = apiPackage.errType
                if(apiPackage.countFailure):
                    return theSelf.rest.failprocess(ip, request, (failureKey, failureDict), errMsg, (tictoc, devid), errType)
                else:
                    return theSelf.rest.failprocess(ip, request, None, errMsg, (tictoc, devid), errType)

        return wrapper
    return realDecorator


class PDAPIError(Exception):
    """
        Exception class related to ParaDrop API calls.
    """

    def __init__(self, etype, msg):
        self.etype = etype
        self.msg = msg

    def __str__(self):
        return "PDAPIError %s: %s" % (self.etype, self.msg)


def isPDError(code):
    """
    Checks all Paradrop API error codes, if the HTTP code is in our set it is
    assumed a PDAPI error.
    """
    return (code in RESP_MSG)


OK = 200
ERR_BADPARAM = 400
ERR_TOKEXPIRE = 401
ERR_BADFORMAT = 402
ERR_BADAUTH = 403
ERR_THRESHOLD = 404
ERR_BADMETHOD = 405
ERR_BADIO = 406
ERR_BADPATH = 407
ERR_CONTACTPD = 501
ERR_DBISSUE = 502
ERR_STATECHANGE = 503
ERR_CHUTESTATE = 504
ERR_UPDATEPENDING = 505
ERR_NOSTATUS = 506
ERR_RESETPENDING = 507
ERR_CHUTEINVALID = 508
ERR_UNIMPLEMENTED = 599

RESP_MSG = {
    OK: None,
    ERR_BADPARAM: "Bad parameter: %s",
    ERR_TOKEXPIRE: "Token expired",
    ERR_BADFORMAT: "Bad format",
    ERR_BADAUTH: "Bad authorization",
    ERR_THRESHOLD: "Access limited due to threshold",
    ERR_BADMETHOD: "Bad method type",
    ERR_BADIO: "Bad IO",
    ERR_BADPATH: "Path not found",
    ERR_CONTACTPD: "Contact Paradrop, ERRORTOKEN: %s",
    ERR_DBISSUE: "Issue with database, please try again",
    ERR_STATECHANGE: "Bad state transition",
    ERR_CHUTESTATE: "Cannot make change with chute in its current state",
    ERR_UPDATEPENDING: "Action already pending for Chute",
    ERR_NOSTATUS: "No status data available, either none exists or bad authorization",
    ERR_RESETPENDING: "Reset already pending for AP",
    ERR_CHUTEINVALID: "Cannot make change, chute would become invalid",
    ERR_UNIMPLEMENTED: "Function unimplemented yet",
}


def getResponse(code, *args):
    """Designed to be called to provide the arguments for the Request.setResponseCode()"""
    if(len(args) == 0):
        return code, RESP_MSG[code]
    else:
        return code, RESP_MSG[code] % (args)


def getErrorToken():
    """Generates a random string which is used to match client issues with log output."""
    return '%010d' % int(random.getrandbits(32))
