
import memcache
#from pprint import pprint

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

    def _recv_value(self, server, flags, rlen):
        rlen += 2 # include \r\n
        buf = server.recv(rlen)
        if len(buf) != rlen:
            raise _Error("received %d bytes when expecting %d"
                    % (len(buf), rlen))

        if len(buf) == rlen:
            buf = buf[:-2]  # strip \r\n

        if flags & Client._FLAG_COMPRESSED:
            buf = decompress(buf)

        if  flags == 0 or flags == Client._FLAG_COMPRESSED:
            # Either a bare string or a compressed string now decompressed...
            val = buf
        elif flags & Client._FLAG_INTEGER:
            val = int(buf)
        elif flags & Client._FLAG_LONG:
            val = long(buf)
        elif flags & Client._FLAG_PICKLE:
            try:
                file = StringIO(buf)
                unpickler = self.unpickler(file)
                if self.persistent_load:
                    unpickler.persistent_load = self.persistent_load
                val = unpickler.load()
            except Exception, e:
                return buf
        else:
            self.debuglog("unknown flags on get: %x\n" % flags)

        return val


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

        #common_keys = []
        common_keys = {}
        tmp_prefix = None
        last_k = None


        #pprint(items[0][1])
        for k in items[0][1] :

            # first get string before :or_
            pos = k.rfind(':')
            if pos == -1 :
                pos = k.rfind('_')

            # if find string prefix
            if pos != -1 :
                tmp_prefix = k[:pos]

                if common_keys.has_key(tmp_prefix) :
                    common_keys[tmp_prefix] += 1
                else :
                    common_keys[tmp_prefix] = 1

                last_k = k
                continue

            
            if last_k == None :
                last_k = k
                continue

            if tmp_prefix != None and k.find(tmp_prefix) != -1:
                if common_keys.has_key(tmp_prefix) :
                    common_keys[tmp_prefix] += 1
                else :
                    common_keys[tmp_prefix] = 1
                continue

            find_prefix = False
            for prefix in common_keys.keys() :
                if k.find(prefix) != -1:
                    common_keys[prefix] += 1
                    find_prefix = True
                    break

            if find_prefix :
                continue

            #find the common prefix of last key and key
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

            # finded
            if _len != 0:
                tmp_prefix = last_k[:_len]
                if common_keys.has_key(tmp_prefix) :
                    common_keys[tmp_prefix] += 1
                else :
                    common_keys[tmp_prefix] = 1
            else :
                common_keys[last_k] = 1
                common_keys[k] = 1

            last_k = k

        return common_keys




#if __name__ == '__main__' :
    #mc = Client(['localhost:11211'])
    #mc = Client(['10.10.3.24:11211'])
    #mc.get_key_prefix(4)

    #pprint(mc.get_stats('slabs'))


    #pprint(mc.get_stats('cachedump 1 10'))

