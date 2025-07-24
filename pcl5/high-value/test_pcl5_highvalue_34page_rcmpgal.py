import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 34Page_rcmpgal.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:34Page-rcmpgal.obj=ac82cc9faa7d07101d9351b8d7ce4fb0b1d33f91002948c57698d509042f7720
    +test_classification:System
    +name: test_pcl5_highvalue_34page_rcmpgal
    +test:
        +title: test_pcl5_highvalue_34page_rcmpgal
        +guid:80cf2931-2967-4c7c-94e6-10d381b40558
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

def test_pcl5_highvalue_34page_rcmpgal(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ac82cc9faa7d07101d9351b8d7ce4fb0b1d33f91002948c57698d509042f7720', timeout=600)
    outputsaver.save_output()
