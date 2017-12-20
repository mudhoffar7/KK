import sys, math, random, csv, types
import copy
import operator
import random
from random import randrange

class KMeans:
    def __init__(self, filename, k):
        self.data, self.restrictions = self.parse_vectors(filename)
        self.k = k
        self.centroids = self.initial_centroids(self.data, self.k)
        self.clusters = list()

    def parse_vectors(self, filename):
        reader = csv.reader(open(filename, 'r'), delimiter=',')
        vectors=[]
        restrictions=[]

        for row_ct, row in enumerate(reader):
            if row_ct > 0:
                new_row = dict()
                new_row["cluster"] = 0
                if int(restrictions[0]) == 0:
                    new_row["key"] = row[0]
                new_row["val"] = tuple([x for i, x in enumerate(row) if i < len(restrictions) and int(restrictions[i]) == 1 and len(x.strip())>=1])
                vectors.append(new_row)    
            else:
                restrictions.extend(row)

        return vectors, restrictions

    def initial_centroids(self, data, k):
        # initialize c (initial centroid) to 0
        row_len = len(data[0]['val'])
        c = [0 for i in range(row_len)]

        for point in data:
            for ndx, val in enumerate(c):
                c[ndx] += float(point['val'][ndx])

        for i in range(row_len):
            c[i] = c[i]/len(data)

        centroids = []
        
        for m in range(int(k)):
            maxdist = 0
            maxndx = 0
            for ndx, point in enumerate(data):
                if len(centroids) > 0:
                    if not any(d.get('val') == point['val'] for d in centroids):
                        dist = self.distance(point['val'], centroids[m-1]['val'])
                else:
                    dist = self.distance(point['val'], c)

                if maxdist < dist:
                    maxdist = dist
                    maxndx = ndx
                    
            cluster = dict()
            cluster['cluster'] = m
            cluster['val'] = data[maxndx]['val']
            centroids.append(cluster)
            
        #print 'Initial Centroid: ', centroids
        return centroids

    def cluster(self):
        change = True

        while change:
            change = False

            for i, point in enumerate(self.data):
                # find the closest centroid
                closest_cluster = self.closest(point)
                if closest_cluster != point['cluster']:
                    change = True
                    self.data[i]['cluster'] = closest_cluster
            
            if change:
                self.recalc_centroids()

        for centroid in self.centroids:
            if 'key' in self.data[0]:
                cluster_points = ([(x['key'], x['val']) for x in self.data if x['cluster'] == centroid['cluster']])
            else:
                cluster_points = ([x['val'] for x in self.data if x['cluster'] == centroid['cluster']])
            self.clusters.append(cluster_points)

        return self.clusters

    def recalc_centroids(self):
        row_len = len(self.data[0]['val'])
        c = [[0 for i in range(row_len)] for j in range(self.k)]
        for point in self.data:
            cluster_ndx = point['cluster']
            for ndx, val in enumerate(c[cluster_ndx]):
                c[cluster_ndx][ndx] += float(point['val'][ndx])

        for cluster_ndx, x in enumerate(c):
            cluster_count = len([d for d in self.data if d['cluster']==cluster_ndx])
            if cluster_count != 0:
                for i in range(row_len):
                    c[cluster_ndx][i] = c[cluster_ndx][i]/cluster_count
        
        for i, centroid in enumerate(self.centroids):
            self.centroids[i]['val'] = c[i]
           
        #print self.centroids

    def distance(self, v1, v2):
        if len(v1) != len(v2): 
           print 'Error can not compute distance between unequal vector lengths.'
           return
        else:
           total = 0
           for i in range(len(v1)):
              val = float(v1[i]) - float(v2[i])
              val = val * val
              total += val
           return math.sqrt(total)

    def closest(self, point):
        minDist = sys.maxint
        minCluster = -1
        for ndx, cluster in enumerate(self.centroids):
            dist = self.distance(cluster['val'], point['val'])
            if minDist > dist:
                minDist = dist
                minCluster = cluster['cluster']

        return minCluster

def loadDataset(filename,k,dataSet=[]):
    set = []
    with open(filename,'rb') as csvfile:
        lines=csv.reader(csvfile)
        dataset=list(lines)
        normalize(dataset)
        banyak=len(dataset)/k
        mulai=0 
        for x in range(len(dataset)):
            for y in range(len(dataset[x])-1):#kalau gakada kelasnya seperti Iris-virginica hapus -1nya
                dataset[x][y]=float(dataset[x][y])
            dataset[x].append(0)#buat kelas baru
            dataSet.append(dataset[x])
        return set

