WSDLDOCstr = """<?xml version=\"1.0\" ?>
<!--  
      COPYRIGHT (c) 2003 OPC Foundation. All rights reserved.
      http://www.opcfoundation.org
      Use subject to the OPC Foundation License Agreement found at the following URL: 
      http://www.opcfoundation.org/Downloads/LicenseAgreement.asp	
--><definitions targetNamespace=\"http://opcfoundation.org/webservices/XMLDA/1.0/\" xmlns=\"http://schemas.xmlsoap.org/wsdl/\" xmlns:http=\"http://schemas.xmlsoap.org/wsdl/http/\" xmlns:mime=\"http://schemas.xmlsoap.org/wsdl/mime/\" xmlns:s=\"http://www.w3.org/2001/XMLSchema\" xmlns:s0=\"http://opcfoundation.org/webservices/XMLDA/1.0/\" xmlns:soap=\"http://schemas.xmlsoap.org/wsdl/soap/\" xmlns:soapenc=\"http://schemas.xmlsoap.org/soap/encoding/\" xmlns:tm=\"http://microsoft.com/wsdl/mime/textMatching/\">

  <types>
    <s:schema elementFormDefault=\"qualified\" targetNamespace=\"http://opcfoundation.org/webservices/XMLDA/1.0/\">
      <s:element name=\"GetStatus\">
        <s:complexType>
          <s:attribute name=\"LocaleID\" type=\"s:string\"/>
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
        <s:attribute name=\"RevisedLocaleID\" type=\"s:string\"/>
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
          <s:enumeration value=\"XML_DA_Version_1_0\"/>
        </s:restriction>
      </s:simpleType>

      <s:complexType name=\"ServerStatus\">
        <s:sequence>
          <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"StatusInfo\" type=\"s:string\"/>
          <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"VendorInfo\" type=\"s:string\"/>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"SupportedLocaleIDs\" type=\"s:string\"/>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"SupportedInterfaceVersions\" type=\"s0:interfaceVersion\"/>
        </s:sequence>
        <s:attribute name=\"StartTime\" type=\"s:dateTime\" use=\"required\"/>
        <s:attribute name=\"ProductVersion\" type=\"s:string\"/>
      </s:complexType>

      <s:element name=\"Read\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Options\" type=\"s0:RequestOptions\"/>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"ItemList\" type=\"s0:ReadRequestItemList\"/>
          </s:sequence>
        </s:complexType>
      </s:element>

      <s:complexType name=\"RequestOptions\">
        <s:attribute default=\"true\" name=\"ReturnErrorText\" type=\"s:boolean\"/>
        <s:attribute default=\"false\" name=\"ReturnDiagnosticInfo\" type=\"s:boolean\"/>
        <s:attribute default=\"false\" name=\"ReturnItemTime\" type=\"s:boolean\"/>
        <s:attribute default=\"false\" name=\"ReturnItemPath\" type=\"s:boolean\"/>
        <s:attribute default=\"false\" name=\"ReturnItemName\" type=\"s:boolean\"/>
        <s:attribute name=\"RequestDeadline\" type=\"s:dateTime\"/>
        <s:attribute name=\"ClientRequestHandle\" type=\"s:string\"/>
        <s:attribute name=\"LocaleID\" type=\"s:string\"/>
      </s:complexType>

      <s:complexType name=\"ReadRequestItemList\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Items\" type=\"s0:ReadRequestItem\"/>
        </s:sequence>
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ReqType\" type=\"s:QName\"/>
        <s:attribute name=\"MaxAge\" type=\"s:int\"/>
      </s:complexType>

      <s:complexType name=\"ReadRequestItem\">
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ReqType\" type=\"s:QName\"/>
        <s:attribute name=\"ItemName\" type=\"s:string\"/>
        <s:attribute name=\"ClientItemHandle\" type=\"s:string\"/>
        <s:attribute name=\"MaxAge\" type=\"s:int\"/>
      </s:complexType>

      <s:element name=\"ReadResponse\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"ReadResult\" type=\"s0:ReplyBase\"/>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"RItemList\" type=\"s0:ReplyItemList\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Errors\" type=\"s0:OPCError\"/>
          </s:sequence>
        </s:complexType>
      </s:element>

      <s:complexType name=\"ReplyItemList\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Items\" type=\"s0:ItemValue\"/>
        </s:sequence>
        <s:attribute name=\"Reserved\" type=\"s:string\"/>
      </s:complexType>

      <s:complexType name=\"ItemValue\">
        <s:sequence>
          <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"DiagnosticInfo\" type=\"s:string\"/>
          <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Value\"/>
          <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Quality\" type=\"s0:OPCQuality\"/>
        </s:sequence>
        <s:attribute name=\"ValueTypeQualifier\" type=\"s:QName\"/>
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ItemName\" type=\"s:string\"/>
        <s:attribute name=\"ClientItemHandle\" type=\"s:string\"/>
        <s:attribute name=\"Timestamp\" type=\"s:dateTime\"/>
        <s:attribute name=\"ResultID\" type=\"s:QName\"/>
      </s:complexType>

      <s:complexType name=\"OPCQuality\">
        <s:attribute default=\"good\" name=\"QualityField\" type=\"s0:qualityBits\"/>
        <s:attribute default=\"none\" name=\"LimitField\" type=\"s0:limitBits\"/>
        <s:attribute default=\"0\" name=\"VendorField\" type=\"s:unsignedByte\"/>
      </s:complexType>

      <s:simpleType name=\"qualityBits\">
        <s:restriction base=\"s:string\">
          <s:enumeration value=\"bad\"/>
          <s:enumeration value=\"badConfigurationError\"/>
          <s:enumeration value=\"badNotConnected\"/>
          <s:enumeration value=\"badDeviceFailure\"/>
          <s:enumeration value=\"badSensorFailure\"/>
          <s:enumeration value=\"badLastKnownValue\"/>
          <s:enumeration value=\"badCommFailure\"/>
          <s:enumeration value=\"badOutOfService\"/>
          <s:enumeration value=\"badWaitingForInitialData\"/>
          <s:enumeration value=\"uncertain\"/>
          <s:enumeration value=\"uncertainLastUsableValue\"/>
          <s:enumeration value=\"uncertainSensorNotAccurate\"/>
          <s:enumeration value=\"uncertainEUExceeded\"/>
          <s:enumeration value=\"uncertainSubNormal\"/>
          <s:enumeration value=\"good\"/>
          <s:enumeration value=\"goodLocalOverride\"/>
        </s:restriction>
      </s:simpleType>

      <s:simpleType name=\"limitBits\">
        <s:restriction base=\"s:string\">
          <s:enumeration value=\"none\"/>
          <s:enumeration value=\"low\"/>
          <s:enumeration value=\"high\"/>
          <s:enumeration value=\"constant\"/>
        </s:restriction>
      </s:simpleType>

      <s:complexType name=\"OPCError\">
        <s:sequence>
          <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Text\" type=\"s:string\"/>
        </s:sequence>
        <s:attribute name=\"ID\" type=\"s:QName\" use=\"required\"/>
      </s:complexType>

      <s:complexType name=\"ArrayOfFloat\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"float\" type=\"s:float\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfInt\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"int\" type=\"s:int\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfUnsignedInt\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"unsignedInt\" type=\"s:unsignedInt\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfLong\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"long\" type=\"s:long\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfUnsignedLong\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"unsignedLong\" type=\"s:unsignedLong\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfDouble\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"double\" type=\"s:double\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfUnsignedShort\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"unsignedShort\" type=\"s:unsignedShort\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfBoolean\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"boolean\" type=\"s:boolean\"/>
        </s:sequence>

      </s:complexType>
      <s:complexType name=\"ArrayOfString\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"string\" nillable=\"true\" type=\"s:string\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfDateTime\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"dateTime\" type=\"s:dateTime\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfAnyType\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"anyType\" nillable=\"true\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfDecimal\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"decimal\" type=\"s:decimal\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfByte\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"byte\" type=\"s:byte\"/>
        </s:sequence>
      </s:complexType>

      <s:complexType name=\"ArrayOfShort\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"short\" type=\"s:short\"/>
        </s:sequence>
      </s:complexType>

      <s:element name=\"Write\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Options\" type=\"s0:RequestOptions\"/>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"ItemList\" type=\"s0:WriteRequestItemList\"/>
          </s:sequence>
          <s:attribute name=\"ReturnValuesOnReply\" type=\"s:boolean\" use=\"required\"/>
        </s:complexType>
      </s:element>

      <s:complexType name=\"WriteRequestItemList\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Items\" type=\"s0:ItemValue\"/>
        </s:sequence>
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
      </s:complexType>

      <s:element name=\"WriteResponse\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"WriteResult\" type=\"s0:ReplyBase\"/>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"RItemList\" type=\"s0:ReplyItemList\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Errors\" type=\"s0:OPCError\"/>
          </s:sequence>
        </s:complexType>
      </s:element>

      <s:element name=\"Subscribe\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Options\" type=\"s0:RequestOptions\"/>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"ItemList\" type=\"s0:SubscribeRequestItemList\"/>
          </s:sequence>
          <s:attribute name=\"ReturnValuesOnReply\" type=\"s:boolean\" use=\"required\"/>
          <s:attribute default=\"0\" name=\"SubscriptionPingRate\" type=\"s:int\"/>
        </s:complexType>
      </s:element>

      <s:complexType name=\"SubscribeRequestItemList\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Items\" type=\"s0:SubscribeRequestItem\"/>
        </s:sequence>
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ReqType\" type=\"s:QName\"/>
        <s:attribute name=\"Deadband\" type=\"s:float\"/>
        <s:attribute name=\"RequestedSamplingRate\" type=\"s:int\"/>
        <s:attribute name=\"EnableBuffering\" type=\"s:boolean\"/>
      </s:complexType>

      <s:complexType name=\"SubscribeRequestItem\">
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ReqType\" type=\"s:QName\"/>
        <s:attribute name=\"ItemName\" type=\"s:string\"/>
        <s:attribute name=\"ClientItemHandle\" type=\"s:string\"/>
        <s:attribute name=\"Deadband\" type=\"s:float\"/>
        <s:attribute name=\"RequestedSamplingRate\" type=\"s:int\"/>
        <s:attribute name=\"EnableBuffering\" type=\"s:boolean\"/>
      </s:complexType>

      <s:complexType name=\"SubscribeReplyItemList\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Items\" type=\"s0:SubscribeItemValue\"/>
        </s:sequence>
        <s:attribute name=\"RevisedSamplingRate\" type=\"s:int\"/>
      </s:complexType>

      <s:complexType name=\"SubscribeItemValue\">
        <s:sequence>
          <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"ItemValue\" type=\"s0:ItemValue\"/>
        </s:sequence>
        <s:attribute name=\"RevisedSamplingRate\" type=\"s:int\"/>
      </s:complexType>

      <s:element name=\"SubscribeResponse\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"SubscribeResult\" type=\"s0:ReplyBase\"/>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"RItemList\" type=\"s0:SubscribeReplyItemList\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Errors\" type=\"s0:OPCError\"/>
          </s:sequence>
          <s:attribute name=\"ServerSubHandle\" type=\"s:string\"/>
        </s:complexType>
      </s:element>

      <s:element name=\"SubscriptionPolledRefresh\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Options\" type=\"s0:RequestOptions\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"ServerSubHandles\" type=\"s:string\"/>
          </s:sequence>
          <s:attribute name=\"HoldTime\" type=\"s:dateTime\"/>
          <s:attribute default=\"0\" name=\"WaitTime\" type=\"s:int\"/>
          <s:attribute default=\"false\" name=\"ReturnAllItems\" type=\"s:boolean\"/>
        </s:complexType>
      </s:element>

      <s:complexType name=\"SubscribePolledRefreshReplyItemList\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Items\" type=\"s0:ItemValue\"/>
        </s:sequence>
        <s:attribute name=\"SubscriptionHandle\" type=\"s:string\"/>
      </s:complexType>

      <s:element name=\"SubscriptionPolledRefreshResponse\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"SubscriptionPolledRefreshResult\" type=\"s0:ReplyBase\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"InvalidServerSubHandles\" type=\"s:string\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"RItemList\" type=\"s0:SubscribePolledRefreshReplyItemList\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Errors\" type=\"s0:OPCError\"/>
          </s:sequence>
          <s:attribute default=\"false\" name=\"DataBufferOverflow\" type=\"s:boolean\"/>
        </s:complexType>
      </s:element>

      <s:element name=\"SubscriptionCancel\">
        <s:complexType>
          <s:attribute name=\"ServerSubHandle\" type=\"s:string\"/>
          <s:attribute name=\"ClientRequestHandle\" type=\"s:string\"/>
        </s:complexType>
      </s:element>

      <s:element name=\"SubscriptionCancelResponse\">
        <s:complexType>
          <s:attribute name=\"ClientRequestHandle\" type=\"s:string\"/>
        </s:complexType>
      </s:element>

      <s:element name=\"Browse\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"PropertyNames\" type=\"s:QName\"/>
          </s:sequence>
          <s:attribute name=\"LocaleID\" type=\"s:string\"/>
          <s:attribute name=\"ClientRequestHandle\" type=\"s:string\"/>
          <s:attribute name=\"ItemPath\" type=\"s:string\"/>
          <s:attribute name=\"ItemName\" type=\"s:string\"/>
          <s:attribute name=\"ContinuationPoint\" type=\"s:string\"/>
          <s:attribute default=\"0\" name=\"MaxElementsReturned\" type=\"s:int\"/>
          <s:attribute default=\"all\" name=\"BrowseFilter\" type=\"s0:browseFilter\"/>
          <s:attribute name=\"ElementNameFilter\" type=\"s:string\"/>
          <s:attribute name=\"VendorFilter\" type=\"s:string\"/>
          <s:attribute default=\"false\" name=\"ReturnAllProperties\" type=\"s:boolean\"/>
          <s:attribute default=\"false\" name=\"ReturnPropertyValues\" type=\"s:boolean\"/>
          <s:attribute default=\"false\" name=\"ReturnErrorText\" type=\"s:boolean\"/>
        </s:complexType>
      </s:element>

      <s:simpleType name=\"browseFilter\">
        <s:restriction base=\"s:string\">
          <s:enumeration value=\"all\"/>
          <s:enumeration value=\"branch\"/>
          <s:enumeration value=\"item\"/>
        </s:restriction>
      </s:simpleType>

      <s:complexType name=\"BrowseElement\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Properties\" type=\"s0:ItemProperty\"/>
        </s:sequence>
        <s:attribute name=\"Name\" type=\"s:string\"/>
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ItemName\" type=\"s:string\"/>
        <s:attribute name=\"IsItem\" type=\"s:boolean\" use=\"required\"/>
        <s:attribute name=\"HasChildren\" type=\"s:boolean\" use=\"required\"/>
      </s:complexType>

      <s:complexType name=\"ItemProperty\">
        <s:sequence>
          <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"Value\"/>
        </s:sequence>
        <s:attribute name=\"Name\" type=\"s:QName\" use=\"required\"/>
        <s:attribute name=\"Description\" type=\"s:string\"/>
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ItemName\" type=\"s:string\"/>
        <s:attribute name=\"ResultID\" type=\"s:QName\"/>
      </s:complexType>

      <s:element name=\"BrowseResponse\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"BrowseResult\" type=\"s0:ReplyBase\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Elements\" type=\"s0:BrowseElement\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Errors\" type=\"s0:OPCError\"/>
          </s:sequence>
          <s:attribute name=\"ContinuationPoint\" type=\"s:string\"/>
          <s:attribute default=\"false\" name=\"MoreElements\" type=\"s:boolean\"/>
        </s:complexType>
      </s:element>

      <s:element name=\"GetProperties\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"ItemIDs\" type=\"s0:ItemIdentifier\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"PropertyNames\" type=\"s:QName\"/>
          </s:sequence>
          <s:attribute name=\"LocaleID\" type=\"s:string\"/>
          <s:attribute name=\"ClientRequestHandle\" type=\"s:string\"/>
          <s:attribute name=\"ItemPath\" type=\"s:string\"/>
          <s:attribute default=\"false\" name=\"ReturnAllProperties\" type=\"s:boolean\"/>
          <s:attribute default=\"false\" name=\"ReturnPropertyValues\" type=\"s:boolean\"/>
          <s:attribute default=\"false\" name=\"ReturnErrorText\" type=\"s:boolean\"/>
        </s:complexType>
      </s:element>

      <s:complexType name=\"ItemIdentifier\">
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ItemName\" type=\"s:string\"/>
      </s:complexType>

      <s:complexType name=\"PropertyReplyList\">
        <s:sequence>
          <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Properties\" type=\"s0:ItemProperty\"/>
        </s:sequence>
        <s:attribute name=\"ItemPath\" type=\"s:string\"/>
        <s:attribute name=\"ItemName\" type=\"s:string\"/>
        <s:attribute name=\"ResultID\" type=\"s:QName\"/>
      </s:complexType>

      <s:element name=\"GetPropertiesResponse\">
        <s:complexType>
          <s:sequence>
            <s:element maxOccurs=\"1\" minOccurs=\"0\" name=\"GetPropertiesResult\" type=\"s0:ReplyBase\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"PropertyLists\" type=\"s0:PropertyReplyList\"/>
            <s:element maxOccurs=\"unbounded\" minOccurs=\"0\" name=\"Errors\" type=\"s0:OPCError\"/>
          </s:sequence>
        </s:complexType>
      </s:element>

    </s:schema>
  </types>
  


  <message name=\"GetStatusSoapIn\">
    <part element=\"s0:GetStatus\" name=\"parameters\"/>
  </message>
  <message name=\"GetStatusSoapOut\">
    <part element=\"s0:GetStatusResponse\" name=\"parameters\"/>
  </message>
  <message name=\"ReadSoapIn\">
    <part element=\"s0:Read\" name=\"parameters\"/>
  </message>
  <message name=\"ReadSoapOut\">
    <part element=\"s0:ReadResponse\" name=\"parameters\"/>
  </message>
  <message name=\"WriteSoapIn\">
    <part element=\"s0:Write\" name=\"parameters\"/>
  </message>
  <message name=\"WriteSoapOut\">
    <part element=\"s0:WriteResponse\" name=\"parameters\"/>
  </message>
  <message name=\"SubscribeSoapIn\">
    <part element=\"s0:Subscribe\" name=\"parameters\"/>
  </message>
  <message name=\"SubscribeSoapOut\">
    <part element=\"s0:SubscribeResponse\" name=\"parameters\"/>
  </message>
  <message name=\"SubscriptionPolledRefreshSoapIn\">
    <part element=\"s0:SubscriptionPolledRefresh\" name=\"parameters\"/>
  </message>
  <message name=\"SubscriptionPolledRefreshSoapOut\">
    <part element=\"s0:SubscriptionPolledRefreshResponse\" name=\"parameters\"/>
  </message>
  <message name=\"SubscriptionCancelSoapIn\">
    <part element=\"s0:SubscriptionCancel\" name=\"parameters\"/>
  </message>
  <message name=\"SubscriptionCancelSoapOut\">
    <part element=\"s0:SubscriptionCancelResponse\" name=\"parameters\"/>
  </message>
  <message name=\"BrowseSoapIn\">
    <part element=\"s0:Browse\" name=\"parameters\"/>
  </message>
  <message name=\"BrowseSoapOut\">
    <part element=\"s0:BrowseResponse\" name=\"parameters\"/>
  </message>
  <message name=\"GetPropertiesSoapIn\">
    <part element=\"s0:GetProperties\" name=\"parameters\"/>
  </message>
  <message name=\"GetPropertiesSoapOut\">
    <part element=\"s0:GetPropertiesResponse\" name=\"parameters\"/>
  </message>
  
  <portType name=\"Service\">
    <operation name=\"GetStatus\">
      <input message=\"s0:GetStatusSoapIn\"/>
      <output message=\"s0:GetStatusSoapOut\"/>
    </operation>
    <operation name=\"Read\">
      <input message=\"s0:ReadSoapIn\"/>
      <output message=\"s0:ReadSoapOut\"/>
    </operation>
    <operation name=\"Write\">
      <input message=\"s0:WriteSoapIn\"/>
      <output message=\"s0:WriteSoapOut\"/>
    </operation>
    <operation name=\"Subscribe\">
      <input message=\"s0:SubscribeSoapIn\"/>
      <output message=\"s0:SubscribeSoapOut\"/>
    </operation>
    <operation name=\"SubscriptionPolledRefresh\">
      <input message=\"s0:SubscriptionPolledRefreshSoapIn\"/>
      <output message=\"s0:SubscriptionPolledRefreshSoapOut\"/>
    </operation>
    <operation name=\"SubscriptionCancel\">
      <input message=\"s0:SubscriptionCancelSoapIn\"/>
      <output message=\"s0:SubscriptionCancelSoapOut\"/>
    </operation>
    <operation name=\"Browse\">
      <input message=\"s0:BrowseSoapIn\"/>
      <output message=\"s0:BrowseSoapOut\"/>
    </operation>
    <operation name=\"GetProperties\">
      <input message=\"s0:GetPropertiesSoapIn\"/>
      <output message=\"s0:GetPropertiesSoapOut\"/>
    </operation>
  </portType>
  
  <binding name=\"Service\" type=\"s0:Service\">
    <soap:binding style=\"document\" transport=\"http://schemas.xmlsoap.org/soap/http\"/>

    <operation name=\"GetStatus\">
      <soap:operation soapAction=\"http://opcfoundation.org/webservices/XMLDA/1.0/GetStatus\" style=\"document\"/>
      <input>
        <soap:body use=\"literal\"/>
      </input>
      <output>
        <soap:body use=\"literal\"/>
      </output>
    </operation>

    <operation name=\"Read\">
      <soap:operation soapAction=\"http://opcfoundation.org/webservices/XMLDA/1.0/Read\" style=\"document\"/>
      <input>
        <soap:body use=\"literal\"/>
      </input>
      <output>
        <soap:body use=\"literal\"/>
      </output>
    </operation>

    <operation name=\"Write\">
      <soap:operation soapAction=\"http://opcfoundation.org/webservices/XMLDA/1.0/Write\" style=\"document\"/>
      <input>
        <soap:body use=\"literal\"/>
      </input>
      <output>
        <soap:body use=\"literal\"/>
      </output>
    </operation>

    <operation name=\"Subscribe\">
      <soap:operation soapAction=\"http://opcfoundation.org/webservices/XMLDA/1.0/Subscribe\" style=\"document\"/>
      <input>
        <soap:body use=\"literal\"/>
      </input>
      <output>
        <soap:body use=\"literal\"/>
      </output>
    </operation>

    <operation name=\"SubscriptionPolledRefresh\">
      <soap:operation soapAction=\"http://opcfoundation.org/webservices/XMLDA/1.0/SubscriptionPolledRefresh\" style=\"document\"/>
      <input>
        <soap:body use=\"literal\"/>
      </input>
      <output>
        <soap:body use=\"literal\"/>
      </output>
    </operation>

    <operation name=\"SubscriptionCancel\">
      <soap:operation soapAction=\"http://opcfoundation.org/webservices/XMLDA/1.0/SubscriptionCancel\" style=\"document\"/>
      <input>
        <soap:body use=\"literal\"/>
      </input>
      <output>
        <soap:body use=\"literal\"/>
      </output>
    </operation>

    <operation name=\"Browse\">
      <soap:operation soapAction=\"http://opcfoundation.org/webservices/XMLDA/1.0/Browse\" style=\"document\"/>
      <input>
        <soap:body use=\"literal\"/>
      </input>
      <output>
        <soap:body use=\"literal\"/>
      </output>
    </operation>

    <operation name=\"GetProperties\">
      <soap:operation soapAction=\"http://opcfoundation.org/webservices/XMLDA/1.0/GetProperties\" style=\"document\"/>
      <input>
        <soap:body use=\"literal\"/>
      </input>
      <output>
        <soap:body use=\"literal\"/>
      </output>
    </operation>

  </binding>

  <service name=\"Service\">
	<port binding=\"s0:Service\" name=\"Service\">
		<soap:address location=\"http://127.0.0.1:7000\"/>
	</port>
  </service>
</definitions>"""
  
