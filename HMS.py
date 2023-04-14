import json
import HMS_class as hmsc
import API_HMC_NLU as hmc_nlu
import API_speech_to_text as stt
import API_text_to_speech as tts
import Database_Cloudant as dbc
import Audio_Record as arec

#Test Responses Model was trained On:
s1 =  "I've been taking my Albuterol as needed for my asthma and it's been keeping my symptoms under control."
s2 =  'I\'ve also been trying to eat healthier, I\'ve been cutting down on processed foods and eating more fruits and vegetables. I\'m also trying to drink more water. I think it\'s been making a difference, my blood pressure has been much better.'
s3 =  'I\'ve also been trying to incorporate more stretching and yoga into my routine. I\'ve been using a foam roller to help with my back pain, and it seems to be working well. The Ibuprofen you prescribed is also helping with the pain.'
s4 = 'I feel ike a 5 out of 5'
s5 = 'I went shopping at the mall'

bemo_path = '/home/karlmarc/Desktop/BEMO/BEMO-main/'

def medicine_check(): #Apply model
    # entry1 = [{
    #         'symptoms' : element,
    #         'status' : self._get_ENTITY_status(res, element, 'SYMPTOM'),
    #         'quantity' : self._get_ENITTY_quantity(res, element, 'SYMPTOM')
        
    #     }]
    
    # entry2 = [{
    #         'medication' : element
    #     }]

    # entry3  = [{
    #         'effect' : element,
    #         'specific' : [
    #             {
    #             'labels' : self._get_ENTITY_partOf_ENTITY(res, element), #call part_of method
    #             }
    #         ],
    #         'status' : self._get_ENTITY_status(res, element, 'EFFECT') 
    #     }]
    
    spoken = 'Hi there, can you tell me what medecine you have taken today and how you physically feel?'
    # print(spoken)

    #Call text-to-speech(spoken) service
    # tts.api_call(spoken, 'spoken_1.wav')
    tts.api_call(spoken, bemo_path + 'spoken_1.wav')
    arec.audio_play2(bemo_path + 'spoken_1.wav')
    
    #Call Audio Recording Program
    arec.audio_rec(bemo_path + 'check_1.wav')
    #Call Speech To Text Program
    user_reply = stt.main('check_1.wav')
    user_reply = s1
    print(user_reply)

    #Call Machine Learning Model deployed on 2nd NLU instance
    # user_reply = "I've been taking my Albuterol as needed for my asthma and it's been keeping my symptoms under control."
    model_response = hmc_nlu.API_HMC_NLU_api_call(user_reply)
    x = hmsc.Medication(model_response)
    
    #Aggregating Data
    check1_data = {
        'SYMPTOM' : x.symptom,
        'MEDICATION' : x.med_taken,
        'EFFECT' : x.effect
    }

    #SIMULATION
    # print(user_reply)
    # # print('--------------------------Med_taken:--------------------------\n', json.dumps(x.med_taken, indent = 2))
    # # print('--------------------------Symptom:--------------------------\n', json.dumps(x.symptom, indent = 2))
    # # print('--------------------------Effects:--------------------------\n', json.dumps(x.effect, indent = 2)) 
    # print(json.dumps(check1_data, indent = 2))
    return check1_data

def food_drink_check(): # Apply model
    # entry = {
    #         'food' : element,
    #         'status' : self._get_ENTITY_status(res, element, "FOOD"),
    #         'time' : self._get_ENITTY_quantity(res, element, "FOOD")
    #     }

    #I NEED TO TRY HMS_CLASS with food effects and create a structure

    spoken = 'Could you also tell me what food and drink you had today?'
    # print(spoken)

    #Call text-to-speech(spoken) service
    #tts.api_call(spoken, bemo_path + 'spoken_2.wav')
    arec.audio_play2(bemo_path + 'spoken_2.wav')

    #Call Audio Recording Program
    arec.audio_rec(bemo_path + 'check_2.wav')

    #Call Speech to text Program
    user_reply = stt.main('check_2.wav')
    user_reply = s2
    print(user_reply)

    #Call Machine Learning Model deployed on 2nd NLU instance
    # user_reply = 'I\'ve also been trying to eat healthier, I\'ve been cutting down on processed foods and eating more fruits and vegetables. I\'m also trying to drink more water. I think it\'s been making a difference, my blood pressure has been much better.'
    model_response = hmc_nlu.API_HMC_NLU_api_call(user_reply)
    y = hmsc.Food(model_response)
    
    #Aggregating Data
    check2_data = {
        'FOOD_DRINK' : y.food,
        'EFFECT' : y.effect,
    }

    # #SIMULATION
    # print(user_reply)
    # # print('--------------------------Food:--------------------------\n', json.dumps(y.food, indent = 2))
    # # print('--------------------------Food Effect:--------------------------\n',json.dumps((y.effect), indent=2))
    # print(json.dumps(check2_data, indent=2))
    return check2_data

