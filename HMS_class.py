import json
import API_HMC_NLU


class Medication:
    def __init__(self, res):
        self.symptom = []
        self.med_taken = []
        self.effect = []
        self._get_symptom(res)
        self._get_med_taken(res)
        self._get_med_effect(res)
        self.symptom = self._remove_duplicates(self.symptom)
        self.med_taken = self._remove_duplicates(self.med_taken)
        self.effect = self._remove_duplicates(self.effect)

        
    def _get_symptom(self, res):
        for i in  range(len(res)):
            if res[i]['type'] == 'affectedBy':
                if res[i]['arguments'][1]['entities'][0]['type'] == "SYMPTOM":
                    currentSymbol = res[i]['arguments'][1]['entities'][0]['text']
                    self.symptom.append(self._symptom_structure(res, currentSymbol))

                else:
                    print("Unexpected Error - 1")
            elif (res[i]['type'] == 'helpingWith'\
                and res[i]['arguments'][0]['entities'][0]['type'] == 'MEDICATION'\
                and res[i]['arguments'][1]['entities'][0]['type'] == 'SYMPTOM'):
                    currentSymbol = res[i]['arguments'][1]['entities'][0]['text']

                    for j in range(len(res)):
                        if (res[j]['type'] == 'takingMed'\
                            and (res[j]['arguments'][1]['text'] ==  res[i]['arguments'][0]['text']) 
                                or res[j]['arguments'][1]['text'] == res[i]['arguments'][0]['entities'][0]['text'] ):
                            self.symptom.append(self._symptom_structure(res, currentSymbol))

                # MEDCINE first SYMPTOM second
                # if the PERSON taken co-relation is true:
                # then append the text
                # CAll another function for pronouns

    def _get_ENTITY_status(self, res, entity_text, entity_type):
        #Returns a List of all STATUS quantifying a specific ENTITY text and type
        status = []
        for i in  range(len(res)):
            if res[i]['type'] == 'quantifiedBy':
                if (res[i]['arguments'][0]['entities'][0]['type'] == entity_type)\
                    and (res[i]['arguments'][0]['entities'][0]['text'] == entity_text\
                         or res[i]['arguments'][0]['text'] == entity_text):
                         #Located correspondoing ENTITY to be qualified/quantified
                         #Check for negated status:
                         current_status_category = res[i]['arguments'][1]['entities'][0]['disambiguation']['subtype'][0]
                         current_status_text = res[i]['arguments'][1]['text'] #May need to pass the second entity text version
                         
                         if self._get_negated_status(res, current_status_text) == True:
                            if len(self._get_ENTITY_status(res, current_status_text, 'STATUS')) > 0:
                                status.append(self._get_ENTITY_status(res, current_status_text, 'STATUS')[0] + " NEGATED " + current_status_category)
                            else:
                                status.append(" NEGATED " + current_status_category)
    
                         else:
                            if res[i]['arguments'][1]['entities'][0]['type'] == "STATUS":
                                if len(self._get_ENTITY_status(res, current_status_text, 'STATUS')) > 0:
                                    status.append(self._get_ENTITY_status(res, current_status_text, 'STATUS')[0] + ' ' + current_status_category)
                                else:
                                    status.append(current_status_category)
        return status
    
    def _get_ENITTY_quantity(self, res, currentSymbol, entity):
        #I could merge that method into _get_ENTITY_status
        #Returns a List of all QUANTITIES quantifying a specific ENTITY
        quantity = []
        for i in  range(len(res)):
            if res[i]['type'] == 'quantifiedBy':
                if (res[i]['arguments'][0]['entities'][0]['type'] == entity)\
                    and (res[i]['arguments'][0]['entities'][0]['text'] == currentSymbol\
                         or res[i]['arguments'][0]['text'] == currentSymbol):
                         #Located correspondoing symptom to be qualified/quantified
                         #Check for negated status:
                         currentQuantity = res[i]['arguments'][1]['entities'][0]['text']
                         currentQuantityText = res[i]['arguments'][1]['text'] #May need to pass the second entity text version
                         if self._get_negated_status(res, currentQuantityText) == True:
                            quantity.append("NEGATED " + currentQuantity)
                         else:
                            if res[i]['arguments'][1]['entities'][0]['type'] == "QUANTITY":
                                quantity.append(currentQuantity)
        return quantity
    
    def _get_med_taken(self, res):
        # _get_med_taken:
        # Method to obtain the medication ENTITIES based on 
        # the PERSON 'takingMed' MEDICATION relationship 
        # or based on MEDICATION applyTo PERSON simultaneously with no negations
        # or MEDICATION helpingWith to SYMPTOMS anD SYMPTOM appliesTo PERSON
        for i in  range(len(res)):
            # print(res[i]['type'])
            if res[i]['type'] == 'takingMed':
                #Medication check here
                if res[i]['arguments'][1]['entities'][0]['type'] == "MEDICATION":
                    #Product Check
                    med_text = res[i]['arguments'][1]['entities'][0]['text']
                    self.med_taken.append(self._med_taken_structure(res, med_text))
                else:
                    print("Unexpected Error - 2")
            elif (res[i]['type'] == 'applyTo'\
                and res[i]['arguments'][0]['entities'][0]['type'] == 'MEDICATION'\
                and res[i]['arguments'][1]['entities'][0]['type'] == 'PERSON'):
                med_text = res[i]['arguments'][0]['entities'][0]['text']
                self.med_taken.append(self._med_taken_structure(res, med_text))
            else:
                pass
            
    
    def _get_negated_status(self, res, currentEntity):
        for i in range(len(res)):
            if res[i]['type'] == 'negatedBy'\
                and (res[i]['arguments'][0]['entities'][0]['text'] == currentEntity\
                    or res[i]['arguments'][0]['text'] == currentEntity):
                if res[i]['arguments'][1]['entities'][0]['type'] == "STATUS":
                    return True
                else:
                    print("Model Error")
        else:
            return False
            
    def _get_med_effect(self, res):
        ##########################################################################################
        #Returns effects: 1. caused by EFFECT producedBy MEDICATION and MEDICATION applyTo PERSON
        #                 2. caused by EFFECT applyTo PERSON
        #                 3. caused by PERSON affectedBy EFFECT
        #Format Example:    
        #          {
        #               'effect 1' : [
        #                   {
        #                       'specific' : [effect 2, effect 3] 
        #                   }
        #               'status of effect 1' : ['status list here']
        #               ]
        #           }
        #           {
        #               'effect 2' : [
        #                   {
        #                       'specific' : [] 
        #                   }
        #               'status of effect 2' : []
        #               ]
        #           }
        ###########################################################################################
        for i in range(len(res)):
            if (res[i]['type'] == 'producedBy'\
                and res[i]['arguments'][0]['entities'][0]['type'] == 'EFFECT'\
                and res[i]['arguments'][1]['entities'][0]['type'] == 'MEDICATION'):
                #EFFECT producedBy MEDICATION
                    currentSymbol = res[i]['arguments'][0]['entities'][0]['text']
                    first_name =  res[i]['arguments'][1]['text']
                    for j in range(len(res)):
                        if ((res[j]['type'] == 'applyTo')\
                            and (res[j]['arguments'][0]['text'] ==  res[i]['arguments'][1]['text'] 
                                or res[j]['arguments'][0]['text'] == res[i]['arguments'][1]['entities'][0]['text']) 
                            and (res[j]['arguments'][1]['entities'][0]['type']=='PERSON') ): # Considering Pronouns
                            # MEDICATION applyTo PERSON
                            self.effect.append(self._effect_structure(res, currentSymbol))
                             
            elif (res[i]['type'] == 'applyTo'\
                and res[i]['arguments'][0]['entities'][0]['type'] == 'EFFECT'\
                and res[i]['arguments'][1]['entities'][0]['type'] == 'PERSON'):
                #EFFECT applyTo PERSON
                starting_data = res[i]['arguments'][0]['text']
                self.effect.append(self._effect_structure(res, starting_data))
        
            
            elif res[i]['type'] == 'affectedBy'\
                and res[i]['arguments'][0]['entities'][0]['type'] == 'PERSON'\
                and res[i]['arguments'][1]['entities'][0]['type'] == 'EFFECT':
                #PERSON affectedBy EFFECT
                 new_effect = res[i]['arguments'][1]['entities'][0]['text']
                 self.effect.append(self._effect_structure(res, new_effect))
    
    def _element_not_in_list(self, list, element):
        # _element_not_in_list: 
        # Method to prevent appending an element that is already in a list
        for i in range(len(list)):
            if element == list[i]:
                return False
        return True            
    
    def _get_ENTITY_partOf_ENTITY(self, res, entityText):
        #returns a list of partOf entities text
        partOf_list = []
        for i in range(len(res)):
            if res[i]['type'] == 'partOf'\
            and res[i]['arguments'][1]['text'] == entityText:
                new_entity = res[i]['arguments'][0]['text']
                new_entity_type = res[i]['arguments'][0]['entities'][0]['type']
                #CONSIDERING EFFECTS
                if  new_entity_type == 'EFFECT'\
                    and res[i]['arguments'][1]['entities'][0]['type'] == 'EFFECT':  #EFFECT partOf EFFECT, 
                    partOf_list.append(new_entity)
                    
                    #CONSIDERING NEW ENTITY HAS NOT ALREADY BEEN ADDED TO EFFECTS:
                    if self._not_recorded(new_entity, new_entity_type) == 1:
                        self.effect.append(
                                {
                                    'label' : new_entity,
                                    'specific': [
                                        {
                                            'labels' : self._get_ENTITY_partOf_ENTITY(res, new_entity)
                                        }
                                    ], 
                                    'status' : self._get_ENTITY_status(res, new_entity, 'EFFECT')                           
                                })

                else:
                    print('unexpected food class error')
        return partOf_list

    def _not_recorded(self, element, element_type):
        # SEARCHING STRUCTURE FOR REDUNDANCIES 
        
        # self.effect STRUCTURE
        if element_type == 'EFFECT':
            for i in range(len(self.effect)):
                if self.effect[i]['label'] == element:
                    return False
        elif element_type == 'MEDICATION':
            for i in range(len(self.med_taken)):
                pass
        elif  element_type == 'SYMPTOM':
            for i in range(len(self.symptom)):
                pass
        else:
            print('Unexpected error: _not_recorded method')
        return True
    
    def _remove_duplicates(self, data):
        unique_entries = []
        for item in data:
            if item not in unique_entries:
                unique_entries.append(item)
        return unique_entries

    def _effect_structure(self, res, element):
        entry  = {
            'effect' : element,
            'specific' : [
                {
                'labels' : self._get_ENTITY_partOf_ENTITY(res, element), #call part_of method
                }
            ],
            'status' : self._get_ENTITY_status(res, element, 'EFFECT') 
        }
        return entry

    def _symptom_structure(self, res, element):
        entry = {
            'symptoms' : element,
            'status' : self._get_ENTITY_status(res, element, 'SYMPTOM'),
            'quantity' : self._get_ENITTY_quantity(res, element, 'SYMPTOM')
        
        }
        return entry
    
    def _med_taken_structure(self, res, element):
        entry = {
            'medication' : element
        }
        return entry

