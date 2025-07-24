import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 78Page_cteffwin2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1200
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:78Page-cteffwin2.obj=1da01f3c8868504332e81edb4e479da564c5a8085aa1ee37644b1c04d79466fb
    +test_classification:System
    +name: test_pcl5_highvalue_78page_cteffwin2
    +test:
        +title: test_pcl5_highvalue_78page_cteffwin2
        +guid:c410fbe3-316e-4385-abf9-042a848ce30a
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

def test_pcl5_highvalue_78page_cteffwin2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1da01f3c8868504332e81edb4e479da564c5a8085aa1ee37644b1c04d79466fb', timeout=1200)
    outputsaver.save_output()
