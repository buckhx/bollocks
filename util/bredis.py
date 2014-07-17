import redis

get_redis = lambda: redis.from_url('redis://root:cfc589ce87e789ee055b4d7d83da6e9e@107.170.116.125:6379?db=1')
conn = get_redis()

defn_key = lambda word: "def$:"+word.lower().replace(" ","_")
slurp = lambda defn: conn.hmset(defn_key(defn['name']), defn)