class Exercise:
    def __init__(self, res):
        self.exercise = []
        self.ex_status = [] #Not exercise-specific 
        self.ex_time = self._get_general_time_entities(res) #Not exercise-specific 
        self._get_exercise(res)
        self.exercise = self._remove_duplicates(self.exercise)
        self.ex_status = self._remove_duplicates(self.ex_status)
        self.ex_time = self._remove_duplicates(self.ex_time)
        # self._get_general_time_entities(res)
        # self._get_ex_status(res)
        # self._get_ex_time(self, res)
    
    def _get_exercise(self, res):
        for i in  range(len(res)):
            if res[i]['type'] == 'engagedIn':
                #Exercuse check here
                if res[i]['arguments'][1]['entities'][0]['type'] == "EXERCISE":
                    #Exercise Check
                    exercise_type = res[i]['arguments'][1]['entities'][0]['type']
                    exercise_text = res[i]['arguments'][1]['text']
                    #Negation Check 
                    if self._get_negated_status(res, exercise_text) == True:
                        self.exercise.append("NEGATED " + self._ex_structure(res, exercise_text))
                    else: 
                        self.exercise.append(self._ex_structure(res, exercise_text))
                else:
                    print("Unexpected Error - 3")

    def _get_ex_status(self, res, currentExercise):
        status = []
        for i in  range(len(res)):
            if res[i]['type'] == 'quantifiedBy':
                #Exercise check here
                if (res[i]['arguments'][0]['entities'][0]['type'] == "EXERCISE")\
                    and (res[i]['arguments'][0]['entities'][0]['text'] == currentExercise\
                         or res[i]['arguments'][0]['text'] == currentExercise):
                         #Located correspondoing symptom to be qualified/quantified
                         #Check for negated status:
                         currentStatus = res[i]['arguments'][1]['entities'][0]['disambiguation']['subtype'][0]
                         currentStatusText = res[i]['arguments'][1]['text'] #May need to pass the second entity text version
                         if self._get_negated_status(res, currentStatusText) == True:
                            status.append("NEGATED " + currentStatus)
                         else:
                            if res[i]['arguments'][1]['entities'][0]['type'] == "STATUS":
                                status.append(currentStatus)
        return status
    
    def _get_ex_time(self, res, exercise_text):
        specific_ex_time = []
        for i in range(len(res)):
            if res[i]['type'] == 'quantifiedBy'\
                and res[i]['arguments'][0]['text'] == exercise_text\
                and res[i]['arguments'][1]['entities'][0]['type'] == 'TIME':
                # EXERCISE quantifiedBy TIME, for specific exercise
                time_text = res[i]['arguments'][1]['text']
                specific_ex_time.append(time_text)
        return specific_ex_time

    def _get_general_time_entities(self, res):
        # _get_general_time_entities:
        #First: we look for TIME quantifiedBy TIME
        #Then for each of those two TIME entities we go down the chain and append (second entity)
        #and the go up the chain and append (first entity) all quantifiedBy relationship
        #Thus possibly including TIME quantifiedBy QUANTITY or STATUS qunatifiedBy TIME
        #Second: we look for  TIME quantified by QUANTITY relationships
        #similarly we go up the chain for the TIME entity
        #Importantly we never append twice the same time entity.
        tmp_time_data = []
        starting_data = ""
        for i in range(len(res)):

            #Case of multiple TIME quantifiers - TIME quantifiedBy TIME
            if res[i]['type'] == 'quantifiedBy'\
            and res[i]['arguments'][0]['entities'][0]['type'] == 'TIME'\
            and res[i]['arguments'][1]['entities'][0]['type'] == 'TIME' :
                starting_data = res[i]['arguments'][0]['text']
                previous_entity = starting_data
                next_entity = res[i]['arguments'][1]['text']
                if self._element_not_in_list(tmp_time_data, previous_entity) == True:
                    tmp_time_data.append(previous_entity)
                if self._element_not_in_list(tmp_time_data, next_entity) == True:
                    tmp_time_data.append(next_entity)
                
                found_new_quantification = True
                while (found_new_quantification == True): #Going down the chain
                    found_new_quantification = False
                    for j in range(len(res)):
                        new_entity = res[j]['arguments'][0]['text']
                        new_entity_type = res[j]['arguments'][0]['entities'][0]['type']
                        if res[j]['type'] == 'quantifiedBy'\
                        and new_entity_type == "TIME"\
                        and next_entity == new_entity:
                            if self._element_not_in_list(tmp_time_data, res[j]['arguments'][1]['text']) == True:
                                tmp_time_data.append(res[j]['arguments'][1]['text'])
                            next_entity = res[j]['arguments'][1]['text']
                            found_new_quantification = True
                
                found_new_quantification = True
                while (found_new_quantification == True): #Going up the chain
                    found_new_quantification = False
                    for j in range(len(res)):
                        new_entity = res[j]['arguments'][1]['text']
                        new_entity_type = res[j]['arguments'][1]['entities'][0]['type']
                        if res[j]['type'] == 'quantifiedBy'\
                        and new_entity_type == "TIME"\
                        and previous_entity == new_entity:
                            if self._element_not_in_list(tmp_time_data, res[j]['arguments'][0]['text']) == True:
                                tmp_time_data.append(res[j]['arguments'][0]['text'])
                            previous_entity = res[j]['arguments'][0]['text']
                            found_new_quantification = True
            
            #TIME quaNtifiedBy QUANTITY
            elif res[i]['type'] == 'quantifiedBy'\
            and res[i]['arguments'][0]['entities'][0]['type'] == 'TIME'\
            and res[i]['arguments'][1]['entities'][0]['type'] ==  'QUANTITY':
                starting_data2 = res[i]['arguments'][1]['text']
                previous_entity = starting_data2
                next_entity = res[i]['arguments'][0]['text']
                if self._element_not_in_list(tmp_time_data, starting_data2) == True:
                    tmp_time_data.append(starting_data2)
                if self._element_not_in_list(tmp_time_data, next_entity) == True:
                    tmp_time_data.append(next_entity)
                
                found_new_quantification = True
                while (found_new_quantification == True): #Going down the chain
                    found_new_quantification = False
                    for j in range(len(res)):
                        new_entity = res[j]['arguments'][1]['text']
                        new_entity_type = res[j]['arguments'][1]['entities'][0]['type']
                        if res[j]['type'] == 'quantifiedBy'\
                        and new_entity_type == "TIME"\
                        and next_entity == new_entity:
                            if self._element_not_in_list(tmp_time_data, res[j]['arguments'][0]['text']) == True:
                                tmp_time_data.append(res[j]['arguments'][0]['text'])
                            next_entity = res[j]['arguments'][0]['text']
                            found_new_quantification = True

        return tmp_time_data

    def _element_not_in_list(self, list, element):
        # _element_not_in_list: 
        # Method to prevent appending an element that is already in a list
        for i in range(len(list)):
            if element == list[i]:
                return False
        return True

    def _get_negated_status(self, res, currentEntity):
        #_get_negated_status;
        # Method to obtain the negated qualifier of an entity entity
        for i in range(len(res)):
            if res[i]['type'] == 'negatedBy'\
                and (res[i]['arguments'][0]['entities'][0]['text'] == currentEntity\
                    or res[i]['arguments'][0]['text'] == currentEntity):
                # print('NEGATED BY X')
                if res[i]['arguments'][1]['entities'][0]['type'] == "STATUS":
                    return True
                else:
                    print("Model Error")
        else:
            return False

    def _remove_duplicates(self, data):
        #Method to remove duplicates
        unique_entries = []
        for item in data:
            if item not in unique_entries:
                unique_entries.append(item)
        return unique_entries

    def _ex_structure(self, res, element):
        #Standardising data
        entry = {
            'exercise' : element,
            'status' : self._get_ex_status(res, element), # Exercise Specific
            'time' : self._get_ex_time(res, element) # Exercise Specific
        
        }
        return entry    

