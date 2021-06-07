
def GetDomainNameFromRequest(request):
    return str(request.questions[0].qname)[:-1]
