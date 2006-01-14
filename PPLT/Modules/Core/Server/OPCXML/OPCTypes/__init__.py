import ZSI;


#
# Import types:
#
from ArrayOfAnyType import *			#done 
from ArrayOfBoolean import *			#done
from ArrayOfByte import *				#done
from ArrayOfDateTime import *			#done
from ArrayOfDecimal import *			#done
from ArrayOfDouble import *				#done
from ArrayOfFloat import *				#done 
from ArrayOfInt import *				#done
from ArrayOfLong import *				#done
from ArrayOfShort import *				#done
from ArrayOfString import *				#done
from ArrayOfUnsignedInt import *		#done
from ArrayOfUnsignedLong import *		#done
from ArrayOfUnsignedShort import *		#done
from BrowseElement import *				#done
from BrowseFilter import *				#done
from Browse import *					#done
from BrowseResponse import *			#done
from GetProperties import *				#done
from GetPropertiesResponse import *
from GetStatus import *
from GetStatusResponse import *
from interfaceVersion import *
from ItemIdentifier import *
from ItemProperty import *
from ItemValue import *
from LimitBits import *
from OPCError import *
from OPCQuality import *
from PropertyReplyList import *
from QualityBits import *
from Read import *
from ReadRequestItemList import *
from ReadRequestItem import *
from ReadResponse import *
from ReplyBase import *
from ReplyItemList import *
from RequestOptions import *
from serverState import *
from ServerStatus import *
from SubscribeItemValue import *
from SubscribePolledRefreshReplyItemList import *
from Subscribe import *
from SubscribeReplyItemList import *
from SubscribeRequestItemList import *
from SubscribeResponse import *
from SubscriptionCancel import *
from SubscriptionCancelResponse import *
from SubscriptionPolledRefresh import *
from SubscriptionPolledRefreshResponse import *
from SubscribeRequestItem import *
from Write import *
from WriteRequestItemList import *
from WriteResponse import *

targetNamespace = 'http://opcfoundation.org/webservices/XMLDA/1.0/'



def rename(name): return("_"+name);