def loadDataset2(filename,k,centroid=[]):
    with open(filename,'rb') as csvfile:
        lines=csv.reader(csvfile)
        dataset=list(lines)
        normalize(dataset)
        banyak=len(dataset)/k
        mulai=0 
        for x in range(k):
            if x==k-1:
                z=dataset[len(dataset)-1]
            else:
                z=dataset[mulai]
            for y in range(len(z)-1):#kalau gakada kelasnya seperti Iris-virginica hapus -1nya
                z[y]=float(z[y])
            z.append(0)#buat kelas baru
            centroid.append(z)
            mulai=mulai+banyak

def normalize(dataset):
    for m in range(len(dataset[0]) - 1):
        temp = []
        for n in range(len(dataset)):
            temp.append(float(dataset[n][m]))
        minimal = min(temp)
        maksimal = max(temp)
        for o in range(len(dataset)):
            if maksimal - minimal == 0:
                dataset[o][m] = temp[o]
            else:
                dataset[o][m] = (temp[o] - minimal) / (maksimal - minimal)

def carijarak(dataset,centroid):
    distance=0
    distance=int(distance)
    #print "---------hitungmulai-------"
    for x in range(len(dataset)-2):#ganti -1 kalau gakada kelas seperti Iris-virginica
        dif=dataset[x]-centroid[x]
        #print dataset[x]
        #print centroid[x]
        distance=distance+(dif*dif)
    #print "--------hitungakhir--------"
    return math.sqrt(distance)

def carikelas(dataset,k,centroid):
    terpendek=9223372036854775807
    kelas=0
    for y in range(k):
        a=carijarak(dataset,centroid[y])
        #print a
        if a<terpendek:
            terpendek=a
            kelas=y+1
            #print a
    #print "kelas"
    return kelas

def printdataset(dataset):
    for x in range(len(dataset)):
        print dataset[x]

def updatecentroid(dataset,k,centroid=[]):

    awal=[]
    for x in range(k):
        for y in range(len(centroid[x])):
            centroid[x][y]=0
    atribut=len(dataset[0])
    #print atribut
    for x in range(len(dataset)):#mencari jumlah total atribut
        kls=dataset[x][atribut-1]
        for y in range(atribut-2):#ganti -1 kalau gak ada kelas
            centroid[kls-1][y]=centroid[kls-1][y]+dataset[x][y]
        centroid[kls-1][atribut-1]=centroid[kls-1][atribut-1]+1#terakhir sendiri
    for x in range(k):#mencari jumlah rata-ratanya
        for y in range(atribut-2):#ganti -1 kalau gak ada kelas
            centroid[x][y]=centroid[x][y]/centroid[x][atribut-1]

#ini KNN

# memuat dataset

 
# membagi dataset untuk cross validation
def cross_validation_split(dataset, jumlah_bagian):
    dataset_split = list()
    dataset_copy = list(dataset)
    ukuran_bagian = int(len(dataset) / jumlah_bagian)
    for i in range(jumlah_bagian):
        bagian = list()
        while len(bagian) < ukuran_bagian:
            index = randrange(len(dataset_copy))
            bagian.append(dataset_copy.pop(index))
        dataset_split.append(bagian)
    return dataset_split
 
#Menghitung akurasi
def akurasi(aktual, diprediksi):
    benar = 0
    for i in range(len(aktual)):
        if aktual[i] == diprediksi[i]:
            benar += 1  
    return benar / float(len(aktual)) * 100.0
    
#Menghitung precision
def precision(aktual, diprediksi, class2):
    jumlah_precision = 0.0
    for class1 in class2:
        class_benar = prediksi_benar = 0
        class_precision = 0.0
        for i in range(len(aktual)):
            if class1 == diprediksi[i]:
                class_benar += 1
                if aktual[i] == diprediksi[i]:
                    prediksi_benar += 1 
        if class_benar > 0:
            class_precision = float(prediksi_benar/float(class_benar)) * 100.0
        print('      - ' + str(class1) + ' = ' + str(class_precision) + '%')
        jumlah_precision += class_precision
    return jumlah_precision/float(len(class2))
    

#Menghitung recall
def recall(aktual, diprediksi, class2):
    jumlah_recall = 0.0
    for class1 in class2:
        class_benar = prediksi_benar = 0
        class_recall = 0.0
        for i in range(len(aktual)):
            if class1 == aktual[i]:
                class_benar += 1
                if class1 == diprediksi[i]:
                    prediksi_benar += 1 
        if class_benar > 0:
            class_recall = float(prediksi_benar/float(class_benar)) * 100.0
        print('      - ' + str(class1) + ' = ' + str(class_recall) + '%')
        jumlah_recall += class_recall
    return jumlah_recall/float(len(class2))
    
    
 
