from itertools import combinations 
import math
import pandas as pd

class General_Tree:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
   
    def Get_Parent(self):
        self = self.parent
        return self

    def Kill_Children(self ,num):
        self.children.pop(num)

    def AddPlus(self):
        self.data = self.data + "+"

    def New_Item(self, child):
        child.parent = self
        self.children.append(child)
   
    def GetVal(self):
        return self.data
   
    def Get_childrens(self):
        RootChild = []
        for x in self.children:
            RootChild.append(x.GetVal())
        return RootChild
   
    def GetChild(self ,num):
        return  self.children[num]


class Fp_Growth(General_Tree):
    def __init__(self , Data , Minsup, Confidence):
  
        self.Data = Data
        self.Minsup = Minsup
        
        if self.Minsup > 100 or self.Minsup <  0 :
           raise TypeError ( "minsup rate must be between 0 - 100 ")
        self.Minsup = int(math.ceil((Minsup*len(self.Data.values.tolist()))/100))
        self.CleanData = None
        self.Label = None
        self.Confidence = Confidence
        
        if self.Confidence  > 100 or self.Confidence <  0 :
             raise TypeError ( "confidence   must be between 0 - 100 ")
        self.Confidence = Confidence

    def __MinsupKiller(self, Data ,Minsup):
  
        count_dic = {}
        clean_dic = {} 
        
        try:
           Data =  Data.applymap(str.lower)
        except:
            TypeError
        Data =  Data.fillna('NaNxx')
        Data =  Data.values.tolist()
        row = 0 
        while True:
            try:    
                Data[row].remove("NaNxxxxass")
            except :   
                ValueError
                row = row + 1 
            if row == len(Data):
                break  
            
        for row in Data:
            for item in row:
                if item in count_dic:
                    count_dic[item] += 1
                else:
                    count_dic[item] = 1
        
        for item, number in count_dic.items():
            if number >= self.Minsup:
                 clean_dic[item] = number
            else:
                for elements in Data:
                    if item in elements:
                        elements.remove(item)

        Data = sorted(Data, key=lambda x: len(x), reverse=True)
        Data = list(filter(None, Data))
        Label = {k: v for k, v in sorted( clean_dic.items(), reverse=True, key=lambda item: item[1])}
        if len(Label) == 0:
              raise TypeError("minimum support candidate and confidences does not exist !!!\n try decrease minsup or confidence rate")
      
        self.Label = Label
        return  Data

    def __Sorter(self):
        self.CleanData  = self.__MinsupKiller(self.Data,self.Minsup)
        Sort_list = []
        row = 0
        sort_based = [x for x in  self.Label.keys()]
        while True:

            for labels in sort_based:

                if labels in self.CleanData[row]:
                    Sort_list.append(labels)

            self.CleanData[row] = Sort_list

            Sort_list = []

            row = row + 1
            if row == len(self.CleanData):
                break
        return self.CleanData

    def __empty(self,num):
        empty_list = []
        for x in range(num):
            empty_list.append([])
        return empty_list

    def __Lister(self,Data):
        empty_lists = self.__empty(len([x for x in self.Label.keys()]))
        indexs = [x for x in self.Label.keys()]
        try:
            for elem in Data:
                var = indexs.index(elem[0])
                empty_lists[var].append(elem)
        except:
            IndexError
        empty_lists = list(filter(None, empty_lists))
        return empty_lists

    def __MakeRoot(self):
        Root = General_Tree("Root")
        return Root


    def __mainroot(self,M):
        Tree_list = []
        if len(M) >= 2:
            for x in M:
                Tree_list.append(General_Tree(x))
            while True:
                Tree_list[-2].New_Item(Tree_list[-1])
                Tree_list.pop(-1)
                if len(Tree_list) == 1:
                    return Tree_list[0]
        elif len(M) == 1:
            Tree_list.append(General_Tree(M[0]))
            return Tree_list[0]

    def __Create_and_Count(self):
        Main  =  self.__MakeRoot()
        Pre_list = self.__Sorter()
        List = self.__Lister(Pre_list)
        item = 0

        while True:
            Leaf = self.__mainroot(List[item][0])
            List[item].pop(0)
            Main.New_Item(Leaf)
            item = item + 1
            if item == len(List):
                break
        Main_Back = Main
        List =  list(filter(None, List) )

        root = 0;  leaf = 0; elem = 0

        while True:
            
            index_list = []
            try:
                for elem in Main.Get_childrens():

                    if (List[root][leaf][item] in elem) == True:
                        index_list.append("Y")


                    else:
                        index_list.append("N")

                if "Y" not in index_list:
                    Leaf = self.__mainroot(List[root][leaf][ List[root][leaf].index(List[root][leaf][item]):])
                    Main.New_Item(Leaf)
                    item= 0
                    leaf = leaf + 1
                    Main = Main_Back
                else:
                    index = index_list.index("Y")
                    Main = Main.GetChild(index)
                    Main.AddPlus()
                    item = item + 1
                    if item == len(List[root][leaf]):
                        leaf = leaf + 1
                        item = 0
                        Main = Main_Back
                if leaf == len(List[root]):
                    leaf = 0
                    item = 0
                    root = root + 1
            except IndexError:
                Main = Main_Back
                break
      
      
        step = 0
        counted_list = [] 
        while True:
            try:

                Main = Main.GetChild(0)
                counted_list.append([])
                counted_list[step].append(Main.GetVal())
            except IndexError:

                while True:
                    Main = Main.Get_Parent()
                    if Main.GetVal() == 'Root'  and len(Main.Get_childrens()) >  0 and  len(Main.GetChild(0).Get_childrens()) == 0:
                            Main = Main.GetChild(0)
                            
                            Main = Main_Back
                            Main.Kill_Children(0)
                            step = step + 1
                            break 
                    else:    
                        Main.Kill_Children(0)
                        if Main.GetVal() == 'Root' and len(Main.Get_childrens()) == 0:
                            break

                        try:
                            if len(Main.Get_Parent().Get_childrens()) > 1:
                                Main = Main.Get_Parent()
                                Main.Kill_Children(0)
                                step = step + 1
                                Main = Main_Back
                                break
                        except IndexError:
                            break

            if Main.GetVal() == 'Root' and len(Main.Get_childrens()) == 0:
                    break
        counted_list = list(filter(None, counted_list))
        return counted_list
    
    
    def __Ready_list(self):
        def couter(elem):
            var = elem.count("+")
            yield var
        
        def replacer(List):
            var = List.replace("+" , "")
            yield var
        
        counted = self.__Create_and_Count()
        final_list = []; List = 0; item = 0 ;  counted_dic = {}
        
        while True:
           
            var = next(couter(counted[List][item]))
            key = counted[List][item]
            key = next(replacer(key))
           

            counted_dic[key] = var + 1
            item = item + 1

            if item == len(counted[List]):
                counted_dic  = {z1: d for z1, d in sorted(counted_dic.items(), reverse=True, key=lambda item: item[1])}
                final_list.append(counted_dic )
                counted_dic  = {}
                List = List + 1
                item = 0
            if List == len(counted):
                break

        return  final_list
    
    def __minsups(self):
      final_list = self.__Ready_list()
      Fp_list = [];    Clean_list = [] ; sizeof = 0
 
      Labels = [x for x in  self.Label.keys()] 
      if len(Labels) == 1:
            self.Label[Labels[0]] =("% {} ").format( (self.Label[Labels[0]]*100)/len(self.Data))
            return self.Label 
      while True:
         index_list = [] ; val_list = [] ;    Seen_list = [] 
         val= 0
         final_list =   [i for n, i in enumerate( final_list) if i not in  final_list[n + 1:]]
  
         for part in  final_list:
           if ( Labels[-1] in part) == True:
             index_list.append(final_list.index(part))
             val_list.append(part.get(Labels[-1]))
             part.pop(Labels[-1])
         
         for index in index_list:
            process_list =  final_list[index].copy()

            for com in range(len(process_list)+1):
                Key_cmb = combinations(process_list.keys(),com+1)
                for key in Key_cmb:
                    temp  = []
                    key = list(key)
                    key.append( Labels[-1])
          
                    if (key not in Seen_list) == True:
                        Seen_list.append(key)
                        temp.append(key)
                        temp.append("======>")
                        temp.append(val_list[val])
                        Fp_list.append(temp)
                    else:
                        var = Seen_list.index(key)
                        var = var + sizeof
                        Fp_list[var][2] = Fp_list[var][2] + val_list[val]
      
            val = val + 1 
         Labels.pop(-1)
         sizeof = sizeof + len(Seen_list)
         if len(Labels) == 1:
         
           Seen_list = None
           break
      
      
      for Fp_item  in  Fp_list:
        if Fp_item[2] >= self.Minsup:
         
             Clean_list.append(Fp_item)
      
      for lab , val  in self.Label.items():
          temp_inside = []
          temp_big = []
          lab = lab.split(" ")
          lab = " ".join(lab)
          temp_inside.append(lab)
          temp_big.append(temp_inside)
          temp_big.append("======>")
          temp_big.append(val)

          Clean_list.append(temp_big)

      
      return tuple(Clean_list)
      

    def Pickaxe(self):
        M_list =  self.__minsups()
        if len(M_list) == 1:
           
           return self.Label , []
        Con_list = []
        Confidence = list()
        queue = 0 
        Pickaxe= M_list
        for m in M_list:
            Con_list.append(set(m[0]))

        while True:
            var = Con_list[queue]
    
            for v in Con_list:
                if (var.issubset(v)) == True and v  !=  var:
                    confidence_temp  = []
                    confidence_var = 100*(M_list[Con_list.index(v)][2] /  M_list[queue][2])
                    if confidence_var >= self.Confidence:
                        confidence_temp.append(M_list[queue][0] )
                        confidence_temp.append(" =======>" )
                        confidence_temp.append( M_list[Con_list.index(v)][0])
                        confidence_temp.append( "confidence =  % {}".format(confidence_var))
                        Confidence.append( confidence_temp)


            queue = queue + 1      
            if queue == len(Con_list):
                break
        
        for Pic_item in Pickaxe:
            Pic_item[2]= ( "% {} ".format((Pic_item[2]*100)/len(self.Data)))

        return Pickaxe ,Confidence 

  
