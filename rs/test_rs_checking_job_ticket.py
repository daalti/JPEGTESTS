import pytest
import logging
import time

collate = "uncollated"
colorMode = "color"
copies = 1
mediaSource = "auto"
mediaSize = "custom"
mediaType = "custom"
plexMode =  "simplex"
duplexBinding = "oneSided"
printQuality = "normal"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple print from a rasterstream (.rs) file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-14986
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:a3.rs=b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617
    +name:test_rs_a3_checking_job_ticket
    +test:
        +title:test_rs_a3_checking_job_ticket
        +guid:49a2a3dc-9098-11eb-984e-cbc099cc17ea
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=RasterStreamICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_a3_checking_job_ticket(setup_teardown, printjob, outputsaver, cdm, job, udw):
    # Start the print job
    jobid = printjob.start_print('b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617')

    # Wait until the job end without problems
    job.wait_for_job_completion_cdm(jobid, timeout=700)

    # Get the ticket
    job_queue = cdm.get("/cdm/jobManagement/v1/history")
    links = {key:value for (key,value) in job_queue["jobList"][-1].items() if key == "links"}
    cdm_ticket = [x["href"] for x in links["links"] if x["rel"] == "jobTicket"]

    # Getting the information of the ticket
    job_ticket = cdm.get(cdm_ticket[0])

    is_simulator = udw.mainUiApp.ControlPanel.isSimulator()
    if not is_simulator:
        global mediaType
        mediaType = "stationery"

    check_job_ticket(job_ticket)

    outputsaver.save_output()


def check_job_ticket(ticket):

    assert ticket["dest"]["print"]["collate"] == collate
    assert ticket["dest"]["print"]["colorMode"] == colorMode
    assert ticket["dest"]["print"]["copies"] == copies
    assert ticket["dest"]["print"]["mediaSource"] == mediaSource
    assert ticket["dest"]["print"]["mediaSize"] == mediaSize
    assert ticket["dest"]["print"]["mediaType"] == mediaType
    assert ticket["dest"]["print"]["plexMode"] == plexMode
    assert ticket["dest"]["print"]["printQuality"] == printQuality
