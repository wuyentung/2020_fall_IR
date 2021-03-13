#%%
import numpy as np
from copy import deepcopy
#%%
import requests

def lineNotifyMessage(token, msg):
  headers = {
      "Authorization": "Bearer " + token,
      "Content-Type" : "application/x-www-form-urlencoded"
  }

  payload = {'message': msg}
  r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
  return r.status_code
#%%
# run pa2 first to create similarity
# get similarity data
similarity = np.genfromtxt("similarity.csv", delimiter=',')
n = similarity.shape[0]
#%%
def adjust(queue, i, n, stored_index):
    ''' adaptive heap operation

    :param stored_index: list of where the data stored
    :param queue: [0,...,n-1], each store {"sim": , "index": , "stored_index": }
    :type queue: [{}, {}]
    :param i: node id
    :param n: size of tree
    :return: None
    '''
    x = queue[i]
    j = 2*i +1
    while j<=n-1 :
        if j<n-1:
            if queue[j]["sim"]<queue[j + 1]["sim"]:
                j = j+1
        if x["sim"] >= queue[j]["sim"]:
            break
        else:
            queue[(j-1) // 2] = queue[j]
            stored_index[queue[j]["index"]] = (j-1) // 2
            j = 2*j +1
    queue[(j-1) // 2] = x
    stored_index[x["index"]] = (j-1) // 2
    pass
    #     else:
    #         queue[(j-1) // 2]["sim"] = queue[j]["sim"]
    #         queue[(j-1) // 2]["index"] = queue[j]["index"]
    #         queue[j]["stored_index"] = (j-1) // 2
    #         j = 2*j +1
    # queue[(j-1) // 2]["sim"] = x["sim"]
    # queue[(j-1) // 2]["index"] = x["index"]
    # queue[x["stored_index"]] = (j-1) // 2
    # pass
#%%
def _adjust(queue, i, n, stored_index):
    ''' original heap operation

    :param stored_index:
    :param queue: [0,...,n-1]
    :param i: node id
    :param n: size of tree
    :return: None
    '''
    x = queue[i]
    # print(x)
    # iter = 1
    j = 2*i +1
    while j<= n-1 :
        # print(iter)
        # print(j)
        if j< n-1:
            if queue[j]<queue[j + 1]:
                j +=1
        if x >= queue[j]:
            break
        else:
            # print("before swap ", queue)
            print("before swap ", stored_index)
            queue[(j-1) // 2] = queue[j]
            print(stored_index[queue[j]], queue[j])
            stored_index[queue[j]] = (j-1) // 2
            # print("after swap ", queue, "\n")
            print("after swap ", stored_index, "\n")
            j =2*j +1
        # print(queue[j // 2], x, j)
        # iter += 1
    # print((j-1) // 2)
    queue[(j-1) // 2] = x
    stored_index[x] = (j-1) // 2
    pass
def build(queue, n, stored_index, test=False):
    '''

    :param stored_index:
    :param queue: [0,...,n-1]
    :param n: size of tree
    :return: None
    '''
    half_n = np.arange(n//2)
    re_n = n//2 - half_n -1
    if test:
        for i in re_n:
            # print(i)
            # print("BEFORE modify place ", i, ", so called: ", queue[i])
            # print(queue)
            _adjust(queue, i, n, stored_index)
            # _adjust(queue, i, n - 1)
            # print("AFTER modify place ", i, ", so called: ", queue[i])
            # print(queue)
            # print("---------\n\n")
        return
    for i in re_n:
        # print(i)
        # print("BEFORE modify place ", i, ", so called: ", queue[i])
        # print(queue)
        adjust(queue, i, n, stored_index)
        # _adjust(queue, i, n - 1)
        # print("AFTER modify place ", i, ", so called: ", queue[i])
        # print(queue)
        # print("---------\n\n")
    pass

#%%
def _pop_item(queue, i, n, stored_index):
    ''' origin pop item in heap

    :param i: index of queue to pop
    :param queue: [0,...,n-1]
    :param n: size of tree
    :return: queue[i] before pop
    '''
    if i >= n:
        raise IndexError("what you wanna pop is out of index")
    x = queue[i]
    stored_index[queue[i]] = n-1

    queue[i] = queue[n-1]
    queue[n-1] = x
    stored_index[queue[i]] = i

    n -=1
    _adjust(queue, i, n, stored_index)
    return x
#%%
def pop_item(queue, i, n, stored_index):
    '''

    :param stored_index:
    :param i: index of queue to pop
    :param queue: [0,...,n-1], each store {"sim": , "index": }
    :type queue: [{}, {}]
    :param n: size of tree
    :return: queue[i] before pop
    '''
    if i >= n:
        raise IndexError("what you wanna pop is out of index")
    x = queue[i]
    stored_index[queue[i]["index"]] = n-1
    queue[i] = queue[n-1]
    stored_index[queue[i]["index"]] = i
    n -=1
    adjust(queue, i, n, stored_index)
    return x
#%%
def _insert(queue, n, item, stored_index):
    ''' origin insert in heap

    :param queue: [0,...,n-1]
    :type queue: list
    :param n: size of tree
    :type n: int
    :param item:
    :return:
    '''
    queue.append(item)
    n +=1
    child_no = n-1
    parent_no = (child_no-1)//2
    while 1:
        if queue[parent_no] >= item:
            break
        else:
            queue[child_no] = queue[parent_no]
            stored_index[queue[child_no]] = child_no
            child_no = (child_no-1)//2
            if child_no == 0:
                break
            parent_no = (child_no-1)//2
    queue[child_no] = item
    stored_index.append(child_no)
    pass
#%%
def insert(queue, n, item, stored_index):
    ''' adaptive insert in heap

    :param stored_index:
    :param queue: [0,...,n-1], each store {"sim": , "index": }
    :type: [{}, {}]
    :param n: size of tree
    :type n: int
    :param item:
    :type: [{}, {}]
    :return:
    '''
    queue.append(item)
    n +=1
    child_no = n-1
    parent_no = (child_no-1)//2
    while 1:
        if queue[parent_no]["sim"] >= item["sim"]:
            break
        else:
            queue[child_no] = queue[parent_no]
            stored_index[queue[child_no]["index"]] = child_no
            child_no = (child_no-1)//2
            if child_no == 0:
                break
            parent_no = (child_no-1)//2
    queue[child_no] = item
    stored_index[item["index"]] = child_no
    pass
#%%
d = 8
q = np.arange(d).tolist()
qid = np.arange(d).tolist()
qlen = d
build(q, d, qid, test=True)
print("t: ", q)
print("tid: ", qid)
#%%
_pop_item(q, 4, qlen, qid)
qlen -=1
#%%
_insert(q, qlen, 8, qid)
qlen +=1
#%%
test = []
print(q)
for i in range(qlen):
    test.append(q[qid[i]])
print(test)
print(qid)
#%%
# let's start
c_sim = np.copy(similarity)
c_index = np.full((n, n), np.arange(n))
stored_index = np.full((n, n), np.arange(n))
merge_flag = [1] *n
merge_dict = {}
# use dict to store cluster
for i in range(n):
    merge_dict[i] = [i]


queue = []
queue_len = []
c = 0
for i in c_sim:
    queue.append([])
    cc = 0
    for j in i:
        queue[c].append({"sim": j,
                         "index": cc})
        # queue[n][0] -> priorityQ of c_sim[n]
        # queue[n][1] -> index of c[n][i]
        cc += 1
    c +=1

# build priorityQ
for i in range(n):
    build(queue[i], n, stored_index[i])
    pop_item(queue[i], stored_index[i][i], n, stored_index[i])
    queue_len.append(n-1)

# #%%
# for i in range(20):
#     print(stored_index[0][i])
#     pop_item(queue[0], i=0, n=queue_len[0], stored_index=stored_index[0])
#     queue_len[0] -=1
#     print(queue_len[0])
#     print(queue[0][0])

# argmax
def argmax_index(queue):
    '''

    :param queue:
    :type: [{},{}]
    :return:
    :rtype: dict
    '''
    for i in range(n):
        if merge_flag[i]:
            local_max = queue[i][0]
            local_max_index = i
    for i in range(n):
        if merge_flag[i]:
            if local_max["sim"] < queue[i][0]["sim"]:
                local_max = queue[i][0]
                local_max_index = i
            # print(len(queue[0]))
    return local_max_index

def get_place(queue, index):
    '''

    :param queue:
    :param index:
    :return:
    '''
    for i in range(len(queue)):
        if queue[i]["index"] == index:
            return i
    raise IndexError
# k = 0
cluster = {8:{},
           13:{},
           20:{}}
merge_record = []
for _ in range(n-1):
    max_index = argmax_index(queue)
    max_index_max_index = queue[max_index][0]["index"]
    k1 = max_index
    k2 = max_index_max_index
    if queue[k1][0]["index"] != k2:
        raise IndexError("iter ", _, "found", "k1= ", k1, ", k2= ", k2, "k1, k2 should be the same\n")
    if k1 > k2:
        # print("here")
        # print("k1= ", k1, ", k2= ", k2)
        k1 = max_index_max_index
        k2 = max_index
        # break
    merge_dict[k1] += merge_dict[k2]
    merge_record.append([k1, k2])
    if not merge_flag[k1]:
        print(False)
        break
    if not merge_flag[k2]:
        print(False)
    merge_flag[k2] = 0
    queue[k1] = []
    queue_len[k1] = 0
    stored_index[k1] = stored_index[k1] *0
    # print("k1= ", k1, ", k2= ", k2)
    # print("merge_flag[k1]", merge_flag[k1])
    # print("merge_flag[k2]", merge_flag[k2])
    # print("merge_dict[k1]: ", merge_dict[k1])
    # print()

    # re_index all stored_index[k1]
    for index in range(n):
        if merge_flag[index] and index != k1:
            # print("index= ", index)
            # pop_item(queue[index], i=stored_index[index][k1], n=queue_len[index], stored_index=stored_index[index])
            pop_item(queue[index], i=get_place(queue[index], k1), n=queue_len[index], stored_index=stored_index[index])
            queue_len[index] -=1
            # print("queue[index][0]", queue[index][0])
            # pop_item(queue[index], i=stored_index[index][k2], n=queue_len[index], stored_index=stored_index[index])
            pop_item(queue[index], i=get_place(queue[index], k2), n=queue_len[index], stored_index=stored_index[index])
            queue_len[index] -=1
            # print("queue[index][0]", queue[index][0])

            if c_sim[index][k1] <= c_sim[index][k2]:
                bigger_sim = c_sim[index][k1]
                bigger_sim_id = k1
            else:
                bigger_sim = c_sim[index][k2]
                bigger_sim_id = k2

            c_sim[index][k1] = c_sim[k1][index] = bigger_sim

            # print("c_sim[index][k1]", c_sim[index][k1], bigger_sim_id)
            insert(queue=queue[index], n=queue_len[index], item={"sim": c_sim[index][k1], "index": k1}, stored_index=stored_index[index])
            queue_len[index] +=1
            # print("queue[index][0]", queue[index][0])
            insert(queue=queue[k1], n=queue_len[k1], item={"sim": c_sim[index][k1], "index": index}, stored_index=stored_index[k1])
            queue_len[k1] +=1
            # print("queue[k1][0]", queue[k1][0])
            # print()
    # print("queue[k1]: ", len(queue[k1]), queue[k1])
    # print("\n----------------------------------\n")
    if sum(merge_flag) in cluster:
        c=0
        for index in range(n):
            if merge_flag[index]:
                # print("Remaining cluster:")
                # print("cluster ", c, ": ", merge_dict[index])
                cluster[sum(merge_flag)][c] = deepcopy(merge_dict[index])
                c += 1
    if sum(merge_flag) == 8:
        print("meet 8 cluster")
        break

print("run total iter: ", _+1)
message = "實驗室網路復活"
token = 'CCgjmKSEGamkEj9JvhuIkFNYTrpPKHyCb1zdsYRjo86'
lineNotifyMessage(token, message)
#%%
print(cluster)

#%%
for cluster_cat, clustered_data in cluster.items():
    for index, key in clustered_data.items():
        key.sort()
for index, key in cluster[13].items():
    print(index, key)
#%%
t = [1, 2, 3]
tt = [5, 6, 8]
data=open("data.txt",'w+')
for item in t:
    print(item+1, file=data)
print("", file=data)
for item in tt:
    print(item, file=data)
data.close()
#%%
for cluster_cat, clustered_data in cluster.items():
    data = open("%d.txt" % cluster_cat, "w+")
    for index, value in clustered_data.items():
        for file_id in value:
            print(file_id+1, file=data)
        print("", file=data)
    data.close()


