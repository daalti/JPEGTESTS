import pytest
import logging

def clear_and_verify_event_cleared(udw,expected_events):
    eng = engine.Enginelib(udw)
    assert expected_events == eng.getNewEventsLogged(cleared_event_log), "Event is not cleared successfully"
 
 
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Event code via JPEG verysmall.jpg file
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-24060
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:verysmall.jpg=fc878bdbba4f8f6d58eaa76d28459fbbe4ef400a43eb85f43933245c3271a163
    +name:test_jpeg_pdlmh_printablewidth_zero
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_pdlmh_printablewidth_zero
        +guid:30fe48eb-31e7-418d-9f38-8a6c3ab4dd17
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & EngineFirmwareFamily=Canon
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
 
def test_jpeg_pdlmh_printablewidth_zero(setup_teardown, printjob, outputsaver, cdm):
    printjob.print_verify('fc878bdbba4f8f6d58eaa76d28459fbbe4ef400a43eb85f43933245c3271a163')
    event_code = "F0.01.08.1C"
    response = cdm.get_raw(cdm.WARNING_EVENT_LOG_ENDPOINT)
    warning_events = response.json().get("events", [])

    event_found = False

    if warning_events is None:
        print("Test Failed: Event code not found.")
    
    for event in warning_events:
        if event.get("eventCode") == event_code:
            event_found = True
            break 
               
    assert event_found, f"Test Failed: Event code {event_code} not found."
    print("Test Passed: Event code found.")