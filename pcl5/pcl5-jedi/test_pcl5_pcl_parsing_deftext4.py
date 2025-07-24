import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using deftext4.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:deftext4.obj=be890bd5ddeab3bc3b1f50adadea8a87324537aa72434e615eeb4b38e5a1c5f4
    +test_classification:System
    +name: test_pcl5_pcl_parsing_deftext4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_parsing_deftext4
        +guid:a63ff4df-0e95-49fc-a38f-4a74668a1439
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_parsing_deftext4(udw, setup_teardown, printjob, outputsaver):
    # printjob.print_verify('be890bd5ddeab3bc3b1f50adadea8a87324537aa72434e615eeb4b38e5a1c5f4', timeout=600)
    # outputsaver.save_output()
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify_multi('be890bd5ddeab3bc3b1f50adadea8a87324537aa72434e615eeb4b38e5a1c5f4', timeout=600,expected_jobs=7)
    else:
        printjob.print_verify('be890bd5ddeab3bc3b1f50adadea8a87324537aa72434e615eeb4b38e5a1c5f4', timeout=600)
    outputsaver.save_output()
