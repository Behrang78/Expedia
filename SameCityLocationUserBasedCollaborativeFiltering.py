import datetime
import pandas as pd
import math
import numpy as np
from numpy import matrix
from collections import defaultdict
from scipy.stats.stats import pearsonr
from heapq import nlargest
from operator import itemgetter
train_file = "/Users/shahriari/Downloads/train.csv"
test_file = "/Users/shahriari/Downloads/test.csv"
output_path = "/Users/shahriari/Documents/ExpediaCompetition/"


def Expedia_Competition():
     print('Starting the Program')
     train_data=pd.read_csv(train_file)
     print('The data is now loaded')
     UserCity=train_data[['user_location_city','user_id']]
     """Converting the data fram UserCity to a dictionary that user_city_location is the ids
     and the user_ids are the values"""
     location_user_dict=UserCity.groupby('user_location_city')['user_id'].apply(list).to_dict()
     """UserCityDict---> the keys are user_id and the values are user_location_city"""
     user_city_dict=UserCity.set_index('user_id')['user_location_city'].to_dict()
     """Computing the ordered set of users"""
     UserList=train_data['user_id'].tolist()
     UserSet=set(UserList)
     SortedUserSet=sorted(UserSet)
     """Computing the ordered set of items"""
     LocationList=train_data['srch_destination_id'].tolist()
     LocationSet=set(LocationList)
     SortedLocationList=sorted(LocationSet)
     """Extracting user_id, destination and rating to build th matrix"""
     user_location_hotelCluster_matrix=train_data[['user_id','srch_destination_id','is_booking','hotel_cluster']]
     user_location_rating=user_location_hotelCluster_matrix.as_matrix()
     User_Item_Rating={}
     Item_User_Rating={}

     print('Start User-based Collaborative Filterting')

     for i in range(len(user_location_rating)):
          User_Item_Rating.setdefault(user_location_rating[i,0],{})
          User_Item_Rating[user_location_rating[i,0]][user_location_rating[i,1]]=user_location_rating[i,2]*user_location_rating[i,3]
          Item_User_Rating.setdefault(user_location_rating[i,1],{})
          Item_User_Rating[user_location_rating[i,1]][user_location_rating[i,0]]=user_location_rating[i,2]*user_location_rating[i,3]
     
     
#     UserDictionary=dict(enumerate(SortedUserSet))
#     UserDictionaryReverse=dict(map(reversed, UserDictionary.items()))
#     ItemDictionary=dict(enumerate(SortedLocationList))
#     ItemDictionaryReverse=dict(map(reversed, ItemDictionary.items()))
#     myarray = np.zeros((np.max(SortedUserSet), np.max(SortedLocationList)))
#     print('Start Making the matrix')
#     for key1, row in User_Item_Rating.iteritems():
#          for key2, value in row.iteritems():
 #              myarray[UserDictionaryReverse.get(key1), ItemDictionaryReverse.get(key2)] = value
     
                        

     print('Start User-based rating computation')     
          
     """Iterating over users"""
     countering=0
     for user in SortedUserSet:
          cityID=user_city_dict[user]
          countering+=1
          if countering % 1000==0:
               print('Read {} lines...'.format(countering))
          
     
          for item in SortedLocationList:
               Same_Location_Users=location_user_dict[cityID]
               total1=0
               total2=0
               

               if User_Item_Rating[user].get(item):
                    continue
               for EachUser in Same_Location_Users:
                    dict1=User_Item_Rating[user]
                    dict2=User_Item_Rating[EachUser]
                    '''Pearson computation of two dictionary values with different keys'''
 #                   FirstUser=UserDictionaryReverse[user]
#                    SecondUser=UserDictionaryReverse[user]
#                    v1=myarray[user,:]
#                    v2=myarray[EachUser,:]
#                    weight=np.dot(v1, v2) / (np.sqrt(np.dot(v1, v1)) * np.sqrt(np.dot(v2, v2)))
                    
                    keys = list(dict1.viewkeys() | dict2.viewkeys())
                    weight=np.corrcoef([dict1.get(x, 0) for x in keys],[dict2.get(x, 0) for x in keys])[0, 1]


                    if(User_Item_Rating.get(EachUser) is None):
                         continue
                    elif(User_Item_Rating.get(EachUser).get(item) is None):
                         continue
                    elif(math.isnan(weight)):
                         continue
                    else:
                         total1=total1+(weight*User_Item_Rating.get(EachUser).get(item))
                         total2=total2+weight
               if total2:
                    average=float(total1)/total2
                    User_Item_Rating.setdefault(user,{})
                    User_Item_Rating[user][item]=math.floor(average)
                    Item_User_Rating.setdefault(item,{})
                    Item_User_Rating[item][user]=math.floor(average)
               else:
                    average=float(0)
                    User_Item_Rating.setdefault(user,{})
                    User_Item_Rating[user][item]=math.floor(average)
                    Item_User_Rating.setdefault(item,{})
                    Item_User_Rating[item][user]=math.floor(average)
                                       
                     
     test_data=pd.read_csv(test_file)
     ItemIDs=test_data['srch_destination_id'].tolist()
     TestItemSet=set(ItemIDs)
     SortedTestItemSet=sorted(TestItemSet)
     UserIDs=test_data['user_id'].tolist()
     TestUserSet=set(UserIDs)
     SortedTestUserSet=sorted(TestUserSet)
     now=datetime.datetime.now()
     path=output_path + 'submission_' + str(now.strftime("%Y-%m-%d-%H-%M"))+'.csv'
     out=open(path,"w")
     out.write("id, hotel_cluster\n")
     for temp in ItemIDs:
          Temporary_Hotel_Clusters=Item_User_Rating.get(item).values()
          Top5=nlargest(5,enumerate(Temporary_Hotel_Clusters),itemgetter(1))
          Top_5=dict(Top5).values()
          out.write(str(temp) + ',')
          if len(Top_5)==0:
               continue
          
          for i,count in enumerate(Top_5):
               if not math.isnan(count):
                    out.write(' '+ str(int(count)))
          out.write("\n")
     
     out.close()

     print('The program is completed!')     
     
Expedia_Competition()     
     



               
          
          



       

    
    
    
   
