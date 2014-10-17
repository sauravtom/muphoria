#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

class Recommender:
    def __init__(self):
        #assert type(data).__name__ == 'dict'

        data = self.processRawData("MuPhoria_Data_Oct.csv")
        '''
        data has to be of the form {userId1:behavior, userId2 : behavior}
        where behavior is a list of all transactions made by that user
        '''
        self.data = data

        #the k in k nearest neighbors
        self.k = 3

    def processRawData(self,csv_file):
        assert csv_file[-4:] == ".csv"
        
        with open(csv_file, 'rb') as f:
            reader = csv.reader(f)
            data = {}
            for row in reader:
                try:    data[row[3]]
                except: data[row[3]] = []
                data[row[3]].append(row)

        return data


    #return a number between 0 and 1
    def compareUsers(self,userId1,userId2):
        user1_items = [i[2] for i in self.data[userId1]]
        user2_items = [i[2] for i in self.data[userId2]]
        
        common_items = 0
        for i in user1_items:
            if i in user2_items:
                common_items += 1

        return 2*common_items*1.00/(len(user1_items) + len(user2_items))


    #returns a sorted dictionary, {userId:distance}
    def computeNearestNeighbors(self,theUserId,k):
        distances = []
        for userId,behavior in self.data.iteritems():
            if userId != theUserId:
                distance = self.compareUsers(userId,theUserId)
                if distance:    distances.append((userId, distance))

        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1],reverse=True)
                
        return distances[:k]

    def recommend(self,userId,n=4,verbose=False):
        #TODO: Add weights
        nearest = self.computeNearestNeighbors(userId,self.k)
        if verbose:
            print "%s Nearest Neighbors\n"%self.k
            print nearest
            print "\n\n"
        
        '''
        #TODO
        Given an dictionary of item:weight
        weightArr = { a:b/totalDistance for (a,b) in nearest_dict }
        totalDistance = 0
        for i in nearest:
            totalDistance += i[1]
        '''
        
        #neighbour products is of the form [(product,frequency).(),...]
        neighborProducts = []

        nearest_users = [i[0] for i in nearest]
        for user in nearest_users:
            temp = [i[2] for i in self.data[user]]
            neighborProducts += temp
        
        neighborProducts = [(x, neighborProducts.count(x)) for x in set(neighborProducts)]
        neighborProducts.sort(key=lambda artistTuple: artistTuple[1],reverse=True)
        
        if verbose:
            print "Products bought by neighbors\n"
            print neighborProducts
            print "\n\n"

        userProducts = [i[2] for i in self.data[userId]]
        userProducts = [(x, userProducts.count(x)) for x in set(userProducts)]
        userProducts.sort(key=lambda artistTuple: artistTuple[1],reverse=True)

        if verbose:
            print "Products bought by user#%s\n"%userId
            print userProducts
            print "\n\n"
        
        recommendations = [i for i in neighborProducts if i[0] not in [j[0] for j in userProducts]]
        
        if verbose:
            print "Recommendations\n"
            print recommendations[:n]

        return recommendations[:n]


if __name__ == '__main__':
    R = Recommender()
    #Give 3 recommendations for user 1851, last argument is whether you want the result in verbose fashion or not
    R.recommend('1851',3,True)

