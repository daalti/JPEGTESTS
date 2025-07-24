import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 31Page_cttcdes.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:31Page-cttcdes.obj=2e258ee2e60a926d29ca1fe6616f9c05a00aeda048702f3b64a64e88891008c7
    +test_classification:System
    +name: test_pcl5_highvalue_31page_cttcdes
    +test:
        +title: test_pcl5_highvalue_31page_cttcdes
        +guid:9e577573-0ea3-4a71-94cc-85af4da8c75b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_31page_cttcdes(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2e258ee2e60a926d29ca1fe6616f9c05a00aeda048702f3b64a64e88891008c7', timeout=600)
    outputsaver.save_output()