class Food:
    def __init__(self, res):
        self.food = [{
            'healthy' : [],
            'unhealthy' : [],
            'other' : []

        }]
        self.effect = []
        self._get_food(res)
        self._get_food_effect(res)
        self.food = self._remove_duplicates(self.food)
        self.effect = self._remove_duplicates(self.effect)
    
    def _get_food(self, res):
        for i in range(len(res)):
            #PERSON eating FOOD
            if res[i]['type'] == 'eating'\
            and res[i]['arguments'][0]['entities'][0]['type'] == 'PERSON'\
            and res[i]['arguments'][1]['entities'][0]['type'] == 'FOOD':
                specific_food = res[i]['arguments'][1]['text']
                #CATEGORISING FOOD
                if res[i]['arguments'][1]['entities'][0]['disambiguation']['subtype'][0] == 'NONE':
                    self.food[0]['other'].append(self._food_structure(res, specific_food))
                    self._get_food_partOf_food(res, specific_food)
                elif res[i]['arguments'][1]['entities'][0]['disambiguation']['subtype'][0] == 'HEALTHY':
                    self.food[0]['healthy'].append(self._food_structure(res, specific_food))
                    self._get_food_partOf_food(res, specific_food)
                elif res[i]['arguments'][1]['entities'][0]['disambiguation']['subtype'][0] == 'UNHEALTHY':
                    self.food[0]['unhealthy'].append(self._food_structure(res, specific_food))
                    self._get_food_partOf_food(res, specific_food)
                else:
                    print('unexpected food class error')

    def _get_food_effect(self, res):
        pass

    def _get_food_partOf_food(self, res, specificfood):
        for i in range(len(res)):
            if res[i]['type'] == 'partOf'\
            and res[i]['arguments'][1]['text'] == specificfood:
                new_food = res[i]['arguments'][0]['text']
                #CATEGORISING FOOD
                if res[i]['arguments'][0]['entities'][0]['disambiguation']['subtype'][0] == 'NONE':
                    self.food[0]['other'].append(self._food_structure(res, new_food))
                    self._get_food_partOf_food(res, new_food)
                    #Mitigate recursion unfinite looping error here - if food already part of the list for example
                elif res[i]['arguments'][0]['entities'][0]['disambiguation']['subtype'][0] == 'HEALTHY':
                    self.food[0]['healthy'].append(self._food_structure(res, new_food))
                    self._get_food_partOf_food(res, new_food)
                    #Mitigate recursion unfinite looping error here - if food already part of the list for exampl
                elif res[i]['arguments'][0]['entities'][0]['disambiguation']['subtype'][0] == 'UNHEALTHY':
                    self.food[0]['unhealthy'].append(self._food_structure(res, new_food))
                    self._get_food_partOf_food(res, new_food)
                    #Mitigate recursion unfinite looping error here - if food already part of the list for example
                else:
                    print('unexpected food class error')
    
    def _get_ENTITY_status(self, res, entity_text, entity_type):
        #Returns a List of all STATUS quantifying a specific ENTITY text and type
        status = []
        for i in  range(len(res)):
            if res[i]['type'] == 'quantifiedBy':
                if (res[i]['arguments'][0]['entities'][0]['type'] == entity_type)\
                    and (res[i]['arguments'][0]['entities'][0]['text'] == entity_text\
                         or res[i]['arguments'][0]['text'] == entity_text):
                         #Located correspondoing ENTITY to be qualified/quantified
                         #Check for negated status:
                         current_status_category = res[i]['arguments'][1]['entities'][0]['disambiguation']['subtype'][0]
                         current_status_text = res[i]['arguments'][1]['text'] #May need to pass the second entity text version
                         
                         if self._get_negated_status(res, current_status_text) == True:
                            if len(self._get_ENTITY_status(res, current_status_text, 'STATUS')) > 0:
                                status.append(self._get_ENTITY_status(res, current_status_text, 'STATUS')[0] + " NEGATED " + current_status_category)
                            else:
                                status.append(" NEGATED " + current_status_category)
    
                         else:
                            if res[i]['arguments'][1]['entities'][0]['type'] == "STATUS":
                                if len(self._get_ENTITY_status(res, current_status_text, 'STATUS')) > 0:
                                    status.append(self._get_ENTITY_status(res, current_status_text, 'STATUS')[0] + ' ' + current_status_category)
                                else:
                                    status.append(current_status_category)
        return status
    
    def _get_ENITTY_quantity(self, res, entity_text, entity_type):
        #Returns a List of all QUANTITY quantifying a specific ENTITY text and type
        quantity = []
        for i in  range(len(res)):
            if res[i]['type'] == 'quantifiedBy':
                if (res[i]['arguments'][0]['entities'][0]['type'] == entity_type)\
                    and (res[i]['arguments'][0]['entities'][0]['text'] == entity_text\
                         or res[i]['arguments'][0]['text'] == entity_text):
                         #Located correspondoing symptom to be qualified/quantified
                         #Check for negated status:
                         current_quantity_category = res[i]['arguments'][1]['entities'][0]['type']
                         current_quantity_text = res[i]['arguments'][1]['text'] #May need to pass the second entity text version
                         if self._get_negated_status(res, current_quantity_text) == True:
                            if len(self._get_ENITTY_quantity(res, current_quantity_text, 'TIME')) > 0:
                                quantity.append(self._get_ENITTY_quantity(res, current_quantity_text, 'TIME')[0] + " NEGATED " + current_quantity_text)
                            else:
                                quantity.append(" NEGATED " + current_quantity_category)
    
                         else:
                            if res[i]['arguments'][1]['entities'][0]['type'] == "TIME":

                                quantity.append(current_quantity_text)
                                if len(self._get_ENITTY_quantity(res, current_quantity_text, 'TIME')) > 0:
                                    quantity.append(self._get_ENITTY_quantity(res, current_quantity_text, 'TIME')[0] + ' ' + current_quantity_text)
                                else:
                                    quantity.append(current_quantity_category)
        return quantity

    def _get_negated_status(self, res, currentEntity):
        for i in range(len(res)):
            if res[i]['type'] == 'negatedBy'\
                and (res[i]['arguments'][0]['entities'][0]['text'] == currentEntity\
                    or res[i]['arguments'][0]['text'] == currentEntity):
                # print('NEGATED BY X')
                if res[i]['arguments'][1]['entities'][0]['type'] == "STATUS":
                    return True
                else:
                    print("Model Error")
        else:
            return False

    def _remove_duplicates(self, data):
        unique_entries = []
        for item in data:
            if item not in unique_entries:
                unique_entries.append(item)
        return unique_entries

    def _food_structure(self, res, element):
        entry = {
            'food' : element,
            'status' : self._get_ENTITY_status(res, element, "FOOD"),
            'time' : self._get_ENITTY_quantity(res, element, "FOOD")
        }
        return entry    


# def main(sentence):
#     #Calling API_HMC_NLU's main function
#     response = API_HMC_NLU.API_HMC_NLU_api_call(sentence)

#     #Saving the model's output in a file for development purposes
#     with open('relationships.json', 'w', encoding='utf-8') as f:
#         json.dump(response, f, ensure_ascii=False, indent=4)

#Printing the model's output in the console
# print(json.dumps(response, indent=2))

# print('### Veryfing Alogorithm Works ###')    
# x = Medication(response)
# print('--------------------------Med_taken:--------------------------\n', json.dumps(x.med_taken, indent = 2))
# print('--------------------------Symptom:--------------------------\n', json.dumps(x.symptom, indent = 2))
# print('--------------------------Effects:--------------------------\n', json.dumps(x.effect, indent = 2))  #Here

# y = Exercise(response)
# print('--------------------------Exercise: --------------------------\n', json.dumps(y.exercise, indent = 2))
# print('--------------------------Ex_time:--------------------------\n', json.dumps(y.ex_time, indent = 2))

# z = Food(response)
# print('--------------------------Food:--------------------------\n', json.dumps(z.food, indent = 2))
# print('--------------------------Food Effect:--------------------------\n',json.dumps((z.effect), indent=2))
