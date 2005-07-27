#!/usr/bin/python

from OPCServices import *
from ZSI.ServiceContainer import ServiceSOAPBinding
import WSDLDoc;

class Service(ServiceSOAPBinding):
    soapAction = {
        'http://opcfoundation.org/webservices/XMLDA/1.0/Browse': 'soap_Browse',
        'http://opcfoundation.org/webservices/XMLDA/1.0/GetProperties': 'soap_GetProperties',
        'http://opcfoundation.org/webservices/XMLDA/1.0/GetStatus': 'soap_GetStatus',
        'http://opcfoundation.org/webservices/XMLDA/1.0/Read': 'soap_Read',
        'http://opcfoundation.org/webservices/XMLDA/1.0/Subscribe': 'soap_Subscribe',
        'http://opcfoundation.org/webservices/XMLDA/1.0/SubscriptionCancel': 'soap_SubscriptionCancel',
        'http://opcfoundation.org/webservices/XMLDA/1.0/SubscriptionPolledRefresh': 'soap_SubscriptionPolledRefresh',
        'http://opcfoundation.org/webservices/XMLDA/1.0/Write': 'soap_Write',
        }

    _wsdl = WSDLDoc.WSDLDOCstr;

 
    def __init__(self, post='', **kw):
        ServiceSOAPBinding.__init__(self, post)


    def soap_Browse(self, ps):
        # input vals in request object
        args = ps.Parse( BrowseSoapInWrapper )

        # assign return values to response object
        response = BrowseSoapOutWrapper()

        # Return the response
        return response

    def soap_GetProperties(self, ps):
        # input vals in request object
        args = ps.Parse( GetPropertiesSoapInWrapper )

        # assign return values to response object
        response = GetPropertiesSoapOutWrapper()

        # Return the response
        return response

    def soap_GetStatus(self, ps):
        # input vals in request object
        args = ps.Parse( GetStatusSoapInWrapper )

        # assign return values to response object
        response = GetStatusSoapOutWrapper()
        status = ns1.ServerStatus_Def();
        status.Set_StatusInfo("Up and running.");
        status.Set_ProductVersion("1.0.0")
        response.Set_Status(status);

        # Return the response
        return response

    def soap_Read(self, ps):
        # input vals in request object
        args = ps.Parse( ReadSoapInWrapper )

        # assign return values to response object
        response = ReadSoapOutWrapper()

        # Return the response
        return response

    def soap_Subscribe(self, ps):
        # input vals in request object
        args = ps.Parse( SubscribeSoapInWrapper )

        # assign return values to response object
        response = SubscribeSoapOutWrapper()

        # Return the response
        return response

    def soap_SubscriptionCancel(self, ps):
        # input vals in request object
        args = ps.Parse( SubscriptionCancelSoapInWrapper )

        # assign return values to response object
        response = SubscriptionCancelSoapOutWrapper()

        # Return the response
        return response

    def soap_SubscriptionPolledRefresh(self, ps):
        # input vals in request object
        args = ps.Parse( SubscriptionPolledRefreshSoapInWrapper )

        # assign return values to response object
        response = SubscriptionPolledRefreshSoapOutWrapper()

        # Return the response
        return response

    def soap_Write(self, ps):
        # input vals in request object
        args = ps.Parse( WriteSoapInWrapper )

        # assign return values to response object
        response = WriteSoapOutWrapper()

        # Return the response
        return response


if __name__=="__main__":
   s = Service();
   srvcon = ZSI.ServiceContainer.ServiceContainer(("10.1.1.4",7000));
   srvcon.setNode(s,post="/OPCXMLDA");
   srvcon.serve_forever();

