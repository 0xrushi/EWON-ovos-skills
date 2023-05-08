from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from ovos_utils.process_utils import RuntimeRequirements
from ovos_utils import classproperty
import sounddevice as sd
import soundfile as sf
from api_scripts.rememberme    import write_to_db, recall_stuff
from api_scripts.ewon  import send_emotion

class MyEwonSkill(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.learning = True

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(internet_before_load=False,
                                   network_before_load=False,
                                   gui_before_load=False,
                                   requires_internet=False,
                                   requires_network=False,
                                   requires_gui=False,
                                   no_internet_fallback=True,
                                   no_network_fallback=True,
                                   no_gui_fallback=True)

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        my_setting = self.settings.get('my_setting')

    @intent_handler(IntentBuilder('ThankYouIntent').require('ThankYouKeyword'))
    def handle_thank_you_intent(self, message):
        """ This is an Adapt intent handler, it is triggered by a keyword."""
        self.speak_dialog("welcome")

    @intent_handler('HowAreYou.intent')
    def handle_how_are_you_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.speak_dialog("how.are.you")
        self.log.info("Message parsed is " + str(message))
    
    @intent_handler('GoToSleep.intent')
    def go_to_sleep(self, message):
        self.speak_dialog("go.toooooo")
        result = send_emotion("sad")

        snore_path = "/home/ovos/.config/mycroft/sounds/snoring.wav"
        data, fs = sf.read(snore_path, dtype='float32')
        sd.play(data, fs)
        sd.wait()  # Wait until sound has finished playing
        # playsound(snore_path)
        # p1 = multiprocessing.Process(target=playsound, args=(snore_path, ))
        # p2 = multiprocessing.Process(target=send_emotion, args=("sad", ))
        # p1.start()   
        # p2.start()
        # p1.join()
        # p2.join()
    
    @intent_handler(IntentBuilder('RememberMeIntent')
                    .require('RememberTo'))
    def remember_me_intent(self, message):
        """
        Match the RememberTo vocab and 
        trigger to send the text to the api

        e.g remember I am keeping the keys in the bedroom drawer
        """
        self.log.info("Message3 parsed is " + str(message.__dict__))
        received_text = message.data.get('utterance')
        if not received_text:
            self.speak_dialog("invalid text")
            return
        if write_to_db(received_text):
            self.speak_dialog("remembered")
            return
        else:
            self.speak_dialog("api error")
            return
        
    @intent_handler(IntentBuilder('RecallIntent')
                    .require('RecallKeyword'))
    def recall_intent(self, message):
        """
        Match the recall vocab and send query to the api to search the database for text

        """
        received_text = message.data.get('utterance')
        if not received_text:
            self.speak_dialog("invalid text")
            return
        
        result = recall_stuff(received_text)
        self.speak_dialog(result)

    def stop(self):
        pass


def create_skill():
    return MyEwonSkill()