def exercise_check(): #Apply model 
    # entry = {
    #         'exercise' : element,
    #         'status' : self._get_ex_status(res, element), # Exercise Specific
    #         'time' : self._get_ex_time(res, element) # Exercise Specific
        
    #     }

    spoken = 'Also, were you physically active this day?'
    # print(spoken)
    
    #Call text-to-speech(spoken) service
    #tts.api_call(spoken, bemo_path + 'spoken_3.wav')
    arec.audio_play2(bemo_path + 'spoken_3.wav')

    #Call Audio Recording Program
    arec.audio_rec(bemo_path + 'check_3.wav')

    #Call Speech to text Program
    user_reply = stt.main('check_3.wav')
    user_reply = s3
    print(user_reply)

    #Call Machine Learning Model deployed on 2nd NLU instance
    # user_reply = 'I\'ve also been trying to incorporate more stretching and yoga into my routine. I\'ve been using a foam roller to help with my back pain, and it seems to be working well. The Ibuprofen you prescribed is also helping with the pain.'
    model_response = hmc_nlu.API_HMC_NLU_api_call(user_reply)
    z = hmsc.Exercise(model_response)
    
    #Aggregating Data
    check3_data = {
        'exercise' : z.exercise,
        'status' : z.ex_status,
        'time' : z.ex_time
    }
    
    #SIMULATION
    # print(user_reply)
    # # print('--------------------------Exercise: --------------------------\n', json.dumps(z.exercise, indent = 2))
    # # print('--------------------------Ex_time:--------------------------\n', json.dumps(z.ex_status, indent = 2))
    # # print('--------------------------Ex_time:--------------------------\n', json.dumps(z.ex_time, indent = 2))
    # print(json.dumps(check3_data, indent=2))
    return check3_data

def wellbeing_check():
    spoken = 'On a scale of 1 to 6 how do you feel today?' #Number Identifying algorithm no need for machine learning
    # print(spoken)

    #Call text-to-speech(spoken)
    tts.api_call(spoken, bemo_path + 'spoken_4.wav')
    arec.audio_play2(bemo_path + 'spoken_4.wav')

    #Call Audio Recording Program
    arec.audio_rec(bemo_path + 'check_4.wav')

    #Call Speech to text Program
    check4_data = stt.main('check_4.wav')

    #wellbeing_score = Call NLU service Program #Keyword or Categories filters
    return check4_data

def day_summary():
    spoken = 'Can you give me a summary of your day?' #Plain Summary -> Later I could extract themes
    # print(spoken)
    #Call text-to-speech(spoken) service
    tts.api_call(spoken, bemo_path + 'spoken_5.wav')
    arec.audio_play2(bemo_path + 'spoken_5.wav')

    #Call Audio Recording Program
    arec.audio_rec(bemo_path + 'check_5.wav')

    #Call Speech to text Program
    check5_data = stt.main('check_5.wav')

    return check5_data

def HM_check():
    check_1 = medicine_check()
    check_2 = food_drink_check()
    check_3 = exercise_check()
    check_4 = wellbeing_check()
    check_5 = day_summary()

    #Aggregated Data Standardised Form
    comb_data = [check_1, check_2, check_3, check_4, check_5]

    #Storing data in databse
    # dbc.database_call(comb_data)
    print(comb_data)
    dbc.create_health_check_doc(comb_data)
    
def main(): #Add arguments for actions 1 or 2
    
    #Action 1: Run the health management checks
    HM_check() #To store on Cloudant dB
    #Action 2: Record emotions,sentiment, pet interactivity 
    # continuous_monitoring(inputA, inputB)  #To store on Cloudant dB

# ~ if __name__ == "__main__":
    # ~ main()