# Cross validation
def jalankan_algoritma(dataset, algoritma, jumlah_bagian, *args):
    bagian2 = cross_validation_split(dataset, jumlah_bagian)
    class_val = list(set(row[-1] for row in dataset))
    akurasi_bagian = 0.0
    precision_bagian = 0.0
    recall_bagian = 0.0
    i = 0
    for bagian in bagian2:
        train_set = list(bagian2)
        train_set.remove(bagian)
        train_set = sum(train_set, [])
        test_set = list()
        for row in bagian:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[-1] = None
        diprediksi = algoritma(train_set, test_set, *args)
        aktual = [row[-1] for row in bagian]
        persentasi_akurasi = akurasi(aktual, diprediksi)
        i += 1
        print('\n   >> Hasil ke-' + str(i) + ' : ')
        print('    - Akurasi = ' + str(persentasi_akurasi) + '%')
        print('    - Precision : ')
        persentasi_precision =  precision(aktual, diprediksi, class_val)
        print('    - Recall : ')
        persentasi_recall = recall(aktual, diprediksi, class_val)
        akurasi_bagian += persentasi_akurasi
        precision_bagian += persentasi_precision
        recall_bagian += persentasi_recall
    print('\n   >>> Akurasi rata-rata: %f%%' % (akurasi_bagian/float(len(bagian2))))
    print(' >>> Precision rata-rata: %f%%' % (precision_bagian/float(len(bagian2))))
    print(' >>> Recall rata-rata: %f%%' % (recall_bagian/float(len(bagian2))))
 
# membagi dataset berdasarkan atribut pada kolom
def test_split(index, atribut, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] < atribut:
            left.append(row)
        else:
            right.append(row)
    return left, right
 
# Menghitung GINI index
def gini_index_get(grup2_child, classes):
    # menghitung banyak data dari split yang dilakukan  
    banyak_record = float(sum([len(grup_child) for grup_child in grup2_child]))
    gini = 0.0
    for grup_child in grup2_child:
        ukuran_grup = float(len(grup_child))
        # menghindari pembagian nol
        if ukuran_grup == 0:
            continue
        gini2 = 0.0
        # menghitung GINI index dari tiap kelas
        for class_val in classes:
            p = [row[-1] for row in grup_child].count(class_val) / ukuran_grup
            gini2 += p * p
        # menghitung GINI split
        gini += (1.0 - gini2) * (ukuran_grup / banyak_record)
    return gini
 
# mencari GINI split terbaik
def get_split_gini(dataset):
    class_values = list(set(row[-1] for row in dataset))
    gini_index, gini_value, gini, gini_grup2_child = 999, 999, 999, None
    for index in range(len(dataset[0])-1):
        for row in dataset:
            grup2_child = test_split(index, row[index], dataset)
            temp_gini = gini_index_get(grup2_child, class_values)
            if temp_gini < gini:
                gini_index, gini_value, gini, gini_grup2_child = index, row[index], temp_gini, grup2_child
    return {'index':gini_index, 'value':gini_value, 'grup2_child':gini_grup2_child}
 
# membuat leaf node
def leaf_node(grup_child):
    value = [row[-1] for row in grup_child]
    return max(set(value), key=value.count)
 
# membuat child split untuk mencari leaf node
def split(node, dalam_maks, ukuran_min, dalam, mode):
    left, right = node['grup2_child']
    del(node['grup2_child'])
    # memeriksa apakah ada split
    if not left or not right:
        node['left'] = node['right'] = leaf_node(left + right)
        return
    # memeriksa kedalaman tree maksimum
    if dalam >= dalam_maks:
        node['left'], node['right'] = leaf_node(left), leaf_node(right)
        return
    # membuat left child
    if len(left) <= ukuran_min:
        node['left'] = leaf_node(left)
    else:
        node['left'] = get_split_mode(left, mode)
        split(node['left'], dalam_maks, ukuran_min, dalam+1, mode)
    # membuat right child
    if len(right) <= ukuran_min:
        node['right'] = leaf_node(right)
    else:
        node['right'] = get_split_mode(right, mode)
        split(node['right'], dalam_maks, ukuran_min, dalam+1, mode)
 

# menjalankan split berdasarkan mode yang dipilih
def get_split_mode(train, mode):
    if mode == 1:
        return get_split_gini(train)
    elif mode == 2:
        return get_split_gain(train)
    else:
        return get_split_me(train)
 
