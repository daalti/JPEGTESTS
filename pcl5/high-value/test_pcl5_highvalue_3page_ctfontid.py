import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_ctfontid.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-ctfontid.obj=437483f008e4bc0f42b87d643462f90c6b61b8dd3bdc9fecbff6e946dd2afe1c
    +test_classification:System
    +name: test_pcl5_highvalue_3page_ctfontid
    +test:
        +title: test_pcl5_highvalue_3page_ctfontid
        +guid:38d2751d-ce94-49f6-a467-b4465349d973
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

def test_pcl5_highvalue_3page_ctfontid(setup_teardown, printjob, outputsaver):
    printjob.print_verify('437483f008e4bc0f42b87d643462f90c6b61b8dd3bdc9fecbff6e946dd2afe1c', timeout=600)
    outputsaver.save_output()
