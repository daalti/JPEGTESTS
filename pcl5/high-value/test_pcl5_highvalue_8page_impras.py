import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 8Page_impras.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:8Page-impras.obj=cf3e773dc433491ed25fbfa2f79548a43f546fd220dcc327493d12bad049aba4
    +test_classification:System
    +name: test_pcl5_highvalue_8page_impras
    +test:
        +title: test_pcl5_highvalue_8page_impras
        +guid:05f6297d-2e16-40e2-a11a-d629e424f357
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

def test_pcl5_highvalue_8page_impras(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cf3e773dc433491ed25fbfa2f79548a43f546fd220dcc327493d12bad049aba4')
    outputsaver.save_output()
