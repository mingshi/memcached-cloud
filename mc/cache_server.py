
import memcache
from pprint import pprint

class Client(memcache.Client):
    def get_stats(self, args = None):
        result = super(Client, self).get_stats(args)

        if (args == 'slabs') :
            _result = {}
            for i  in range(0, len(result)) :
                slabs = {}
                slab_result = result[i][1]
                for s in slab_result :
                    pos = s.find(':')
                    if pos == -1 :
                        slabs[s] = slab_result[s]
                    else :
                        slab_id  = s[:pos]
                        slab_key = s[pos+1:]
                        if not slabs.has_key(slab_id) :
                            slabs[slab_id] = {}
                        slabs[slab_id][slab_key]= slab_result[s]

                _result[i] = slabs

            return _result

        return result;

    def reset_stats(self) :
        for s in self.servers :
            s.send_cmd('stats reset')
            s.expect('RESET')

    def get_key_prefix(self, slab_id) :
        result = self.get_stats('slabs')
        slab_id = str(slab_id)
        slabs = result[0]
        if not slabs.has_key(slab_id) :
            return None

        slab_info = slabs[slab_id]
        items_count = slab_info['total_chunks']
        if int(items_count) <=0 :
            print slab_info['total_chunks']
            return None

        items = self.get_stats('cachedump ' + str(slab_id) + ' ' + str(items_count))

        common_keys = []
        tmp_prefix = None
        last_k = None
        #pprint(items[0][1])
        for k in items[0][1] :
            pos = k.rfind(':')
            if pos == -1 :
                pos = k.rfind('_')

            if pos != -1 :
                tmp_prefix = k[:pos]
                try :
                    common_keys.index(tmp_prefix)
                except Exception, e :
                    common_keys.append(tmp_prefix)

                last_k = k
                continue

            
            if last_k == None :
                last_k = k
                continue

            len0 = len(last_k)
            _len = len0/2
            pos = k.find(last_k[:_len])
            if pos == -1:
                while pos == -1 and _len > 1:
                    _len -= 1
                    pos = k.find(last_k[:_len])
            else :
                while pos != -1 and _len <= len0 :
                    _len += 1
                    pos = k.find(last_k[:_len])

            if _len != 0:
                tmp_prefix = last_k[:_len]
                    


            print k
            last_k = k

        print common_keys





if __name__ == '__main__' :
    mc = Client(['localhost:11211'])
    #mc = Client(['10.10.3.24:11211'])
    #mc.get_key_prefix(4)

    pprint(mc.get_stats('slabs'))


    #pprint(mc.get_stats('cachedump 1 10'))

