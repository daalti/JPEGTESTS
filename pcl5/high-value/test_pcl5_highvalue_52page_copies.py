import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 52Page_copies.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:52Page-copies.obj=a421b190945ceb103a3e0b50cb01a63bc7c6b81620c1edf813dbaba9bc0e68b0
    +test_classification:System
    +name: test_pcl5_highvalue_52page_copies
    +test:
        +title: test_pcl5_highvalue_52page_copies
        +guid:20aac875-1945-41f6-bfdb-61bbffa6131f
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

def test_pcl5_highvalue_52page_copies(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a421b190945ceb103a3e0b50cb01a63bc7c6b81620c1edf813dbaba9bc0e68b0', timeout=600)
    outputsaver.save_output()
