import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 29Page_sd.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:29Page-sd.obj=064c926856263681d1ed8b476778973b69431c18e54b26ce6bc610114876358a
    +test_classification:System
    +name: test_pcl5_basicfunctionality_29page_sd
    +test:
        +title: test_pcl5_basicfunctionality_29page_sd
        +guid:c6faf4ec-b97d-40a1-99a8-39f1bbb33617
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_29page_sd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('064c926856263681d1ed8b476778973b69431c18e54b26ce6bc610114876358a',timeout=240)
    outputsaver.save_output()