# membuat decision tree
def buat_tree(train, dalam_maks, ukuran_min, mode):
    root = get_split_mode(train, mode)
    split(root, dalam_maks, ukuran_min, 1, mode)
    return root
 
# melakukan prediksi dengan decision tree
def prediksikan(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return prediksikan(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return prediksikan(node['right'], row)
        else:
            return node['right']
 
# menjalankan algoritma Classification and Regression Tree 
def decision_tree(train, test, dalam_maks, ukuran_min, mode):
    tree = buat_tree(train, dalam_maks, ukuran_min, mode)
    prediksi2 = list()
    for row in test:
        prediksi = prediksikan(tree, row)
        prediksi2.append(prediksi)
    return(prediksi2)

def main():
	threshold = 0

	if len(sys.argv) > 3 or len(sys.argv) < 2:
		print "Usage: python kmeans.py <filename> num_clusters"
		return    

	if len(sys.argv) == 3:
		numClusters = int(sys.argv[2])
		
	filename = sys.argv[1]

	kmeans = KMeans(sys.argv[1], numClusters)
	clusters = kmeans.cluster()

	for i, cluster in enumerate(clusters):
		print "Cluster "+str(i+1)+":"
		centroid = kmeans.centroids[i]['val']
		print "Center: ", centroid
		print "Num Points: ", len(cluster)
		print "Points: "
		maxdist = 0
		mindist = sys.maxint
		avgdist = 0
		for point in cluster:
			if type(point[1]) == tuple: 
				distance = kmeans.distance(centroid, point[1])
			else:
				distance = kmeans.distance(centroid, point)

			print point, ", distance=", distance
			avgdist += distance
			if distance > maxdist:
				maxdist = distance
			if distance < mindist:
				mindist = distance
		
		print "Max distance: ", maxdist
		print "Min distance: ", mindist
		print "Avg distance: ", avgdist/len(cluster), "\n"
		
	k=numClusters
	#print k
	dataset=[]
	centroid=[]
	loadDataset('iris2.data',k,dataset)
	#######################Membuat K Means############################################
	loadDataset2('iris2.data',k,centroid)
	#printdataset(centroid)

	for x in range(len(dataset)):
		#print "---------mulai--------------"
		kelas=carikelas(dataset[x],k,centroid)
		dataset[x][len(dataset[x])-1]=kelas
		#print kelas
		#print "----------Akhir-------------"
	#print len(dataset)


	updatecentroid(dataset,k,centroid)#mengupdate centroid
	#print "==============dataset=============="
	#printdataset(dataset)
	#print "centroid"
	#printdataset(centroid)
	while True:
		cek=1#udah konfergen belum
		for x in range(len(dataset)):
			#print "---------mulai--------------"
			kelas=carikelas(dataset[x],k,centroid)
			if dataset[x][len(dataset[x])-1]!=kelas:
				cek=0
			dataset[x][len(dataset[x])-1]=kelas
			#print kelas
			#print "----------Akhir-------------"
		updatecentroid(dataset,k,centroid)#mengupdate centroid
		#printdataset(centroid)
		if cek==1:
			#print "Sudah Konfergen"
			break
		#input()
	#print "===================Data Baru Setelah K Means============================"
	#printdataset(dataset)
	##################################Akhir K Means########################################
	testset=[]
	trainingset=[]
	predictions=[]
	#splitx(testset,trainingset,dataset)
	#print len(testset)
	mode = 1
	while True:
		if mode in [1]:
			break
	bagian = input('\n  > Masukkan banyak pembagian dari database untuk cross validation: ')
	while True:
		if bagian < 2:
			bagian = input('\n  Bagian harus lebih dari 1.\n\n  > Masukkan banyak pembagian dari database untuk cross validation: ')
		else:
			break
	dalam_maks = input('\n  > Masukkan kedalaman maksimum dari decision tree yang ingin digunakan : ')
	ukuran_min = input('\n  > Masukkan jumlah minimum record dari tiap leaf node dari decision tree yang ingin digunakan : ')
	while True:
		if dalam_maks < 1 or ukuran_min < 1:
			print('\n   Harus lebih dari 0.')
			dalam_maks = input('\n  > Masukkan kedalaman maksimum dari decision tree yang ingin digunakan : ')
			ukuran_min = input('\n  > Masukkan jumlah minimum record dari tiap leaf node dari decision tree yang ingin digunakan : ')
		else:
			break
	jalankan_algoritma(dataset, decision_tree, bagian, dalam_maks, ukuran_min, mode)
            

if __name__ == '__main__':
    main()
    
