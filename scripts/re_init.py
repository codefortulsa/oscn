
import oscn


cc=oscn.request.Case('adair-CM-2018-123')

cc_data={'index':cc.index, 'text':cc.text, 'source':cc.source}


new_cc=oscn.request.Case(**cc_data)

import ipdb; ipdb.set_trace()
