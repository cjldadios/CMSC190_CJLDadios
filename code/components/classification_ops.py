
""" Classifier ops """


import csv
import numpy

import sklearn
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KDTree
# import pandas as pd
from sklearn.model_selection import train_test_split
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

import pickle

# https://www.datacamp.com/community/tutorials/
# k-nearest-neighbor-classification-scikit-learn


from global_vars import *
from global_ops import *
from folder_ops import *


# Convert a dictionary of "class name" vs numpy array
# into a dictionary of className and id
def get_class_code(class_features):
    class_code = {} # dictionary

    index = 0
    for key in class_features.keys():
        class_code[key] = index
        index += 1

    # Save as csv to
    create_folder("./temp")
    csv_file = "./temp/class_legend.csv"
    dictionary_to_csv(class_code, csv_file)

    return class_code

# End get_class_code



# Create a list of just all the features in a numpy array,
# And also create a list of just the corresponding label for each feature row
def get_features_and_labels(class_feat_dict, class_code_dict):
    combined_features = []
    labels = []

    is_initialized_labels_list = False

    for name, feat_list in class_feat_dict.items():
        # if name == "bell":
            # break

        print("\nname: {}".format(name))
        print("feat_list.shape: {}".format(feat_list.shape))

        index = 0
        rows = numpy.size(feat_list, 0)
        print("rows: {}".format(rows))

        print(name + " shape: " + str(feat_list.shape))
        print(name + " size: " + str(rows))
        
        for vect in feat_list:
            print("name: " + name)
            print("index: " + str(index))
            print("total: " + str(rows))
            # print(vect)

            labels.append(class_code_dict[name])
            
            if index == 0: # instanciate numpy array
                features = numpy.array(vect)
            else: # stack numpy array rows
                features = numpy.vstack([features, vect])

            index += 1

            # if index == 50: # remove this if not debugging
            #     break

        # End for each class feature row

        print("features.shape: {}".format(features.shape))

        # stack the features array of one class onto the other
        if not is_initialized_labels_list: # first iteration
            combined_features = numpy.array(features)
            # Update
            is_initialized_labels_list = True
        else: # not the first iteration    
            # print("\ncombined_features:")
            # print(combined_features)
            # print("features:")
            # print(features)
            print("combined_features.shape: ")
            print(combined_features.shape)
            print("features.shape: ")
            print(features.shape)
            combined_features \
                = numpy.append(combined_features, features, axis=0)
            # print("combined_features:")
            # print(combined_features)
            print("combined_features.shape: ")
            print(combined_features.shape)

    # End for each class
        
    # print("labels:")
    # print(labels)
    # print("features:")
    # print(features)

    # labels_len = len(labels)
    # print("labels len: " + str(labels_len))
    # print("labels: ")
    # # print(labels)
    # ind = 0
    # for lab in labels:
        # print("label [" + str(ind) + "]: " + str(lab) \
    #         + "\tlen: " + str(labels_len))
    #     ind += 1

    return combined_features, labels

# End get_features_and_labels()



def test_classify(features, labels, test=None):
    print("\nTest Classify...");

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.3)
            # 70% training and 30% test

    # print("features.shape: {}".format(features.shape))
    # print("labels.shape: {}".format(labels.shape))

    results = []

    ks = [1]

    if test != None:
        ks = [1, 3, 5, 7, 9]

    for k in ks:
        #Create KNN Classifier
        neighbors_no = k
        knn = KNeighborsClassifier(n_neighbors=neighbors_no)

        #Train the model using the training sets
        knn.fit(X_train, y_train)

        #Predict the response for test dataset
        y_pred = knn.predict(X_test)

        # Model Accuracy, how often is the classifier correct?
        print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

        results.append("Accuracy: " \
            + str(metrics.accuracy_score(y_test, y_pred)))


    f = open("./Files/accuracy.txt", "w+") # Create/write new file of not exist,
    if test != None:
        f.close()
        label = ""
        if len(test) > 0:
            label = "_".join(test)
            label = "_" + label
        f = open("./Files/accuracy" + "_" + label + ".txt", "w+")
    for k, res in zip(ks, results):
        f.write("Accuracy")
        print("Accuracy")
        print("k = {}: {}".format(k, res))
        f.write("k = {}: {}\n".format(k, res))
    f.close()
    
    # if test is not None:
    #     halt()

    # print("test: ")
    # print(y_test)
    # print(y_test.shape)
    # print("prediction:")
    # print(y_pred)
    # print(y_pred.shape)

# End test_classify()



def classify(feat_vect, features, labels):
    print("\nClassify...");

    #Create KNN Classifier
    knn = KNeighborsClassifier(n_neighbors=1)

    #Train the model using the training sets
    knn.fit(features, labels)

    # print("feat_vect.ndim: " + str(feat_vect.ndim))    
    if feat_vect.ndim == 1:
        print("Converting 1d array input into 2d...")
        feat_vect = feat_vect.reshape(1, -1)
        """https://stackoverflow.com/questions/45554008
            /error-in-python-script-expected-2d-array
                -got-1d-array-instead"""
        # print("feat_vect.ndim: " + str(feat_vect.ndim))    
    
    prediction = knn.predict(feat_vect)
    # prediction = knn.predict(feat_vect.reshape(1, -1))
    # print("prediction:")
    # print(prediction)
    # print("prediction.shape:")
    # print(prediction.shape)
    # classList.append(prediction)

    # return classList
    return prediction
# End classify()



def get_class_name_using_id(inst_id_list, class_code_dict):

    key_list = list(class_code_dict.keys()) 
    val_list = list(class_code_dict.values()) 
    
    # inst_id_list is not a list but just an inst_id
    if not isinstance(inst_id_list,(list, numpy.ndarray)):
        # list out keys and values separately 
        name = key_list[val_list.index(inst_id_list)]
        return name # return a value
    else: # inst_id_list is an list or numpy array
        names = []
        for inst_id in inst_id_list:
            name = key_list[val_list.index(inst_id)]
            names.append(name)

        return names # return a list

# End get_class_name_using_id()





def simplify_pattern(rhythym_class_name_dict_list):
    print("Applying bias to common drum patterns...")

    """ Impose bias
        Edit the prediction with the common drum hits
    """

    print("rhythym_class_name_dict_list:")
    print(rhythym_class_name_dict_list)

    return rhythym_class_name_dict_list

# End simplify_pattern


def kdtree_classify(stacked_features_list):
    print("kdtree_classify...")

    X = stacked_features_list

    tree = KDTree(X)

    dist, ind = tree.query(X[:1], k=3)

    print("ind: {}".format(ind))

    halt()


# End kdtree_classify()