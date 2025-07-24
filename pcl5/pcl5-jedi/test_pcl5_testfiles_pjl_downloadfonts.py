import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using downloadfonts.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:downloadfonts.pcl=22a76f9345ac56a8116152f73713ca17ad2622b8bade769b5c0b9bdd4cf7e36c
    +test_classification:System
    +name: test_pcl5_testfiles_pjl_downloadfonts
    +test:
        +title: test_pcl5_testfiles_pjl_downloadfonts
        +guid:7faeb873-d939-4241-b803-a946cffffcb2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pjl_downloadfonts(setup_teardown, printjob, outputsaver):
    printjob.print_verify('22a76f9345ac56a8116152f73713ca17ad2622b8bade769b5c0b9bdd4cf7e36c', timeout=600)
    outputsaver.save_output()
