import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using pjlappendcr.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pjlappendcr.pcl=017c4edf8dff72ee4eb23708c2abeb0f8fc93f7b21a2645f76bfc99f6a43ae93
    +test_classification:System
    +name: test_pcl5_testfiles_pjl_pjlappendcr
    +test:
        +title: test_pcl5_testfiles_pjl_pjlappendcr
        +guid:a34d1fa8-8f61-4d49-8c34-51cad8f717d9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pjl_pjlappendcr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('017c4edf8dff72ee4eb23708c2abeb0f8fc93f7b21a2645f76bfc99f6a43ae93', timeout=600)
    outputsaver.save_output()
