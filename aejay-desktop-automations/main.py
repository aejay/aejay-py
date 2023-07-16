import os
from credential_management import CredentialManager
from screen_management import Funkifier, FunkyState
from state_management import StateManager, RemoteState, ProductivityTask
from ui import MenuIcon

def main():
    funkifier = Funkifier()
    funkifier.start()
    
    mqtt_url = os.environ.get("AEJAY_MQTT_URL") or ""
    cred_name = os.environ.get("AEJAY_MQTT_CRED") or ""
    update_topic = os.environ.get("AEJAY_MQTT_UPDATE_TOPIC") or ""
    request_topic = os.environ.get("AEJAY_MQTT_REQUEST_TOPIC") or ""
    machine_type = os.environ.get("AEJAY_TYPE") or "WorkMachine"
    is_work_machine = machine_type == "WorkMachine"

    def icon_change_handler(state: FunkyState):
        funkifier.funkify_screen(state)

    def exit_handler():
        funkifier.funkify_screen(FunkyState.NORMAL)

    menu = MenuIcon(change_callback=icon_change_handler, exit_callback=exit_handler)

    def mqtt_change_handler(state: RemoteState):
        desired_state: FunkyState
        if state.meeting_joined:
            desired_state = FunkyState.NORMAL
        elif is_work_machine and state.current_task not in [ProductivityTask.PROJECT_WORK, ProductivityTask.OFFICE_WORK]:
            desired_state = FunkyState.STEP_AWAY
        elif not is_work_machine and state.current_task in [ProductivityTask.PROJECT_WORK, ProductivityTask.OFFICE_WORK]:
            desired_state = FunkyState.STEP_AWAY
        elif state.medication_due:
            desired_state = FunkyState.MEDICATION_DUE
        elif state.german_due:
            desired_state = FunkyState.GERMAN_DUE
        else:
            desired_state = FunkyState.NORMAL
        menu.set_funkiness(desired_state)

    cred = CredentialManager().get_credentials(cred_name)
    state_manager = StateManager(
        mqtt_url, 
        cred.Username, 
        cred.Password, 
        update_topic,
        request_topic,
        on_update=mqtt_change_handler
    )
    state_manager.Start()

    menu.icon.run()

    funkifier.stop()

if __name__ == "__main__":
    main()
