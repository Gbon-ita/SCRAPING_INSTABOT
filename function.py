def str_to_numeric(a):
	b=[]
	for i in a:
		if i!='.':
			b.append(i)
	b= ''.join(b)
	b=int(b)
	return(b)
import json
import pickle
import os
def load_file(user,file_name):
    folder_path = './{}'.format(user)
    pickle_in = open("{}/{}".format(folder_path,file_name),'rb')
    var = pickle.load(pickle_in)
    return var



def save_file(File,user,file_name):
    folder_path = './{}'.format(user)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    pickle_out = open("{}/{}".format(folder_path,file_name),'wb')
    pickle.dump(File,pickle_out)
    pickle_out.close()


def save_dict(File,user,file_name):
    folder_path = './{}'.format(user)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    with open('{}/{}.pickle'.format(folder_path,file_name), 'wb') as handle:
        pickle.dump(File, handle, protocol=pickle.HIGHEST_PROTOCOL)

def save_dict_json(File,user,file_name):
    folder_path = './{}'.format(user)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    J = json.dumps(File)
    f = open('{}/{}.json'.format(folder_path,file_name),'w')
    f.write(J)
    f.close()
