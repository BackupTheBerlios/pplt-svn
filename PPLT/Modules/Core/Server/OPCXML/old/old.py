from Service_services import *
from ZSI.ServiceContainer import ServiceSOAPBinding
import ZSI.ServiceContainer

class Service(ServiceSOAPBinding):
    soapAction = {
        'http://schemas.spdj.de/base/0.1/GetStatus': 'soap_GetStatus',
        }
    _wsdl = """<?xml version=\"1.0\" ?>
<definitions targetNamespace=\"http://schemas.spdj.de/base/0.1/\" xmlns=\"http://schemas.xmlsoap.org/wsdl/\" xmlns:http=\"http://schemas.xmlsoap.org/wsdl/http/\" xmlns:mime=\"http://schemas.xmlsoap.org/wsdl/mime/\" xmlns:s=\"http://www.w3.org/2001/XMLSchema\" xmlns:s0=\"http://schemas.spdj.de/base/0.1/\" xmlns:soap=\"http://schemas.xmlsoap.org/wsdl/soap/\" xmlns:soapenc=\"http://schemas.xmlsoap.org/soap/encoding/\" xmlns:tm=\"http://microsoft.com/wsdl/mime/textMatching/\">
	<types>
		<s:schema elementFormDefault=\"qualified\" targetNamespace=\"http://schemas.spdj.de/base/0.1/\">
			<s:element name=\"GetStatus\">
				<s:complexType>
					<s:attribute name=\"LocalID\" type=\"s:string\"/>
					<s:attribute name=\"ClientRequestHandle\" type=\"s:string\"/>
				</s:complexType>
			</s:element>
			<s:element name=\"GetStatusResponse\">
				<s:complexType>
					<s:sequence>
						<s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"GetStatusResult\" type=\"s0:ReplyBase\"/>
						<s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Status\" type=\"s0:ServerStatus\"/>
					</s:sequence>
				</s:complexType>
			</s:element>
			<s:complexType name=\"ReplyBase\">
				<s:attribute name=\"RcvTime\" type=\"s:dateTime\" use=\"required\"/>
				<s:attribute name=\"ReplyTime\" type=\"s:dateTime\" use=\"required\"/>				
				<s:attribute name=\"ClientRequestHandle\" type=\"s:string\"/>				
				<s:attribute name=\"RevisedLocalID\" type=\"s:string\"/>	
				<s:attribute name=\"ServerState\" type=\"s0:serverState\" use=\"required\"/>					
			</s:complexType>
			<s:simpleType name=\"serverState\">
				<s:restriction base=\"s:string\">
					<s:enumeration value=\"running\"/>
					<s:enumeration value=\"failed\"/>
					<s:enumeration value=\"noConfig\"/>
					<s:enumeration value=\"suspended\"/>
					<s:enumeration value=\"test\"/>															
					<s:enumeration value=\"commFault\"/>					
				</s:restriction>
			</s:simpleType>
			<s:simpleType name=\"interfaceVersion\">
					<s:restriction base=\"s:string\">
						<s:enumeration value=\"XML_BASE_VERSION_0_1\"/>
					</s:restriction>
			</s:simpleType>
			<s:complexType name=\"ServerStatus\">
				<s:sequence>
						<s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"StatusInfo\" type=\"s:String\"/>				
						<s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"VendorInfo\" type=\"s:String\"/>				
						<s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"SupportedLocalIDs\" type=\"s:String\"/>										
						<s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"SupportedInterfaceVersions\" type=\"s0:interfaceVersion\"/>																
				</s:sequence>				
			</s:complexType>
		</s:schema>
	</types>
	
	<message name=\"GetStatusSoapIn\">
		<part element=\"s0:GetStatus\" name=\"parameters\"/>
	</message>
	<message name=\"GetStatusSoapOut\">
		<part element=\"s0:GetStatusResponse\" name=\"parameters\"/>
	</message>
	
	<portType name=\"Service\">
		<operation name=\"GetStatus\">
			<input message=\"s0:GetStatusSoapIn\"/> 
			<output message=\"s0:GetStatusSoapOut\"/> 
		</operation>
		<!-- Auth -->
		<!-- GetProperties -->
		<!-- Browse -->	
	</portType>
	
	<binding name=\"Service\" type=\"s0:Service\">
		<soap:binding style=\"document\" transport=\"http://schemas.xmlsoap.org/soap/http\"/>
		<!-- Server Status -->
		<operation name=\"GetStatus\">
			<soap:operation soapAction=\"http://schemas.spdj.de/base/0.1/GetStatus\" style=\"document\"/>
			<input>
				<soap:body use=\"literal\"/>
			</input> 
			<output>
				<soap:body use=\"literal\"/>
			</output>
		</operation>
		<!-- Auth -->
		<!-- GetProperties -->
		<!-- Browse -->		
	</binding>

	<service name=\"Service\">
    <port binding=\"s0:Service\" name=\"Service\">
      <soap:address location=\"http://localhost:7000\"/>
    </port>
	</service>
</definitions>"""

    def __init__(self, post='', **kw):
        ServiceSOAPBinding.__init__(self, post)


    def soap_GetStatus(self, ps):
        # input vals in request object
        args = ps.Parse( GetStatusSoapInWrapper )

        # assign return values to response object
        response = GetStatusSoapOutWrapper()

        status = ns1.ServerStatus();
        status.Set_StatusInfo("Up and running.");
        response.Set_Status(status);
        # Return the response
        return response

if __name__=="__main__":
   s = Service();
   srvcon = ZSI.ServiceContainer.ServiceContainer(("10.1.1.4",7000));
   srvcon.setNode(s,post="/OPCXMLDA");
   srvcon.serve_forever();
