import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 5Page_style.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-style.obj=bc315827460caf8cb945a9b1a3e39a3a593392c5761222c7c37128f24be28c72
    +test_classification:System
    +name: test_pcl5_highvalue_5page_style
    +test:
        +title: test_pcl5_highvalue_5page_style
        +guid:39c917da-782b-4e7e-9eb2-be9fdf2bf3f2
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

def test_pcl5_highvalue_5page_style(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bc315827460caf8cb945a9b1a3e39a3a593392c5761222c7c37128f24be28c72', timeout=300)
    outputsaver.save_output()
