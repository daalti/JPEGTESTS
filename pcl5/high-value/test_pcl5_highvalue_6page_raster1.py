import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 6Page_raster1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:6Page-raster1.obj=c6955a89cd8de375bbe80f6b82bfd424113cbee007f7389417f3ab2c5b97799e
    +test_classification:System
    +name: test_pcl5_highvalue_6page_raster1
    +test:
        +title: test_pcl5_highvalue_6page_raster1
        +guid:134341c6-0621-4445-831d-0bf2158c83ac
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

def test_pcl5_highvalue_6page_raster1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c6955a89cd8de375bbe80f6b82bfd424113cbee007f7389417f3ab2c5b97799e')
    outputsaver.save_output()
